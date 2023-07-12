import uuid
from core.redis import redis
from .logging import fastapi_logger
from .client import Client
from .manager import connection_manager


class Room:
    def __init__(self, id=None):
        if not id:
            self.id = str(uuid.uuid4())
            fastapi_logger.info(f"Room is created: {self.id}")
        else:
            self.id = id
        self.key = f'room:{self.id}'

    def __eq__(self, __value: object) -> bool:
        if self.id == __value.id:
            return True
        return False

    async def has_clients(self):
        client_set = await redis.smembers(self.key)
        fastapi_logger.info(f"client_set {client_set}")
        return True if len(client_set) != 0 else False

    async def add_client(self, client: Client):
        await redis.sadd(self.key, client.key)
        await self.notify_join(client)
        await client.join_room(self)

    async def remove_client(self, client: Client, connect_die=False):
        await redis.srem(self.key, client.key)
        if not connect_die:
            await self.notify_leave(client)
            await client.leave_room()
        remove_flag = not await self.has_clients()
        fastapi_logger.info(f"remove_flag {remove_flag}")
        if remove_flag:
            await connection_manager.remove_room(self)
            fastapi_logger.info(f"Room is removed: {self.id}")

    async def notify_join(self, client):
        await redis.publish(self.key, f"Client {client.name} join the room.")

    async def notify_leave(self, client):
        await redis.publish(self.key, f"Client {client.name} leave the room.")
