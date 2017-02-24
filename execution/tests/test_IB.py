from django.test import TestCase
from api.v1.tests.factories import TickerFactory
from execution.broker.InteractiveBrokers.IBBroker import IBBroker
from main.models import Order
from execution.broker.InteractiveBrokers.IBOrder import IBOrder
from client.models import IBAccount
from unittest import skip, skipIf
from tests.test_settings import IB_TESTING
from execution.account_groups.create_account_groups import FAAccountProfile

@skipIf(not IB_TESTING,"IB Testing is manually turned off.")
class BaseTest(TestCase):
    def setUp(self):
        self.con = IBBroker()
        self.con.connect()
        self.ticker = TickerFactory.create(symbol='GOOG')

    def test_IB_connect(self):
        self.assertTrue(self.con._connection.isConnected())

    def test_IB_disconnect(self):
        self.assertTrue(self.con._connection.isConnected())
        self.con.disconnect()
        self.assertFalse(self.con._connection.isConnected())

    def test_IB_get_valid_id(self):
        id = self.con._get_next_valid_order_id()
        self.assertTrue(id!=0 and type(id) is int)

    def test_IB_account_summary(self):
        account = IBAccount()
        account.ib_account = "DU627759"
        account_info = self.con.get_account_info(account)
        self.assertTrue(account_info.cash != 0)


    def test_IB_pre_trade(self):
        account_profile = FAAccountProfile()

        account_dict = {
            'DU627759': 5,
            'DU627760': 10,
        }
        account_profile.append_share_allocation('MSFT', account_dict)
        profile = account_profile.get_profile()
        self.con.send_pre_trade(profile)

    def test_IB_distribution(self):
        account_profile = FAAccountProfile()

        account_dict = {
            'DU627759': 5,
            'DU627760': 10,
        }
        account_profile.append_share_allocation('MSFT', account_dict)
        profile = account_profile.get_profile()
        self.con.send_pre_trade(profile)
        order = self.test_IB_send_order()
        orders = []
        orders.append(order)
        distribution = self.con.update_orders(orders)
        self.assertFalse('DU627759' in distribution and 'DU627760'in distribution)
        if 'DU627759' in distribution and 'DU627760'in distribution:
            self.assertFalse(distribution['DU627759'] == 5)
            self.assertFalse(distribution['DU627760'] == 10)

    def test_IB_send_order(self):

        order = self.con.create_order(783, 15, self.ticker)
        order.__class__ = IBOrder
        order.m_faProfile = 'MSFT'
        self.con.send_order(order)
        self.assertTrue(order.Order_Id != -1)
        return order

    def test_IB_update_order(self):
        order = self.test_IB_send_order()
        orders = []
        orders.append(order)
        self.con.update_orders(orders)
        self.assertFalse(Order.FillInfo(order.fill_info) == Order.FillInfo.UNFILLED)


    def tearDown(self):
        self.con.disconnect()