import commbuys_scraper
from cityofboston_scraper import CityOfBostonScraper

def scrape():
    """Run through all the scrapers"""
    # commbuys_scraper.scrape()
    cityofboston_scraper = CityOfBostonScraper()
    cityofboston_scraper.scrape()
