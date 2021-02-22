import requests

from datetime import datetime, date, timedelta
from requests.adapters import HTTPAdapter
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from urllib3.util.retry import Retry

from quant_framework.internal.models import HistoricalPrice
from quant_framework.internal.utils import db
from quant_framework.data_providers import DataProvider


class EODHistoricalData(DataProvider):
    '''
    A data provider that fetches data using eodhistoricaldata.com
    '''
    name = 'eod_historical_data'
    documentation_url = 'https://eodhistoricaldata.com/financial-apis/api-for-historical-data-and-volumes/'

    def __init__(self, api_token):
        self.api_token = api_token
        self.endpoint = 'https://eodhistoricaldata.com'

    def fetch_ticker_data(self, ticker, req_date):
        '''
        Fetches the data for a specified ticker and date
        Also prefetches data for a +/-365 days to quicken subsequent lookups (and keep API usage low)
        '''
        db_fetch_attempt = self._fetch_from_db(ticker, req_date)        
        if db_fetch_attempt:
            return db_fetch_attempt
        else:
            start = req_date - timedelta(days=365)
            end = req_date + timedelta(days=365)

            records = self._fetch_range(ticker, start, end)

            # Write the prefetched records to the DB for fast access in the future
            self._write_records_to_db(ticker, records)

            # Fetch the correct date from the API response
            # It's possible that the requested date is a weekend or some other date that the stock market is not open
            # In this case, fetch the most recent closing price before the requested date
            prev = None
            for record in records:
                if datetime.strptime(record['date'], '%Y-%m-%d').date() == req_date:
                    return record
                elif datetime.strptime(record['date'], '%Y-%m-%d').date() > req_date:
                    # We assume that the response is in ascending order, so, the moment we 
                    # see a date larger than our requested date, we know we've passed what we want
                    return prev
                
                prev = record
                
            # Return None if no data was found for the requested date
            return None

    def fetch_ticker_data_range(self, ticker, start, end):
        '''
        Fetches the data for a specified ticker and date range
        Also prefetches data for a +/-365 days to quicken subsequent lookups (and keep API usage low)
        '''
        start_new = start - timedelta(days=365)
        end_new = end + timedelta(days=365)

        records = self._fetch_range(ticker, start_new, end_new)

        # First, write the prefetched records to the DB for fast access in the future
        self._write_records_to_db(ticker, records)

        records_selected = []
        for record in records:
            if datetime.strptime(record['date'], '%Y-%m-%d').date() >= start and \
                    datetime.strptime(record['date'], '%Y-%m-%d').date() <= end:
                records_selected.append(record)

        return records_selected

    def _fetch_from_db(self, ticker, req_date):
        engine = db.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        # First, try to find the exact date in the datebase
        result = session.query(HistoricalPrice) \
            .filter(HistoricalPrice.data_provider == 'eod_historical_data') \
            .filter(HistoricalPrice.ticker == ticker) \
            .filter(HistoricalPrice.date == req_date.strftime('%Y-%m-%d')) \
            .first()

        if not result:
            # Backup: If we couldn't find the date record in the database (like if the date was on a weekend),
            # then we find the most recent record before what was requested
            # Note: We have an additional filter that ensure we are only checking max 3 days before the requested date

            # This query gets the next nearest
            result = session.query(HistoricalPrice) \
                .filter(HistoricalPrice.data_provider == 'eod_historical_data') \
                .filter(HistoricalPrice.ticker == ticker) \
                .filter(HistoricalPrice.date <= req_date.strftime('%Y-%m-%d')) \
                .filter(HistoricalPrice.date - req_date.strftime('%Y-%m-%d') >= -3) \
                .order_by(HistoricalPrice.date.desc()) \
                .first()
        
        # If we did find a result, convert to a dictionary
        if result:
            result = result.as_dict()

        # If we've found the result, convert to a dict
        return result

    def _fetch_range(self, ticker, start, end):
        s = requests.Session()

        # Retry policy with backoff to ensure we can get around rate limiting
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[ 429, 500, 502, 503, 504 ])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = f'{self.endpoint}/api/eod/{ticker}.US'  # TODO: Allow for markets outside of the USA
        params = {
            'api_token': self.api_token,
            'from': start.strftime('%Y-%m-%d'),
            'to': end.strftime('%Y-%m-%d'),
            'period': 'd',
            'fmt': 'json'
        }

        response = s.get(url, params=params)

        r_json = response.json()
        return r_json

    def _write_records_to_db(self, ticker, records):
        engine = db.get_engine()

        with engine.connect() as conn:
            for record in records:
                insert_stmt = insert(HistoricalPrice).values(
                    data_provider='eod_historical_data',
                    ticker=ticker,
                    date=record['date'],
                    open=record['open'],
                    high=record['high'],
                    low=record['low'],
                    close=record['close'],
                    adjusted_close=record['adjusted_close'],
                    volume=record['volume']
                )

                insert_stmt = insert_stmt.on_conflict_do_nothing(
                    index_elements=['data_provider', 'date', 'ticker']
                )
                
                conn.execute(insert_stmt)
