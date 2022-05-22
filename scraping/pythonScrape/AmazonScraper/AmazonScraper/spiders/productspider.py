import scrapy
from AmazonScraper.items import AmazonscraperItem
from scrapy.loader import ItemLoader


class ProductspiderSpider(scrapy.Spider):
    name = 'productspider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?bbn=2617941011&rh=n%3A2617941011%2Cp_6%3AATVPDKIKX0DER&dc&qid=1649136515&rnid=2638374011&ref=lp_2617942011_nr_p_6_0']

    def parse(self, response):

        for product in response.xpath('//div[@data-index and @data-asin and @data-uuid]'):
            item = ItemLoader(item=AmazonscraperItem(), selector=product)

            item.add_xpath('asin', '//div[@data-index and @data-asin and @data-uuid]/@data-asin')
            # item.add_xpath('name', '')

            item.add_xpath('imagelink', '//div[@data-index and @data-asin and @data-uuid]//img/@src')

            yield item.load_item()


        pass
