from pydantic import BaseModel


class CaseCreateSchema(BaseModel):
    title: str


class CaseViewSchema(CaseCreateSchema):
    id: int
