from manager import Manager

from scrapers.cityofboston_scraper import CityOfBostonScraper
from scrapers.commbuys_scraper import CommBuysScraper
from scrapers.massgov_eopss_scraper import MassGovEOPSSScraper
from scrapers.memphis_council_calendar_scraper import MemphisCouncilCalScraper
from notifiers.massgov_notifier import MassGovNotifier
from notifiers.cityofboston_notifier import CityOfBostonNotifier
from notifiers.commbuys_notifier import CommBuysNotifier
import scraper
import notifier
import logging

manager = Manager()

site_dict = {
    'COMMBUYS': {
        'scraper': CommBuysScraper(),
        'notifier': CommBuysNotifier()
    },
    'CITYOFBOSTON': {
        'scraper': CityOfBostonScraper(),
        'notifier': CityOfBostonNotifier()
    },
    'MASSGOV_EOPSS': {
        'scraper': MassGovEOPSSScraper(),
        'notifier': MassGovNotifier()
    },
    'MEMPHIS_COUNCIL_CALENDAR': {
        'scraper': MemphisCouncilCalScraper(),
        'notifier': None
    }
}

@manager.command
def scrape(site=''):
    """runs scraper for given <site>"""
    scraper.scrape([site_dict[site]['scraper']])

@manager.command
def notify(site='', recipients=''):
    """runs notifier for given <site>, sending email to <recipient>"""
    notifier.send_new_notifications(
        [r.strip() for r in recipients.split(',')],
        notifiers=[site_dict[site]['notifier']]
    )

@manager.command
def dryrun(site='', recipients=''):
    """scrape/notify for given <site>, sending email to <recipient>"""
    scrape(site)
    notify(site, recipients)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    manager.main()
