import scrapy


class TestproxyPySpider(scrapy.Spider):
    name = 'testProxy'
    allowed_domains = ['AmazonScraper']
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):

        yield {'IP': response.json()}
        pass