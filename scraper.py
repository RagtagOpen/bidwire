from datetime import datetime
from lxml import etree, html
import logging
import scrapelib

log = logging.getLogger(__name__)

# The URL for the table of bid results. Accepts a form POST with
# the parameters 'currentPage=N' and 'mode=navigation' to iterate through result
# pages.
BID_RESULTS_URL = "https://www.commbuys.com/bso/external/publicBids.sdo"

# Expects a 'bidId=<BID-ID>' query param.
BID_DETAIL_URL = "https://www.commbuys.com/bso/external/bidDetail.sdo"


def scrape():
    """Iterates through all of Commbuys and extracts bids."""
    scraper = scrapelib.Scraper()
    results_found = True
    current_page = 1
    while results_found:
        page = scraper.post(BID_RESULTS_URL, data={
            'mode': 'navigation', 'currentPage': current_page})
        bid_ids = scrape_results_page(page)
        for bid_id in bid_ids:
            bid_page = scraper.get(BID_DETAIL_URL, params={'bidId': bid_id})
            scrape_bid_page(bid_page)
        results_found = len(bid_ids) != 0
        current_page += 1


def scrape_results_page(page):
    """Scrapes the given page as a Commbuys results page.

    Args:
    page -- a response object containing a results page

    Returns:
    bid_ids -- a list of strings with the bid identifiers found
    """
    tree = html.fromstring(page.content)
    rows = tree.xpath('//table[@id="resultsTable"]/tr')
    bid_ids = []
    for row in rows:
        tds = row.xpath('td')
        # We expect the bid id to be the first column of the row
        if len(tds) < 1:
            log.error("No columns found in row: {}".format(
                etree.tostring(row)))
            continue
        bid_ids.append("".join(tds[0].xpath('a/text()')).strip())
    return bid_ids


def scrape_bid_page(page):
    """Scrapes the given page as a Commbuys bid detail page.

    Relies on the position of information inside the main results table, since
    the HTML contains no semantically-meaninful ids or classes.

    Raises ValueError if it encounters parsing errors.
    """
    tree = html.fromstring(page.content)
    bid_id = _get_next_sibling_text_for(tree, "Bid Number:")
    description = _get_next_sibling_text_for(tree, "Description:")
    department = _get_next_sibling_text_for(tree, "Department:")
    organization = _get_next_sibling_text_for(tree, "Organization:")
    location = _get_next_sibling_text_for(tree, "Location:")
    open_date_str = _get_next_sibling_text_for(tree, "Bid Opening Date:")
    open_date = None
    try:
        open_date = datetime.strptime(open_date_str, '%m/%d/%Y %I:%M:%S %p')
    except ValueError:
        log.warning("Could not parse {} into date".format(open_date_str))
    # Discard empty strings from 'items'
    # TODO: Clean this code up -- find a more robust way of extracting items
    items = list(filter(None, _get_siblings_text_for(tree, "Item #")))
    print(bid_id, description, department, organization, location, open_date,
          items)


def _get_next_sibling_text_for(tree, text):
    """Returns the text in the next 'td' cell after the one with 'text'.

    Raises:
      ValueError if next sibling can't be found.
    """
    siblings_text = _get_siblings_text_for(tree, text)
    if len(siblings_text) == 0:
        raise ValueError("Could not find next sibling of '{}'".format(text))
    return siblings_text[0]


def _get_siblings_text_for(tree, text):
    """Returns the list of texts in the next 'td' cells after the one with 'text'."""
    xpath = '//td[contains(text(), "{}")]/following-sibling::td/text()'.format(text)
    siblings = tree.xpath(xpath)
    return [sib.strip() for sib in siblings]
