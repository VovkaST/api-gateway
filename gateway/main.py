from fastapi import FastAPI

from common import get_config_path, load_config
from gateway.srv_clients.routes import clients_router
from gateway.srv_goods.routes import goods_router

app = FastAPI()
app.config = load_config(get_config_path("local.yaml"))
app.include_router(clients_router)
app.include_router(goods_router)
