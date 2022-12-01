from random import randint

from fastapi import FastAPI
from starlette.requests import Request

from srv_cases.schemas import CaseCreateSchema, CaseViewSchema

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
app = FastAPI()


@app.get("/cases/list")
async def get_all_cases(request: Request):
    return cases


@app.get("/cases/{case_id}")
async def get_case(request: Request, case_id: int):
    filtered = list(filter(lambda c: c["id"] == case_id, cases))
    if filtered:
        return filtered[0]


@app.post("/cases")
async def create_case(request: Request, data: CaseCreateSchema):
    id_ = randint(1, 100)
    new_case = CaseViewSchema(id=id_, **data.dict())
    cases.append(new_case.dict())
    return new_case
