import enum
from sqlalchemy import Column, Integer, String

from quant_framework.internal.models.base import Base


class Strategy(Base):
    __tablename__ = 'strategies'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    interval = Column(Integer, nullable=False)
    class_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    fingerprint = Column(String, nullable=False)
    state = Column(String, default='IDLE', server_default='IDLE', nullable=False)

    def __repr__(self):
        return f'<Strategy(name="{self.name}", description="{self.description}", \
            interval={self.interval}, class_name="{self.class_name}", file_path="{self.file_path}", \
            fingerprint="{self.fingerprint}", state="{self.state}")>'