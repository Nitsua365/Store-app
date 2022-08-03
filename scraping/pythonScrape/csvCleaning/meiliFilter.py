import meilisearch
import json
import pprint
import AmazonScraper.Login as Login
from urllib.parse import urlparse

client = meilisearch.Client(url=Login.meilisearch['URL'], api_key=Login.meilisearch['API_KEY'])

index = client.index(uid=Login.meilisearch['SEARCH_INDEX'])

# results = index.get_documents({ 'limit': 9000 })
# results = results['results']
#
#
# def renameObjID(item):
#     item['ASIN'] = item['objectID']
#     del item['objectID']
#     return item
#
# def filterBadProducts(item):
#     if item['productpagelink'] and len(urlparse(item['productpagelink']).path) == 0:
#         return False
#
#     linkTitle = urlparse(item['productpagelink']).path.split('/')[1].split('-')
#     count = 0
#     for i in linkTitle:
#         if item['productname'].find(i.strip()) == -1:
#             count += 1
#
#     if (count / len(linkTitle)) <= 0.9:
#         return False
#
#     return True
#
#
#
# results = list(map(renameObjID, results))
#
# badProducts = list(filter(filterBadProducts, results))
# badProductsASIN = list(map(lambda x: x['ASIN'], badProducts))
#
# def getGoodProducts(item):
#     return item['ASIN'] not in badProductsASIN
#
# goodProducts = list(filter(getGoodProducts, results))

#Write to JSON
# outFile = open('goodProducts.json', 'r')
#
# out = json.dumps(goodProducts)
# outFile.write(out)

# index.delete_all_documents()

# goodProducts = json.load(outFile)
#
# pprint.pprint(goodProducts)
#
# index.add_documents(goodProducts, 'ASIN')
