import os
from functools import wraps
from pathlib import Path

import yaml
from dotenv import load_dotenv
from starlette.requests import Request
from starlette.responses import Response
from yaml_tags import BaseTag, tag_registry

from gateway.rabbit import send_request_to_queue


class Singletone(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def router(method, path: str, service_url: str = None, data_key: str = None):
    app_method = method(path)

    def wrapper(endpoint):
        @app_method
        @wraps(endpoint)
        async def decorator(request: Request, response: Response, **kwargs):
            path = request.scope["path"]
            request_method = request.scope["method"].lower()
            data = kwargs.get(data_key)
            data = data.dict() if data else {}
            response = await send_request_to_queue(
                config=request.app.config,
                message={
                    "path": path,
                    "method": request_method,
                    "data": data,
                    "headers": {},
                },
            )
            return response

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
        return _prefix + result + _suffix


def load_config(config_path: Path) -> dict:
    tag_registry.require("env_tag")
    env_path = f"{config_path.absolute().parent}/.env"
    load_dotenv(dotenv_path=env_path)
    with open(config_path) as f:
        return yaml.load(f, Loader=yaml.Loader)


def get_config_path(file_name: str) -> Path:
    current_dir = Path(__file__).absolute().parent
    return current_dir / "config" / file_name
