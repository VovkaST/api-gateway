from typing import List

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    id: int = Field(..., description="Идентификатор")
    name: str = Field(..., description="Наименование")
    parent_id: int = Field(None, description="Родительская категория")


class CategoryViewSchema(BaseModel):
    name: str = Field(..., description="Наименование категории")


class GoodSchema(BaseModel):
    name: str = Field(..., description="Наименование")
    category_id: int = Field(..., description="Категория")


class GoodViewSchema(BaseModel):
    id: int = Field(..., description="Идентификатор")
    name: str = Field(..., description="Наименование")
    category: CategoryViewSchema = Field(..., description="Категория")


class ChildCategoryItemViewSchema(BaseModel):
    id: int = Field(..., description="Идентификатор")
    name: str = Field(..., description="Наименование")


class CategoryItemViewSchema(BaseModel):
    id: int = Field(..., description="Идентификатор")
    name: str = Field(..., description="Наименование")
    child: List[ChildCategoryItemViewSchema] = Field(
        None, description="Родительская категория"
    )
