import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from core.client import Client
from core.config import settings
from core.logging import fastapi_logger
from core.room import Room
from core.manager import connection_manager
from core.redis import redis


router = APIRouter()


async def consume_msg(client):
    sub_task = None
    while True:
        data = await client.recv()
        if data.get('type') == 'JOIN':
            has_room = await redis.exists(f"room:{data.get('room')}")  # check room exist
            if has_room:
                client.set_name(data.get('name'))
                room = Room(id=data.get('room'))
                await room.add_client(client)
                sub_task = asyncio.create_task(client.subscribe_channel())

        elif data.get('type') == 'CREATE':
            client.set_name(data.get('name'))
            room = Room()
            await connection_manager.create_room(room)
            await room.add_client(client)
            sub_task = asyncio.create_task(client.subscribe_channel())

        elif data.get('type') == 'PUBLISH':
            await client.publish(data.get('message', ''))

        elif data.get('type') == 'LEAVE':
            if client.now_room:
                await client.now_room.remove_client(client)
                if sub_task:
                    sub_task.cancel()
                    sub_task = None


async def send_heartbeat(client):
    while True:
        await client.send_heartbeat()
        await asyncio.sleep(settings.CONN_HEARTBEAT)


@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client = Client(conn=websocket)
    await connection_manager.connect(client)

    loop = asyncio.get_running_loop()
    heartbeat = loop.create_task(send_heartbeat(client))
    msgs = loop.create_task(consume_msg(client))
    tasks = [heartbeat, msgs]
    try:
        await asyncio.gather(*tasks)
    except Exception as ex:
        if not isinstance(ex, WebSocketDisconnect):
            fastapi_logger.error("Error happened", exc_info=True)
        for t in tasks:
            t.cancel()

    if client.now_room:
        await client.now_room.remove_client(client, connect_die=True)
    fastapi_logger.info(f'Client is disconnected: {client.name}')
    await connection_manager.disconnect(client)


@router.get("/health")
def health_check():
    return {"Hello": "World"}
