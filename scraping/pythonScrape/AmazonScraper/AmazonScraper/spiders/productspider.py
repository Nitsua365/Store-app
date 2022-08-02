import scrapy
from AmazonScraper.items import AmazonscraperItem
from scrapy.loader import ItemLoader

import logging

class ProductspiderSpider(scrapy.Spider):
    name = 'productspider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?bbn=16310091&rh=n%3A16310091%2Cp_85%3A2470955011&dc&qid=1657489410&rnid=2470954011&ref=lp_16310161_nr_p_85_1']

    # start_urls = ['https://www.amazon.com/s?k=harley&rh=n%3A2204830011&ref=nb_sb_noss']

    # start_urls = ['https://www.amazon.com/s?i=luxury&bbn=18981045011&rh=p_85%3A2470955011&dc&ds=v1%3AgJftK6XGJdQgWpjVAu38ZBaV5mcT%2FUsx5ypFaxYEAcc&crid=1PNIV8G8IXN09&qid=1657497682&rnid=2470954011&sprefix=%2Cluxury%2C575&ref=sr_nr_p_85_1']

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

            # get product page link
            item.add_xpath('productpagelink', './/h2/a/@href')

            # build affiliate link
            item.add_xpath('affiliatelink', './/h2/a/@href')

            yield response.follow(item.get_output_value('productpagelink'), callback=self.getPageFields, cb_kwargs={'item': item}, dont_filter=True)

        next_page = response.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        pass
