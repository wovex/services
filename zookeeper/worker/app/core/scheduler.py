import os
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.manager import zk, cm


def sync_to_zk():
    data = {'conn': cm.count}
    payload = json.dumps(data).encode('utf-8')
    if not zk.exists(f"/my/node/{os.environ['NODE_NAME']}"):
        zk.create(f"/my/node/{os.environ['NODE_NAME']}", payload, ephemeral=True, makepath=True)
    else:
        zk.set(f"/my/node/{os.environ['NODE_NAME']}", payload)


scheduler = AsyncIOScheduler()
scheduler.add_job(sync_to_zk, 'interval', seconds=5)
