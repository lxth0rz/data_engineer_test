import re
import scrapy
import itertools
import pandas as pd
from datetime import datetime
from scrapy.loader import ItemLoader
from  itemloaders.processors import TakeFirst, MapCompose

from ..items import BearspaceItem

class BearspaceSpider(scrapy.Spider):

    name = "bearspace"

    start_urls = ["https://www.bearspace.co.uk/purchase"]

    base_next_url = 'https://www.bearspace.co.uk/purchase?page='

    df = None

    def __init__(self):
        self.df = pd.DataFrame(columns=['url', 'title', 'media', 'height_cm', 'width_cm', 'price_gbp'])

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

        # Looking for the load more button if still visible
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
        # Iterating through the list of rows (media_or_dim_found_in_the_first_3_elements), using complex regular
        # expression to match dimensions and media, extracting numerical values and storing them in flattened list,
        # and setting height_cm, width_cm and media_found variables accordingly.
        for row in media_or_dim_found_in_the_first_3_elements:

            # Complex regex expression used to match dimensions and media, for ex: -but not limited to-
            # '99x99 cm'
            # '100cm x 80cm'
            # '38x32cm'
            # 'height 70cm x width 100cm'
            # '92X45 CM'
            # '58W x 85.5Hcm'
            # '30cm  diam '
            dim_found = re.findall("height\s*(\d+)cm\s*x\s*width\s*(\d+)cm|([WHwhcmCMs\d\.]{1,6})\s*(?:x|X)\s*([WHwhcmCMs\d\.]{1,6})|(\d{2,3})\s*cm.*?diam", row)
            if dim_found:
                # Extracting numerical values from the matched dimensions and storing them in a flattened list.
                dim = list(itertools.chain.from_iterable([re.findall('[\d\.]+', x) for x in dim_found[0]]))
                if 'diam' in row:
                     height_cm = width_cm = dim[0].strip()
                else:
                    height_cm, width_cm = dim
            else:
                if len(row) > 1 and row != '' and not media_found:
                    media_found = True
                    media = row

        # This line of code creates an instance of the ItemLoader class and assigns it to the variable loader.
        # The ItemLoader class is a utility class provided by Scrapy that makes it easy to populate items with data obtained from a spider.
        loader = ItemLoader(item=BearspaceItem(), response=response)

        # 1. str.strip() method is used to remove any leading and trailing whitespaces from the input data.
        # This line of code is essentially setting the default input processor of the loader to remove any leading
        # and trailing whitespaces from the input data before it is loaded into the item.
        # 2. MapCompose function is used to compose multiple input processing functions together.
        # In this case, it is only being used to apply the single str.strip()
        loader.default_input_processor = MapCompose(str.strip)

        # TakeFirst() is a built-in function from the scrapy library that is used to select the first non-null/non-empty value from a list of values.
        loader.default_output_processor = TakeFirst()

        # Adding values to the loader object for the url, title, media, width_cm, height_cm, and price_gbp fields and loading the final item.
        loader.add_value("url", response.url)
        loader.add_xpath("title", "//h1[@data-hook='product-title']/text()")
        loader.add_value("media", media)
        loader.add_value("width_cm", width_cm)
        loader.add_value("height_cm", height_cm)
        loader.add_xpath("price_gbp", "//span[@data-hook='formatted-primary-price']/text()")
        item = loader.load_item()

        item = {'url': item['url'],
                'title': item['title'],
                'media': item['media'],
                'height_cm': item['height_cm'],
                'width_cm': item['width_cm'],
                'price_gbp': item['price_gbp'],}

        # Adding the scraped item to the dataframe and resetting the index.
        self.df = pd.concat([self.df, pd.DataFrame([item])],
                            ignore_index=True)

        # Send to post-processing pipeline -if any-
        yield item

    def closed(self, reason):

        """
        :param reason: The reason parameter passed to the closed function is likely a string that explains why the spider or scraping process has closed.
        :return:
        """

        print(self.df)
        # Format date and time into a string
        datetime_string = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        output_file_name = datetime_string + '.csv'

        """
        This line of code uses the to_csv() method of the pandas DataFrame self.df to save its contents to a csv file.
        The first parameter passed to the method is the file name, which is generated by concatenating the datetime_string
        and '.csv'. The second parameter is index=False, which tells the method to not write the DataFrame's index to the
        file. This line of code makes sure that the scraped data is saved to a csv file with a unique filename, which is
        generated based on the current date and time and without the index.
        """
        self.df.to_csv(output_file_name, index=False)