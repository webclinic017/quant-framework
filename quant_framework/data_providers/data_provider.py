from abc import ABC, abstractmethod

class DataProvider(ABC):
    @abstractmethod
    def fetch_ticker_eod(self, ticker, date):
        pass

    @abstractmethod
    def fetch_ticker_eod_range(self, ticker, start, end):
        pass
