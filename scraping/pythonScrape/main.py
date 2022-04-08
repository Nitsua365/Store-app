import copy
import os
import signal
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException

from psycopg2 import connect

import Login
from Login import amazonLogin
from Login import chromeData


def getScrapeLinkFromDepartment(cursor, department):
    cursor.execute("SELECT scrapelink FROM amazon_department WHERE name = %s", (department,))
    return cursor.fetchone()[0]


def getAllScrapeLinks(cursor):
    cursor.execute("SELECT scrapelink, name FROM amazon_department WHERE scrapelink IS NOT NULL")
    return cursor.fetchall()

def createProductTable(cursor, conn):
    try:
        query = "CREATE TABLE IF NOT EXISTS amazon_products (ASIN VARCHAR(20) PRIMARY KEY NOT NULL, ProductName VARCHAR(500), Department VARCHAR(100), Manufacturer VARCHAR(255), Rating NUMERIC(3, 2), PictureRefLink VARCHAR(500), CountryOfOrigin VARCHAR(60), DateScrapped DATE NOT NULL DEFAULT CURRENT_DATE, Price NUMERIC(10, 2), AffiliateLink VARCHAR(500), ProductPageLink VARCHAR(500));"
        cursor.execute(query)
        conn.commit()
    except Exception as err:
        print(err)


def insertProducts(cursor, productList, conn):
    query = "INSERT INTO amazon_products(ASIN, ProductName, Department, Manufacturer, Rating, PictureRefLink, CountryOfOrigin, Price, AffiliateLink, ProductPageLink) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (ASIN) DO NOTHING;"
    for product in productList:
        try:
            cursor.execute(query, (product["ASIN"], product["ProductName"], product["Department"], product["Manufacturer"], product["Rating"], product["PictureRefLink"], product["CountryOfOrigin"], product["Price"], product["AffiliateLink"], product["ProductPageLink"]))
            conn.commit()
        except Exception as err:
            print(err, file=sys.stderr)

def scrapeProductPage(URL, driver, price, department):
    affiliateWait = WebDriverWait(driver, 10)
    attributeWait = WebDriverWait(driver, 2)

    affiliateLink = None

    # navigate to product page
    driver.get(URL)

    time.sleep(1)

    # click full link button
    try:
        # click amazon stripe tab
        getLinkButton = affiliateWait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="amzn-ss-text-link"]/span/strong/a[@title="Text"]')))
        getLinkButton.click()

        getFullLinkButton = affiliateWait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="amzn-ss-full-link-radio-button"]//span[contains(text(), "Full Link")]')))
        getFullLinkButton.click()

        # get the affiliate link
        getAffiliateLink = affiliateWait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="amzn-ss-text-fulllink-textarea"]')))
        affiliateLink = getAffiliateLink.get_attribute('value')

        # time.sleep(1)
    except ElementNotInteractableException:
        print("ERROR: cannot get affiliate link", file=sys.stderr)
    except TimeoutException:
        print("ERROR: cannot get affiliate link", file=sys.stderr)

    try:
        # get ASIN
        getASIN = attributeWait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "ASIN")]//following-sibling::td')))
        ASIN = getASIN.get_attribute('innerHTML').strip()
    except TimeoutException:
        try:
            getASIN = attributeWait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "ASIN")]//following-sibling::span')))
            ASIN = getASIN.get_attribute('innerHTML').strip()
        except TimeoutException:
            ASIN = None
            print("ERROR: No ASIN found", file=sys.stderr)

    try:
        # get product name
        qetProductName = attributeWait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]')))
        productName = qetProductName.get_attribute('innerHTML').strip()
    except NoSuchElementException:
        productName = None
        print("ERROR: no product name found")
    except TimeoutException:
        productName = None
        print("ERROR: no product name found")

    try:
        # get Manufacturer
        getManufacturer = attributeWait.until(EC.presence_of_element_located((By.XPATH, "//th[not(contains(text(), 'Recommended')) and not(contains(text(), 'recommended')) and not(contains(text(), 'discontinued')) and not(contains(text(), 'Discontinued')) and contains(text(), 'Manufacturer')]//following-sibling::td")))
        manufacturer = getManufacturer.get_attribute('innerHTML').strip()
    except TimeoutException:
        try:
            getManufacturer = attributeWait.until(EC.presence_of_element_located((By.XPATH, "//span[not(contains(text(), 'Recommended')) and not(contains(text(), 'recommended')) and not(contains(text(), 'discontinued')) and not(contains(text(), 'Discontinued')) and contains(text(), 'Manufacturer')]//following-sibling::span")))
            manufacturer = getManufacturer.get_attribute('innerHTML').strip()
        except TimeoutException:
            manufacturer = None
            print("ERROR: no manufacturer found", file=sys.stderr)

    try:
        # get rating
        getRating = attributeWait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "out of 5")]')))
        rating = float(getRating.get_attribute('innerHTML').strip()[0:3])
    except NoSuchElementException:
        rating = None
        print("ERROR: no rating found")
    except TimeoutException:
        rating = None
        print("ERROR: no rating found")

    # get picture ref link
    try:
        getPictureRefLink = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="landingImage"]')))
        pictureRefLink = getPictureRefLink.get_attribute('src')
    except NoSuchElementException:
        pictureRefLink = None
        print("ERROR: no picture ref found")
    except TimeoutException:
        pictureRefLink = None
        print("ERROR: no picture ref found")

    try:
        # get country of origin
        getCountryOfOrigin = attributeWait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*")))
        countryOfOrigin = getCountryOfOrigin.get_attribute('innerHTML').strip()
    except NoSuchElementException:
        countryOfOrigin = None
        print("ERROR: No Country of Origin found", file=sys.stderr)
    except TimeoutException:
        countryOfOrigin = None
        print("ERROR: No Country of Origin found", file=sys.stderr)

    # get product page
    productPage = driver.current_url

    return {
        'AffiliateLink': affiliateLink,
        'ASIN': ASIN,
        'ProductName': productName,
        'Department': department,
        'Manufacturer': manufacturer,
        'Rating': rating,
        'PictureRefLink': pictureRefLink,
        'CountryOfOrigin': countryOfOrigin,
        'Price': price,
        'ProductPageLink': productPage
    }

def filterProductList(productList):
    removeNulls = list(filter(lambda x: (x['ASIN'] is not None) and (x['AffiliateLink'] is not None) and (x['CountryOfOrigin'] is not None), productList))
    removeChina = list(filter(lambda x: 'China'.lower() not in x['CountryOfOrigin'].lower(), removeNulls))
    return removeChina

def loginToAmazon(driver):
    loginButton = driver.find_element_by_xpath("//*[@id='nav-link-accountList']")
    loginPage = loginButton.get_attribute('href')

    driver.get(loginPage)

    # enter email
    emailPrompt = driver.find_element_by_xpath("//*[@id='ap_email']")
    emailPrompt.send_keys(amazonLogin['email'])

    # click continue
    continueButton = driver.find_element_by_xpath("//*[@id='continue']")
    continueButton.click()

    # enter password
    password = driver.find_element_by_xpath("//*[@id='ap_password']")
    password.send_keys(amazonLogin['password'])

    # click login
    signIn = driver.find_element_by_xpath("//*[@id='signInSubmit']")
    signIn.click()


def main():
    with connect("dbname=" + Login.postgres['dbname'] + " user=" + Login.postgres['user']) as conn:
        with conn.cursor() as cursor:

            options = Options()
            options.headless = False
            # options.add_argument(chromeData['data'])
            driver = webdriver.Chrome(executable_path='./webdriver/chromedriver', options=options)

            # Navigate to amazon
            driver.get('https://amazon.com')

            # login to amazon affiliate account
            loginToAmazon(driver)

            # create product table
            createProductTable(cursor, conn)

            # get baby products scrape page
            scrapeLinksAndDepartments = getAllScrapeLinks(cursor)

            # web driver wait
            wait = WebDriverWait(driver, 10)

            for linkAndDepartment in scrapeLinksAndDepartments:

                # driver.start_session()
                # driver.start_client()

                departmentName = linkAndDepartment[1]
                link = linkAndDepartment[0]

                time.sleep(1)

                driver.get(link)

                time.sleep(1)

                # get max page numbers
                getPageNumber = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[28]/div/div/span/span[4]')))
                pageNumberCount = int(getPageNumber.get_attribute('innerHTML').strip())

                # loop through each page
                for i in range(0, pageNumberCount):

                    # pre-load the next page link
                    nextPageElem = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')))
                    nextPageLink = nextPageElem.get_attribute('href')

                    productLinks = list(map(lambda x: x.get_attribute('href'), wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-index and @data-asin and @data-component-id and @data-uuid]//h2/a')))))
                    productPrices = list(map(lambda x: float(x.get_attribute('innerHTML')[1:]), wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="a-price"]/*[@class="a-offscreen"]')))))
                    productPrices = productPrices[0:len(productLinks)]

                    scrapedProducts = []

                    # loop through each product on page
                    for productURL in range(0, len(productLinks)):
                        print("productURL", productLinks[productURL])

                        # add products to scraped products list
                        scrapedProducts.append(scrapeProductPage(URL=productLinks[productURL], driver=driver, price=productPrices[productURL], department=departmentName))

                    # Filter product list
                    insertList = filterProductList(scrapedProducts)

                    # Insert products into database
                    insertProducts(cursor, insertList, conn)

                    # go to the next page in the pagination
                    driver.get(nextPageLink)
                    time.sleep(1)


            # close chromium driver
            driver.close()

            # shutdown database connection
            cursor.close()
            conn.close()


if __name__ == "__main__":
    main()
