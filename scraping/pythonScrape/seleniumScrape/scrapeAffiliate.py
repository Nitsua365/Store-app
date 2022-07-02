import random
import signal
import sys
import time
from redis import Redis
from AmazonScraper import Login
from seleniumScrape.utils.scrapeFunctions import loginToAmazon
from utils import scrapeFunctions

from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True
# options.add_argument("user-data-dir=" + Login.chromeData['data'])
# options.add_argument("profile-directory=" + sys.argv[2])
driver = webdriver.Chrome(executable_path='../webdriver/chromedriver', options=options)

driver.get('https://amazon.com')

# login to amazon acct
loginToAmazon(driver)

rd = Redis(host=Login.redis['host'], port=Login.redis['port'], db=Login.redis['db'], username='default', password=Login.redis['password'])

R_KEYS = list(map(lambda x: x.decode('utf-8'), list(rd.keys('amazon_products:*'))))
random.shuffle(R_KEYS)

for key in R_KEYS:

    db_affil = None
    db_page = None

    try:
        db_affil = str(rd.hget(name=key, key='affiliatelink').decode('utf-8'))
        db_page = str(rd.hget(name=key, key='productpagelink').decode('utf-8'))
    except:
        db_affil = None
        continue

    if db_affil is None or db_affil == 'None' or len(db_affil) == 0:

        affil = scrapeFunctions.scrapeAffiliate(URL=db_page, driver=driver)

        if affil is not None and len(affil) != 0:
            print('inserting', key, affil)
            rd.hset(name=key, key='affiliatelink', value=affil)

rd.close()

driver.close()