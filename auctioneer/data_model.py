from dataclasses import dataclass, field
from typing import List


@dataclass
class Bid:
    id: int
    amount: int
    bidder: str
    auction: str


@dataclass
class Bidder:
    bidder_id: str
    host: str
    port: str


@dataclass
class Auction:
    id: str


@dataclass
class InMemDb:
    auctions: List[Auction] = field(default_factory=list)
    bidders: List[Bidder] = field(default_factory=list)
    bids: List[Bid] = field(default_factory=list)

localdb = InMemDb()