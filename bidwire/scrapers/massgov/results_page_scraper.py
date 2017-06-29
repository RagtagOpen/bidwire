from lxml import etree, html

from utils import ensure_absolute_url


SITE_ROOT = 'https://www.mass.gov'

def scrape_results_page(page_str, xpath_list):
    """Scrapes HTML page and returns dictionary of URL => document title

    Args:
    page_str -- the entire HTML page as a string
    xpath_list -- list of xpath expressions (section and link element)

    Returns:
    document_ids -- a dictionary of relative URL path => description
    """
    assert xpath_list and len(xpath_list) > 1
    document_ids = {}
    tree = html.fromstring(page_str)
    document_list = tree.xpath(xpath_list[0])
    doc_xpath = xpath_list[1]
    for doc in document_list:
        elems = doc.xpath(doc_xpath)
        if elems:
            url = ensure_absolute_url(SITE_ROOT, elems[0].get('href'))
            document_ids[url] = elems[0].text.strip()
    return document_ids
