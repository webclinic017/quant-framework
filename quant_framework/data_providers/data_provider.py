from abc import ABC, abstractmethod


class DataProvider(ABC):
    '''
    An abstract class that all data providers must inherit from
    Data Providers are intended to be wrappers around vendors that provide daily stock market data
    '''
    @property
    @abstractmethod
    def name(self):
        pass
    
    @property
    @abstractmethod
    def documentation_url(self):
        pass

    @abstractmethod
    def fetch_ticker_data(self, ticker, date):
        pass

    @abstractmethod
    def fetch_ticker_data_range(self, ticker, start, end):
        pass
