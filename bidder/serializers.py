from pydantic import BaseModel

class Bidder(BaseModel):
    bidder_id: str
    delay: int

class BidRequest(BaseModel):
    # bidder_id: str
    # amount: int
    auction_id: int

class SetBidRequest(BaseModel):
    amount: int
