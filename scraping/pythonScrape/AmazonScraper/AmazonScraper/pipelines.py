# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import date
import redis
import Login

class AmazonscraperPipeline:

    def __init__(self):
        self.redisCli = redis.Redis(host=Login.redis['host'], port=Login.redis['port'], db=Login.redis['db'], username='default', password=Login.redis['password'])
        self.items = []

    def close_spider(self, spider):
        self.redisCli.close()

    def process_item(self, item, spider):
        if 'countryoforigin' in item and item['countryoforigin'].lower() != 'china' and 'asin' in item:
            key = 'amazon_products:' + item['asin']
            del item['asin']
            item['datescrapped'] = date.today().strftime('%Y-%m-%d')
            self.redisCli.hset(name=key, mapping=item)

        return item
