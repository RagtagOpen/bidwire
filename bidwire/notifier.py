import bid
from cityofboston_notifier import CityOfBostonNotifier
from commbuys_notifier import CommBuysNotifier


def send_new_bids_notifications(recipient_emails):
    """
    Sends new bids notifications for each site/notifier.

    For simplicity, we don't store the time of the last notification sent, and
    instead we rely on the fact that we notify once a day, and scrape at least
    once a day (but sometimes might scrape more than once, because we are
    testing the scrapers). So we retrieve the bids added to the database in the
    last 23 hours, which should include all new bids since the last notification
    (this is not perfect, and will miss new bids if a second scrape happened
    immediately after the previous notification went out). A more robust
    solution would involve storing a timestamp of the last check, and always
    checking against that timestamp.

    Return:
    new_bids_dict -- map from bid.site to list of new bids sent in notification
    """
    notifiers = [
        CityOfBostonNotifier(recipients=recipient_emails),
        CommBuysNotifier(recipients=recipient_emails)
    ]
    new_bids_dict = {}
    for notifier in notifiers:
        site = notifier.get_site()
        new_bids = bid.get_bids_from_last_n_hours(23, notifier.get_site())
        if len(new_bids) > 0:
            notifier.send_new_bids_notification(new_bids)
        new_bids_dict[site] = new_bids
    return new_bids_dict
