import scrapy
from AmazonScraper.items import AmazonscraperItem
from scrapy.loader import ItemLoader
import meilisearch


import logging

class ProductspiderSpider(scrapy.Spider):
    name = 'productspider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?i=hpc&bbn=3760901&rh=p_85%3A2470955011%2Cp_6%3AATVPDKIKX0DER&dc&ds=v1%3AXD0ZxGV7QEG8N9Y3cT2RXisZ3IhpoDo5NItAIZKJDAA&crid=160RQC2UUK33F&qid=1663174667&rnid=331556011&sprefix=%2Chpc%2C89&ref=sr_nr_p_6_1', 'https://www.amazon.com/s?i=industrial&bbn=16310091&rh=p_85%3A2470955011%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A1248921011&dc&crid=1PU3IJVKDPZKT&qid=1663174691&rnid=1248919011&sprefix=%2Cindustrial%2C87&ref=sr_nr_p_72_1&ds=v1%3ANSVJvDeh9aU9Zqk16%2FW5uu6lYDtE4A4lbNacMtenNX4', 'https://www.amazon.com/s?i=toys-and-games&bbn=165793011&rh=p_85%3A2470955011%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A1248963011&dc&crid=3S8RCWSO0YP9F&qid=1663174753&rnid=1248961011&sprefix=%2Ctoys-and-games%2C88&ref=sr_nr_p_72_1&ds=v1%3AObUBq93ZMSWNrJMlydUpb0xTc9UbV1niLx7PVJGNwK0', 'https://www.amazon.com/s?i=mobile&bbn=2335752011&rh=p_85%3A2470955011%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2491149011&dc&crid=23ZGNT6PQYHLR&qid=1663174827&rnid=2491147011&sprefix=%2Cmobile%2C83&ref=sr_nr_p_72_1&ds=v1%3AIo8GePc7u4fvHPTc%2F46FAt0XZCRxT0r24yWM9ZBIkH4']

    def getPageFields(self, response, item):
        # scrape country of origin
        COO = response.xpath("//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of "
                             "origin')]//following-sibling::*").get() 
        item.add_value(field_name='countryoforigin', value=COO)

        # scrape manufacturer
        manufacturer = response.xpath("//*[not(contains(text(), 'Recommended')) and not(contains(text(), "
                                      "'recommended')) and not(contains(text(), 'discontinued')) and not(contains("
                                      "text(), 'Discontinued')) and contains(text(), "
                                      "'Manufacturer')]//following-sibling::*").get()

        if manufacturer is not None and len(manufacturer) < 100:
            item.add_value(field_name='manufacturer', value=manufacturer)

        return item.load_item()


    def parse(self, response):

        for product in response.xpath('//div[@data-index and @data-asin and @data-uuid]'):

            item = ItemLoader(item=AmazonscraperItem(), selector=product, response=response)

            # get ASIN
            item.add_xpath('ASIN', '@data-asin')

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

            # get product page link
            item.add_xpath('productpagelink', './/h2/a/@href')

            # build affiliate link
            item.add_xpath('affiliatelink', './/h2/a/@href')

            yield response.follow(item.get_output_value('productpagelink'), callback=self.getPageFields, cb_kwargs={'item': item}, dont_filter=True)

        next_page = response.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        pass
