import re
import logging
import scrapelib
from document import Document
from datetime import datetime
from datetime import date as dtdate
from .base_scraper import BaseScraper
from lxml import html
from concurrent.futures import ThreadPoolExecutor


# Logger object for this module
log = logging.getLogger(__name__)


class NoticesScraper(BaseScraper):
    NOTICES_URL = "https://www.boston.gov/public-notices"

    def __init__(self, threads=4):
        self.scraper = scrapelib.Scraper()
        self.thread_executor = ThreadPoolExecutor(threads)

    def scrape_desc(self, href):
        desc_page = self.scraper.get('https://www.boston.gov' + href)
        tree = html.fromstring(desc_page.content)
        try:
            return html.tostring(tree.xpath('//div["field-item even"=@class]')[0]).decode()
        except:
            # the description is a list
            return html.tostring(tree.xpath('//div["body"=@class]/ol')[0]).decode()

    def scrape_notice_div(self, div):
        title_a = div.xpath(".//div['n-li-t'=@class]/a")[0]
        year, month, day_and_start, end = div.xpath("//span['dc:date'=@property]/@content")[0].split('-')
        day, start = day_and_start.split('T')
        date = dtdate(int(year), int(month), int(day))
        posted_candidates = div.xpath("//span['dl-d'=@class]")
        for cand in posted_candidates:
            if cand.text is None:
                continue
            if re.match('\d\d/\d\d/\d\d\d\d - \d:\d\d[ap]m', cand.text):
                posted = datetime.strptime(cand.text, '%m/%d/%Y - %I:%M%p')
                break
        else:
            raise ValueError("Couldn't get time of post")
        return Document(
            url='https;//www.boston.gov' + title_a.attrib['href'],
            title=title_a.attrib['title'],
            site=Document.Site.BOSTON.name,
            description=self.scrape_desc(title_a.attrib['href'])
        )

    def get_site(self):
        return Document.Site.BOSTON_NOTICES

    def scrape_notices_page(self, content):
        tree = html.fromstring(content)
        notice_divs = tree.xpath('//div["g g--m0 n-li"=@class]')
        log.info("Found {} notices".format(len(notice_divs)))
        return self.thread_executor.map(self.scrape_notice_div, notice_divs)

    def scrape_notices(self):
        notices_page = self.scraper.get(self.NOTICES_URL)
        return self.scrape_notices_page(notices_page.content)

    def scrape(self, session):
        session.bulk_save_objects(self.scrape_notices())
        session.commit()