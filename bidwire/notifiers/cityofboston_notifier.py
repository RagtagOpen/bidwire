from .notifier_utils import make_bid_item_body, make_doc_item_body
from .base_notifier import BaseNotifier
from bid import Bid
from notice import Notice


class CityOfBostonNotifier(BaseNotifier):
    def get_site(self):
        return Bid.Site.CITYOFBOSTON

    def get_listings_pre_text(self, bids_length):
        formatted_text = "{} new listings".format(bids_length)
        return "We have found " + formatted_text + " since we last sent " + \
            " you an update: "

    def make_item_body(self, item):
        return make_bid_item_body(item)


class CityOfBostonNoticeNotifier(BaseNotifier):
    def get_site(self):
        return Notice.Site.BOSTON

    def make_item_body(self, item):
        assert isinstance(item, Notice)
        return make_doc_item_body(item)

    def get_listings_pre_text(self, items_length):
        return "{} new notices".format(items_length)