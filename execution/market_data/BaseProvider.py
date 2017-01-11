from abc import abstractmethod
class BaseProvider(object):
    def __init__(self):
        pass
    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def disconnect(self):
        pass
    @abstractmethod
    def getBestBidAsk(self, symbol):
        pass

