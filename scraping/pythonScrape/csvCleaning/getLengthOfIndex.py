import meilisearch
import json
import pprint
import AmazonScraper.Login as Login
from urllib.parse import urlparse

client = meilisearch.Client(url=Login.meilisearch['URL'], api_key=Login.meilisearch['API_KEY'])

index = client.index(uid=Login.meilisearch['SEARCH_INDEX'])

results = index.get_documents({ 'limit': 10000000 })
print(len(results['results']))
