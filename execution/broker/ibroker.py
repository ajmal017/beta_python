from abc import ABC, abstractmethod, abstractproperty


class IBroker(ABC):
    def __init__(self):
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
    def request_market_depth(self, ticker):
        pass

    @abstractmethod
    def requesting_market_depth(self):
        pass