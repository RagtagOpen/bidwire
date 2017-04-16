import logging
import os
import sendgrid
from sendgrid.helpers.mail import *
from yattag import Doc

ADMIN_EMAIL = "bidwire-admin@googlegroups.com"
DEBUG_EMAIL = "bidwire-logs@googlegroups.com"

log = logging.getLogger(__name__)

ITEMS_DELIMITER = " ### "

class BaseNotifier:
    # type is derived from the return of get_site
    def __init__(self, recipients):
        self.type = self.get_site().value
        self.recipients = recipients

    def get_site(self):
        raise NotImplementedError

    def get_items(self, bid):
        if bid.items:
            return ITEMS_DELIMITER.join(bid.items)
        else:
            return bid.description

    def send_new_bids_notification(self, bids):
        log.info("Sending notifications to {} about bids {}" \
                 .format(self.recipients, bids))
        sg = sendgrid.SendGridAPIClient(
            apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(ADMIN_EMAIL)
        subject = "Changes detected on {}".format(self.type)
        content = Content("text/html", self.make_email_body(bids))
        for recipient in self.recipients:
            to_email = Email(recipient)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
        self.send_debug_email(sg, from_email, bids)

    def send_debug_email(self, sendgrid_client, from_email, bids):
        subject = "{} Scraping Status".format(self.type)
        content = Content("text/html", "{} new bids found".format(len(bids)))
        to_email = Email(DEBUG_EMAIL)
        mail = Mail(from_email, subject, to_email, content)
        response = sendgrid_client.client.mail.send.post(
            request_body=mail.get())

    def make_email_body(self, bids):
        formatted_text = "{} new bids on {}".format(len(bids), self.type)
        doc, tag, text = Doc().tagtext()

        with tag('p'):
            text("We have found " + formatted_text + " since we last sent " +
                 " you an update: ")
        with tag('ul'):
            for bid in bids:
                with tag('li'):
                    with tag('strong'):
                        with tag('a', href=bid.get_url()):
                            text(bid.description)
                    text(": " + self.get_items(bid))

        return doc.getvalue()
