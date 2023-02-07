import asyncio
import os
import random
import uuid
from typing import Dict

import aiohttp
from fastapi import FastAPI

import serializers


async def send_post_request(url: str, data: Dict, ):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            return await resp.json()


async def send_get_request(url: str, data: Dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


AUC_BASE = f'http://{os.getenv("AUC_HOST", "localhost")}:{os.getenv("AUC_PORT",8000)}'
BIDDER_REGIS = AUC_BASE + '/bidder'
BID = AUC_BASE + '/make_bid'

port = int(os.getenv("PORT"))
host = "host.docker.internal"

app = FastAPI()

bidder_id = uuid.uuid4().hex
delay = float(os.getenv("DELAY", 190))/1000
print(delay)

BID_AMT = os.getenv("BID_AMT", random.randint(1, 1000))


@app.on_event("startup")
async def register_bidder():
    print("registering bidder with uuid ", bidder_id)
    res = await send_post_request(BIDDER_REGIS, data={
        'bidder_id': bidder_id,
        'host': host,
        'port': port
    })
    return res


#
@app.post('/set/bid')
async def register_bid(bid: serializers.SetBidRequest):
    global BID_AMT
    BID_AMT = bid.amount
    return f"Bid Amount successfully updated to {BID_AMT}"


@app.get('/webhook/send_bid')
async def bid():
    await asyncio.sleep(delay)
    return {
        'bidder_id': bidder_id,
        'amount': BID_AMT
    }


import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host=host, port=port)
