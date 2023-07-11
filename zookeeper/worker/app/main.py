import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.conn import router as conn_router
from core.manager import init_zookeeper, zk
from core.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if zk.exists(f"/my/node/{os.environ['NODE_NAME']}"):
        print("delete node", flush=True)
        zk.delete(f"/my/node/{os.environ['NODE_NAME']}")


init_zookeeper()


scheduler.start()

app = FastAPI(lifespan=lifespan)

app.include_router(conn_router)
