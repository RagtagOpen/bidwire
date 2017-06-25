from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, func, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from enum import Enum

Base = declarative_base()


class Document(Base):
    class Site(Enum):
        # TODO(anaulin): Remove user-visible site string representation from enum.
        MASSGOV_EOPSS = "the EOPSS pages"
        MEMPHIS_COUNCIL_CALENDAR = "the Memphis City Council Meeting Calendar"
        CITYOFBOSTON = "Boston public notices"
        KNOX_CO_TN_AGENDAS = "the Knox County, TN County Commission Meeting Agendas"

    __tablename__ = 'documents'

    # Unique database id for this document.
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Full URL for the document (also used as lookup key, so must be unique)
    url = Column(String, unique=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    # A stringified value of a Document.Site.name, which represents which
    # source this bid came from.
    site = Column(Text)

    @validates('site')
    def validate_site(self, key, site):
        known_sites = [s.name for s in Document.Site]
        assert site in known_sites, "{} isn't a known Document.Site".format(site)
        return site

    def get_url(self):
        # TODO(anaulin): We should probably be storing absolute URLs for all sites, instead of composing this here
        if self.site == Document.Site.MASSGOV_EOPSS.name:
            return "https://www.mass.gov/" + self.url
        return self.url

    def __repr__(self):
        return "<Document(id={}, url={}, title={}, created_at={})>".format(
            self.id, self.url, self.title, self.created_at)


def get_new_urls(session, urls, site):
    """Returns the urls from the given list that are not present in our
    database

    Arguments:
    session -- the db session to use to make the query
    identifiers -- a list of strings representing the identifiers to check
    site -- the site associated with the identifiers
    """
    query = session.query(Document.url).filter(
        Document.url.in_(urls), Document.site == site.name)
    found_urls = [d.url for d in query]
    return list(set(urls) - set(found_urls))


def get_docs_from_last_n_hours(session, hours, site):
    """Returns the Documents that have created_at equal to or later than now -
    'hours'

    Arguments:
    session -- the db session to use to make the query
    hours -- which most recent N hours are we checking for new bids
    site -- what source site are we counting new bids for
    """
    query = session.query(Document).filter(
        Document.created_at >= datetime.today() - timedelta(hours=hours),
        Document.site == site.name
    )
    return query.all()


def get_doc_count_per_site(session):
    """
    Returns a dict (site -> doc_count) with the current count of documents in the
    database.

    Arguments:
    session -- the db session to use to make the query
    """
    query = session.query(func.count(Document.id), Document.site).group_by(Document.site)
    pairs = query.all()
    count_dict = {}
    for pair in pairs:
        count, site_str = pair
        count_dict[Document.Site[site_str]] = count
    return count_dict
