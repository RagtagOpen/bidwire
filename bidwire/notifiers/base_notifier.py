import logging
import os
import sendgrid
import bidwire_settings
from sendgrid.helpers.mail import *
from yattag import Doc

log = logging.getLogger(__name__)


class BaseNotifier:
    # type is derived from the return of get_site
    def __init__(self, recipients=bidwire_settings.EMAIL_RECIPIENTS):
        self.type = self.get_site().value
        self.recipients = recipients

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

    def get_additional_list_text(self, item):
        """Text after each link is displayed on each line
        
        Returns:
        text -- string of text after the link in the list in email
        """
        raise NotImplementedError

    def get_link_description(self, item):
        """Text after each link is displayed on each line

        Returns:
        text -- string of text after the link in the list in email
        """
        raise NotImplementedError

    def send_new_items_notification(self, bids):
        log.info("Sending notifications to {} about bids {}"
                 .format(self.recipients, bids))
        sg = sendgrid.SendGridAPIClient(
            apikey=bidwire_settings.SENDGRID_API_KEY)
        from_email = Email(bidwire_settings.ADMIN_EMAIL)
        subject = "Changes detected on {}".format(self.type)
        content = Content("text/html", self.make_email_body(bids))
        for recipient in self.recipients:
            to_email = Email(recipient)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())

    def make_email_body(self, items):
        doc, tag, text = Doc().tagtext()
        with tag('p'):
            text(self.get_listings_pre_text(len(items)))
        with tag('ul'):
            for item in items:
                with tag('li'):
                    with tag('strong'):
                        with tag('a', href=item.get_url()):
                            if self.get_link_description(item):
                                text(self.get_link_description(item))
                    if self.get_additional_list_text(item):
                        text(self.get_additional_list_text(item))

        return doc.getvalue()
