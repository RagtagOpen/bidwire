import commbuys_notifier
import bid
from cityofboston_notifier import CityOfBostonNotifier
from commbuys_notifier import CommBuysNotifier


def send_new_bids_notification():
    """Run through all the notifiers"""
    notifiers = [CityOfBostonNotifier(), CommBuysNotifier()]
    for notifier in notifiers:
        # Retrieve the bids we found in the last 23 hours -- if we
        # scrape once a day, this means the new bids in the last scrape.
        new_bids = bid.get_bids_from_last_n_hours(23, notifier.get_site())
        notifier.send_new_bids_notification(new_bids)
