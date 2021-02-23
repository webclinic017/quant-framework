# Quant Framework

Quant Framework, or `qf` is a simple python framework for backtesting algorithmic trading strategies.

### Setup

1. Install the package with `pip install quant_framework`
2. In your directory, create a directory called `strategies` and save the filepath. For me, this was `/Users/brendangeck/trading/strategies`
3. Create an empty Postgres database and a user with full permissions on that DB, and save the connection string to that DB. I use `postgres://qf:qf@localhost:5432/qf`
4. Create a `.env` file with variables for the results of steps 2 and 3 above:
  a. QUANT_FRAMEWORK_STRATEGY_FOLDER=/Users/brendangeck/trading/strategies
  b. QUANT_FRAMEWORK_DB=postgres://qf:qf@localhost:5432/qf
5. Run qf by executing `quant_framework`. You will see a flask service spin up on port 5000
6. Create a data provider. Currently, we only support [EOD Historical Data](https://eodhistoricaldata.com/financial-apis/):
```
curl --location --request POST 'http://localhost:5000/api/data-provider' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "eod_historical_data_default",
    "class_name": "EODHistoricalData",
    "init_kwargs": {
        "api_token": "YOUR_API_TOKEN"
    }
}'
```
7. Create a strategy in your `strategies` folder. For example, I create a file `strategies/mock_buy_and_hold.py` with the contents :
```
from quant_framework.strategies import Strategy


class MockBuyAndHold(Strategy):
    name = 'mock_buy_and_hold'
    description = 'Simulates buying and holding a small portfolio of shares, gradually adding an additional share each day'
    interval = '0 0 1 * *'

    def begin(self, context):
        self.tickers = [
            'AAPL',
            'GOOG',
            'TSLA'
        ]
        
        print('----- Starting Portfolio Performance -----')
        print(self.get_portfolio_value())

    def update(self, context):
        for t in self.tickers:
            try:
                self.buy(t, 1)
            except ValueError as e:
                print(e)

    def finish(self, context):
        for t in self.tickers:
            self.close(t)

        print('----- Final Portfolio Performance -----')
        print(self.get_portfolio_value())
```

8. Since `MockBuyAndHold` inherits from `quant_framework.strategies.Strategy`, it will be detected by the qf under the hood, and stored in the qf database. To trigger a backtest, you can do:
```
{
    "strategy": "mock_buy_and_hold",
    "data_provider": "eod_historical_data_default",
    "start": "2020-01-01",
    "end": "2020-03-01"
}
```

This will trigger the qf `backtest` functionality, which will create an instance of your MockBuyAndHold class, call the `start` function a single time, call the `update` function every `interval`, and call the `finish` function when the desired timeframe has completely elapsed.
You should see the starting and final outputs of your portfolio

### Work in Progress

As you can see, a lot still needs to be added to QF to make it viable in a production environment. Here are the things I'm working on next:

1. Supporting stock exchange calendars and retrying a strategy the next day the market is open
2. Supporting dividends and stock splits
3. Creating a simple front-end to allow for easier usability (`curl`ing to create data providers and backtests is not ideal)
4. Support for live trading by integrating with live brokers such as [Alpaca](https://alpaca.markets/)

