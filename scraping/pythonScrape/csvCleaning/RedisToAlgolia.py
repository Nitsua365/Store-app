from algoliasearch.search_client import SearchClient
from redis import Redis

from AmazonScraper import Login

# algolia init
alg_client = SearchClient.create('NNQKCWQ55R', 'b34829cc44639b18b05179e13050d5e5')
index = alg_client.init_index("amazon_products")


rd = Redis(host=Login.redis['host'], port=Login.redis['port'], db=Login.redis['db'], username='default',
           password=Login.redis['password'])

products = list(map(lambda x: x.decode('ascii'), rd.keys(pattern='amazon_products:*')))



for product in products:
    item = rd.hgetall(name=product)
    ASIN = product[product.find(':') + 1:]

    newItem = {}

    for key, value in item.items():
        newItem[key.decode('ascii')] = value.decode('ascii')

    newItem['objectID'] = ASIN

    print('inserting ', newItem['objectID'], newItem['productname'])
    print(index.save_object(newItem).wait())
