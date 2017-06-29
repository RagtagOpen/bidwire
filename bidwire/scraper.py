import logging
import traceback

from db import Session
from scrapers.boston_bid_scraper import CityOfBostonScraper
from scrapers.commbuys_scraper import CommBuysScraper
from scrapers.massgov_eopss_scraper import MassGovEOPSSScraper


log = logging.getLogger(__name__)


def scrape(site_config):
    """Run through all the scrapers.

    Arguments:
    site_config -- dictionary keyed by site enum that says which scrapers to use
    """
    for site, config in site_config.items():
        log.info("Scraping site {}".format(site))
        scraper = config['scraper']
        try:
            scraper.scrape(Session())
        except Exception as err:
            log.error("Caught exception thrown by scraper: {}".format(scraper))
            log.error("Exception caught: {}: {}".format(type(err), err))
            traceback.print_exc()
