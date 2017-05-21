from document import Document, get_new_urls
from .base_scraper import BaseScraper
import logging
import scrapelib

from .massgov import url_scraper_dict
from .massgov import results_page_scraper


log = logging.getLogger(__name__)

URL_PREFIX = 'http://www.mass.gov/eopss/funding-and-training/'


class MassGovEOPSSScraper(BaseScraper):
    def __init__(self):
        self.url_dict = url_scraper_dict.MASSGOV_DICT

    def get_site(self):
        return Document.Site.MASSGOV_EOPSS

    def scrape(self, session):
        """Iterates through all the sites in url_dict to extract new documents.

        This is implemented as follows:
          1. Download each of the pages.
          2. Extract the URLs from the pages.
          3. Check which of those URLs are not yet in our database.
          4. For each of the URLs that are not yet in our database, 
             add them as a new Bid object to the database.
        """
        scraper = scrapelib.Scraper()
        for url, xpaths in self.url_dict.items():
            page = scraper.get(URL_PREFIX + url)
            # doc_ids is dictionary: relative URL => title of doc
            doc_ids = \
                results_page_scraper.scrape_results_page(page.content, xpaths)
            log.info("Found docs: {}".format(doc_ids))
            new_urls = get_new_urls(
                session,
                doc_ids.keys(),  # relative URL is the identifier
                self.get_site()
            )
            log.info("New docs: {}".format(new_urls))
            new_docs = self.add_new_documents(new_urls, doc_ids)
            session.add_all(new_docs)
            # Save all the new docs from this results page in one db call.
            session.commit()

    def add_new_documents(self, new_urls, doc_ids):
        docs = []
        for url in new_urls:
            docs.append(Document(
                url=url,
                title=doc_ids[url],
                site=self.get_site().name
            ))
        return docs
