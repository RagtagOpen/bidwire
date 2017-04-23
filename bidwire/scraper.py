from scrapers.cityofboston_scraper import CityOfBostonScraper
from scrapers.commbuys_scraper import CommBuysScraper

def scrape():
    """Run through all the scrapers"""
    scrapers = [CommBuysScraper(), CityOfBostonScraper()]
    for scraper in scrapers:
        scraper.scrape()
