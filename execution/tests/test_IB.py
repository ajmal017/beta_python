from django.test import TestCase
from api.v1.tests.factories import TickerFactory
from execution.broker.InteractiveBrokers.IBBroker import IBBroker
from main.models import Order
from client.models import IBAccount
from unittest import skip, skipIf


ib_testing = True

@skipIf(not ib_testing,"IB Testing is manually turned off.")
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
        account.ib_account = "DU299694"
        account_info = self.con.get_account_info(account)
        self.assertTrue(account_info.cash != 0)

    def test_IB_send_order(self):

        order = self.con.create_order(783, 1, self.ticker)
        self.con.send_order(order)
        self.assertTrue(order.Order_Id != -1)
        return order

    @skip("Unfinished")
    def test_IB_update_order(self):
        order = self.test_IB_send_order()
        orders = []
        orders.append(order)
        self.con.update_orders(orders)
        self.assertFalse(order.fill_info == Order.FillInfo.UNFILLED)

    def tearDown(self):
        self.con.disconnect()