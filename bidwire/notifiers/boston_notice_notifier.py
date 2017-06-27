from .base_notifier import BaseNotifier
from .notifier_utils import make_doc_item_body
from document import Document


class BostonNoticeNotifier(BaseNotifier):
    def get_site(self):
        return Document.Site.BOSTON_NOTICES

    def make_item_body(self, item):
        return make_doc_item_body(item)

    def get_listings_pre_text(self, items_length):
        return "We have found {} new notices since we last sent you an update:".format(items_length)