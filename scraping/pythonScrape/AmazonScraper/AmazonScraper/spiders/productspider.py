import scrapy
from AmazonScraper.items import AmazonscraperItem
from scrapy.loader import ItemLoader

import logging

class ProductspiderSpider(scrapy.Spider):
    name = 'productspider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?bbn=2619533011&rh=n%3A2619533011%2Cp_6%3AATVPDKIKX0DER&dc&qid=1649136580&rnid=2661622011&ref=lp_2619534011_nr_p_6_0']


    def getPageFields(self, response, item):
        # scrape country of origin
        COO = response.xpath("//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*").get()
        item.add_value(field_name='countryoforigin', value=COO)

        return item.load_item()


    def parse(self, response):

        for product in response.xpath('//div[@data-index and @data-asin and @data-uuid]'):

            item = ItemLoader(item=AmazonscraperItem(), selector=product, response=response)

            # get ASIN
            item.add_xpath('asin', '@data-asin')

            # get productname
            item.add_xpath('productname', './/h2//span[@class="a-size-base-plus a-color-base a-text-normal"]')

            # get department
            item.add_xpath('department', '//select[@aria-describedby="searchDropdownDescription"]/option[@selected="selected"]')

            # get price
            item.add_xpath('price', './/span[@class="a-price"]/span[@class="a-offscreen"]')

            # get rating
            item.add_xpath('rating', './/i[@class="a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom"]/span')

            # get image link
            item.add_xpath('picturereflink', './/img/@src')

            # get the unfiltered URL for navigation
            unfiltered_URL = response.xpath('.//h2/a/@href').get()

            # get product page link
            item.add_value('productpagelink', unfiltered_URL)

            # build affiliate link
            item.add_value('affiliatelink', item.get_output_value('productpagelink'))

            yield response.follow(unfiltered_URL, callback=self.getPageFields, cb_kwargs={'item': item}, dont_filter=True)

        next_page = response.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        pass
