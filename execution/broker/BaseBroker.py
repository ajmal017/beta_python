from abc import ABC, abstractmethod

class BaseBroker(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def current_time(self):
        pass
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
    def send_order(self, order_request):
        pass
    @abstractmethod
    def send_orders(self, order_requests):
        pass
    @abstractmethod
    def update_orders(self, order_request):
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

