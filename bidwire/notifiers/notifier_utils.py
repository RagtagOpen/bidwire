import logging
import os
import sendgrid
import bidwire_settings
from sendgrid.helpers.mail import *
from yattag import Doc

log = logging.getLogger(__name__)

ITEMS_DELIMITER = " ### "


def get_items(bid):
    if bid.items:
        return ITEMS_DELIMITER.join(bid.items)
    else:
        return bid.description


def append_items(bid):
    return ": " + get_items(bid)


def send_email(subject, mail_body, recipients):
    log.info("Sending email to recipients {}".format(recipients))
    sg = sendgrid.SendGridAPIClient(apikey=bidwire_settings.SENDGRID_API_KEY)
    from_email = Email(bidwire_settings.ADMIN_EMAIL)
    content = Content("text/html", mail_body)
    for recipient in recipients:
        to_email = Email(recipient)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        log.info("Sendgrid response status: {}".format(response.status_code))


def make_html_body(items, func_format_item, pre_list_text=None):
    """Returns an HTML email body listing all new items.

    The produced HTML looks like:
    <pre_list_text>
    <list of new items, generated calling func_format_item>
    <post_list_text>

    Arguments:
    items -- a list of new items to put in the email (can be any type)
    func_format_item -- a function that takes one item and returns an
        HTML-formatted version of this item
    pre_list_text -- any text to put before the item list
    post_list_text -- any text to put after the item list

    Returns:
    the resulting HTML, as a string
    """
    doc, tag, text = Doc().tagtext()
    if pre_list_text:
        with tag('p'):
            text(pre_list_text)
    with tag('ul'):
        for item in items:
            with tag('li'):
                # Append the HTML for the item to the doc as-is (don't escape)
                doc.asis(func_format_item(item))
    return doc.getvalue()


def make_bid_item_body(bid):
    """Returns the HTML for one Bid item"""
    doc, tag, text = Doc().tagtext()
    with tag('strong'):
        with tag('a', href=bid.get_url()):
            text(bid.description)
    text(append_items(bid))

    return doc.getvalue()


def make_doc_item_body(document):
    """Returns the HTML for one Document item"""
    doc, tag, text = Doc().tagtext()
    with tag('strong'):
        with tag('a', href=document.url):
            text(document.title)
    return doc.getvalue()
