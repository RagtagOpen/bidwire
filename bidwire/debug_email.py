import sendgrid
from sendgrid.helpers.mail import *
from yattag import Doc

import bid
import bidwire_settings


class DebugEmail:
    def __init__(self, sg_client=None):
        """
        Arguments:
        sg_client (optional) -- SendgridAPIClient object to use for email
          sending; if not provided, one will be constructed using default settings
        """
        if not sg_client:
            self.sg_client = sendgrid.SendGridAPIClient(
                apikey=bidwire_settings.SENDGRID_API_KEY)
        else:
            self.sg_client = sg_client

    def send(self, bids_dict, recipients_notified, elapsed_secs):
        """Composes and sends the debug email.

        Arguments:
        bids_dict -- {site: bids} dictionary with new bids we just sent
            notifications about
        recipients_notified -- list of strings with emails that received the
            notifications
        elapsed_secs -- integer number of seconds that elapsed between the
            beginning and the end of the entire Bidwire run
        """
        subject = "Bidwire status"
        content = Content(
            "text/html",
            self._make_content(bids_dict,
                               recipients_notified,
                               elapsed_secs)
        )
        from_email = Email(bidwire_settings.ADMIN_EMAIL)
        to_email = Email(bidwire_settings.DEBUG_EMAIL)
        mail = Mail(from_email, subject, to_email, content)
        response = self.sg_client.client.mail.send.post(
            request_body=mail.get())

    def _make_content(self, bids_dict, recipients_notified, elapsed_secs):
        doc, tag, text = Doc().tagtext()
        with tag('p'):
            text("New bids found:")
            with tag('ul'):
                for site, bids in bids_dict.items():
                    with tag('li'):
                        text("{}: {} new bids".format(site.value, len(bids)))
        with tag('p'):
            obfuscated_emails = [self._obfuscate_email(
                e) for e in recipients_notified]
            text("Notifications were sent to {}".format(
                ", ".join(obfuscated_emails)))

        with tag('p'):
            text("Total time elapsed: {}m {}sec".format(int(elapsed_secs / 60),
                                                        elapsed_secs % 60))

        with tag('p'):
            text("Current database contents:")
            with tag('ul'):
                for site, count in bid.get_bid_count_per_site().items():
                    with tag('li'):
                        text("{}: {} total bids".format(site.value, count))

        return doc.getvalue()

    def _obfuscate_email(self, email):
        parts = email.split("@")
        return "{}***@{}".format(parts[0][0], parts[1])
