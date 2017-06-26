import pytest

from scrapers.massgov import results_page_scraper
from . import utils

def test_scrape_results_page():
    page_str = open(utils.get_abs_filename('massgov-results-page.html'), 'r').read()
    xpath_list = ['//ul[@class="category"]/li', './h2/span/a[@class="titlelink"]']
    url_dict = results_page_scraper.scrape_results_page(page_str, xpath_list)
    assert len(url_dict) == 2
    assert "https://www.mass.gov/eopss/docs/ogr/homesec/ffy2017-bidders-conference-presentation-hsgp.pdf" \
           in url_dict.keys()
    assert "FFY 2017 Bidder's General Information Presentation" in url_dict.values()
