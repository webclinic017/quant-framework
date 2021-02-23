from abc import ABC, abstractmethod


class Broker(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def buy_limit(self, ticker, amount, price):
        pass

    @abstractmethod
    def buy_market(self, ticker, amount):
        pass
    
    @abstractmethod
    def sell_limit(self, ticker, amount, price):
        pass

    @abstractmethod
    def sell_market(self, ticker, amount):
        pass

    @abstractmethod
    def close_market(self, ticker):
        pass

    @abstractmethod
    def get_portfolio_value(self):
        pass

    @abstractmethod
    def get_portfolio(self):
        pass

    @abstractmethod
    def get_cash(self):
        pass