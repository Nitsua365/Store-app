# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import date
from redis import Redis

import Login


class AmazonscraperPipeline:
    # @classmethod
    # def from_crawler(cls, crawler):

    def open_spider(self, spider):
        self.client = Redis(host=Login.redis['host'], port=Login.redis['port'], db=Login.redis['db'])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['countryoforigin'] is not None and item['countryoforigin'].lower() != 'china' :
            key = 'amazon_products:' + item['asin']
            item['datescrapped'] = date.today()
            del item['asin']
            self.client.hset(name=key, mapping=item)
