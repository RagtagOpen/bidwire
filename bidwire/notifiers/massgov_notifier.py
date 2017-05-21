from .base_notifier import BaseNotifier
from .notifier_utils import make_doc_item_body
from document import Document


class MassGovNotifier(BaseNotifier):
    def get_site(self):
        return Document.Site.MASSGOV_EOPSS

    def get_listings_pre_text(self, items_length):
        formatted_text = "{} new Funding and Training documents" \
            .format(items_length)
        return "We have found " + formatted_text + " since we last sent " + \
            " you an update: "

    def make_item_body(self, doc):
        return make_doc_item_body(doc)
