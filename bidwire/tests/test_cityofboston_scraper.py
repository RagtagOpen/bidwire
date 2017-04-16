import os
import pytest

from cityofboston_scraper import CityOfBostonScraper


def _abs_file(filename):
    """Given a filename relative to the current file, returns the absolute filename"""
    absolute_current_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(absolute_current_dir, filename)


def test_scrape_results_page():
    page_str = open(_abs_file('cityofboston-results-page.html'), 'r').read()
    cityofboston_scraper = CityOfBostonScraper()
    bid_ids = cityofboston_scraper.scrape_results_page(page_str)
    assert len(bid_ids) == 79
    assert "23315" in bid_ids
    assert "23360" in bid_ids
