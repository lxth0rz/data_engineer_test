# Task Title: 1. Parsing HTML
# Description: Scraping and Parsing HTML to Extract Painting Information and Create a Dataframe using Python
# Requirements: Task You will scrape and process simple html page located here candidateEvalData/webpage.html

#import modules

from lxml import html
import re
import requests
import pandas as pd
from datetime import datetime
from urllib.parse import urljoin

#get html and tree
def _request_local_webpage(page_local_path):

    ## using the urljoin() function from the urllib.parse module to join two URL parts together.
    html_page_link  = urljoin(base_url, page_local_path)

    # using text rather than content, Both response.content and response.text will return the same data,
    # but in different formats. If you are planning to parse the HTML content and extract information from it,
    # we should use response.text, as it will be easier to work with.
    html_content = requests.get(html_page_link).text

    # converts html string to a tree of elements for easy parsing using XPath.
    tree = html.fromstring(html_content)

    return tree

def _extracting_data(tree):

    # parse artist name
    artist_name_obj = tree.xpath('//*[@id="main_center_0_lblLotPrimaryTitle"]/text()')
    artist_name = 'N/A' # Why N/A => If the extraction failed, we will know without breaking the script execution.
    if artist_name_obj and len(artist_name_obj) > 0:
        artist_name = ''.join([x.strip() for x in artist_name_obj])  #  removes unnecessary spaces, new line, carriage return and puts them together in one string

    # parse painting name
    painting_name_obj = tree.xpath('//*[@id="main_center_0_lblLotSecondaryTitle"]/.//text()')
    painting_name = 'N/A'
    if painting_name_obj and len(painting_name_obj) > 0:
        painting_name = ''.join([x.strip() for x in painting_name_obj])

    price_gbp = 'N/A'
    price_usd = 'N/A'
    price_gbp_est = 'N/A'
    price_usd_est = 'N/A'
    image_link = 'N/A'
    sale_date = 'N/A'

    data = {'artist_name': artist_name, 'painting_name': painting_name, 'price_gbp': price_gbp,
            'price_usd': price_usd, 'price_gbp_est': price_gbp_est, 'price_usd_est': price_usd_est,
            'image_link': image_link, 'sale_date': sale_date}

    return data

def main():
    tree = _request_local_webpage('candidateEvalData/webpage.html')
    data = _extracting_data(tree)
    df = pd.DataFrame(data, index=[0])
    print(df.to_csv())

#parse price GBP

#parse price US

#parse price GBP est

#parse price US est

#image link

if __name__ == '__main__':
    # behind the scene we set a local server using python3 -m http.server is useful when you want to test or preview
    # a web page or application that you are developing locally. We will use it to request the web page using requests lib.
    base_url = 'http://localhost:8000/'
    main()