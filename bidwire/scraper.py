from cityofboston_scraper import CityOfBostonScraper
from commbuys_scraper import CommBuysScraper


def scrape():
    """Run through all the scrapers"""
    scrapers = [CommBuysScraper(), CityOfBostonScraper()]
    for scraper in scrapers:
        scraper.scrape()
