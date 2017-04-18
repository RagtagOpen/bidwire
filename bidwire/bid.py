from datetime import datetime, timedelta
from db import Session
from sqlalchemy import Column, Integer, String, DateTime, func, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()


class Bid(Base):
    class Site(Enum):
        COMMBUYS = "CommBuys"
        CITYOFBOSTON = "Boston's Bids and RFPs page"
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
    site = Column(Text)

    def get_url(self):
        if self.site == Bid.Site.CITYOFBOSTON.name:
            return "https://www.cityofboston.gov/purchasing/bids.asp?ID={}" \
                .format(self.identifier)
        elif self.site == Bid.Site.COMMBUYS.name:
            return "https://www.commbuys.com/bso/external/bidDetail.sdo?bidId={}" \
                .format(self.identifier)
        raise NotImplementedError

    def __repr__(self):
        return "<Bid(id={}, identifier={}, description={}, created_at={})>".format(
            self.id, self.identifier, self.description, self.created_at)


def get_new_identifiers(identifiers, site):
    """Returns the identifiers from the given list that are not present in our
    database

    Arguments:
    identifiers -- a list of strings representing the identifiers to check
    site -- the site associated with the identifiers
    """
    session = Session()
    found_identifiers = []
    query = session.query(Bid.identifier).filter(
        Bid.identifier.in_(identifiers), Bid.site == site.name)
    found_identifiers = [b.identifier for b in query]
    return list(set(identifiers) - set(found_identifiers))


def get_bids_from_last_n_hours(hours, site):
    """Returns the Bids that have created_at equal to or later than now -
    'hours'
    """
    session = Session()
    query = session.query(Bid).filter(
        Bid.created_at >= datetime.today() - timedelta(hours=hours),
        Bid.site == site.name
    )
    return query.all()
