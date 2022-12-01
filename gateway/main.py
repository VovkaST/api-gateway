from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from common import get_config_path, load_config, router
from gateway.const import CASES_SERVICE_URL
from gateway.schemas.cases import CaseCreateSchema

app = FastAPI()
app.config = load_config(get_config_path("local.yaml"))


@router(method=app.get, path="/", service_url=CASES_SERVICE_URL)
async def get_main_page(request: Request, response: Response):
    pass


@router(method=app.get, path="/cases", service_url=CASES_SERVICE_URL)
async def get_all_cases(request: Request, response: Response):
    pass


@router(
    method=app.post,
    path="/cases",
    service_url=CASES_SERVICE_URL,
    data_key="data",
)
async def create_case(
    request: Request, response: Response, data: CaseCreateSchema
):
    pass
