from scrapers.memphis_council_calendar_scraper import MemphisCouncilCalScraper
from . import utils


def test_get_docs_from_page():
    memphis_scraper = MemphisCouncilCalScraper()
    page_str = open(utils.get_abs_filename(
        'memphis-city-council-calendar.html'), 'r').read()
    docs = memphis_scraper._get_docs_from_calendar(page_str)
    assert len(docs) == 26
    for doc in docs:
        # All URLs should be absolute.
        assert doc.url.startswith("http://")
