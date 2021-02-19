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
    def set_broker(self, broker):
        self.context['broker'] = broker

    @final
    def set_data_provider(self, data_provider):
        self.context['data_provider'] = data_provider
    
    @final
    def fetch_ticker_data(self, ticker):
        data_provider = self.context['data_provider']
        timestamp = self.context['timestamp']
        return data_provider.fetch_ticker_data(ticker, timestamp.date())

    @final
    def buy(self, ticker, amount):
        broker = self.context['broker']
        ticker_data = self.fetch_ticker_data(ticker)

        broker.buy(ticker, amount, ticker_data['close'])
    
    @final
    def sell(self, ticker, amount):
        broker = self.context['broker']
        ticker_data = self.fetch_ticker_data(ticker)

        broker.sell(ticker, amount, ticker_data['close'])
    
    @final
    def close(self, ticker):
        broker = self.context['broker']
        ticker_data = self.fetch_ticker_data(ticker)

        broker.close(ticker, ticker_data['close'])
    
    @final
    def get_portfolio_value(self):
        broker = self.context['broker']

        portfolio = broker.get_portfolio()

        # Calculate portfolio value by summing the value of current possitions
        # plus the value of your free cash

        value = 0
        for ticker, size in portfolio.items():
            ticker_data = self.fetch_ticker_data(ticker)
            value += ticker_data['close'] * size
        value += broker.get_total_cash()

        return value
