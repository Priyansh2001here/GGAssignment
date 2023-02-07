import asyncio
import sqlite3
from typing import List

import aiohttp
from fastapi import FastAPI
from starlette.responses import JSONResponse

import models
import serializers
from http_helper import send_get_request
from models import database

app = FastAPI()


async def trigger_bidders_to_bid(bidders: List):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for bidder in bidders:
            url = f"http://{bidder.host}:{bidder.port}/webhook/send_bid"
            print(f"sending bid request to {url}")
            tasks.append(send_get_request(url, {}, session))
        responses = await asyncio.gather(*tasks)
        return responses


@app.post("/bidder")
async def register_bidder(bidder: serializers.Bidder):
    print("Bidder Registered", bidder.dict())
    try:
        query = models.Bidder.insert().values(bidder_id=bidder.bidder_id, host=bidder.host, port=bidder.port)
        last_record_id = await database.execute(query)
        return {
            **bidder.dict(),
            "pk": last_record_id
        }
    except sqlite3.IntegrityError as _:
        return JSONResponse(status_code=200, content={})


@app.post('/auction')
async def register_auction(auction_id: str):
    query = models.Auction.insert().values(uuid=auction_id)
    last_record_id = await database.execute(query)
    return {
        "pk": last_record_id
    }


# @app.get('/auction')
# async def register_auction(auction_id: str):
#     query = models.Auction.select().where(models.Auction.c.uuid == auction_id)
#     obj = await database.fetch_one(query=query)
#     if obj is not None:
#         return 404


@app.get('/bid/{auction_id}')
async def start_bidding(auction_id: str):
    query = models.Bidder.select()
    bidders = await database.fetch_all(query)
    responses = await trigger_bidders_to_bid(bidders)
    max_bid = 0
    max_bidder = ""
    bids = []
    for bid in responses:
        if bid is not None:


            bids.append({
                "amount" : bid["amount"],
            "bidder" :bid["bidder_id"],
            "auction" : auction_id
            })

            if max_bid < int(bid["amount"]):
                max_bid = int(bid["amount"])
                max_bidder = bid["bidder_id"]

    # insert_query  = "INSERT INTO bids(amount, bidder, auction) VALUES (:amount, :bidder, :auction)"
    insert_query=models.Bid.insert()
    await database.execute_many(insert_query, bids)

    if max_bidder == "":
        return JSONResponse(status_code=204, content={"message": "No bidders available"})
    return {
        "max_bid": max_bid,
        "max_bidder": max_bidder
    }


@app.get('/bidder', response_model=List[serializers.Bidder])
async def list_bidders():
    query = models.Bidder.select()
    return await database.fetch_all(query)
