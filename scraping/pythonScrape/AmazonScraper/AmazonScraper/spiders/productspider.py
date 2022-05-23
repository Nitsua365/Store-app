import scrapy
from AmazonScraper.items import AmazonscraperItem
from scrapy.loader import ItemLoader


class ProductspiderSpider(scrapy.Spider):
    name = 'productspider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?bbn=2617941011&rh=n%3A2617941011%2Cp_6%3AATVPDKIKX0DER&dc&qid=1649136515&rnid=2638374011&ref=lp_2617942011_nr_p_6_0']

    def getPageFields(self, response):
        COI = response.get_xpath("//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*")

        yield {
            'COI': COI
        }

    def parse(self, response):

        for product in response.xpath('//div[@data-index and @data-asin and @data-uuid]'):

            item = ItemLoader(item=AmazonscraperItem(), selector=product)

            # get ASIN
            item.add_xpath('asin', '@data-asin')

            # get productname
            item.add_xpath('name', './/h2//span[@class="a-size-base-plus a-color-base a-text-normal"]')

            # get department
            item.add_xpath('department', '//select[@aria-describedby="searchDropdownDescription"]/option[@selected="selected"]')

            # get price
            item.add_xpath('price', './/span[@class="a-price"]/span[@class="a-offscreen"]')

            # get rating
            item.add_xpath('rating', './/i[@class="a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom"]/span')

            # get image link
            item.add_xpath('imagelink', './/img/@src')

            # get product page link
            item.add_xpath('productlink', './/h2/a/@href')

            # yield response.follow(item.get_output_value('productlink'), callback=self.getPageFields)

            yield item.load_item()

        next_page = response.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        pass
