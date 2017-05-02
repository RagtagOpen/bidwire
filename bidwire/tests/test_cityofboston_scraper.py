import pytest

from scrapers.cityofboston_scraper import CityOfBostonScraper
from . import test_utils

def test_scrape_results_page():
    page_str = open(test_utils._abs_file('cityofboston-results-page.html'), 'r').read()
    cityofboston_scraper = CityOfBostonScraper()
    bid_ids = cityofboston_scraper.scrape_results_page(page_str)
    assert len(bid_ids) == 79
    assert "23315" in bid_ids
    assert "23360" in bid_ids
