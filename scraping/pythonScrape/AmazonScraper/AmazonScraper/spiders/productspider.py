import scrapy
from AmazonScraper.items import AmazonscraperItem
from scrapy.loader import ItemLoader
import meilisearch


import logging

class ProductspiderSpider(scrapy.Spider):
    name = 'productspider'
    allowed_domains = ['amazon.com']
    start_urls = [
                'http://www.amazon.com/s?i=garden&bbn=23987782011&rh=n%3A23987782011%2Cp_85%3A2470955011&s=review-rank&dc&ds=v1%3A%2Bt1SuEH1vbvhrc2tDbE3fwWLyKKEuh4QXtQfxq7jWO8&qid=1660454003&rnid=2470954011&ref=sr_st_review-rank'
                'http://www.amazon.com/s?i=garden&bbn=23987757011&rh=n%3A23987757011%2Cp_85%3A2470955011&s=review-rank&dc&ds=v1%3A88ehHEf1CLWnT0M9ZUG8mR4QyJ8AClFy1jd2WXmLXTo&qid=1660454044&rnid=2470954011&ref=sr_st_review-rank',
                'http://www.amazon.com/s?i=garden&bbn=23551244011&rh=n%3A23551244011%2Cp_85%3A2470955011&s=review-rank&dc&ds=v1%3AZLJqKCAwMdvaJV1v4slEpqaXwmBR62BSf7h2QyYpwPM&qid=1660454093&rnid=2470954011&ref=sr_st_review-rank',
                'http://www.amazon.com/s?i=lawngarden&bbn=553824&rh=n%3A553824%2Cp_85%3A2470955011&s=review-rank&dc&ds=v1%3A4HOfGz4nilES4%2FGIgbAj9fNZjDrb9QDxAlgUFwk3zxo&qid=1660454139&rnid=2470954011&ref=sr_st_review-rank'
                ]

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
