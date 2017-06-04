import logging
import re
from datetime import datetime
from datetime import date as dtdate
import scrapelib

from lxml import etree, html

from .base_scraper import BaseScraper
from bid import Bid, get_new_identifiers
from notice import Notice
from utils import execute_parallel

# Logger object for this module
log = logging.getLogger(__name__)

compiled_reg_exp = re.compile("bids\.asp\?ID=(\d+)")


# TODO: add https://www.boston.gov/public-notices
# Might not be appropriate for this file. Review the story:
# https://www.pivotaltracker.com/n/projects/1996883/stories/145036889


class BostonPublicNoticeScraper(BaseScraper):
    notices_url = "https://www.boston.gov/public-notices"

    def __init__(self):
        self.scraper = scrapelib.Scraper()

    def scrape(self, session):
        page = self.scraper.get(self.notices_url)
        notice_ids = self.scrape_notices_page(page.content)

    @staticmethod
    def scrape_notice_div(div):
        title_a = div.xpath("//div['n-li-t'=@class]/a")[0]
        year, month, day_and_start, end = div.xpath("//span['dc:date'=@property]/@content")[0].split('-')
        day, start = day_and_start.split('T')
        date = dtdate(year, month, day)
        posted_candidates = div.xpath("//span['dl-d'=@class]")
        for cand in posted_candidates:
            if re.match('\d\d/\d\d/\d\d\d\d - \d:\d\d[ap]m', cand.text):
                posted = datetime.strptime(cand.text, '%m/%d/%Y - %I:%M%p')
                break
        else:
            raise ValueError("Couldn't get time of post")
        return Notice(
            title=title_a.get('title'),
            href=title_a.get('href'),
            start=datetime.combine(date, datetime.strptime(start, '%H:%M:%S').time()),
            end=datetime.combine(date, datetime.strptime(end, '%H:%M').time()),
            location=div.xpath("//div['name-block'=@class]")[0].text,
            thoroughfare=div.xpath("//div['thoroughfare'=@class]")[0].text,
            premise=div.xpath("//div['premise'=@class]")[0].text,
            city=div.xpath("//span['locality'=@class]")[0].text,
            state=div.xpath("//span['state'=@class]")[0].text,
            postcode=div.xpath("//span['postal-code'=@class]")[0].text,
            posted=posted
        )

    def scrape_notices_page(self, content):
        tree = html.fromstring(content)
        notice_divs = tree.xpath('//div["g g--m0 n-li"=@class]')
        return map(self.scrape_notice_div, notice_divs)


class CityOfBostonScraper(BaseScraper):
    def __init__(self):
        self.results_url = "https://www.cityofboston.gov/purchasing/bid.asp"
        self.details_url = "https://www.cityofboston.gov/purchasing/bids.asp"
        self.scraper = scrapelib.Scraper()

    def scrape(self, session):
        """Iterates through a single results page and extracts bids.

        This is implemented as follows:
          1. Download the results page.
          2. Extract the bid identifiers from this page.
          3. Check which of those identifiers are not yet in our database.
          4. For each of the identifiers not yet in our database:
            4.1. Download the detail page for each identifier.
            4.2. Extract the fields we are interested in.
            4.3. Create a Bid object and store it in the database.

        Arguments:
        session -- database session to use for persisting items
        """
        page = self.scraper.get(self.results_url)
        bid_ids = self.scrape_results_page(page.content)
        log.info("Found bid ids: {}".format(bid_ids))
        new_ids = get_new_identifiers(session, bid_ids, self.get_site())
        arg_tuples = [(self.scrape_bid_page, bid_id) for bid_id in new_ids]
        bids = execute_parallel(arg_tuples)
        session.bulk_save_objects(bids)
        session.commit()

    def get_site(self):
        return Bid.Site.CITYOFBOSTON

    def scrape_results_page(self, page_str):
        """Scrapes the City of Boston results page.

        Args:
        page_str -- the entire HTML page as a string

        Returns:
        bid_ids -- a list of strings with the bid identifiers found
        """
        tree = html.fromstring(page_str)
        # Bid urls are encoded as `bids.asp?ID=<bidId>` in the table
        bid_id_urls = tree.xpath('//b/a/@href')
        bid_ids = []
        for bid_id_url in bid_id_urls:
            bid_id = self.get_bid_id(bid_id_url)
            if bid_id is None:
                continue
            bid_ids.append("".join(bid_id).strip())
        return bid_ids

    def get_bid_id(self, href):
        """Extracts the ID from the href link"""
        regexp_match = compiled_reg_exp.match(href)
        if regexp_match:
            return regexp_match.group(1)
        return None

    def scrape_bid_page(self, bid_id):
        """Scrapes the City of Boston bid detail page for the given bid_id.

        Relies on the position of information inside the main results table,
        since the HTML contains no semantically-meaninful ids or classes.

        Raises ValueError if it encounters parsing errors.
        """
        page = self.scraper.get(self.details_url, params={'ID': bid_id})
        tree = html.fromstring(page.content)
        first_center = tree.xpath('//center')[0]
        start_text_element = first_center.xpath('b')[0]
        description = start_text_element.text.strip()
        items = ["".join(first_center.xpath('text()'))]
        return Bid(
            identifier=bid_id,
            description=description,
            items=items,
            site=self.get_site().name
        )
