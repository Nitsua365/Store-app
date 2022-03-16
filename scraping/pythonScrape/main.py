from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selectorlib import Extractor, Formatter
from psycopg2 import connect

def getLinkFromDepartment(cursor, department):
    cursor.execute("SELECT link FROM amazon_department WHERE name = %s", (department,))
    return cursor.fetchone()[0]

def scrapeProductList():
    return 0

def main():

    # db client initialize
    conn = connect("dbname=americazon user=austinblanchard")
    cursor = conn.cursor()

    #  initialize driver
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(executable_path='./webdriver/chromedriver', options=options)

    # get baby department link
    baby_URL = getLinkFromDepartment(cursor=cursor, department="Baby")

    # get baby url
    driver.get(baby_URL)

    # click get scrape page for baby department
    currElem = driver.find_elements_by_xpath("//div[@class='a-checkbox a-checkbox-fancy aok-float-left apb-browse-refinements-checkbox']")
    currElem[16].click()

    scrapeURL = driver.current_url

    currElem = driver.


    # close chromium driver
    driver.close()

    # shutdown database connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
