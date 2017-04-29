from .document_notifier import DocumentNotifier
from document import Document


class MassGovNotifier(DocumentNotifier):
    def get_site(self):
        return Document.Site.MASSGOV_EOPSS

    def get_listings_pre_text(self, bids_length):
        formatted_text = "{} new Funding and Training documents" \
            .format(bids_length)
        return "We have found " + formatted_text + " since we last sent " + \
             " you an update: "
