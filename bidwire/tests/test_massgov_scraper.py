import os
import pytest

from scrapers.massgov import results_page_scraper


def _abs_file(filename):
    """Given a filename relative to the current file, returns the absolute filename"""
    absolute_current_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(absolute_current_dir, filename)


def test_scrape_results_page():
    page_str = open(_abs_file('massgov-results-page.html'), 'r').read()
    xpath_list = ['//ul[@class="category"]/li', './h2/span/a[@class="titlelink"]']
    url_dict = results_page_scraper.scrape_results_page(page_str, xpath_list)
    assert len(url_dict) == 2
    assert "/eopss/docs/ogr/homesec/ffy2017-bidders-conference-presentation-hsgp.pdf" \
           in url_dict.keys()
    assert "FFY 2017 Bidder's General Information Presentation" in url_dict.values()