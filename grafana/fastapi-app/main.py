import os
import time
from typing import Union, Tuple
from fastapi import FastAPI, Request
from starlette.routing import Match
from prometheus_client import Summary, Counter, make_asgi_app
from logger import init_log, LOG


APP_NAME = os.environ.get("APP_NAME", "app")

REQUEST_TIME = Summary(
    'fastapi_request_processing_seconds',
    'Time spent processing request',
    ["method", "path", "status_code", "app_name"])

REQUEST_COUNT = Counter(
    "fastapi_requests_total",
    "Total count of requests by method and path.",
    ["method", "path", "app_name"]
)

app = FastAPI()
init_log()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


def get_path(request: Request) -> Tuple[str, bool]:
    for route in request.app.routes:
        match, _ = route.matches(request.scope)
        if match == Match.FULL:
            return route.path, True
    return request.url.path, False


@app.middleware("http")
async def send_metrics(request: Request, call_next):
    method = request.method
    path, is_handled_path = get_path(request)
    REQUEST_COUNT.labels(method=method, path=path, app_name=APP_NAME).inc()
    if not is_handled_path:
        return await call_next(request)
    start_time = time.perf_counter()
    response = await call_next(request)
    status_code = response.status_code
    process_time = time.perf_counter() - start_time
    REQUEST_TIME.labels(method=method, path=path, status_code=status_code, app_name=APP_NAME).observe(process_time)
    return response


@app.get("/")
def read_root():
    LOG.info("Hello World")
    return {"msg": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
