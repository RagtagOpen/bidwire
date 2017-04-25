from .base_notifier import BaseNotifier
from bid import Bid


class MassGovNotifier(BaseNotifier):
    def get_site(self):
        return Bid.Site.MASSGOV_EOPSS

    def get_items(self, bid):
        """No items or description so override base get_items"""
        return None

    def get_listings_pre_text(self, bids_length):
        formatted_text = "{} new Funding and Training documents" \
            .format(bids_length)
        return "We have found " + formatted_text + " since we last sent " + \
             " you an update: "
