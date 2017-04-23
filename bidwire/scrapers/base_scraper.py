import abc
import concurrent.futures
import logging

from datetime import datetime
from lxml import etree, html
import scrapelib

from bid import Bid, get_new_identifiers
from db import Session


class BaseScraper(metaclass=abc.ABCMeta):
    """The interface that must be implemented by all scrapers."""

    @abc.abstractmethod
    def scrape(self):
        """
        This method performs all scraping for this scraper. Must be implemented
        by subclasses.
        """
        pass
