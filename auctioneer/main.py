from typing import List

from fastapi import FastAPI
from starlette.responses import JSONResponse

import serializers
from http_helper import trigger_bidders_to_bid

app = FastAPI()

import data_model


@app.post("/bidder")
async def register_bidder(bidder: serializers.Bidder):
    print("Bidder Registered", bidder.dict())
    data_model.localdb.bidders.append(data_model.Bidder(bidder.bidder_id, bidder.host, bidder.port))
    return {
        **bidder.dict(),
    }


@app.post('/auction')
async def register_auction(auction_id: str):
    # query = data_model.Auction.insert().values(uuid=auction_id)
    data_model.localdb.auctions.append(auction_id)
    return JSONResponse(status_code=201, content={
        "message": "Auction Created Sucessfully"
    })


@app.get('/bid/{auction_id}', response_model=serializers.BidRequest)
async def start_bidding(auction_id: str):
    bidders = data_model.localdb.bidders
    responses = await trigger_bidders_to_bid(bidders)
    print(responses)

    max_bid = max(responses, key=lambda x:-1 if x is None else int(x.get("amount", -1)))
    if len(responses) == 0:
        return JSONResponse(status_code=204, content={"message": "No bidders available"})
    return max_bid


@app.get('/bidder', response_model=List[serializers.Bidder])
async def list_bidders():
    return data_model.localdb.bidders
