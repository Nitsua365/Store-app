# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import date
import redis
import Login


class AmazonscraperPipeline:

    def open_spider(self, spider):
        self.redisCli = redis.Redis(host=Login.redis['host'], port=Login.redis['port'], db=Login.redis['db'])

    def close_spider(self, spider):
        self.redisCli.close()

    def process_item(self, item, spider):
        if item['countryoforigin'] is not None and item['countryoforigin'].lower() != 'china':
            key = 'amazon_products:' + item['asin']
            item['datescrapped'] = date.today()
            del item['asin']
            print('hello')
            self.redisCli.hset(name=key, mapping=item)
