from pydantic import BaseModel, Field


class GoodSchema(BaseModel):
    name: str = Field(..., description="Наименование")
    category_id: int = Field(..., description="Категория")


class GoodViewSchema(GoodSchema):
    id: int = Field(..., description="Идентификатор")


class CategorySchema(GoodSchema):
    id: int = Field(..., description="Идентификатор")
    name: str = Field(..., description="Наименование")
    parent_id: int = Field(None, description="Родительская категория")
