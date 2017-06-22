"""Main BidWire entrypoint"""

import logging
import notifier
import os
import scraper
import time

from bidwire_settings import SITE_CONFIG
from debug_email import DebugEmail


log = logging.getLogger(__name__)


def main():
    log.info("Starting Bidwire run")
    start = time.time()

    scraper.scrape(SITE_CONFIG)
    log.info("Scraping complete. Sending notifications.")
    new_bids = notifier.send_new_notifications(SITE_CONFIG)
    elapsed_secs = time.time() - start

    log.info("Notification sending complete. Sending debug email.")
    DebugEmail().send(new_bids, SITE_CONFIG, elapsed_secs)


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=os.getenv('BIDWIRE_LOG_LEVEL', logging.INFO))
    main()
