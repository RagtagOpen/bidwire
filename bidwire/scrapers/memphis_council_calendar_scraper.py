import logging
import urllib.parse

import scrapelib
from lxml import html

import db

from .base_scraper import BaseScraper
from document import Document, get_new_urls


log = logging.getLogger(__name__)


class MemphisCouncilCalScraper(BaseScraper):
    SITE_ROOT_URL = "http://memphistn.gov/"
    CALENDAR_PAGE_URL = "http://www.memphistn.gov/Government/CityCouncil/CityCouncilMeetingCalendar,AgendasMinutes.aspx"

    def __init__(self):
        self.scraper = scrapelib.Scraper()

    def scrape(self):
        """Scrapes MemphisCouncilCalScraper.SITE_ROOT_URL and stores any new documents in the DB."""
        page = self.scraper.get(MemphisCouncilCalScraper.CALENDAR_PAGE_URL)
        documents = self._get_docs_from_calendar(page.content)
        log.info("Found {} documents".format(len(documents)))

        # Only store in the database documents that are new to us.
        # (Not the most efficient implementation, but good enough, given that there are usually
        # less than 20 documents on this page.)
        session = db.Session()
        doc_urls = [doc.url for doc in documents]
        new_urls = get_new_urls(
            session, doc_urls, Document.Site.MEMPHIS_COUNCIL_CALENDAR)
        new_docs = [doc for doc in documents if doc.url in new_urls]
        log.info("New documents: {}".format(new_docs))
        session.bulk_save_objects(new_docs)
        session.commit()

    def _get_docs_from_calendar(self, page_str):
        """Scrape the calendar page, extracting links and titles to documents.

        Returns:
        list of Document objects (not yet persisted to database)
        """
        page = self.scraper.get(MemphisCouncilCalScraper.CALENDAR_PAGE_URL)
        doctree = html.fromstring(page_str)
        # Extract all the rows from the table of class "councilTable", except
        # the ones with 'th'
        rows = doctree.xpath(
            '//table[contains(@class, "councilTable")]//tr[not(descendant::th)]')
        documents = []
        for row in rows:
            # We expect each row to have 5 cells in order: date, agenda,
            # schedule, docs, minutes
            cells = row.xpath('td')
            if len(cells) != 5:
                log.error("Unexpected number of cells in row: {}".format(
                    row.text_content()))
                continue
            date_str = cells[0].text.strip()  # Something like "Jan 3"
            doc_links = cells[3].xpath('a')
            for link in doc_links:
                hrefs = link.xpath('@href')
                if len(hrefs) < 1:
                    log.error("Unexpected number of hrefs in link: {}".format(
                        link.text_content()))
                    continue
                doc_url = self._ensure_absolute_url(hrefs[0])
                # Because the text in the links is often the same (e.g "Council Documents"), we add
                # the date string to the title to help disambiguate
                doc_title = "{}: {}".format(date_str, link.text.strip())
                documents.append(Document(
                    url=doc_url,
                    title=doc_title,
                    site=Document.Site.MEMPHIS_COUNCIL_CALENDAR.name
                ))
        return documents

    def _ensure_absolute_url(self, url):
        """If the given URL is relative, makes it absolute by prepending the site root URL."""
        if not url.startswith(MemphisCouncilCalScraper.SITE_ROOT_URL):
            return urllib.parse.urljoin(MemphisCouncilCalScraper.SITE_ROOT_URL, url)
        return url
