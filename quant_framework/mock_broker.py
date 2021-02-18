class MockBroker():
    '''
    A broker that mimics the buying and selling of shares on a public market based 
    on the historical price of the asset at the speficied timestamp

    The hypothetical positions are stored within the 'portfolio' of this class

    This is intended to be used while backtesting so that you don't accidentally create buy
    or sell orders with an actual broker
    '''

    def __init__(self):
        self.portfolio = {}  # The positions currently in the mock brokerage account
        self.allowance = 100000  # The amount of money available to purchase stocks with
    
    def buy(self, ticker, amount, price):
        '''
        Simulates a limit buy order according to the specified parameters that is immediately fulfilled
        '''
        if price * amount > self.allowance:
            raise ValueError('Account does not have enough funds for this order')

        if ticker not in self.portfolio.keys():
            self.portfolio[ticker] = 0

        self.portfolio[ticker] += amount
        self.allowance -= price * amount
    
    def sell(self, ticker, amount, price):
        '''
        Simulates a limit sell order according to the specified parameters that is immediately fulfilled
        '''
        if ticker not in self.portfolio.keys() or self.portfolio[ticker] < amount:
            raise ValueError('Account has fewer than the requested number of shares')

        self.portfolio[ticker] -= amount
        self.allowance += price * amount

    def close(self, ticker, price):
        '''
        Simulates creating a limit sell order for all owned shares according to the specified parameters 
        that is immediately fulfilled
        '''
        if ticker not in self.portfolio.keys():
            raise ValueError('Account has no shares of the provided ticker')

        amount = self.portfolio[ticker]
        self.sell(ticker, amount, price)
