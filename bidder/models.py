# import databases
# import sqlalchemy
#
# DATABASE_URL = "sqlite:///./test.db"
#
# database = databases.Database(DATABASE_URL)
#
# metadata = sqlalchemy.MetaData()
#
# Bidder = sqlalchemy.Table(
#     "bidders",
#     sqlalchemy.Column("bidder_id", sqlalchemy.String),
#     sqlalchemy.Column("delay", sqlalchemy.Integer, sqlalchemy.CheckConstraint('delay >= 10 AND delay <= 500')),
# )
# Bid = sqlalchemy.Table(
#     "bids",
#     sqlalchemy.Column("bidder_id", sqlalchemy.String),
#     sqlalchemy.Column("auction_id", sqlalchemy.String),
#     sqlalchemy.Column("amount", sqlalchemy.Integer),
# )
#
# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )
# metadata.create_all(engine)
