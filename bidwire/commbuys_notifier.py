from base_notifier import BaseNotifier
from bid import Bid
import bidwire_settings


class CommBuysNotifier(BaseNotifier):
    def __init__(self):
        BaseNotifier.__init__(self, bidwire_settings.EMAIL_RECIPIENTS)

    def get_site(self):
        return Bid.Site.COMMBUYS
