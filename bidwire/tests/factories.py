import random
import time

import factory
import factory.alchemy

import bid
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
