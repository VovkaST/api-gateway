from aio_pika import connect_robust
from aio_pika.patterns import RPC


async def send_request_to_queue(config: dict, message: dict):
    rmq = config["rmq"]
    connection = await connect_robust(rmq["url"])

    async with connection:
        channel = await connection.channel()
        rpc = await RPC.create(channel)
        result, status_code = await rpc.proxy.resolve(**message)
        return result, status_code
