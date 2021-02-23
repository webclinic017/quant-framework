from quant_framework.brokers.broker import Broker

class MockBroker(Broker):
    '''
    A broker that mimics the buying and selling of shares on a public market based 
    on the historical price of the asset at the speficied timestamp

    The hypothetical positions are stored within the 'portfolio' of this class

    This is intended to be used while backtesting so that you don't accidentally create buy
    or sell orders with an actual broker
    '''
    name = 'mock_broker'

    def __init__(self, context):
        self.portfolio = {}  # The positions currently in the mock brokerage account
        self.cash = 100000  # The amount of money available to purchase stocks with
        self.context = context
    
    def buy_limit(self, ticker, amount, price):
        '''
        Simulates a limit buy order according to the specified parameters that is immediately fulfilled
        '''
        if price * amount > self.cash:
            raise ValueError('Account does not have enough funds for this order')

        if ticker not in self.portfolio.keys():
            self.portfolio[ticker] = 0

        self.portfolio[ticker] += amount
        self.cash -= price * amount
    
    def buy_market(self, ticker, amount):
        '''
        Simulates purchasing stock at whatever the current price is.
        This is accomplished by having this broker make use of the data provider to determine price,
            vs. the `buy_limit` function where the price must be explicitly provided
        '''
        data_provider = self.context['data_provider']  # The provider we will use to fetch stock data
        current_timestamp = self.context['current_timestamp']  # Either the current datetime in the backtest or the true UTC "now"
        
        ticker_data = data_provider.fetch_historical_price_data(ticker, current_timestamp.date())
        price = ticker_data['close']

        # Since the mock broker does not place an actual order, we can just use the limit order
        # function, as this simply adds the desired amount to our portfolio
        self.buy_limit(ticker, amount, price)

    def sell_limit(self, ticker, amount, price):
        '''
        Simulates a limit sell order according to the specified parameters that is immediately fulfilled
        '''
        if ticker not in self.portfolio.keys() or self.portfolio[ticker] < amount:
            raise ValueError('Account has fewer than the requested number of shares')

        self.portfolio[ticker] -= amount
        self.cash += price * amount
    
    def sell_market(self, ticker, amount):
        '''
        Simulates selling stock at whatever the current price is.
        This is accomplished by having this broker make use of the data provider to determine price,
            vs. the `sell_limit` function where the price must be explicitly provided
        '''
        data_provider = self.context['data_provider']  # The provider we will use to fetch stock data
        current_timestamp = self.context['current_timestamp']  # Either the current datetime in the backtest or the true UTC "now"
        
        ticker_data = data_provider.fetch_historical_price_data(ticker, current_timestamp.date())
        price = ticker_data['close']

        # Since the mock broker does not place an actual order, we can just use the limit order
        # function, as this simply removes the desired amount to our portfolio
        self.sell_limit(ticker, amount, price)

    def close_market(self, ticker):
        '''
        Simulates creating a sell order for all owned shares according to the specified parameters 
        that is immediately fulfilled
        '''
        amount = self.portfolio[ticker]
        self.sell_market(ticker, amount)

    def get_portfolio_value(self):
        # Calculate portfolio value by summing the value of current possitions
        # plus the value of your free cash
        data_provider = self.context['data_provider']  # The provider we will use to fetch stock data
        current_timestamp = self.context['current_timestamp']  # Either the current datetime in the backtest or the true UTC "now"

        value = 0
        for ticker, size in self.portfolio.items():
            ticker_data = data_provider.fetch_historical_price_data(ticker, current_timestamp.date())
            value += ticker_data['close'] * size
        value += self.cash

        return value

    def get_portfolio(self):
        return self.portfolio

    def get_cash(self):
        return self.cash