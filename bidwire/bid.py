from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, func, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from enum import Enum

Base = declarative_base()


class Bid(Base):
    class Site(Enum):
        COMMBUYS = "CommBuys"
        CITYOFBOSTON = "Boston's Bids and RFPs page"
        MASSGOV_EOPSS = "the EOPSS pages"
    __tablename__ = 'bids'

    # Unique database id for this bid.
    id = Column(Integer, primary_key=True)
    # Unique identifier for this bid, as assigned to it by the source of the
    # bid. Will have different format sfor different sites/sources.
    identifier = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())
    description = Column(Text)
    department = Column(Text)
    organization = Column(Text)
    location = Column(Text)
    open_date = Column(DateTime)
    # A JSON list of strings, representing items that the bid is for.
    items = Column(JSON)
    # A stringified value of a Bid.Site.name, which represents which source this
    # bid came from.
    site = Column(Text)

    @validates('items')
    def validate_items(self, key, items):
        assert type(items) is list, "'items' must be a list of strings"
        return items

    @validates('site')
    def validate_site(self, key, site):
        known_sites = [s.name for s in Bid.Site]
        assert site in known_sites, "{} is not a known Bid.Site".format(site)
        return site

    def get_url(self):
        if self.site == Bid.Site.CITYOFBOSTON.name:
            return "https://www.cityofboston.gov/purchasing/bids.asp?ID={}" \
                .format(self.identifier)
        elif self.site == Bid.Site.COMMBUYS.name:
            return "https://www.commbuys.com/bso/external/bidDetail.sdo?bidId={}" \
                .format(self.identifier)
        elif self.site == Bid.Site.MASSGOV_EOPSS.name:
            return "http://www.mass.gov" + self.identifier
        raise NotImplementedError

    def __repr__(self):
        return "<Bid(id={}, identifier={}, description={}, created_at={})>".format(
            self.id, self.identifier, self.description, self.created_at)


def get_new_identifiers(session, identifiers, site):
    """Returns the identifiers from the given list that are not present in our
    database

    Arguments:
    session -- the db session to use to make the query
    identifiers -- a list of strings representing the identifiers to check
    site -- the site associated with the identifiers
    """
    found_identifiers = []
    query = session.query(Bid.identifier).filter(
        Bid.identifier.in_(identifiers), Bid.site == site.name)
    found_identifiers = [b.identifier for b in query]
    return list(set(identifiers) - set(found_identifiers))


def get_bids_from_last_n_hours(session, hours, site):
    """Returns the Bids that have created_at equal to or later than now -
    'hours'

    Arguments:
    session -- the db session to use to make the query
    hours -- which most recent N hours are we checking for new bids
    site -- what source site are we counting new bids for
    """
    query = session.query(Bid).filter(
        Bid.created_at >= datetime.today() - timedelta(hours=hours),
        Bid.site == site.name
    )
    return query.all()


def get_bid_count_per_site(session):
    """
    Returns a dict (site -> bid_count) with the current count of bids in the
    database.

    Arguments:
    session -- the db session to use to make the query
    """
    query = session.query(func.count(Bid.id), Bid.site).group_by(Bid.site)
    pairs = query.all()
    count_dict = {}
    for pair in pairs:
        count, site_str = pair
        count_dict[Bid.Site[site_str]] = count
    return count_dict
