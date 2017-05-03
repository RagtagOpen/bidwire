from .base_notifier import BaseNotifier
from document import Document


class MassGovNotifier(BaseNotifier):
    def get_site(self):
        return Document.Site.MASSGOV_EOPSS

    def get_additional_list_text(self, doc):
        """For the mass.gov sites, we only want to display the document title
            with no additional text, so just return an empty string
        """
        return ""

    def get_link_description(self, doc):
        return doc.title

    def get_listings_pre_text(self, bids_length):
        formatted_text = "{} new Funding and Training documents" \
            .format(bids_length)
        return "We have found " + formatted_text + " since we last sent " + \
             " you an update: "
