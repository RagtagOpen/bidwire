from base_notifier import BaseNotifier

class CityOfBostonNotifier(BaseNotifier):
    def __init__(self):
        BaseNotifier.__init__(self, "City of Boston")

    def getUrl(self, bid):
        return "https://www.cityofboston.gov/purchasing/bids.asp?ID={}".format(
            bid.identifier)
