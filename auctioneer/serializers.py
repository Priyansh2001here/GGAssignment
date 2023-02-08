from pydantic import BaseModel

class Bidder(BaseModel):
    bidder_id: str
    host: str
    port: str

class BidRequest(BaseModel):
    bidder_id: str
    amount: int
