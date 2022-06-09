import os.path
from redis import Redis

import csv
import sys

from AmazonScraper import Login

if len(sys.argv) != 2:
    print('params must be <csv file name>', file=sys.stderr)
    quit(-1)

if not os.path.exists(sys.argv[1]) or not sys.argv[1].endswith(".csv"):
    print('Invalid file', sys.argv[1], file=sys.stderr)
    quit(-1)

rd = Redis(host=Login.redis['host'], port=Login.redis['port'], db=Login.redis['db'], username='default', password=Login.redis['password'])

productsCSVFile = open(sys.argv[1], 'r')
hashKeyName = sys.argv[1][:sys.argv[1].rindex('.csv')]

reader = csv.reader(productsCSVFile)

headerVals = []

for header in reader:
    headerVals = header
    break

for row in reader:
    if len(headerVals) != len(row):
        print("rows are different", file=sys.stderr)
        quit(-1)

    hashKey = hashKeyName + ':' + row[0]

    values = {}

    for ndx in range(1, len(row)):
        values[headerVals[ndx]] = row[ndx]

    print(rd.hset(name=hashKey, mapping=values))


rd.close()
productsCSVFile.close()