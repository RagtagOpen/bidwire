from lxml import etree, html

def scrape_results_page(page_str, xpath_list):
    """Scrapes EOPSS page

    Args:
    page_str -- the entire HTML page as a string
    xpath_list -- list of xpath expressions (section and link element)

    Returns:
    document_ids -- a dictionary of relative URL path => description
    """
    tree = html.fromstring(page_str)
    document_list = tree.xpath(xpath_list[0])
    document_ids = {}
    doc_xpath = xpath_list[1]
    for doc in document_list:
        if not doc.xpath(doc_xpath):
            continue
        elem = doc.xpath(doc_xpath)[0]
        document_ids[elem.get('href')] = elem.text.strip()
    return document_ids