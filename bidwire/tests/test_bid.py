import pytest

from bid import Bid, get_new_identifiers, get_bid_count_per_site
import db

from . import common
from . import factories


class TestBid():
    def test_validates_items_are_a_list(self):
        with pytest.raises(AssertionError) as exception_info:
            factories.BidFactory(items="this is not a list!")
        assert "must be a list" in str(exception_info.value)

    def test_validates_site_is_known_value(self):
        with pytest.raises(AssertionError) as exception_info:
            factories.BidFactory(site="FOOBAR")
        assert "not a known Bid.Site"

    def test_get_url_commbuys(self):
        bid = factories.BidFactory(site=Bid.Site.COMMBUYS.name)
        url = bid.get_url()
        assert "commbuys.com" in url
        assert "bidId={}".format(bid.identifier) in url

    def test_get_url_cityofboston(self):
        bid = factories.BidFactory(site=Bid.Site.CITYOFBOSTON.name)
        url = bid.get_url()
        assert "cityofboston.gov" in url
        assert "ID={}".format(bid.identifier) in url

    def test_get_new_identifiers(self):
        saved_bid = factories.BidFactory()

        identifiers = [saved_bid.identifier, "new-identifier"]
        new_identifiers = get_new_identifiers(self.session, identifiers,
                                              Bid.Site.COMMBUYS)
        assert len(new_identifiers) == 1
        assert "new-identifier" in new_identifiers

    def test_get_bid_count_per_site(self):
        count_dict = get_bid_count_per_site(self.session)
        for site in Bid.Site:
            assert site in count_dict
            assert count_dict[site] > 0

    @classmethod
    def setup_class(self):
        common.Session.configure(bind=db.engine)
        self.session = common.Session()

    @classmethod
    def teardown_class(self):
        common.Session.remove()
