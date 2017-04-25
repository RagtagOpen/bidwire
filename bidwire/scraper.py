from scrapers.cityofboston_scraper import CityOfBostonScraper
from scrapers.commbuys_scraper import CommBuysScraper
from scrapers.massgov_eopss_scraper import MassGovEOPSSScraper

def scrape():
    """Run through all the scrapers"""
    scrapers = [MassGovEOPSSScraper()]
    # scrapers = [CommBuysScraper(), CityOfBostonScraper()]
    for scraper in scrapers:
        scraper.scrape()
