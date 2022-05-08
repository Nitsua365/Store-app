import subprocess
import os
import signal
import time

from psycopg2 import connect
import Login

pid = []


def getScrapeDepartments(cursor):
    cursor.execute("SELECT scrapeLink, name FROM amazon_department WHERE scrapeLink IS NOT NULL")
    return cursor.fetchall()


def getScrapeLinkFromDepartment(cursor, department):
    cursor.execute("SELECT scrapelink, name FROM amazon_department WHERE name = %s", (department,))
    return cursor.fetchone()[0]


def createProductTable(cursor, conn):
    try:
        query = "CREATE TABLE IF NOT EXISTS amazon_products (ASIN VARCHAR(20) PRIMARY KEY NOT NULL, ProductName VARCHAR(500), Department VARCHAR(100), Manufacturer VARCHAR(255), Rating NUMERIC(3, 2), PictureRefLink VARCHAR(500), CountryOfOrigin VARCHAR(60), DateScrapped DATE NOT NULL DEFAULT CURRENT_DATE, Price NUMERIC(10, 2), AffiliateLink VARCHAR(500), ProductPageLink VARCHAR(500));"
        cursor.execute(query)
        conn.commit()
    except Exception as err:
        print(err)


def quitThread(signal, frame):
    for i in pid:
        print("killing process: ", i.pid)
        i.send_signal(signal.SIGINT)


with connect("dbname=" + Login.postgres['dbname'] + " user=" + Login.postgres['user']) as conn:
    with conn.cursor() as cursor:

        departmentNameList = getScrapeDepartments(cursor)

        createProductTable(cursor=cursor, conn=conn)

        count = 0

        signal.signal(signal.SIGINT, quitThread)

        for scrapeLink, name in departmentNameList:

            time.sleep(1)

            cmd = 'python3 scrapeDepartment.py \"' + name + '\" ' + "Profile " + str(count + 1)

            if scrapeLink is None:
                print("No scrape link for:", name, "or department doesn't exist")
            else:
                pid.append(subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, preexec_fn=os.setsid))

            count += 1

            if count == 6:
                break

        for i in range(0, count):
            pid[i].wait()
