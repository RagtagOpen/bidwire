"""Main BidWire entrypoint"""

import bid
import logging
import notifier
import scraper

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # Run ALL the scraping!
    scraper.scrape()
    # Send notifications for new bids
    notifier.send_new_bids_notification()
