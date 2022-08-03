# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import date
import redis
import Login
import meilisearch
from scrapy.utils.serialize import ScrapyJSONEncoder

class AmazonscraperPipeline:

    def __init__(self):
        self.redisCli = redis.Redis(host=Login.redis['host'], port=Login.redis['port'], db=Login.redis['db'], username='default', password=Login.redis['password'])
        self.items = []
        self.meili = meilisearch.Client(url=Login.meilisearch['URL'], api_key=Login.meilisearch['API_KEY'])
        self.meiliIndx = self.meili.index(uid=Login.meilisearch['SEARCH_INDEX'])

    def close_spider(self, spider):
        self.redisCli.close()

    def process_item(self, item, spider):
        if 'countryoforigin' in item and item['countryoforigin'].lower() != 'china' and 'asin' in item and 'affiliatelink' in item:
            item['datescrapped'] = date.today().strftime('%Y-%m-%d')

            # # insert item into meili
            if len(self.items) > 20:
                self.meiliIndx.add_documents(documents=self.items, primary_key='ASIN')
                self.items.clear()
            else:
                self.items.append(item)

            # insert item into redis
            key = 'amazon_products:' + item['asin']
            del item['asin']
            self.redisCli.hset(name=key, mapping=item)
            self.redisCli.expire(name=key, time=43200)


        return item
