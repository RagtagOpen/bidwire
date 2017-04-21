"""Main BidWire entrypoint"""

import debug_email
import logging
import notifier
import scraper
from bidwire_settings import EMAIL_RECIPIENTS


def main():
    scraper.scrape()
    new_bids = notifier.send_new_bids_notifications(EMAIL_RECIPIENTS)
    debug_email.send_debug_email(new_bids, EMAIL_RECIPIENTS)


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    main()
