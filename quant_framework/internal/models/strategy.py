import enum
from sqlalchemy import Column, Integer, String, Enum

from quant_framework.internal.models.base import Base

class StrategyState(enum.Enum):
    IDLE='IDLE'
    BACKTEST='BACKTEST'


class Strategy(Base):
    __tablename__ = 'strategies'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    interval = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    fingerprint = Column(String, nullable=False)
    state = Column(Enum(StrategyState), server_default=StrategyState.IDLE.value, nullable=False)

    def as_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'interval': self.interval,
            'class_name': self.class_name,
            'file_path': self.file_path,
            'fingerprint': self.fingerprint,
            'state': self.state.value
        }
    
    def __repr__(self):
        return f'<Strategy(name="{self.name}", description="{self.description}", \
            interval={self.interval}, class_name="{self.class_name}", file_path="{self.file_path}", \
            fingerprint="{self.fingerprint}", state="{self.state}")>'