import random
import time

import factory
import factory.alchemy

import bid
import document
from . import common


class BidFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory of Bid objects for testing."""
    class Meta:
        model = bid.Bid

        # Test-only scoped session
        sqlalchemy_session = common.Session

    identifier = factory.Sequence(lambda n: "Bid-%s-%s" % (time.time(),
                                                           random.random()))
    site = bid.Bid.Site.COMMBUYS.name

class DocumentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory of Bid objects for testing."""
    class Meta:
        model = document.Document

        # Test-only scoped session
        sqlalchemy_session = common.Session

    url = factory.Sequence(lambda n: "http://Document-%s-%s" % (time.time(),
                                                           random.random()))
    site = document.Document.Site.MASSGOV_EOPSS.name
