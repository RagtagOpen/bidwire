import logging
import os
import sendgrid
import bidwire_settings
from .base_notifier import BaseNotifier
from sendgrid.helpers.mail import *
from yattag import Doc

log = logging.getLogger(__name__)

ITEMS_DELIMITER = " ### "


class BidNotifier(BaseNotifier):
    def get_items(self, bid):
        if bid.items:
            return ITEMS_DELIMITER.join(bid.items)
        else:
            return bid.description

    def get_additional_list_text(self, bid):
        return ": " + self.get_items(bid)

    def get_link_description(self, bid):
        return bid.description