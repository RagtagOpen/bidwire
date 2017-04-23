import os
import pytest

from scrapers.commbuys_scraper import CommBuysScraper


def _abs_file(filename):
    """Given a filename relative to the current file, returns the absolute filename"""
    absolute_current_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(absolute_current_dir, filename)


def test_scrape_results_page():
    page_str = open(_abs_file('commbuys-results-page.html'), 'r').read()
    commbuys_scraper = CommBuysScraper()
    bid_ids = commbuys_scraper.scrape_results_page(page_str)
    assert len(bid_ids) == 25
    assert "BD-17-1002-1003-001-14907" in bid_ids
    assert "BD-17-1022-DMH08-8210B-14821" in bid_ids
