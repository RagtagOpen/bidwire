import os

from bid import Bid
from document import Document
from notifiers.cityofboston_notifier import CityOfBostonNotifier
from notifiers.commbuys_notifier import CommBuysNotifier
from notifiers.massgov_notifier import MassGovNotifier
from notifiers.memphis_council_calendar_notifier import MemphisCouncilCalNotifier
from scrapers.cityofboston_scraper import CityOfBostonScraper
from scrapers.commbuys_scraper import CommBuysScraper
from scrapers.massgov_eopss_scraper import MassGovEOPSSScraper
from scrapers.memphis_council_calendar_scraper import MemphisCouncilCalScraper

POSTGRES_ENDPOINT = os.environ.get('POSTGRES_ENDPOINT', 'localhost')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
DEBUG_EMAIL = os.environ.get('DEBUG_EMAIL', 'bidwire-logs@googlegroups.com')
ADMIN_EMAIL = "bidwire-admin@googlegroups.com"


def get_recipients_list():
    # The env variable should contain a comma-separated recipient list.
    recipients_str = os.environ.get('EMAIL_RECIPIENTS',
                                    'bidwire-logs@googlegroups.com')
    # Split into array of strings and strip whitespace.
    return [r.strip() for r in recipients_str.split(',')]


# List of e-mail recipients. Array of e-mail addresses.
EMAIL_RECIPIENTS = get_recipients_list()

# A dictionary representing which scrapers, notifiers and recipients to
# use for each site
SITE_CONFIG = {
    Bid.Site.COMMBUYS: {
        'scraper': CommBuysScraper(),
        'notifier': CommBuysNotifier(),
        'recipients': EMAIL_RECIPIENTS
    },
    Bid.Site.CITYOFBOSTON: {
        'scraper': CityOfBostonScraper(),
        'notifier': CityOfBostonNotifier(),
        'recipients': EMAIL_RECIPIENTS
    },
    Document.Site.MASSGOV_EOPSS: {
        'scraper': MassGovEOPSSScraper(),
        'notifier': MassGovNotifier(),
        'recipients': EMAIL_RECIPIENTS
    },
    Document.Site.MEMPHIS_COUNCIL_CALENDAR: {
        'scraper': MemphisCouncilCalScraper(),
        'notifier': MemphisCouncilCalNotifier(),
        # TODO(anaulin): Replace this with env-variable-based config for Memphis recipients
        'recipients': ["bidwire-logs@googlegroups.com"]
    }
}
