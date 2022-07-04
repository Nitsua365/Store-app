import scrapy
from AmazonScraper.items import AmazonscraperItem
from scrapy.loader import ItemLoader


class ProductspiderSpider(scrapy.Spider):
    name = 'productspider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?bbn=16310091&rh=n%3A16310091%2Cp_6%3AATVPDKIKX0DER&dc',
                  'https://www.amazon.com/s?k=lawn+%2B+garden&i=lawngarden&rh=p_6%3AATVPDKIKX0DER&dc&pf_rd_i=2972638011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=fd6a347f-cea4-4a8c-b2d3-0330aab46c24&pf_rd_r=B0CXS8B45YTXA1MPHS03&pf_rd_s=merchandised-search-8&pf_rd_t=101&qid=1656970648&rnid=19346684011&ref=sr_pg_1']

    def getPageFields(self, response, item):
        # scrape country of origin
        COO = response.xpath("//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*").get()
        item.add_value(field_name='countryoforigin', value=COO)

        # if item.get_output_value('asin') is None or item.get_output_value('asin') == '':
        # ASIN = response.xpath("//th[contains(text(), 'ASIN')]//following-sibling::*").get()
        #
        # if ASIN is None or len(ASIN) == 0:
        #     ASIN = response.xpath("//span[contains(text(), 'ASIN')]//following-sibling::*").get()

        # item.add_value(field_name='asin', value=ASIN)

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

            yield response.follow(item.get_output_value('productpagelink'), callback=self.getPageFields, cb_kwargs={'item': item}, dont_filter=True)

        next_page = response.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        pass
