import pytest

from scrapers.boston_bid_scraper import CityOfBostonScraper
from . import utils

def test_scrape_results_page():
    page_str = open(utils.get_abs_filename('cityofboston-results-page.html'), 'r').read()
    cityofboston_scraper = CityOfBostonScraper()
    bid_ids = cityofboston_scraper.scrape_results_page(page_str)
    assert len(bid_ids) == 79
    assert "23315" in bid_ids
    assert "23360" in bid_ids
