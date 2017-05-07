from scrapers.cityofboston_scraper import CityOfBostonScraper
from scrapers.commbuys_scraper import CommBuysScraper
from scrapers.massgov_eopss_scraper import MassGovEOPSSScraper

scrapers = [CommBuysScraper(), CityOfBostonScraper(), MassGovEOPSSScraper()]


def scrape(scrapers=scrapers):
    """Run through all the scrapers"""
    for scraper in scrapers:
        scraper.scrape()
