from core.redis import redis


class ConnectionManager:
    async def connect(self, client):
        await redis.sadd('active_clients', client.key)

    async def disconnect(self, client):
        await redis.srem('active_clients', client.key)

    async def create_room(self, room):
        await redis.sadd('active_rooms', room.key)

    async def remove_room(self, room):
        await redis.srem('active_rooms', room.key)


connection_manager = ConnectionManager()
