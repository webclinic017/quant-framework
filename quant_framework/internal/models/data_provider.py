import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.dialects.postgresql import JSONB

from quant_framework.internal.models.base import Base


class DataProvider(Base):
    __tablename__ = 'data_providers'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    class_name = Column(String)
    init_kwargs = Column(JSONB)

    def as_dict(self):
        return {
            'name': self.name,
            'class_name': self.class_name,
            'init_kwargs': self.init_kwargs
        }
    
    def __repr__(self):
        return f'<DataProvider(name="{self.name}", class_name="{self.class_name}", init_kwargs={self.init_kwargs}")>'