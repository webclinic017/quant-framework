from abc import ABC, abstractmethod
from typing import final


class Strategy(ABC):

    # Abstract properties and methods (the user must override these)

    @property
    @abstractmethod
    def name(self):
        pass
    
    @property
    @abstractmethod
    def description(self):
        pass
    
    @property
    @abstractmethod
    def interval(self):
        pass

    @abstractmethod
    def begin(self, context):
        '''
        Run once at the beginning of the strategy execution
        '''
        pass

    @abstractmethod
    def update(self, context):
        '''
        Re-run for each `interval` window
        '''
        pass

    @abstractmethod
    def finish(self, context):
        '''
        Run once upon completion of the strategy execution
        '''
        pass

    # Non-abstract utility functions the user will use, but will NOT override

    @final
    def __init__(self, context):
        self.context = context

    @final
    def buy(self, ticker, amount):
        broker = self.context['broker']
        broker.buy_market(ticker, amount)
    
    @final
    def sell(self, ticker, amount):
        broker = self.context['broker']
        broker.sell_market(ticker, amount)
    
    @final
    def close(self, ticker):
        broker = self.context['broker']
        broker.close_market(ticker)
    
    @final
    def get_portfolio_value(self):
        broker = self.context['broker']
        return broker.get_portfolio_value()
