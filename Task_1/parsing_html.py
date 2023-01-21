# Task Title: 1. Parsing HTML
# Description: Scraping and Parsing HTML to Extract Painting Information and Create a Dataframe using Python
# Requirements: Task You will scrape and process simple html page located here candidateEvalData/webpage.html

#import modules

import re
import json
import traceback
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
    try:
        html_content = requests.get(html_page_link).text
    except:
        print(traceback.print_exc())
        print("Please, make sure you are running a simple HTTP server.")
        exit(1)
    # converts html string to a tree of elements for easy parsing using XPath.
    tree = html.fromstring(html_content)

    return tree

def _post_processing(field, field_name="None"):
    #  removes unnecessary spaces, new line, carriage return and puts them together in one string
    #  Also, here we can add more initial data cleaning rules.
    field = ''.join([x.strip() for x in field])

    if field_name == "artist_name":
        #  the regular expression r'\(.*\)$' matches a string that starts with an opening parenthesis,
        #  followed by any characters (including whitespace) zero or more times, and ends with a closing
        #  parenthesis and the end of the string.
        # Note: This should be improved if scraping more than a single webpage, as it will likely be necessary to handle more cases.
        field = re.sub(r'\(.*\)$', '', field)

    elif field_name == "price_gbp" or field_name == 'price_usd':
        field = re.sub(r'GBP\s|,|USD\s', ' ', field)

    elif field_name == "price_gbp_est" or field_name == 'price_usd_est':
        # the following expressions should be also improved.
        field = re.sub(r'GBP\s|USD\s|\(|\)', '', field)
        field = re.sub(r',', ' ', field)
        field = re.sub(r'\s*\-\s*', ' , ', field)

    elif field_name == "sale_date":
        # to convert "11 February 2016," to the desired format "2016-02-11"
        # we might clean the comma before passing to datetime, but it will take care of it and remove it for us.
        # However, the better is clean the date string before passing to strptime
        field = datetime.strptime(field, "%d %B %Y,").strftime("%Y-%m-%d")

    elif field_name == 'image_link':
        pass

    return field.strip()

def _extracting_data(tree):
    # load xpaths from config file
    with open("XPath.config", "r") as file:
        xpaths = json.load(file)

    data = {}
    for field, xpath in xpaths.items():
        obj = tree.xpath(xpath)
        value = 'N/A'
        if obj and len(obj) > 0:
            value = _post_processing(obj, field_name=field)
        data[field] = value

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
    # 1. Open the Terminal and cd to the parent directory of candidateEvalData directory.
    # 2. run the Python server => python3 -m http.server
    # 3. Now the webpage.html could be accessed using the following URL: http://localhost:8000/candidateEvalData/webpage.html
    base_url = 'http://localhost:8000/'
    main()