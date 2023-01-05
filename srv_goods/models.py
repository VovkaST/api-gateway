from sqlalchemy import Column, ForeignKey, Integer, Text

from srv_goods.database import Base


class Good(Base):
    __tablename__ = "good"
    __table_args = {"comment": "Таблица товаров"}

    id = Column(Integer, primary_key=True, comment="Идентификатор")
    name = Column(Text(length=255), nullable=False, comment="Наименование")
    category_id = Column(
        Integer,
        ForeignKey("category.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Категория",
    )


class Category(Base):
    __tablename__ = "category"
    __table_args = {"comment": "Категории товаров"}

    id = Column(Integer, primary_key=True, comment="Идентификатор")
    name = Column(
        Text(length=255), nullable=True, comment="Название категории"
    )
    parent_id = Column(
        Integer,
        ForeignKey("category.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Родительская категория",
    )
