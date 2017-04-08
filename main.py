"""Main BidWire entrypoint"""

import bid
import bidwire_settings
import logging
import notifier
import scraper

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # Run ALL the scraping!
    scraper.scrape()
    # Retrieve the bids we found in the last 23 hours -- if we
    # scrape once a day, this means the new bids in the last scrape.
    new_bids = bid.get_bids_from_last_n_hours(23)
    notifier.send_new_bids_notification(new_bids,
                                        bidwire_settings.EMAIL_RECIPIENTS)
