from sqlalchemy import Column, Integer, Text

from srv_clients.database import Base


class Client(Base):
    __tablename__ = "client"
    __table_args = {"comment": "Таблица клиентов"}

    id = Column(Integer, primary_key=True, comment="Идентификатор")
    surname = Column(Text(length=255), nullable=False, comment="Фамилия")
    name = Column(Text(length=255), nullable=False, comment="Имя")
    country = Column(Text(length=255), comment="Страна")
