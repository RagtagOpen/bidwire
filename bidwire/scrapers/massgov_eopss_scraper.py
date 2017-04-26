from bid import Bid, get_new_identifiers
from .base_scraper import BaseScraper
from .massgov import url_scraper_dict
from .massgov import results_page_scraper
from db import Session
import logging
import scrapelib

# Logger object for this module
log = logging.getLogger(__name__)

URL_PREFIX = 'http://www.mass.gov/eopss/funding-and-training/'


class MassGovEOPSSScraper(BaseScraper):
    def __init__(self):
        self.url_dict = url_scraper_dict.get_dict();

    def get_site(self):
        return Bid.Site.MASSGOV_EOPSS

    def scrape(self):
        """Iterates through all the sites in url_dict to extract new documents.

        This is implemented as follows:
          1. Download each of the pages.
          2. Extract the URLs from the pages.
          3. Check which of those URLs are not yet in our database.
          4. For each of the URLs that are not yet in our database, 
             add them as a new Bid object to the database.
        """
        scraper = scrapelib.Scraper()
        session = Session()
        for url, xpaths in self.url_dict.items():
            page = scraper.get(URL_PREFIX + url)
            # doc_ids is dictionary: relative URL => title of doc
            doc_ids = \
                results_page_scraper.scrape_results_page(page.content, xpaths)
            log.info("Found docs: {}".format(doc_ids))
            new_ids = get_new_identifiers(
                session,
                doc_ids.keys(),  # relative URL is the identifier
                self.get_site()
            )
            log.info("New docs: {}".format(new_ids))
            new_bids = self.add_new_bids(new_ids, doc_ids)
            session.add_all(new_bids)
            # Save all the new bids from this results page in one db call.
            session.commit()

    def add_new_bids(self, new_ids, doc_ids):
        bids = []
        for new_id in new_ids:
            bids.append(Bid(
                identifier=new_id,
                description=doc_ids[new_id],
                site=self.get_site().name
            ))
        return bids
