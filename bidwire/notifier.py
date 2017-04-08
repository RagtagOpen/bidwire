import logging
import os
import sendgrid
from sendgrid.helpers.mail import *
from yattag import Doc


ADMIN_EMAIL = "bidwire-admin@googlegroups.com"
ITEMS_DELIMITER = " ### "

log = logging.getLogger(__name__)


def send_new_bids_notification(bids, recipients):
    log.info("Sending notifications to {} about bids {}".format(recipients,
                                                                bids))
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(ADMIN_EMAIL)
    subject = "Changes detected on CommBuys"
    content = Content("text/html", make_email_body(bids))
    for recipient in recipients:
        to_email = Email(recipient)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())


def make_email_body(bids):
    doc, tag, text = Doc().tagtext()

    with tag('p'):
        text("We have found {} new bids on CommBuys since we last sent you an update: ".format(
            len(bids)))
    with tag('ul'):
        for bid in bids:
            with tag('li'):
                with tag('strong'):
                    with tag('a', href=bid.url()):
                        text(bid.description)
                text(": ")
                if bid.items:
                    text(ITEMS_DELIMITER.join(bid.items))
                else:
                    text(bid.description)

    return doc.getvalue()
