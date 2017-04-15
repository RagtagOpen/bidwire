from bid import Bid, get_new_identifiers
from datetime import datetime
from lxml import etree, html
from base_scraper import BaseScraper
import logging
import scrapelib
import concurrent.futures
import re

# Logger object for this module
log = logging.getLogger(__name__)

compiled_reg_exp = re.compile("bids\.asp\?ID=(\d+)")


class CityOfBostonScraper(BaseScraper):
    def __init__(self):
        BaseScraper.__init__(
            self,
            "https://www.cityofboston.gov/purchasing/bid.asp",
            "https://www.cityofboston.gov/purchasing/bids.asp"
        )

    def get_site(self):
        return 'CITY_OF_BOSTON'

    def get_details_for_bid(self, scraper, bid_id):
        """Gets bid details from results page"""
        return scraper.get(self.details_url, params={'ID': bid_id}), bid_id

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

    def scrape_bid_page(self, page, bid_id):
        """Scrapes the given page as a City of Boston bid detail page.

        Relies on the position of information inside the main results table,
        since the HTML contains no semantically-meaninful ids or classes.

        Raises ValueError if it encounters parsing errors.
        """
        tree = html.fromstring(page.content)
        first_center = tree.xpath('//center')[0]
        start_text_element = first_center.xpath('b')[0]
        description = start_text_element.text.strip()
        items = "".join(first_center.xpath('text()'))
        return Bid(
            identifier=bid_id,
            description=description,
            items=items,
            site=self.get_site()
        )
