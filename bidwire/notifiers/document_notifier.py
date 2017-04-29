import logging
import os
import sendgrid
import bidwire_settings
from .base_notifier import BaseNotifier
from sendgrid.helpers.mail import *
from yattag import Doc

log = logging.getLogger(__name__)


class DocumentNotifier(BaseNotifier):
    def get_additional_list_text(self, doc):
        return None

    def get_link_description(self, doc):
        return doc.title