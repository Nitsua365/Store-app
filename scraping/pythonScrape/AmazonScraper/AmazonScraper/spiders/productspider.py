import scrapy
from AmazonScraper.items import AmazonscraperItem
from scrapy.loader import ItemLoader
import meilisearch


import logging

class ProductspiderSpider(scrapy.Spider):
    name = 'productspider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?keywords=Ice+Makers&i=appliances&rh=n%3A2399939011%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2661618011&dc&c=ts&qid=1664153442&rnid=2661617011&ts_id=2399939011&ref=sr_nr_p_72_1&ds=v1%3A3RwfG6BY62SC%2BV5Ky7bnZy6N%2B9NCrY2Zgb14lEnkGAI', 
                    'https://www.amazon.com/s?keywords=Beverage+Refrigerators&i=appliances&rh=n%3A2686328011%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2661618011&dc&c=ts&qid=1664153456&rnid=2661617011&ts_id=2686328011&ref=sr_nr_p_72_1&ds=v1%3Ai1daUgUZ1%2BLggFN13UI%2FGDhLU3%2B8pdLky6hiYdGsx4E',
                    'https://www.amazon.com/s?i=appliances&bbn=3741271&rh=n%3A3741271%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2661618011&dc&ds=v1%3Axo6pUqZf0KVKNcA9JwxKr72eu2%2FwUAS1pzB55XxahNg&qid=1664153471&rnid=2661617011&ref=sr_nr_p_72_1',
                    'https://www.amazon.com/s?keywords=Wine+Cellars&i=kitchen&rh=n%3A3741521%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A1248915011&dc&c=ts&qid=1664153479&rnid=1248913011&ts_id=3741521&ref=sr_nr_p_72_1&ds=v1%3AAvnYdY6M06lHiF9Ku2NeMqFNlRLTGiZrQdNolIUH50M',
                    'https://www.amazon.com/s?keywords=Freezers&i=appliances&rh=n%3A3741331%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2661618011&dc&c=ts&qid=1664153488&rnid=2661617011&ts_id=3741331&ref=sr_nr_p_72_1&ds=v1%3AALM6jaUJbRNG0d9q%2B6uj20b3ZUaQVEcPTF1dFmYrG%2BE',
                    'https://www.amazon.com/s?keywords=Microwave+Ovens&i=kitchen&rh=n%3A289935%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A1248915011&dc&c=ts&qid=1664153498&rnid=1248913011&ts_id=289935&ref=sr_nr_p_72_1&ds=v1%3AZr46dhF9to7LxH1Jae6QtjFbBWGnvQqvIl%2FahWCv4lM',
                    'https://www.amazon.com/s?keywords=Refrigerators&i=appliances&rh=n%3A3741361%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2661618011&dc&c=ts&qid=1664153509&rnid=2661617011&ts_id=3741361&ref=sr_nr_p_72_1&ds=v1%3A4TKvRghrhiMQuFJ%2Fc4jg26%2FgPyZsMlv03FyCILeRykQ',
                    'https://www.amazon.com/s?i=appliances&bbn=2383576011&rh=n%3A2383576011%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2661618011&dc&ds=v1%3AmsRLkFEJFxF4D0ysFya0jjIMtHllq2awQ1saeGsoBnE&qid=1664153523&rnid=2661617011&ref=sr_nr_p_72_1',
                    'https://www.amazon.com/s?keywords=Range+Hoods&i=appliances&rh=n%3A3741441%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2661618011&dc&c=ts&qid=1664153533&rnid=2661617011&ts_id=3741441&ref=sr_nr_p_72_1&ds=v1%3Aewt7tYjEc912KkE8wrl6tANUqMMOuCFP9rw2TGXOwBo',
                    'https://www.amazon.com/s?i=kitchen&bbn=289913&rh=n%3A289913%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A1248915011&dc&ds=v1%3A%2Fn6XFoROlbD519DiJN0qXsTuktJezaak3DhXSYG3vqI&qid=1664153553&rnid=1248913011&ref=sr_nr_p_72_1',
                    'https://www.amazon.com/s?i=appliances&bbn=18116199011&rh=n%3A18116199011%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2661618011&dc&language=en_US&brr=1&pf_rd_i=2619525011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=e3f7683c-69c9-4cd2-bf07-aa64968c413e&pf_rd_r=G1P0QNQN84R5BF8NAGXE&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1664153567&rd=1&rnid=2661617011&ref=sr_nr_p_72_1&ds=v1%3AIc8oBj3H9Z2VLey7%2FqsD3ZAMB%2BdIsMYX9cZxuQtDgek',
                    'https://www.amazon.com/s?i=appliances&bbn=18116203011&rh=n%3A18116203011%2Cp_6%3AATVPDKIKX0DER%2Cp_72%3A2661618011&dc&language=en_US&brr=1&pf_rd_i=2619525011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=e3f7683c-69c9-4cd2-bf07-aa64968c413e&pf_rd_r=G1P0QNQN84R5BF8NAGXE&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1664153576&rd=1&rnid=2661617011&ref=sr_nr_p_72_1&ds=v1%3A8i3zneygQqrgap7nrAL9fBLNPC4OmBBKyObAohf5uZs']

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
