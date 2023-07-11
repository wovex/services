from fastapi import APIRouter, WebSocket
from core.manager import cm


router = APIRouter()


@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cm.add_conn()
    try:
        while True:
            data = await websocket.receive_json()
            print("Get data: %s"  %data, flush=True)
            if data.get(''):
                break
    except Exception:
        print("disconnect", flush=True)
    cm.remove_conn()


@router.get("/health")
def health_check():
    return {"Hello": "World"}
