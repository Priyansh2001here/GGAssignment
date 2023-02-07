import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import UniqueConstraint

DATABASE_URL = "sqlite:///./auctioneer.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

Bid = sqlalchemy.Table(
    "bids",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("amount", sqlalchemy.BigInteger),
    sqlalchemy.Column("bidder", sqlalchemy.String, sqlalchemy.ForeignKey("bidders.bidder_id")),
    sqlalchemy.Column("auction", sqlalchemy.String, sqlalchemy.ForeignKey("auction.uuid"))
)

Bidder = sqlalchemy.Table(
    "bidders",
    metadata,
    sqlalchemy.Column("bidder_id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("host", sqlalchemy.String),
    sqlalchemy.Column("port", sqlalchemy.String),
    UniqueConstraint("host", "port", name="unique_bidder_host")
)


Auction = sqlalchemy.Table(
    "auction",
    metadata,
    sqlalchemy.Column("uuid", sqlalchemy.String, primary_key=True),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
