from fastapi import FastAPI
from api.stats import router as stats_router
from core.manager import init_zookeeper


init_zookeeper()


app = FastAPI()
app.include_router(stats_router)
