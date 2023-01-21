# Task Title: 1. Parsing HTML
# Description: Scraping and Parsing HTML to Extract Painting Information and Create a Dataframe using Python
# Requirements: Task You will scrape and process simple html page located here candidateEvalData/webpage.html

#import modules

import re
from lxml import html
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

def _post_processing(field, field_type="None"):
    #  removes unnecessary spaces, new line, carriage return and puts them together in one string
    #  Also, here we can add more initial data cleaning rules.
    field = ''.join([x.strip() for x in field])

    if field_type == "name":
        #  the regular expression r'\(.*\)$' matches a string that starts with an opening parenthesis,
        #  followed by any characters (including whitespace) zero or more times, and ends with a closing
        #  parenthesis and the end of the string.
        # Note: This should be improved if scraping more than a single webpage, as it will likely be necessary to handle more cases.
        field = re.sub(r'\(.*\)$', '', field)

    elif field_type == "currency":
        field = re.sub(r'GBP\s|,|USD\s', ' ', field)

    elif field_type == "estimate":
        # the following expressions should be also improved.
        field = re.sub(r'GBP\s|USD\s|\(|\)', '', field)
        field = re.sub(r',', ' ', field)
        field = re.sub(r'\s*\-\s*', ' , ', field)

    elif field_type == "date":
        # to convert "11 February 2016," to the desired format "2016-02-11"
        # we might clean the comma before passing to datetime, but it will take care of it and remove it for us.
        # However, the better is clean the date string before passing to strptime
        field = datetime.strptime(field, "%d %B %Y,").strftime("%Y-%m-%d")

    return field.strip()

def _extracting_data(tree):

    # parse artist name
    artist_name_obj = tree.xpath('//*[@id="main_center_0_lblLotPrimaryTitle"]/text()')
    artist_name = 'N/A' # Why N/A => If the extraction failed, we will know without breaking the script execution, then we can check later for a fix.
    if artist_name_obj and len(artist_name_obj) > 0:
        artist_name = _post_processing(artist_name_obj, "name")

    # parse painting name
    painting_name_obj = tree.xpath('//*[@id="main_center_0_lblLotSecondaryTitle"]/.//text()')
    painting_name = 'N/A'
    if painting_name_obj and len(painting_name_obj) > 0:
        painting_name = _post_processing(painting_name_obj, field_type="name")

    # parse price GBP
    price_gbp_obj = tree.xpath('//*[@id="main_center_0_lblPriceRealizedPrimary"]/text()')
    price_gbp = 'N/A'
    if price_gbp_obj and len(price_gbp_obj) > 0:
        price_gbp = _post_processing(price_gbp_obj, field_type="currency")

    # parse price US
    price_usd_obj = tree.xpath('//*[@id="main_center_0_lblPriceRealizedSecondary"]/text()')
    price_usd = 'N/A'
    if price_usd_obj and len(price_usd_obj) > 0:
        price_usd = _post_processing(price_usd_obj, field_type="currency")

    #parse price GBP est
    price_gbp_est_obj = tree.xpath('//*[@id="main_center_0_lblPriceEstimatedPrimary"]/text()')
    price_gbp_est = 'N/A'
    if price_gbp_est_obj and len(price_gbp_est_obj) > 0:
        price_gbp_est = _post_processing(price_gbp_est_obj, field_type="estimate")

    #parse price USD est
    price_usd_est_obj = tree.xpath('//*[@id="main_center_0_lblPriceEstimatedSecondary"]/text()')
    price_usd_est = 'N/A'
    if price_usd_est_obj and len(price_usd_est_obj) > 0:
        price_usd_est = _post_processing(price_usd_est_obj, field_type="estimate")

    #extract image link
    image_link_obj = tree.xpath('//*[@id="imgLotImage"]/@src')
    image_link = 'N/A'
    if image_link_obj and len(image_link_obj) > 0:
        image_link = _post_processing(image_link_obj, field_type="url")

    #extract sale date
    sale_date_obj = tree.xpath('//*[@id="main_center_0_lblSaleDate"]/text()')
    sale_date = 'N/A'
    if sale_date_obj and len(sale_date_obj) > 0:
        sale_date = _post_processing(sale_date_obj, field_type="date")

    data = {'artist_name': artist_name, 'painting_name': painting_name, 'price_gbp': price_gbp,
            'price_usd': price_usd, 'price_gbp_est': price_gbp_est, 'price_usd_est': price_usd_est,
            'image_link': image_link, 'sale_date': sale_date}

    return data

def main():
    tree = _request_local_webpage('candidateEvalData/webpage.html')
    data = _extracting_data(tree)
    df = pd.DataFrame(data, index=[0])
    print(df.to_csv())


if __name__ == '__main__':
    print("Please, make sure you are running a simple HTTP server.")
    # behind the scene we set a local server using python3 -m http.server is useful when you want to test or preview
    # a web page or application that you are developing locally. We will use it to request the web page using requests lib.

    # So, in order to run the script...
    # Open the Terminal and cd to the directory where candidateEvalData/webpage.html exists
    # run the Python server => python3 -m http.server
    # Now the webpage.html could be accessed using the following URL: http://localhost:8000/candidateEvalData/webpage.html
    base_url = 'http://localhost:8000/'
    main()