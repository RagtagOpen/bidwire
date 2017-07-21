import logging
import scrapelib
from lxml import html

from sqlalchemy.exc import IntegrityError

from document import Document
from scrapers.base_scraper import BaseScraper
from utils import ensure_absolute_url

log = logging.getLogger(__name__)


class KnoxvilleTNMeetingScraper(BaseScraper):
    SITE_ROOT_URL = 'https://knoxvillecitytn.iqm2.com/Citizens/'
    MEETING_SCHEDULE_URL = 'https://knoxvillecitytn.iqm2.com/Citizens/Calendar.aspx'

    def __init__(self) -> None:
        self.scraper = scrapelib.Scraper()

    def scrape(self, session):
        page = self.scraper.get(self.MEETING_SCHEDULE_URL)
        documents = self._get_docs_from_schedule(page.content)
        log.debug("Found %d documents", len(documents))
        new_docs = []
        for doc in documents:
            try:
                with session.begin_nested():
                    session.add(doc)
            except IntegrityError:
                log.debug('Already have document %s', doc)
            else:
                new_docs.append(doc)
        log.info("%d New Documents: %s", len(new_docs), new_docs)
        session.commit()

    def _get_docs_from_schedule(self, page_str):
        """
        Parse the contents of the meeting schedule page and extract document
        links and title.

        Parameters:
        A string containing the page HTML

        Returns:
        list of Document objects (not yet persisted to database)
        """
        doctree = html.fromstring(page_str)

        rows = doctree.xpath(".//div[@id='ContentPlaceholder1_pnlMeetings']/div")
        documents = []
        for row in rows:
            if "MeetingRow" not in row.get("class", ""):
                log.debug("skipping row")
                continue

            date = None
            name = None
            docs_for_meeting = []

            for element in row.iter():
                if element.get("class") == "RowLink":
                    links = element.findall("a")
                    if len(links) != 1:
                        raise ValueError("Wrong number of date links in meeting row")
                    date = links[0].text

                if element.get("class") == "RowRight MeetingLinks":
                    links = element.findall(".//a")
                    for link in links:

                        doc_name, doc_href = link.text, link.get('href')
                        if doc_href == "#":
                            doc_href = ""
                        if doc_name and doc_href:
                            docs_for_meeting.append((doc_name, doc_href))

                if element.get("class") == "MainScreenText RowDetails":
                    name = element.text

            if not (name and date):
                raise ValueError("Either name or date was missing from a row.")

            for doc in docs_for_meeting:
                doc_url = ensure_absolute_url(self.SITE_ROOT_URL, doc[1])

                # The anchor title is useless, so use the meeting name in the doc name
                doc_name = "{} {}: {}".format(date, name, doc[0])
                documents.append(
                    Document(
                        url=doc_url,
                        title=doc_name,
                        site=Document.Site.KNOXVILLE_TN_MEETINGS.name,
                    )
                )

        return documents
