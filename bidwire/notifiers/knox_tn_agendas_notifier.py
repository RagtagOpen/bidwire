from .base_notifier import BaseNotifier
from .notifier_utils import make_doc_item_body
from document import Document


class KnoxCoTNAgendaNotifier(BaseNotifier):
    def get_site(self):
        return Document.Site.KNOX_CO_TN_AGENDAS

    def get_listings_pre_text(self, items_length):
        return ("We have found {} new documents ".format(items_length) +
                "since we last sent you an update:")

    def make_item_body(self, doc):
        return make_doc_item_body(doc)
