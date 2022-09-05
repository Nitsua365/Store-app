import scrapy
from AmazonScraper.items import AmazonscraperItem
from scrapy.loader import ItemLoader
import meilisearch


import logging

class ProductspiderSpider(scrapy.Spider):
    name = 'productspider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?keywords=Outdoor+Lighting+Products&i=tools&rh=n%3A495236%2Cp_85%3A2470955011%2Cp_6%3AATVPDKIKX0DER&dc&c=ts&qid=1661663488&rnid=339807011&ts_id=495236&ref=sr_nr_p_6_2&ds=v1%3A8aXjtrdGRF%2FJE6nYyv3etBTBxPYPDk%2F%2BrELVEkPnSLY',
                    'https://www.amazon.com/s?i=appliances&bbn=2619525011&rh=p_85%3A2470955011%2Cp_6%3AATVPDKIKX0DER&dc&ds=v1%3AVnKBUr0JeWu6dY7fVHQmY11u8yT9UTTjfU5uymETD9Q&crid=XVGWM75XPEF9&qid=1661664126&rnid=2661622011&sprefix=%2Cappliances%2C171&ref=sr_nr_p_6_2',
                    'https://www.amazon.com/s?i=office-products&bbn=1064954&rh=p_85%3A2470955011%2Cp_6%3AATVPDKIKX0DER&dc&ds=v1%3Abex62%2B%2FZGDZNQowek5TbTbKLwgbeyVje8Qz1Gazz2SE&crid=X29UGURKS7SI&qid=1661664298&rnid=331539011&sprefix=%2Coffice-products%2C103&ref=sr_nr_p_6_1']

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
