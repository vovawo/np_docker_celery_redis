from typing import Optional
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

import sentry_sdk
import json
import redis
import os
import time


sentry_sdk.init(
    os.environ.get("SENTRY_LINK"),
    traces_sample_rate=1.0
)


app = FastAPI()

redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
pool = redis.ConnectionPool(host=redis_host, port=redis_port)


@app.get("/warehouses")
def get_warehouses(city_ref: Optional[str] = Query(None, max_length=50)):
    start = time.time()

    if city_ref:
        r = redis.StrictRedis(connection_pool=pool)
        reply = json.loads(r.execute_command('JSON.GET', 'warehouses_ukr', f'.{city_ref}'))
        return JSONResponse({"warehouses": reply,
                                "time": time.time() - start})
    return JSONResponse({"warehouses": []})
