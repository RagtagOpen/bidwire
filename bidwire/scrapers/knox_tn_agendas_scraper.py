import logging
import scrapelib
from lxml import html
from urllib import parse

from sqlalchemy.exc import IntegrityError

from document import Document
from scrapers.base_scraper import BaseScraper
from utils import ensure_absolute_url

log = logging.getLogger(__name__)


class KnoxCoTNAgendaScraper(BaseScraper):
    SITE_ROOT_URL = 'https://destinyhosted.com/'
    MEETING_SCHEDULE_URL = 'https://destinyhosted.com/agenda_publish.cfm?id=56691&mt=ALL'

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
        log.info("New Documents: %s", new_docs)
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

        tables = doctree.findall('body/div/form/table/tbody')

        # There should be 3 tables on the page. The second one is the one we want
        if len(tables) < 2:
            log.error("Knox Agendas: required table not found in page")
            raise ValueError('required table not found in page')

        table = tables[1]

        # We don't care about the table header, it contains the values Agendas and Meetings
        rows = table.findall('tr')

        documents = []
        for row in rows:
            # The first cell is a link to the Agenda doc and the anchor text is the date of the meeting
            # The second cell is the name of the meeting
            agenda, meeting = row.findall('td')[:2]

            meeting_name = meeting.text.strip()
            agenda_anchor = agenda.find('a')

            if agenda_anchor is None:
                log.error("Knox Agendas: no document link in the meetings table")
                raise ValueError('no document link in the meetings table')

            agenda_date = agenda_anchor.text.strip()
            doc_url = agenda_anchor.get('href')

            if not doc_url:
                log.error("Knox Agendas: no href in the anchor tag for %s: %s", agenda_date, meeting_name)
                raise ValueError('no href in document anchor')

            doc_url = ensure_absolute_url(self.SITE_ROOT_URL, doc_url)

            # The anchor title is useless, so use the meeting name in the doc name
            doc_name = "{}: {}".format(agenda_date, meeting_name)
            documents.append(
                Document(
                    url=doc_url,
                    title=doc_name,
                    site=Document.Site.KNOX_CO_TN_AGENDAS.name,
                )
            )

        return documents
