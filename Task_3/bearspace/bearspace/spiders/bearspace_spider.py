import re
import scrapy
import itertools
from scrapy.loader import ItemLoader
from  itemloaders.processors import TakeFirst, MapCompose

from ..items import BearspaceItem

class BearspaceSpider(scrapy.Spider):
    name = "bearspace"
    start_urls = ["https://www.bearspace.co.uk/purchase"]

    base_next_url = 'https://www.bearspace.co.uk/purchase?page='

    def parse(self, response):
        self.logger.info("Crawling page %s", response.url)

        # getall() method is used to extract all the matching elements from an XPath or CSS selector expression.
        artwork_urls = response.xpath("//a[@data-hook='product-item-container']/@href").getall()
        if artwork_urls and len(artwork_urls):
            for url in artwork_urls:
                yield scrapy.Request(url,
                                     self.parse_artwork)
        else:
            self.logger.error("Cannot extract artwork urls.")

        load_more_button = response.xpath(".//button[@data-hook='load-more-button' and contains(text(), 'Load More')]")
        if load_more_button and len(load_more_button) > 0:
            if '?page=' not in response.url:
                next_url = self.base_next_url + "2"
            else:
                current_page = re.findall(self.base_next_url.replace('?', '\?') + '(\d+)', response.url)
                if current_page and len(current_page) > 0:
                    current_page = current_page[0]
                    next_url = self.base_next_url + str(int(current_page) + 1)

            yield scrapy.Request(next_url,
                                 self.parse)

    def parse_artwork(self, response):

        self.logger.info("Scraping data from %s", response.url)

        media = 'NaN'
        height_cm = 'NaN'
        width_cm = 'NaN'

        full_desc = response.xpath("//pre[@data-hook='description']/.//text()").getall()
        media_or_dim_found_in_the_first_3_elements = full_desc[:3]

        media_found = False
        for row in media_or_dim_found_in_the_first_3_elements:
            dim_found = re.findall("([WHwhcmCMs\d\.]{1,6})\s*(?:x|X)\s*([WHwhcmCMs\d\.]{1,6})|(\d{2,3})\s*cm.*?diam", row)
            if dim_found:
                dim = list(itertools.chain.from_iterable([re.findall('[\d\.]+', x) for x in dim_found[0]]))
                if 'diam' in row:
                     height_cm = width_cm = dim[0].strip()
                else:
                    height_cm, width_cm = dim
            else:
                if len(row) > 1 and row != '' and not media_found:
                    media_found = True
                    media = row

        # if media == 'NaN':
        #     print(response.url)
        #
        # if height_cm == 'NaN' or width_cm == 'NaN':
        #     print(response.url)

        # ItemLoader is a convenient way of populating items, in this example BearspaceItem is an item class that defines the fields that we want to scrape.
        # MapCompose and TakeFirst are processors that can be used to process the input and output of each field.
        # MapCompose applies the provided function to each value of the field, in this case str.strip which will remove the leading and trailing whitespaces.
        # TakeFirst takes the first non-empty value from the input and discards the rest.
        # The add_xpath method takes the field name, the xpath expression, and an optional re keyword argument that is used to extract the value using regular expressions.
        # The load_item() method returns the populated item.
        # Please note that you need to have scrapy installed, if not you can install it via pip by running pip install scrapy.

        loader = ItemLoader(item=BearspaceItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        loader.default_output_processor = TakeFirst()

        loader.add_value("url", response.url)
        loader.add_xpath("title", "//h1[@data-hook='product-title']/text()")
        loader.add_value("media", media)
        loader.add_value("width_cm", width_cm)
        loader.add_value("height_cm", height_cm)
        loader.add_xpath("price_gbp", "//span[@data-hook='formatted-primary-price']/text()")

        yield loader.load_item()
