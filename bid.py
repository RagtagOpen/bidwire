from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Bid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True)
    identifier = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return "<Bid(id={}, identifier={})>".format(self.id, self.identifier)
