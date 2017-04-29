import bid
import document
from db import Session
from notifiers.cityofboston_notifier import CityOfBostonNotifier
from notifiers.commbuys_notifier import CommBuysNotifier
from notifiers.massgov_notifier import MassGovNotifier
from bidwire_settings import DEBUG_EMAIL

def send_new_notifications(recipient_emails):
    """
    Sends new notifications for each site/notifier.

    For simplicity, we don't store the time of the last notification sent, and
    instead we rely on the fact that we notify once a day, and scrape at least
    once a day (but sometimes might scrape more than once, because we are
    testing the scrapers). So we retrieve the bids/docs added to the database in the
    last 23 hours, which should include all new bids/docs since the last notification
    (this is not perfect, and will miss new bids/docs if a second scrape happened
    immediately after the previous notification went out). A more robust
    solution would involve storing a timestamp of the last check, and always
    checking against that timestamp.

    Return:
    new_bids_dict -- map from bid.site to list of new bids sent in notification
    """
    notifiers = {
        CityOfBostonNotifier(recipients=recipient_emails) :
            bid.get_bids_from_last_n_hours,
        CommBuysNotifier(recipients=recipient_emails) :
            bid.get_bids_from_last_n_hours,
        MassGovNotifier(recipients=[DEBUG_EMAIL]) :
            document.get_docs_from_last_n_hours
    }
    new_items_dict = {}
    for notifier, get_new_items in notifiers.items():
        site = notifier.get_site()
        new_items = get_new_items(Session(), 23, site)
        if new_items:
            notifier.send_new_items_notification(new_items)
        new_items_dict[site] = new_items
    return new_items_dict
