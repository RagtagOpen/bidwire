import abc

class BaseScraper(metaclass=abc.ABCMeta):
    """The interface that must be implemented by all scrapers."""

    @abc.abstractmethod
    def scrape(self, session):
        """
        This method performs all scraping for this scraper. Must be implemented
        by subclasses.

        Arguments:
        session -- database session to use for persisting items
        """
        pass
