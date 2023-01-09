from pydantic import BaseModel, Field


class ClientSchema(BaseModel):
    surname: str = Field(..., description="Фамилия")
    name: str = Field(..., description="Имя")
    country: str = Field(..., description="Страна")


class ClientViewSchema(ClientSchema):
    id: int = Field(..., description="Идентификатор")
