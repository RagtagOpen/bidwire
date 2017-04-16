from base_notifier import BaseNotifier
from bid import Bid


class CityOfBostonNotifier(BaseNotifier):
    def get_site(self):
        return Bid.Site.CITYOFBOSTON

    def get_items(self, bid):
        if type(bid.items) is list:
            return bid.items[0]
        return bid.items
