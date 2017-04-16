from base_notifier import BaseNotifier
from bid import Bid


class CityOfBostonNotifier(BaseNotifier):
    def __init__(self):
        BaseNotifier.__init__(self, ["bidwire-logs@googlegroups.com"])

    def get_site(self):
        return Bid.Site.CITYOFBOSTON
