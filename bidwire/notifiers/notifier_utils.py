import logging
import os
import sendgrid
import bidwire_settings
from .base_notifier import BaseNotifier
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