import logging
import traceback

from bid import Bid, get_bids_from_last_n_hours
from db import Session
from document import Document, get_docs_from_last_n_hours
from notifiers.boston_bid_notifier import CityOfBostonNotifier
from notifiers.commbuys_notifier import CommBuysNotifier
from notifiers.massgov_notifier import MassGovNotifier
from notifiers.memphis_council_calendar_notifier import MemphisCouncilCalNotifier

log = logging.getLogger(__name__)


def get_new_items(session, hours, site):
    if isinstance(site, Bid.Site):
        return get_bids_from_last_n_hours(session, hours, site)
    return get_docs_from_last_n_hours(session, hours, site)


def send_new_notifications(notifier_config):
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

    Args:
    notifier-config -- a dictionary from site enum to a dictionary containing
        the notifier to use ('notifier') and the emails to send notifications
        to ('recipients')
    Return:
    new_bids_dict -- map from bid.site to list of new bids sent in notification
    """
    new_items_dict = {}
    for site, config in notifier_config.items():
        notifier = config['notifier']
        recipient_emails = config['recipients']
        new_items = get_new_items(Session(), 23, site)
        if new_items:
            try:
                notifier.send_new_items_notification(
                    new_items, recipient_emails)
            except Exception as err:
                log.error(
                    "Caught exception thrown by notifier: {}".format(notifier))
                log.error("Exception caught: {}: {}".format(type(err), err))
                traceback.print_exc()
            new_items_dict[site] = new_items
        else:
            log.info("No new items for {}. Skipping notification.".format(site))
    return new_items_dict
