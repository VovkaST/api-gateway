from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import DeclarativeMeta, backref, relationship
from sqlalchemy.orm.collections import InstrumentedList

from srv_goods.database import Base


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


class Good(BaseModel):
    __tablename__ = "good"
    __table_args = {"comment": "Таблица товаров"}

    name = Column(Text(length=255), nullable=False, comment="Наименование")
    category_id = Column(
        Integer,
        ForeignKey("category.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Категория",
    )
    category = relationship("Category", lazy="immediate")


class Category(BaseModel):
    __tablename__ = "category"
    __table_args = {"comment": "Категории товаров"}

    id = Column(Integer, primary_key=True, comment="Идентификатор")
    name = Column(
        Text(length=255), nullable=True, comment="Название категории"
    )
    parent_id = Column(
        Integer,
        ForeignKey("category.id", ondelete="RESTRICT"),
        comment="Родительская категория",
    )
    child = relationship(
        "Category",
        lazy="immediate",
        backref=backref("parent", remote_side=[id]),
    )
