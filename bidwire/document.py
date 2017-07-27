from datetime import datetime, timedelta
from urllib.parse import urlparse
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
        BOSTON_NOTICES = "Boston public notices"
        KNOX_CO_TN_AGENDAS = "the Knox County, TN County Commission Meeting Agendas"
        KNOXVILLE_TN_MEETINGS = "the Knoxville, TN City Meeting Calendar"

    __tablename__ = 'documents'

    # Unique database id for this document.
    id = Column(Integer, primary_key=True)
    # Full URL for the document (also used as lookup key, so must be unique)
    url = Column(String, unique=True)
    title = Column(String)
    created_at = Column(DateTime, default=func.now())
    # A stringified value of a Document.Site.name, which represents which
    # source this bid came from.
    site = Column(Text)

    @validates('site')
    def validate_site(self, key, site):
        known_sites = [s.name for s in Document.Site]
        assert site in known_sites, "{} isn't a known Document.Site".format(site)
        return site

    @validates('url')
    def validate_url(self, key, url):
        assert bool(urlparse(url).netloc), "{} should be an absolute URL".format(url)
        return url

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
    found_urls = set(d.url for d in query)
    return list(set(urls) - found_urls)


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
