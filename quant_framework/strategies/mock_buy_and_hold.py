from datetime import date, timedelta

from quant_framework.strategies.strategy import Strategy, RunMode
from quant_framework.brokers.mock_broker import MockBroker
from quant_framework.data_providers.mock_data_provider import MockDataProvider


class MockBuyAndHold(Strategy):
    name = 'mock_buy_and_hold'
    description = 'Simulates buying and holding a small portfolio of shares, gradually adding an additional share each day'
    interval = timedelta(days=1),
    run_mode = RunMode.BACKTEST

    def begin(self, timestamp):
        self.broker = MockBroker()
        self.data_provider = MockDataProvider()

        self.tickers = [
            'AAPL',
            'GOOG',
            'TSLA'
        ]

    def update(self, timestamp):
        for t in self.tickers:
            try:
                price = self.data_provider.fetch_ticker_eod(t, timestamp.date())['adjusted_close']
                self.broker.buy(t, 1, price)
            except ValueError as e:
                print(e)

    def finish(self, timestamp):
        for t in self.tickers:
            price = self.data_provider.fetch_ticker_eod(t, timestamp.date())['adjusted_close']
            self.broker.close(t, price)

        print('----- Final Portfolio Performance -----')
        print(self.broker.allowance)