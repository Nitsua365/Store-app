import os.path
from redis import Redis

import csv
import sys

if not os.path.exists(sys.argv[1]) or not sys.argv[1].endswith(".csv"):
    print('Invalid file', sys.argv[1], file=sys.stderr)
    quit(-1)

rd = Redis(host='localhost', port=6379, db=0)

productsCSVFile = open(sys.argv[1], 'r')

reader = csv.reader(productsCSVFile)

headerVals = []

for header in reader:
    headerVals = header
    break

for row in reader:
    if len(headerVals) != len(row):
        print("rows are different", file=sys.stderr)
        quit(-1)

    hashKey = "products:"

    hashKey += row[0] + ' '

    values = {}

    for ndx in range(1, len(row)):
        values[headerVals[ndx]] = row[ndx]

    rd.hset(name=hashKey, mapping=values)


rd.close()
productsCSVFile.close()