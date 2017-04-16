from db import Session
from bid import Bid, get_new_identifiers
from datetime import datetime
from lxml import etree, html
import logging
import scrapelib
import concurrent.futures

# Logger object for this module
log = logging.getLogger(__name__)

# Number of concurrent threads to process results page
NUMBER_OF_THREADS = 5


class BaseScraper:
    def __init__(self, results_url, details_url):
        self.results_url = results_url
        self.details_url = details_url

    def get_site(self):
        raise NotImplementedError

    def scrape(self):
        """Iterates through a single results page and extracts bids.
        If site requires iterating over multiple pages, the class must
        override this method.

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
        session = Session()
        page = scraper.get(self.results_url)
        bid_ids = self.scrape_results_page(page.content)
        log.info("Found bid ids: {}".format(bid_ids))
        new_ids = get_new_identifiers(bid_ids, self.get_site())
        self.process_new_bids(new_ids, session, scraper)
        # Save all the new bids from this results page in one db call.
        session.commit()

    def process_new_bids(self, new_ids, session, scraper):
        """Gets bid details from results page and adds Bid objects to db session

        Args:
        new_ids -- list of new bid ids
        session -- the active database session
        scraper -- scraper object
        """
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=NUMBER_OF_THREADS
            ) as executor:
            # Use a thread pool for concurrently retrieving the HTML data
            futures = list(map(lambda bid_id:
                               executor.submit(
                                self.get_details_for_bid, scraper,
                                bid_id), new_ids))
            for future in concurrent.futures.as_completed(futures):
                try:
                    bid_page, bid_id = future.result()
                except Exception as exc:
                    log.error("Exception: {}".format(exc))
                else:
                    bid = self.scrape_bid_page(bid_page, bid_id)
                    log.info("Found new bid: {}".format(bid))
                    session.add(bid)

    def get_details_for_bid(self, scraper, bid_id):
        raise NotImplementedError

    def scrape_results_page(self, page_str):
        raise NotImplementedError

    def scrape_bid_page(self, page, bid_id):
        raise NotImplementedError
