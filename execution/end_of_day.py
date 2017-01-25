import logging
import types
from collections import defaultdict
from datetime import timedelta
from functools import partial
from logging import DEBUG, INFO, WARN, ERROR
from time import sleep

import numpy as np
from django.db import transaction
from django.db.models import Sum, F, Case, When, Value, FloatField
from django.utils import timezone

from main.management.commands.rebalance import TAX_BRACKET_LESS1Y, TAX_BRACKET_MORE1Y, get_position_lots_by_tax_lot


from client.models import ClientAccount
from execution.market_data.InteractiveBrokers.IBProvider import IBProvider
from execution.broker.ETNA.ETNABroker import ETNABroker
from execution.broker.InteractiveBrokers.IBBroker import IBBroker
from execution.account_groups.create_account_groups import FAAccountProfile
from main.models import MarketOrderRequest, ExecutionRequest, Execution, Ticker, MarketOrderRequestAPEX, \
    Fill, ExecutionFill, ExecutionDistribution, Transaction, PositionLot, Sale, Order
# TODO remove obsolete functionality


short_sleep = partial(sleep, 1)
long_sleep = partial(sleep, 10)

tax_bracket_egt1Y = 0.2
tax_bracket_lt1Y = 0.3

verbose_levels = {
    3 : DEBUG,
    2 : INFO,
    1 : WARN,
    0 : ERROR,
    }

ib_account_list = list()
ib_account_cash = dict()

logger = logging.getLogger('betasmartz.daily_process')
logger.setLevel(logging.INFO)


class BrokerManager(object):
    _brokers = dict()
    def get(self, broker_name):
        if broker_name not in self._brokers:
            if broker_name == "IB":
                broker = IBBroker()
            elif broker_name == "ETNA":
                broker = ETNABroker()
            broker.connect()
            self._brokers[broker_name] = broker
        return self._brokers[broker_name]


broker_manager =  BrokerManager()

class ProviderManager(object):
    _providers = dict()
    def get(self, provider_name):
        if provider_name not in self._providers:
            if provider_name == "IB":
                provider = IBProvider()
                provider.connect()
            self._providers[provider_name] = provider
        return self._providers[provider_name]


provider_manager =  ProviderManager()

def get_options():
    opts = types.SimpleNamespace()
    opts.verbose = 0
    return opts


@transaction.atomic()
def reconcile_cash_client_account(account):
    account_cash = account.cash_balance
    goals = account.goals.all()

    goals_cash = 0
    for goal in goals:
        goals_cash += goal.cash_balance

    # obtaining account_info object. This represents info as of with real brokers account
    account_info = broker_manager.get(account.broker).get_account_info(account.broker_account)


    difference = account_info.cash - (account_cash + goals_cash)
    if difference > 0:
        #there was deposit
        account_cash += difference
    elif difference < 0:
        #withdrawals
        if abs(difference) < account_cash:
            account_cash -= abs(difference)
        else:
            logger.exception("cash < sum of goals cashes for " + str(account.broker_account))
            raise Exception("cash < sum of goals cashes for " + str(account.broker_account))
            # we have a problem - we should not be able to withdraw more than account_cash
    account.cash_balance = account_cash
    account.save()
    return difference


def reconcile_cash_client_accounts():
    client_accounts = ClientAccount.objects.all()
    with transaction.atomic():
        for account in client_accounts:
            try:
                reconcile_cash_client_account(account)
            except:
                print("exception")


def get_execution_requests():
    ers = ExecutionRequest.objects.all().filter(order__state=MarketOrderRequest.State.APPROVED.value)
    return ers


def transform_execution_requests(execution_requests):
    '''
    transform django ExecutionRequests into allocation object, which we will use to keep track of allocation fills
    :param execution_requests: list of ExecutionRequest
    :return:
    '''
    allocations = defaultdict(lambda: defaultdict(float))
    for e in execution_requests.select_related('order__account__ib_account__ib_account', 'asset__symbol'):
        allocations[e.asset.symbol][e.order.account.ib_account.ib_account] += e.volume
    return allocations


def approve_mor(mor):
    mor.state = MarketOrderRequest.State.APPROVED.value
    mor.save()

def create_orders():
    '''
    from outstanding MOR and ER create MorApex and ApexOrder
    '''
    x=1
    ers_temp = ExecutionRequest.objects.all().filter(order__state=MarketOrderRequest.State.APPROVED.value)\
        .annotate(ticker_id=F('asset__id'))\
        .values('ticker_id', 'order__account')\
        .annotate(volume=Sum('volume'))
    ers = list()

    class ERSkey:
        def __init__(self):
            self.broker = ""
            self.broker_acc_id = ""
            self.ticker_id = ""
            self.volume = 0

        def __eq__(self, other):
            if self.broker == other.broker and self.ticker_id == other.ticker_id and self.broker_acc_id == other.broker_acc_id:
                return True
            return False
        def increment_volume(self, vol):
            self.volume += vol


    for er in ers_temp:
        er_obj = ERSkey()
        acc = ClientAccount.objects.get(pk=er['order__account'])
        er_obj.broker = acc.broker
        er_obj.broker_acc_id = acc.broker_acc_id
        er_obj.ticker_id = er['ticker_id']
        er_obj.volume = er['volume']

        if er_obj in ers:
            ers[ers.index(er_obj)].increment_volume(er['volume'])
        else:
            ers.append(er_obj)
    for grouped_volume_per_share in ers:
        ticker = Ticker.objects.get(id=grouped_volume_per_share.ticker_id)

        # TODO get actual price
        provider = provider_manager.get("IB")
        md = provider.get_market_depth_L1(ticker.symbol)
        order = broker_manager.get(grouped_volume_per_share.broker).create_order(price=md.get_mid(), quantity=grouped_volume_per_share.volume, ticker=ticker)
        order.save()
        mor_ids = MarketOrderRequest.objects.all().filter(state=MarketOrderRequest.State.APPROVED.value,
                                                          execution_requests__asset_id=ticker.id).\
            values_list('id', flat=True).distinct()

        for id in mor_ids:
            mor = MarketOrderRequest.objects.get(id=id)
            MarketOrderRequestAPEX.objects.create(market_order_request=mor, ticker=ticker, order=order)


def send_order(order):
    order.Status = Order.StatusChoice.Sent.value
    order.save()
    mors = MarketOrderRequest.objects.filter(morsAPEX__order=order).distinct()
    for m in mors:
        m.state = MarketOrderRequest.State.SENT.value
        m.save()


def mark_order_as_complete(order):
    order.Status = Order.StatusChoice.Filled.value
    order.save()


@transaction.atomic
def process_fills():
    '''
    from existing apex fills create executions, execution distributions, transactions and positionLots - pro rata all fills
    :return:
    '''
    fills = Fill.objects\
        .filter(order__Status__in=Order.StatusChoice.complete_statuses())\
        .annotate(ticker_id=F('order__ticker__id'))\
        .values('id', 'ticker_id', 'price', 'volume','executed')

    complete_mor_ids = set()
    complete_order_ids = set()
    for fill in fills:
        ers = ExecutionRequest.objects\
            .filter(asset_id=fill['ticker_id'], order__morsAPEX__order__Status__in=Order.StatusChoice.complete_statuses())
        sum_ers = np.sum([er.volume for er in ers])

        for er in ers:
            pro_rata = er.volume/float(sum_ers)
            volume = fill['volume'] * pro_rata

            apex_fill = Fill.objects.get(id=fill['id'])
            ticker = Ticker.objects.get(id=fill['ticker_id'])
            mor = MarketOrderRequest.objects.get(execution_requests__id=er.id)
            complete_mor_ids.add(mor.id)

            order = Order.objects.get(morsAPEX__market_order_request__execution_requests__id=er.id)
            complete_order_ids.add(order.id)

            execution = Execution.objects.create(asset=ticker, volume=volume, price=fill['price'],
                                                 amount=volume*fill['price'], order=mor, executed=fill['executed'])
            ExecutionFill.objects.create(fill=apex_fill, execution=execution)
            trans = Transaction.objects.create(reason=Transaction.REASON_ORDER,
                                               amount=volume*fill['price'],
                                               to_goal=er.goal, executed=fill['executed'])
            ed = ExecutionDistribution.objects.create(execution=execution, transaction=trans, volume=volume,
                                                      execution_request=er)

            if volume > 0:
                PositionLot.objects.create(quantity=volume, execution_distribution=ed)
            else:
                create_sale(ticker.id, volume, fill['price'], ed)

    for mor_id in complete_mor_ids:
        mor = MarketOrderRequest.objects.get(id=mor_id)
        mor.state = MarketOrderRequest.State.COMPLETE.value
        mor.save()

    for order_id in complete_order_ids:
        order = Order.objects.get(id=order_id)
        order.Status = Order.StatusChoice.Archived.value

        sum_fills = Fill.objects.filter(order_id=order_id).aggregate(sum=Sum('volume'))
        if sum_fills['sum'] == order.Quantity:
            order.fill_info = Order.FillInfo.FILLED.value
        elif sum_fills['sum'] == 0:
            order.fill_info = Order.FillInfo.UNFILLED.value
        else:
            order.fill_info = Order.FillInfo.PARTIALY_FILLED.value
        order.save()

def create_sale(ticker_id, volume, current_price, execution_distribution):
    # start selling PositionLots from 1st until quantity sold == volume
    position_lots = get_position_lots_by_tax_lot(ticker_id,
                                                 current_price,
                                                 execution_distribution.execution_request.goal_id)

    left_to_sell = abs(volume)
    for lot in position_lots:
        if left_to_sell == 0:
            break

        new_quantity = max(lot.quantity - left_to_sell, 0)
        left_to_sell -= lot.quantity - new_quantity
        lot.quantity = new_quantity
        lot.save()
        if new_quantity == 0:
            lot.delete()

        Sale.objects.create(quantity=- (lot.quantity - new_quantity),
                            sell_execution_distribution=execution_distribution,
                            buy_execution_distribution=lot.execution_distribution)

# obsolete - delete
def example_usage_with_IB():
    options = get_options()
    logging.root.setLevel(verbose_levels.get(options.verbose, ERROR))
    con = InteractiveBrokers()
    con.connect()
    con.request_account_summary()

    con.request_market_depth('GOOG')
    while con.requesting_market_depth():
        short_sleep()

    long_sleep()
    long_sleep()
    long_sleep()

    account_dict = dict()
    account_dict['DU493341'] = 40
    account_dict['DU493342'] = 60
    profile = FAAccountProfile()
    profile.append_share_allocation('AAPL', account_dict)

    account_dict['DU493341'] = 60
    account_dict['DU493342'] = 40
    profile.append_share_allocation('MSFT', account_dict)
    con.replace_profile(profile.get_profile())

    #con.request_profile()
    short_sleep()

    order_id = con.make_order(ticker='MSFT', limit_price=57.57, quantity=100)
    con.place_order(order_id)

    order_id = con.make_order(ticker='AAPL', limit_price=107.59, quantity=-100)
    con.place_order(order_id)

    long_sleep()
    con.current_time()

    con.request_market_depth('GOOG')
    while con.requesting_market_depth():
        short_sleep()

    short_sleep()

    long_sleep()
    long_sleep()


'''
class Command(BaseCommand):
    help = 'execute orders'

    def handle(self, *args, **options):
        logger.setLevel(logging.DEBUG)
'''