import os
from functools import wraps
from pathlib import Path
from typing import Any, Optional

import yaml
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from starlette import status
from yaml_tags import BaseTag, tag_registry

from gateway.rabbit import send_request_to_queue


def router(
    method,
    path: str,
    data_key: Optional[str] = None,
    status_code: Optional[int] = status.HTTP_200_OK,
    response_model: Optional[Any] = None,
):
    app_method = method(
        path, status_code=status_code, response_model=response_model
    )

    def wrapper(endpoint):
        @app_method
        @wraps(endpoint)
        async def decorator(request: Request, **kwargs):
            request_method = request.scope["method"].lower()
            data = kwargs.get(data_key)
            data = data.dict() if data else {}
            response_data, response_status_code = await send_request_to_queue(
                config=request.app.config,
                message={
                    "path": request.scope["path"],
                    "method": request_method,
                    "data": data,
                    "headers": {},
                },
            )
            if response_status_code >= status.HTTP_400_BAD_REQUEST:
                raise HTTPException(
                    status_code=response_status_code, detail=response_data
                )
            return response_data

    return wrapper


@tag_registry.register("env_tag")
class EnvTag(BaseTag):
    def _from_yaml(
        self,
        _loader,
        _work_dir,
        _prefix,
        _suffix,
        param=None,
        *args,
        **kwargs,
    ) -> str:
        result = os.environ.get(param, "")
        return f"{_prefix}{result}{_suffix}"


def load_config(config_path: Path) -> dict:
    tag_registry.require("env_tag")
    env_path = f"{config_path.absolute().parent}/.env"
    load_dotenv(dotenv_path=env_path)
    with open(config_path) as f:
        return yaml.load(f, Loader=yaml.Loader)


def get_config_path(file_name: str) -> Path:
    current_dir = Path(__file__).absolute().parent
    return current_dir / "config" / file_name
