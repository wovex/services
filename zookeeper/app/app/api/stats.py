import json
from fastapi import APIRouter
from core.manager import zk


router = APIRouter()


@router.get("/health")
def health_check():
    return {"Hello": "World"}


@router.get("/nodes")
def get_nodes():
    children = zk.get_children("/my/node")
    data = {}
    for node in children:
        n = zk.get(f"my/node/{node}")
        data[node] = json.loads(n[0].decode('utf-8'))
    return data
