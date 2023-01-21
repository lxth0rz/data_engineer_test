import scrapy


class BearspaceSpiderSpider(scrapy.Spider):
    name = 'bearspace_spider'
    allowed_domains = ['bearspace.co.uk']
    start_urls = ['http://bearspace.co.uk/']

    def parse(self, response):
        pass
