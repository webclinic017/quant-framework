import enum
from sqlalchemy import Column, Integer, Numeric, String, Date, UniqueConstraint

from quant_framework.internal.models.base import Base


class HistoricalPrice(Base):
    __tablename__ = 'historical_prices'

    id = Column(Integer, primary_key=True)
    data_provider = Column(String)
    ticker = Column(String)
    date = Column(Date)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    adjusted_close = Column(Numeric)
    volume = Column(Numeric)

    __table_args__ = (
        UniqueConstraint('data_provider', 'date', 'ticker', name='_data_provider_date_ticker'),
    )

    def as_dict(self):
        return {
            'data_provider': self.data_provider,
            'ticker': self.ticker,
            'date': str(self.date),
            'open': float(self.open),
            'high': float(self.high),
            'low': float(self.low),
            'close': float(self.close),
            'adjusted_close': float(self.close),
            'volume': float(self.close),
        }

    def __repr__(self):
        return f'<HistoricalPrice(data_provider="{self.data_provider}", ticker="{self.ticker}", date="{self.date}", \
            "open={self.open}" high={self.high}, low="{self.low}", close="{self.close}", adjusted_close="{self.adjusted_close}" \
            volume="{self.volume}")>'