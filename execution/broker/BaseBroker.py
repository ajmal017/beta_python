from abc import abstractmethod
from main.models import Order


class BaseBroker(object):
    def __init__(self):
        pass
    def create_order(self, price, quantity, ticker):
        side = Order.SideChoice.Buy.value if quantity > 0 else Order.SideChoice.Sell.value
        security = self.get_security(ticker.symbol)
        order = Order.objects.create(Price=price,
                                     Quantity=quantity,
                                     SecurityId=security.symbol_id,
                                     Symbol=security.Symbol,
                                     Side=side,
                                     TimeInForce=0,
                                     ExpireDate=0,
                                     ticker=ticker)
        return order
    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def disconnect(self):
        pass
    @abstractmethod
    def request_account_summary(self):
        pass
    @abstractmethod
    def send_order(self, order):
        pass
    def send_orders(self, orders):
        for order in orders:
            self.send_order(order)
        return orders
    @abstractmethod
    def update_orders(self, orders):
        pass
    @abstractmethod
    def get_security(self, symbol):
        pass
    @abstractmethod
    def send_pre_trade(self, trade_info):
        pass
    @abstractmethod
    def send_post_trade(self, trade_info):
        pass
    @abstractmethod
    def get_post_trade(self):
        pass
    @abstractmethod
    def cancel_order(self, orderid):
        pass

