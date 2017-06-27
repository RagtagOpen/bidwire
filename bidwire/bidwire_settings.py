import os

from bid import Bid
from document import Document
from notifiers.boston_bid_notifier import CityOfBostonNotifier
from notifiers.boston_notice_notifier import BostonNoticeNotifier
from notifiers.commbuys_notifier import CommBuysNotifier
from notifiers.knox_tn_agendas_notifier import KnoxCoTNAgendaNotifier
from notifiers.massgov_notifier import MassGovNotifier
from notifiers.memphis_council_calendar_notifier import MemphisCouncilCalNotifier
from scrapers.boston_bid_scraper import CityOfBostonScraper
from scrapers.boston_notice_scraper import NoticesScraper
from scrapers.commbuys_scraper import CommBuysScraper
from scrapers.knox_tn_agendas_scraper import KnoxCoTNAgendaScraper
from scrapers.massgov_eopss_scraper import MassGovEOPSSScraper
from scrapers.memphis_council_calendar_scraper import MemphisCouncilCalScraper

POSTGRES_ENDPOINT = os.environ.get('POSTGRES_ENDPOINT', 'localhost')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
DEBUG_EMAIL = os.environ.get('DEBUG_EMAIL', 'bidwire-logs@googlegroups.com')
ADMIN_EMAIL = "bidwire-admin@googlegroups.com"


def get_recipients_list(env_var_name, default_recipients='bidwire-logs@googlegroups.com'):
    """Extracts and parses a list of email address from the given env variable.

    Arguments:
    env_var_name -- string with the name of the environment variable to use to
        load recipient list; env variable should contain comma-separated list of
        email addresses
    default_recipients (optional) -- the comma-separated list of emails to use if
        no env variable can be found
    """
    recipients_str = os.environ.get(env_var_name, default_recipients)
    # Split into array of strings and strip whitespace.
    return [r.strip() for r in recipients_str.split(',')]

# List of e-mail recipients. Array of e-mail addresses.
EMAIL_RECIPIENTS = get_recipients_list('EMAIL_RECIPIENTS')

# List of e-mail recipients for MEMPHIS_COUNCIL_CALENDAR
MEMPHIS_COUNCIL_CALENDAR_RECIPIENTS = get_recipients_list('MEMPHIS_COUNCIL_CAL_RECIPIENTS')

# List of e-mail recipients for KNOX_COUNTY_COMMISSION_AGENDAS
KNOX_COUNTY_COMMISSION_AGENDA_RECIPIENTS = get_recipients_list('KNOX_COUNTY_COMMISSION_AGENDA_RECIPIENTS')

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
    Document.Site.BOSTON_NOTICES: {
        'scraper': NoticesScraper(),
        'notifier': BostonNoticeNotifier(),
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
        'recipients': MEMPHIS_COUNCIL_CALENDAR_RECIPIENTS
    },
    Document.Site.KNOX_CO_TN_AGENDAS: {
        'scraper': KnoxCoTNAgendaScraper(),
        'notifier': KnoxCoTNAgendaNotifier(),
        'recipients': KNOX_COUNTY_COMMISSION_AGENDA_RECIPIENTS
    },
}
