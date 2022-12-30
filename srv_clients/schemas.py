from pydantic import BaseModel, Field


class ClientSchema(BaseModel):
    surname: str = Field(..., description="")
    name: str = Field(..., description="")
    country: str = Field(..., description="")


class ClientViewSchema(ClientSchema):
    id: int = Field(..., description="")
