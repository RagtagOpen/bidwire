from base_notifier import BaseNotifier
from bid import Bid


class CityOfBostonNotifier(BaseNotifier):
    def get_site(self):
        return Bid.Site.CITYOFBOSTON

    def get_listings_pre_text(self, bids_length):
        formatted_text = "{} new listings".format(bids_length)
        return "We have found " + formatted_text + " since we last sent " + \
             " you an update: "
