from db import Session
from bid import Bid, get_new_identifiers
from datetime import datetime
from lxml import etree, html
from base_scraper import BaseScraper
import logging
import scrapelib
import concurrent.futures

# Logger object for this module
log = logging.getLogger(__name__)


class CommBuysScraper(BaseScraper):
    def __init__(self):
        BaseScraper.__init__(
            self,
            "https://www.commbuys.com/bso/external/publicBids.sdo",
            "https://www.commbuys.com/bso/external/bidDetail.sdo"
        )

    def get_site(self):
        return Bid.Site.COMMBUYS

    def scrape(self):
        """Iterates through all of Commbuys and extracts bids.

        This is implemented as follows, starting on the first results page:
          1. Download the results page.
          2. Extract the bid identifiers from this page.
          3. Check which of those identifiers are not yet in our database.
          4. For each of the identifiers not yet in our database:
            4.1. Download the detail page for each identifier.
            4.2. Extract the fields we are interested in.
            4.3. Create a Bid object and store it in the database.
          5. Go to the next page. Repeat from step #1.
        """
        scraper = scrapelib.Scraper()
        current_page = 1
        session = Session()
        while True:
            page = scraper.post(self.results_url, data={
                'mode': 'navigation', 'currentPage': current_page})
            bid_ids = self.scrape_results_page(page.content)
            log.info("Results page {} found bid ids: {}".format(
                current_page, bid_ids))
            if not bid_ids:
                log.info("Page {} has no results. Done scraping."
                         .format(current_page))
                break
            new_ids = get_new_identifiers(bid_ids, self.get_site())
            self.process_new_bids(new_ids, session, scraper)
            # Save all the new bids from this results page in one db call.
            session.commit()
            current_page += 1

    def get_details_for_bid(self, scraper, bid_id):
        """Gets bid details from results page"""
        return scraper.get(self.details_url, params={'bidId': bid_id}), bid_id

    def scrape_results_page(self, page_str):
        """Scrapes the given page as a Commbuys results page.

        Args:
        page_str -- the entire HTML page as a string

        Returns:
        bid_ids -- a list of strings with the bid identifiers found
        """
        tree = html.fromstring(page_str)
        rows = tree.xpath('//table[@id="resultsTable"]/tr')
        bid_ids = []
        for row in rows:
            tds = row.xpath('td')
            # We expect the bid id to be the first column of the row
            if len(tds) < 1:
                log.error("No columns found in row: {}".format(
                    etree.tostring(row)))
                continue
            bid_ids.append("".join(tds[0].xpath('a/text()')).strip())
        return bid_ids

    def scrape_bid_page(self, page, bid_id):
        """Scrapes the given page as a Commbuys bid detail page.

        Relies on the position of information inside the main results table,
        since the HTML contains no semantically-meaninful ids or classes.

        Raises ValueError if it encounters parsing errors.
        """
        tree = html.fromstring(page.content)
        bid_id = self._get_next_sibling_text_for(tree, "Bid Number:")
        description = self._get_next_sibling_text_for(tree, "Description:")
        department = self._get_next_sibling_text_for(tree, "Department:")
        organization = self._get_next_sibling_text_for(tree, "Organization:")
        location = self._get_next_sibling_text_for(tree, "Location:")
        open_date_str = self._get_next_sibling_text_for(tree,
                                                        "Bid Opening Date:")
        open_date = None
        try:
            open_date = datetime.strptime(open_date_str,
                                          '%m/%d/%Y %I:%M:%S %p')
        except ValueError:
            log.warning("Could not parse {} into date".format(open_date_str))
        # Discard empty strings from 'items'
        # TODO: Look into a more robust way of extracting items
        items = list(filter(None, self._get_siblings_text_for(tree,
                                                              "Item #")))
        return Bid(
            identifier=bid_id,
            description=description,
            department=department,
            organization=organization,
            location=location,
            open_date=open_date,
            items=items,
            site=self.get_site().name
        )

    def _get_next_sibling_text_for(self, tree, text):
        """Returns the text in the next 'td' cell after the one with 'text'.

        Raises:
          ValueError if next sibling can't be found.
        """
        siblings_text = self._get_siblings_text_for(tree, text)
        if len(siblings_text) == 0:
            raise ValueError("Could not find next sibling of '{}'"
                             .format(text))
        return siblings_text[0]

    def _get_siblings_text_for(self, tree, text):
        """Returns the list of texts in the next 'td' cells after the one with
        'text'."""
        xpath_str = '//td[contains(text(), "{}")]/following-sibling::td/text()'
        xpath = xpath_str.format(text)
        siblings = tree.xpath(xpath)
        return [sib.strip() for sib in siblings]
