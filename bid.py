from db import Session
from sqlalchemy import Column, Integer, String, DateTime, func, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Bid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True)
    identifier = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())
    description = Column(Text)
    department = Column(Text)
    organization = Column(Text)
    location = Column(Text)
    open_date = Column(DateTime)
    items = Column(JSON)

    def __repr__(self):
        return "<Bid(id={}, identifier={}, description={}, created_at={})>".format(
            self.id, self.identifier, self.description, self.created_at)


def get_new_identifiers(identifiers):
    """Returns the identifiers from the given list that are not present in our
    database

    Arguments:
    identifiers -- a list of strings representing the identifiers to check
    """
    session = Session()
    found_identifiers = []
    query = session.query(Bid.identifier).filter(
        Bid.identifier.in_(identifiers))
    found_identifiers = [b.identifier for b in query]
    return list(set(identifiers) - set(found_identifiers))
