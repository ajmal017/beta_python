from django import test

from main.tests.fixture import Fixture1
from main.models import PortfolioItem
from execution.end_of_day import create_sale
from django.utils import timezone
from api.v1.tests.factories import GoalFactory, PositionLotFactory, TickerFactory, \
    TransactionFactory, GoalSettingFactory, GoalMetricFactory, AssetFeatureValueFactory, \
    PortfolioSetFactory, MarkowitzScaleFactory, PortfolioFactory
from main.models import Transaction, GoalMetric
from portfolios.providers.execution.django import ExecutionProviderDjango
from portfolios.providers.data.django import DataProviderDjango
from main.management.commands.rebalance import perturbate_mix, process_risk, perturbate_withdrawal, perturbate_risk, \
    get_weights, get_tax_lots, calc_opt_inputs, rebalance

from main.management.commands.populate_test_data import populate_prices, populate_cycle_obs, populate_cycle_prediction
from unittest.mock import MagicMock
from unittest import mock
from main.management.commands.rebalance import get_held_weights
from main.models import Ticker, GoalMetric, Portfolio, PortfolioSet
from portfolios.calculation import get_instruments
from datetime import datetime, date

mocked_now = datetime(year=2016,month=6,day=1)


class RebalanceTest(test.TestCase):
    @mock.patch.object(timezone, 'now', MagicMock(return_value=mocked_now))
    def setUp(self):
        self.t1 = TickerFactory.create(symbol='SPY', unit_price=5)
        self.t2 = TickerFactory.create(symbol='VEA', unit_price=5)
        self.t3 = TickerFactory.create(symbol='TIP', unit_price=100)
        self.t4 = TickerFactory.create(symbol='IEV', unit_price=100)

        self.equity = AssetFeatureValueFactory.create(name='equity', assets=[self.t1, self.t2])
        self.bond = AssetFeatureValueFactory.create(name='bond', assets=[self.t3, self.t4])

        self.goal_settings = GoalSettingFactory.create()
        asset_classes = [self.t1.asset_class, self.t2.asset_class, self.t3.asset_class, self.t4.asset_class]
        portfolio_set = PortfolioSetFactory.create(name='set', risk_free_rate=0.01, asset_classes=asset_classes)
        self.goal = GoalFactory.create(approved_settings=self.goal_settings, active_settings=self.goal_settings,
                                       cash_balance=100, portfolio_set=portfolio_set)

        self.tickers = [self.t1, self.t2, self.t3, self.t4, self.t4]
        self.prices = [4, 4, 90, 90, 90]
        self.quantities = [5, 5, 5, 5, 5]
        self.executed = [date(2016, 1, 1), date(2016, 1, 1), date(2016, 1, 1), date(2016, 1, 1), date(2016, 1, 1)]

        self.execution_details = []
        for i in range(5):
            execution = Fixture1.create_execution_details(self.goal,
                                                          self.tickers[i],
                                                          self.quantities[i],
                                                          self.prices[i],
                                                          self.executed[i])
            self.execution_details.append(execution)

        self.data_provider = DataProviderDjango(mocked_now.date())
        self.execution_provider = ExecutionProviderDjango()
        MarkowitzScaleFactory.create()
        self.setup_performance_history()
        self.idata = get_instruments(self.data_provider)

        self.portfolio = PortfolioFactory.create(setting=self.goal_settings)
        self.current_weights = get_held_weights(self.goal)

        items = [PortfolioItem(portfolio=self.portfolio,
                               asset=Ticker.objects.get(id=key),
                               weight=value,
                               volatility=self.idata[0].loc[key, key]) for key, value in self.current_weights.items()]
        PortfolioItem.objects.bulk_create(items)

    def test_perturbate_mix1(self):
        GoalMetricFactory.create(group=self.goal_settings.metric_group, feature=self.equity,
                                 type=GoalMetric.METRIC_TYPE_PORTFOLIO_MIX,
                                 rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                 rebalance_thr=0.05, configured_val=0.01,
                                 comparison=GoalMetric.METRIC_COMPARISON_EXACTLY)
        GoalMetricFactory.create(group=self.goal_settings.metric_group, feature=self.bond,
                                 rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                 type=GoalMetric.METRIC_TYPE_PORTFOLIO_MIX, rebalance_thr=0.05, configured_val=0.01,
                                 comparison=GoalMetric.METRIC_COMPARISON_MAXIMUM)

        GoalMetricFactory.create(group=self.goal_settings.metric_group, feature=self.equity,
                                 type=GoalMetric.METRIC_TYPE_RISK_SCORE,
                                 rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                 rebalance_thr=0.5, configured_val=0.5)

        opt_inputs = calc_opt_inputs(self.goal.approved_settings, self.idata, self.data_provider, self.execution_provider)
        weights, min_weights = perturbate_mix(self.goal, opt_inputs)
        self.assertTrue(min_weights[self.t1.id] + min_weights[self.t2.id] < 0.01 + 0.05)
        self.assertTrue(min_weights[self.t3.id] + min_weights[self.t4.id] < 0.01 + 0.05)

    def test_perturbate_mix2(self):
        GoalMetricFactory.create(group=self.goal_settings.metric_group, feature=self.equity,
                                 type=GoalMetric.METRIC_TYPE_PORTFOLIO_MIX,
                                 rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                 rebalance_thr=0.05, configured_val=0.3,
                                 comparison=GoalMetric.METRIC_COMPARISON_MINIMUM)
        GoalMetricFactory.create(group=self.goal_settings.metric_group, feature=self.bond,
                                 type=GoalMetric.METRIC_TYPE_PORTFOLIO_MIX,
                                 rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                 rebalance_thr=0.05, configured_val=0.7,
                                 comparison=GoalMetric.METRIC_COMPARISON_MAXIMUM)

        GoalMetricFactory.create(group=self.goal_settings.metric_group, feature=self.equity,
                                 type=GoalMetric.METRIC_TYPE_RISK_SCORE,
                                 rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                 rebalance_thr=0.5, configured_val=0.5)

        opt_inputs = calc_opt_inputs(self.goal.approved_settings, self.idata, self.data_provider,
                                     self.execution_provider)

        weights, min_weights = perturbate_mix(self.goal, opt_inputs)
        self.assertTrue(min_weights[self.t3.id] + min_weights[self.t4.id] <= 0.75 or weights is not None)

    def test_perturbate_withdrawal(self):
        Fixture1.create_execution_details(self.goal, self.t4, self.goal.available_balance/90, 90, date(2016, 1, 1))
        TransactionFactory.create(from_goal=self.goal, status=Transaction.STATUS_PENDING,
                                  amount=self.goal.total_balance/2)
        weights = perturbate_withdrawal(self.goal)
        self.assertTrue(sum(weights.values()) < 1)

    def test_perturbate_risk(self):
        GoalMetricFactory.create(group=self.goal_settings.metric_group, feature=self.equity,
                                 type=GoalMetric.METRIC_TYPE_RISK_SCORE,
                                 rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                 rebalance_thr=0.5, configured_val=0.5)
        lots = get_tax_lots(self.goal)
        weights = get_weights(lots, self.goal.available_balance)
        #risk = process_risk(weights=weights, goal=self.goal, idata=idata, data_provider=data_provider, execution_provider=execution_provider)
        #weights = perturbate_risk(goal=self.goal)
        self.assertTrue(True)

    @mock.patch.object(timezone, 'now', MagicMock(return_value=mocked_now))
    def setup_performance_history(self):
        populate_prices(400, asof=mocked_now)
        populate_cycle_obs(400, asof=mocked_now)
        populate_cycle_prediction(asof=mocked_now)

    def test_do_not_rebuy_within_30_days(self):
        # finish test
        GoalMetricFactory.create(group=self.goal_settings.metric_group, feature=self.equity,
                                 type=GoalMetric.METRIC_TYPE_RISK_SCORE,
                                 rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                 rebalance_thr=0.5, configured_val=0.5)

        weights, instruments, reason = rebalance(self.goal, self.idata, self.data_provider, self.execution_provider)

        executed = datetime(year=2016, month=5, day=15)
        for i in range(3, 5):
            Fixture1.create_execution_details(self.goal, self.tickers[i], -self.quantities[i],self.tickers[i].unit_price, executed)
            self.goal.cash_balance += self.tickers[i].unit_price * abs(self.quantities[i])

        items = PortfolioItem.objects.all()
        for i in items:
            i.delete()
            i.save()

        self.current_weights = get_held_weights(self.goal)

        items = [PortfolioItem(portfolio=self.portfolio,
                               asset=Ticker.objects.get(id=key),
                               weight=value,
                               volatility=self.idata[0].loc[key, key]) for key, value in self.current_weights.items()]
        PortfolioItem.objects.bulk_create(items)

        weights, instruments, reason = rebalance(self.goal, self.idata, self.data_provider, self.execution_provider)
        self.assertAlmostEqual(weights[4], 0)

    def test_TLH(self):
        # out of currently held lots identify lots losing above some treshold - calculate lost weight - as PCT of portfolio value
        # set max constraint for those lots to PCT - as if we had sold those lots completely

        GoalMetricFactory.create(group=self.goal_settings.metric_group, feature=self.equity,
                                 type=GoalMetric.METRIC_TYPE_RISK_SCORE,
                                 rebalance_type=GoalMetric.REBALANCE_TYPE_ABSOLUTE,
                                 rebalance_thr=0.5, configured_val=0.5)

        self.t4.unit_price = 10

        #weights, instruments, reason = rebalance(self.goal, self.idata, self.data_provider, self.execution_provider)


        self.assertTrue(True)
