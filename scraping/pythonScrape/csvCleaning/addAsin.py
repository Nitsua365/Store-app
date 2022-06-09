# for data wrangling

import pandas as pd
import itertools

asinFile = pd.read_csv('asin.csv')
amazon_products = pd.read_csv('amazon_products.csv')

asinFile['asin'] = asinFile['asin'].str[16:]

amazon_products.insert(loc=0, column='asin', value=asinFile['asin'])

amazon_products.to_csv('amazon_products.csv', index=False)