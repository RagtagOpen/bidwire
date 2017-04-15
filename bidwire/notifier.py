import commbuys_notifier
from cityofboston_notifier import CityOfBostonNotifier

def send_new_bids_notification(bids, recipients):
    cityofboston_notifier = CityOfBostonNotifier()
    # commbuys_notifier.send_new_bids_notification(bids, recipients)
    cityofboston_notifier.send_new_bids_notification(bids, recipients)
