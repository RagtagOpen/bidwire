import logging
import re
from concurrent.futures import ThreadPoolExecutor
import scrapelib

from lxml import html

from .base_scraper import BaseScraper
from bid import Bid, get_new_identifiers

# Logger object for this module
log = logging.getLogger(__name__)

compiled_reg_exp = re.compile("bids\.asp\?ID=(\d+)")


class CityOfBostonScraper(BaseScraper):
    RESULTS_URL = "https://www.cityofboston.gov/purchasing/bid.asp"
    DETAILS_URL = "https://www.cityofboston.gov/purchasing/bids.asp"

    def __init__(self, threads=1, processes=4):
        self.scraper = scrapelib.Scraper()
        self.thread_executor = ThreadPoolExecutor(threads)

    def scrape_bids(self, session):
        """Iterates through a single results page and extracts bids.

        This is implemented as follows:
          1. Download the results page.
          2. Extract the bid identifiers from this page.
          3. Check which of those identifiers are not yet in our database.
          4. For each of the identifiers not yet in our database:
            4.1. Download the detail page for each identifier.
            4.2. Extract the fields we are interested in.
            4.3. Create a Bid object and store it in the database.

        Arguments:
        session -- database session to use for persisting items
        """
        bid_page = self.scraper.get(self.RESULTS_URL)
        bid_ids = self.scrape_results_page(bid_page.content)
        log.info("Found bid ids: {}".format(bid_ids))
        new_ids = get_new_identifiers(session, bid_ids, self.get_site())
        bids = self.thread_executor.map(self.scrape_bid_page, map(self.get_bid_page, new_ids))
        session.bulk_save_objects(bids)

    def get_bid_page(self, bid_id):
            return bid_id, self.scraper.get(self.DETAILS_URL, params={'ID': bid_id}).content

    def scrape(self, session):
        self.scrape_bids(session)

    def get_site(self):
        return Bid.Site.CITYOFBOSTON

    def scrape_results_page(self, page_str):
        """Scrapes the City of Boston results page.

        Args:
        page_str -- the entire HTML page as a string

        Returns:
        bid_ids -- a list of strings with the bid identifiers found
        """
        tree = html.fromstring(page_str)
        # Bid urls are encoded as `bids.asp?ID=<bidId>` in the table
        bid_id_urls = tree.xpath('//b/a/@href')
        bid_ids = []
        for bid_id_url in bid_id_urls:
            bid_id = self.get_bid_id(bid_id_url)
            if bid_id is None:
                continue
            bid_ids.append("".join(bid_id).strip())
        return bid_ids

    def get_bid_id(self, href):
        """Extracts the ID from the href link"""
        regexp_match = compiled_reg_exp.match(href)
        if regexp_match:
            return regexp_match.group(1)
        return None

    def scrape_bid_page(self, pair):
        """Scrapes the City of Boston bid detail page for the given bid_id.

        Relies on the position of information inside the main results table,
        since the HTML contains no semantically-meaninful ids or classes.

        Raises ValueError if it encounters parsing errors.
        """
        bid_id, page = pair
        tree = html.fromstring(page)
        first_center = tree.xpath('//center')[0]
        start_text_element = first_center.xpath('b')[0]
        description = start_text_element.text.strip()
        items = ["".join(first_center.xpath('text()'))]
        return Bid(
            identifier=bid_id,
            description=description,
            items=items,
            site=self.get_site().name
        )