UL_CATEGORY_LI = '//ul[@class="category"]/li'
H2_A_TITLELINK = './h2/a[@class="titlelink"]'
SPAN_A_TITLELINK = './span/a[@class="titlelink"]'
DIV_BODYFIELD_P = '//div[contains(@class,"bodyfield")]/p'

CATEGORY_H2_XPATH = [ UL_CATEGORY_LI, H2_A_TITLELINK ]
BODYFIELD_SPAN_XPATH = [ DIV_BODYFIELD_P, SPAN_A_TITLELINK ]

"""Mapping of relative URL (for EOPSS pages) to the xpath needed 
    to extract documents (1st xpath for section, 2nd xpath for document link)
"""
MASSGOV_DICT = {
        'homeland-sec/grants/docs/':
            [
                UL_CATEGORY_LI,
                './h2/span/a[@class="titlelink"]'
            ],
        'homeland-sec/grants/hs-grant-guidance-and-policies.html':
            BODYFIELD_SPAN_XPATH,
        'homeland-sec/grants/standard-documents.html':
            [
                '//div[contains(@class,"bodyfield")]/ul/li',
                SPAN_A_TITLELINK
            ],
        'law-enforce/grants/': CATEGORY_H2_XPATH,
        'law-enforce/grants/2017-muni-public-safety-staffing-grant.html':
            BODYFIELD_SPAN_XPATH,
        'law-enforce/grants/le-grants-public-records.html':
            BODYFIELD_SPAN_XPATH,
        'justice-and-prev/grants/': CATEGORY_H2_XPATH,
        'justice-and-prev/grants/bgp/': CATEGORY_H2_XPATH,
        'hwy-safety/grants/': CATEGORY_H2_XPATH,
        'hwy-safety/grants/ffy-2017-traffic-enforcement-grant-program.html':
            BODYFIELD_SPAN_XPATH,
        'hwy-safety/grants/ffy2017-hsd-grant-opportunities.html':
            BODYFIELD_SPAN_XPATH,
        'hwy-safety/grants/ffy-2017-step.html': BODYFIELD_SPAN_XPATH,
        'hwy-safety/grants/highway-safety-grants-public-records.html':
            BODYFIELD_SPAN_XPATH
    }

