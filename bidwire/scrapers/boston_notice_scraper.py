import logging
import scrapelib
from document import Document, get_new_urls
from .base_scraper import BaseScraper
from lxml import html
from concurrent.futures import ThreadPoolExecutor


# Logger object for this module
log = logging.getLogger(__name__)


class BostonNoticeScraper(BaseScraper):
    NOTICES_URL = "https://www.boston.gov/public-notices"

    def __init__(self, threads=4):
        self.scraper = scrapelib.Scraper()
        self.thread_executor = ThreadPoolExecutor(threads)

    def scrape_desc(self, href):
        desc_page = self.scraper.get('https://www.boston.gov' + href)
        tree = html.fromstring(desc_page.content)
        try:
            return tree.xpath(
                '//div["intro-text supporting-text squiggle-border-bottom"=@class]'
            )[0].text.strip()
        except IndexError:  # indicates the event's been canceled, ignore it
            return

    def scrape_notice_div(self, div):
        title_a = div.xpath(".//div['n-li-t'=@class]/a")[0]
        return Document(
            url='https://www.boston.gov' + title_a.attrib['href'],
            title=title_a.attrib['title'],
            site=Document.Site.BOSTON_NOTICES.name,
            description=self.scrape_desc(title_a.attrib['href'])
        )

    def get_site(self):
        return Document.Site.BOSTON_NOTICES

    def scrape_notices_page(self, session, content):
        tree = html.fromstring(content)
        notice_divs = tree.xpath('//div["g g--m0 n-li"=@class]')
        log.info("Found {} notices".format(len(notice_divs)))
        hrefs = {self.NOTICES_URL.replace('/public-notices', a.attrib['href']) for a in tree.xpath('//div["g g--m0 n-li"=@class]//div["n-li-t"=@class]/a')}
        newurls = get_new_urls(session, hrefs, self.get_site())
        return self.thread_executor.map(
            self.scrape_notice_div,
            filter(lambda div: self.NOTICES_URL.replace(
                '/public-notices',
                div.xpath('//div["n-li-t"=@class]/a')[0].attrib['href']
            ) in newurls, notice_divs)
        )

    def scrape_notices(self, session):
        notices_page = self.scraper.get(self.NOTICES_URL)
        return self.scrape_notices_page(session, notices_page.content)

    def scrape(self, session):
        session.bulk_save_objects(self.scrape_notices(session))
        session.commit()
