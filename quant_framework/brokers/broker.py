from abc import ABC, abstractmethod


class Broker(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def buy(self, ticker, amount, price):
        pass
    
    @abstractmethod
    def sell(self, ticker, amount, price):
        pass

    @abstractmethod
    def get_portfolio(self):
        pass

    @abstractmethod
    def get_total_cash(self):
        pass