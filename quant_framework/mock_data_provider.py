from datetime import date, timedelta

class MockDataProvider():
    '''
    A data provider that mimics a 3rd party data provider like Polygon.io, Bloomberg, etc.
    All functions return the same static data regardless of provided parameters
    '''

    def fetch_ticker_eod(self, ticker, date):
        '''
        Simulates fetching the price and volume data for a ticker for a specific date
        '''
        return {
            'date': date.strftime('%Y-%m-%d'),
            'open': 500,
            'high': 500,
            'low': 500,
            'close': 500,
            'adjusted_close': 500,
            'volume': 1000
        }

    def fetch_ticker_eod_range(self, ticker, start, end):
        '''
        Simulates fetching the price and volume data for a ticker for a range of dates
        '''

        delta = end - start
        
        results = []
        for i in range(delta.days + 1):
            day = start + timedelta(days=i)

            results.append({
                'date': day.strftime('%Y-%m-%d'),
                'open': 500,
                'high': 500,
                'low': 500,
                'close': 500,
                'adjusted_close': 500,
                'volume': 1000
            })

        return results
