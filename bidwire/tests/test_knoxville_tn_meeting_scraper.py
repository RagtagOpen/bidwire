import responses

from document import Document
from scrapers.knoxville_tn_meetings_scraper import KnoxvilleTNMeetingScraper
from . import common
from . import utils


class TestKnoxvilleMeetingScraper(object):
    session = None
    page_str = ""

    def test_get_docs_from_page(self):
        scraper = KnoxvilleTNMeetingScraper()
        docs = scraper._get_docs_from_schedule(self.page_str)

        # verified by hand for the date the page source was pulled
        assert len(docs) == 72
        for doc in docs:
            # All URLs should be absolute.
            assert doc.url.startswith('https://')
        actual_titles = {doc.title for doc in docs}
        sample_expected_titles = {
            'Jan 12, 2017 5:30 PM  Beer Board - Workshop: Agenda',
            'Feb 28, 2017 6:00 PM  City Council - Regular Meeting: Agenda',
            'Mar 28, 2017 6:00 PM  City Council - Regular Meeting: Agenda Packet',
            'Jul 18, 2017 6:00 PM  City Council - Regular Meeting: Agenda Packet',
        }
        assert sample_expected_titles & actual_titles == sample_expected_titles

    @responses.activate
    def test_full_scraper(self):
        self.session.query(Document).delete()
        count = self.session.query(Document).count()
        assert count == 0
        responses.add(
            responses.GET,
            KnoxvilleTNMeetingScraper.MEETING_SCHEDULE_URL,
            body=self.page_str,
            status=200,
            match_querystring=True
        )
        scraper = KnoxvilleTNMeetingScraper()
        scraper.scrape(self.session)
        docs = self.session.query(Document).all()
        assert len(docs) == 72
        sample_expected_titles = {
            'Jan 12, 2017 5:30 PM  Beer Board - Workshop: Agenda',
            'Feb 28, 2017 6:00 PM  City Council - Regular Meeting: Agenda',
            'Mar 28, 2017 6:00 PM  City Council - Regular Meeting: Agenda Packet',
            'Jul 18, 2017 6:00 PM  City Council - Regular Meeting: Agenda Packet',
        }
        actual_titles = {doc.title for doc in docs}
        assert sample_expected_titles & actual_titles == sample_expected_titles

    @classmethod
    def setup_class(cls):
        cls.session = common.Session()

        with open(utils.get_abs_filename('knoxville_tn_results_page.html'), 'r') as page:
            cls.page_str = page.read()

    @classmethod
    def teardown_class(cls):
        common.Session.remove()

    def setup_method(self, test_method):
        self.session.begin_nested()

    def teardown_method(self, test_method):
        self.session.rollback()
