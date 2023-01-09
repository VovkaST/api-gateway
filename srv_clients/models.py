from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm.collections import InstrumentedList

from srv_clients.database import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, comment="Идентификатор")

    def to_dict(self) -> dict:
        data = dict()
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            elif isinstance(v, Base):
                v = v.to_dict()
            elif isinstance(v, InstrumentedList):
                v = [item.to_dict() for item in v]
            data[k] = v
        return data


class Client(BaseModel):
    __tablename__ = "client"
    __table_args = {"comment": "Таблица клиентов"}

    surname = Column(Text(length=255), nullable=False, comment="Фамилия")
    name = Column(Text(length=255), nullable=False, comment="Имя")
    country = Column(Text(length=255), comment="Страна")
