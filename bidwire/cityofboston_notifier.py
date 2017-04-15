from base_notifier import BaseNotifier


class CityOfBostonNotifier(BaseNotifier):
    def __init__(self):
        BaseNotifier.__init__(self, "City of Boston")

    def get_site(self):
        return 'CITY_OF_BOSTON'

    def get_items(self, bid):
        if type(bid.items) is list:
            return bid.items[0]
        return bid.items

    def get_url(self, bid):
        return "https://www.cityofboston.gov/purchasing/bids.asp?ID={}".format(
            bid.identifier)
