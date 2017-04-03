"""Main BidWire entrypoint"""

import logging
import scraper

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # Run ALL the scraping!
    scraper.scrape()
