import bidwire_settings
import sendgrid
from sendgrid.helpers.mail import *
from yattag import Doc


def send_debug_email(bids_dict, recipients_notified):
    sg = sendgrid.SendGridAPIClient(apikey=bidwire_settings.SENDGRID_API_KEY)
    subject = "Bidwire status"
    content = Content("text/html", _make_debug_content(bids_dict,
                                                       recipients_notified))
    from_email = Email(bidwire_settings.ADMIN_EMAIL)
    to_email = Email(bidwire_settings.DEBUG_EMAIL)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


def _make_debug_content(bids_dict, recipients_notified):
    doc, tag, text = Doc().tagtext()
    with tag('p'):
        text("New bids found:")
        with tag('ul'):
            for site, bids in bids_dict.items():
                with tag('li'):
                    text("{}: {} new bids".format(site.value, len(bids)))
    with tag('p'):
        obfuscated_emails = [obfuscate_email(e) for e in recipients_notified]
        text("Notifications were sent to {}".format(
            ", ".join(obfuscated_emails)))

    return doc.getvalue()


def obfuscate_email(email):
    parts = email.split("@")
    return "{}***@{}".format(parts[0][0], parts[1])
