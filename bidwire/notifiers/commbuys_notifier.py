from .base_notifier import BaseNotifier
from bid import Bid


class CommBuysNotifier(BaseNotifier):
    def get_site(self):
        return Bid.Site.COMMBUYS

    def get_listings_pre_text(self, bids_length):
        formatted_text = "{} new bids on {}" \
            .format(bids_length, self.get_site().value)
        return "We have found " + formatted_text + " since we last sent " + \
             " you an update: "
