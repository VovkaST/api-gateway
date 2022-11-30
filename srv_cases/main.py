from random import randint

from fastapi import FastAPI
from starlette.requests import Request

from srv_cases.schemas import CaseCreateSchema, CaseViewSchema

app = FastAPI()


cases = [
    {
        "id": 1,
        "title": "Case 1",
    },
    {
        "id": 2,
        "title": "Case 2",
    },
]


@app.get("/cases")
async def get_all_cases(request: Request):
    return cases


@app.post("/cases")
async def create_case(request: Request, data: CaseCreateSchema):
    id_ = randint(1, 100)
    new_case = CaseViewSchema(id=id_, **data.dict())
    cases.append(new_case.dict())
    return new_case
