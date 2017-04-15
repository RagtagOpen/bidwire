import logging
import os
import sendgrid
from sendgrid.helpers.mail import *
from yattag import Doc

ADMIN_EMAIL = "bidwire-admin@googlegroups.com"
ITEMS_DELIMITER = " ### "
DEBUG_EMAIL = "bidwire-logs@googlegroups.com"

log = logging.getLogger(__name__)

class BaseNotifier:
    def __init__(self, type):
        self.type = type

    def getItems(self, bid):
        return bid.items

    def send_new_bids_notification(self, bids, recipients):
        log.info("Sending notifications to {} about bids {}".format(recipients,
                                                                    bids))
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(ADMIN_EMAIL)
        subject = "Changes detected on {}".format(self.type)
        content = Content("text/html", self.make_email_body(bids))
        for recipient in recipients:
            to_email = Email(recipient)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
        # send_debug_email(sg, from_email, bids)

    def send_debug_email(self, sendgrid_client, from_email, bids):
        subject = "{} Scraping Status".format(self.type)
        content = Content("text/html", "{} new bids found".format(len(bids)))
        to_email = Email(DEBUG_EMAIL)
        mail = Mail(from_email, subject, to_email, content)
        response = sendgrid_client.client.mail.send.post(request_body=mail.get())

    def make_email_body(self, bids):
        doc, tag, text = Doc().tagtext()

        with tag('p'):
            text("We have found {} new bids on {} since we last sent you an update: ".format(
                len(bids), self.type))
        with tag('ul'):
            for bid in bids:
                with tag('li'):
                    with tag('strong'):
                        with tag('a', href=self.getUrl(bid)):
                            text(bid.description)
                    text(": " + self.getItems(bid))

        return doc.getvalue()
