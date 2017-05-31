import logging
import os
import sendgrid
import bidwire_settings
from sendgrid.helpers.mail import *
from yattag import Doc


from .notifier_utils import send_email, make_html_body

log = logging.getLogger(__name__)


class BaseNotifier:
    def __init__(self):
        self.site_name = self.get_site().value

    # TODO(anaulin): Remove this method, and replace it with setting the
    # site_name in each constructor.
    def get_site(self):
        """Identifies the site type of the notifier

        Returns:
        site -- object of type Bid.Site
        """
        raise NotImplementedError

    def get_listings_pre_text(self, items_length):
        """Heading text before listings are displayed

        Arguments:
        bids_length -- number of new bids in the email

        Returns:
        text -- string of text preceding the listings
        """
        raise NotImplementedError

    def make_item_body(self, item):
        """Returns the HTML-formatted item for the new item list, as string."""
        raise NotImplementedError

    def send_new_items_notification(self, bids, recipients):
        log.info("Sending notifications to {} about bids {}"
                 .format(recipients, bids))
        subject = "Changes detected on {}".format(self.site_name)
        send_email(subject, self.make_email_body(bids), recipients)

    def make_email_body(self, items):
        return make_html_body(
            items,
            self.make_item_body,
            pre_list_text=self.get_listings_pre_text(len(items))
        )
