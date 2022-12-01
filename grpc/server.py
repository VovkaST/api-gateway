import asyncio
import json

from aio_pika import connect_robust
from aio_pika.patterns import RPC

from grpc.common import get_config_path, load_config


async def resolve(*args, **kwargs) -> str:
    return json.dumps({"args": args, "kwargs": kwargs})


async def server() -> None:
    config = load_config(get_config_path("local.yaml"))
    rmq = config["rmq"]

    connection = await connect_robust(rmq["url"])

    channel = await connection.channel()
    rpc = await RPC.create(channel)
    await rpc.register(resolve.__name__, resolve, auto_delete=True)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(server())
