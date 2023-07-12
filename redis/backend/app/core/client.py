import uuid
from core.redis import redis
from .logging import fastapi_logger


class Client:
    def __init__(self, conn) -> None:
        self.id = str(uuid.uuid4())
        self.name = "Unknown"
        self.conn = conn
        self.now_room = None
        self.key = f"client:{self.id}"
        fastapi_logger.info(f"Client is created: {self.id}")

    def __eq__(self, __value: object) -> bool:
        if self.id == __value.id:
            return True
        return False

    async def send_heartbeat(self):
        await self.conn.send_json({
            'type': 'HEARTBEAT'
        })

    async def recv(self):
        return await self.conn.receive_json()

    async def send(self, data: dict):
        await self.conn.send_json(data)

    async def publish(self, message: str):
        if self.now_room:
            await redis.publish(self.now_room.key, self.name + " say " + message)

    async def join_room(self, room):
        self.now_room = room
        await self.send({
            'type': "SYSTEM",
            'message': f"Join room {room.id} successfully"
        })

    async def leave_room(self):
        if self.now_room:
            await self.send({
                'type': 'SYSTEM',
                'room': f"Leave room {self.now_room.id} successfully"
            })
            self.now_room = None

    def set_name(self, name):
        if name:
            self.name = name

    async def subscribe_channel(self):
        fastapi_logger.info(f"Client {self.name} start to subscribe channel: {self.now_room.id}")
        pubsub = redis.pubsub()
        await pubsub.subscribe(self.now_room.key)

        async for message in pubsub.listen():
            fastapi_logger.info(f'get publish message: {message}')
            if message['type'] == 'message':
                fastapi_logger.info(message["data"])
                await self.send({
                    'type': "MESSAGE",
                    'message': message["data"]
                })
