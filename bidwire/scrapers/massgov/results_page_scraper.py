from lxml import etree, html


def scrape_results_page(page_str, xpath_list):
    """Scrapes HTML page and returns dictionary of URL => document title

    Args:
    page_str -- the entire HTML page as a string
    xpath_list -- list of xpath expressions (section and link element)

    Returns:
    document_ids -- a dictionary of relative URL path => description
    """
    document_ids = {}
    if not xpath_list or len(xpath_list) < 2:
        return document_ids

    tree = html.fromstring(page_str)
    document_list = tree.xpath(xpath_list[0])
    doc_xpath = xpath_list[1]
    for doc in document_list:
        if not doc.xpath(doc_xpath):
            continue
        elem = doc.xpath(doc_xpath)[0]
        document_ids[elem.get('href')] = elem.text.strip()
    return document_ids