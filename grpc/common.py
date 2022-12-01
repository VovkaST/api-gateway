import os
from pathlib import Path

import aiohttp
import yaml
from dotenv import load_dotenv
from yaml_tags import BaseTag, tag_registry


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
    ):
        result = os.environ.get(param, "")
        return _prefix + result + _suffix


def load_config(config_path: Path):
    tag_registry.require("env_tag")
    env_path = f"{config_path.absolute().parent}/.env"
    load_dotenv(dotenv_path=env_path)
    with open(config_path) as f:
        return yaml.load(f, Loader=yaml.Loader)


def get_config_path(file_name: str):
    current_dir = Path(__file__).absolute().parent
    return current_dir / "config" / file_name


async def make_request(
    url: str, method: str, data: dict = None, headers: dict = None
):
    if not headers:
        headers = {}
    async with aiohttp.ClientSession() as session:
        request = getattr(session, method)
        async with request(url, json=data, headers=headers) as response:
            data = await response.json()
            return data, response.status
