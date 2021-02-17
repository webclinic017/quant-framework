from abc import ABC, abstractmethod

class Broker(ABC):
    @abstractmethod
    def buy(self, ticker, amount, price):
        pass

    @abstractmethod
    def sell(self, ticker, amount, price):
        pass
