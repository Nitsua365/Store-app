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

nullDict = { 'ASIN': None, 'AffiliateLink': None, 'CountryOfOrigin': None }

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


def insertProducts(cursor, productList, conn, pageNum):
    insertQuery = "INSERT INTO amazon_products(ASIN, ProductName, Department, Manufacturer, Rating, PictureRefLink, CountryOfOrigin, Price, AffiliateLink, ProductPageLink) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (ASIN) DO NOTHING;"
    sessionQuery = "INSERT INTO scrape_session(departmentname, pageleftoff) VALUES (%s, %s) ON CONFLICT (departmentname) DO UPDATE SET pageleftoff = EXCLUDED.pageleftoff;"
    for product in productList:
        try:
            cursor.execute(insertQuery, (product["ASIN"], product["ProductName"], product["Department"], product["Manufacturer"], product["Rating"], product["PictureRefLink"], product["CountryOfOrigin"], product["Price"], product["AffiliateLink"], product["ProductPageLink"]))
            conn.commit()

            # insert session information
            cursor.execute(sessionQuery, (product["Department"], pageNum))
            conn.commit()
        except Exception as err:
            print(err, file=sys.stderr)

def scrapeProductPage(URL, driver, department):
    affiliateWait = WebDriverWait(driver, 10)
    attributeWait = WebDriverWait(driver, 2)

    affiliateLink = None

    # navigate to product page
    driver.get(URL)

    # time.sleep(1)

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

    except ElementNotInteractableException:
        print("ERROR: cannot get affiliate link ELEMENT", file=sys.stderr, end='')
        return nullDict
    except TimeoutException:
        print("ERROR: cannot get affiliate link TIMEOUT", file=sys.stderr, end='')
        return nullDict

    try:
        # get ASIN
        getASIN = attributeWait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "ASIN")]//following-sibling::td')))
        ASIN = getASIN.get_attribute('innerHTML').strip().encode("ascii", "ignore").decode()
    except TimeoutException:
        try:
            getASIN = attributeWait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "ASIN")]//following-sibling::span')))
            ASIN = getASIN.get_attribute('innerHTML').strip().encode("ascii", "ignore").decode()
        except TimeoutException:
            ASIN = None
            print("ERROR: No ASIN found", file=sys.stderr, end='')

    try:
        #get product price
        getProductPrice = attributeWait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="a-offscreen" and contains(text(), "$")]')))
        productPrice = float(getProductPrice.get_attribute('innerHTML').strip()[1:].replace(',', ''))
    except TimeoutException:
        productPrice = None
        print("ERROR: No price found", file=sys.stderr, end='')
    except NoSuchElementException:
        productPrice = None
        print("ERROR: no price found", file=sys.stderr, end='')


    try:
        # get product name
        getProductName = attributeWait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]')))
        productName = getProductName.get_attribute('innerHTML').strip().encode("ascii", "ignore").decode()
    except NoSuchElementException:
        productName = None
        print("ERROR: no product name found", file=sys.stderr, end='')
    except TimeoutException:
        productName = None
        print("ERROR: no product name found", file=sys.stderr, end='')

    try:
        # get Manufacturer
        getManufacturer = attributeWait.until(EC.presence_of_element_located((By.XPATH, "//th[not(contains(text(), 'Recommended')) and not(contains(text(), 'recommended')) and not(contains(text(), 'discontinued')) and not(contains(text(), 'Discontinued')) and contains(text(), 'Manufacturer')]//following-sibling::td")))
        manufacturer = getManufacturer.get_attribute('innerHTML').strip().encode("ascii", "ignore").decode()
    except TimeoutException:
        try:
            getManufacturer = attributeWait.until(EC.presence_of_element_located((By.XPATH, "//span[not(contains(text(), 'Recommended')) and not(contains(text(), 'recommended')) and not(contains(text(), 'discontinued')) and not(contains(text(), 'Discontinued')) and contains(text(), 'Manufacturer')]//following-sibling::span")))
            manufacturer = getManufacturer.get_attribute('innerHTML').strip().encode("ascii", "ignore").decode()
        except TimeoutException:
            manufacturer = None
            print("ERROR: no manufacturer found", file=sys.stderr, end='')

    try:
        # get rating
        getRating = attributeWait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "out of 5")]')))
        rating = float(getRating.get_attribute('innerHTML').strip()[0:3])
    except NoSuchElementException:
        rating = None
        print("ERROR: no rating found", file=sys.stderr, end='')
    except TimeoutException:
        rating = None
        print("ERROR: no rating found", file=sys.stderr, end='')

    # get picture ref link
    try:
        getPictureRefLink = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="landingImage"]')))
        pictureRefLink = getPictureRefLink.get_attribute('src')
    except NoSuchElementException:
        pictureRefLink = None
        print("ERROR: no picture ref found", file=sys.stderr, end='')
    except TimeoutException:
        pictureRefLink = None
        print("ERROR: no picture ref found", file=sys.stderr, end='')

    try:
        # get country of origin
        getCountryOfOrigin = attributeWait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Country of Origin') or contains(text(), 'Country/Region of origin')]//following-sibling::*")))
        countryOfOrigin = getCountryOfOrigin.get_attribute('innerHTML').strip().encode("ascii", "ignore").decode()
    except NoSuchElementException:
        countryOfOrigin = None
        print("ERROR: No Country of Origin found", file=sys.stderr, end='')
    except TimeoutException:
        countryOfOrigin = None
        print("ERROR: No Country of Origin found", file=sys.stderr, end='')

    # get product page
    productPage = driver.current_url

    # print(' ' + URL, file=sys.stderr)

    return {
        'AffiliateLink': affiliateLink,
        'ASIN': ASIN,
        'ProductName': productName,
        'Department': department,
        'Manufacturer': manufacturer,
        'Rating': rating,
        'PictureRefLink': pictureRefLink,
        'CountryOfOrigin': countryOfOrigin,
        'Price': productPrice,
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



with connect("dbname=" + Login.postgres['dbname'] + " user=" + Login.postgres['user']) as conn:
    with conn.cursor() as cursor:

        def killSig(signal, frame):
            print("received: ", signal)
            driver.close()
            cursor.close()
            conn.close()

        options = webdriver.ChromeOptions()
        options.headless = True
        # options.add_argument("user-data-dir=" + Login.chromeData['data'])
        # options.add_argument("profile-directory=" + sys.argv[2])
        driver = webdriver.Chrome(executable_path='./webdriver/chromedriver', options=options)

        signal.signal(signal.SIGINT, killSig)

        # Navigate to amazon
        driver.get('https://amazon.com')

        # login to amazon affiliate account
        loginToAmazon(driver)

        # create product table
        # createProductTable(cursor, conn)

        # get products scrape page
        # scrapeLinksAndDepartments = getAllScrapeLinks(cursor)

        # web driver wait
        wait = WebDriverWait(driver, 20)

        departmentName = sys.argv[1]

        # Navigate to scraping page
        dropDownDepartments = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-search-dropdown-card"]')))
        dropDownDepartments.click()

        department = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchDropdownBox"]//option[contains(text(), "' + departmentName + '")]')))
        department.click()

        search = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-search-submit-button"]')))
        search.click()

        getScrapePage = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="a-link-normal"]//span[contains(text(), "Amazon.com") and @class="a-size-base a-color-base"]')))
        getScrapePage.click()

        # get max page numbers
        getPageNumber = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="search"]//span[@class="s-pagination-item s-pagination-disabled"]')))
        pageNumberCount = int(getPageNumber.get_attribute('innerHTML').strip())

        # loop through each page
        for i in range(0, pageNumberCount):

            # pre-load the next page link
            nextPageElem = wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')))
            nextPageLink = nextPageElem.get_attribute('href')

            productLinks = list(
                map(lambda x: x.get_attribute('href'), wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//div[@data-index and @data-asin and @data-component-id and @data-uuid]//h2/a')))))

            scrapedProducts = []

            # loop through each product on page
            for productURL in range(0, len(productLinks)):
                print("productURL", productLinks[productURL])

                # add products to scraped products list
                scrapedProducts.append(
                    scrapeProductPage(URL=productLinks[productURL], driver=driver,
                                      department=departmentName))

            # Filter product list
            insertList = filterProductList(scrapedProducts)

            # Insert products into database
            insertProducts(cursor, insertList, conn, i)

            # go to the next page in the pagination
            driver.get(nextPageLink)
            time.sleep(1)


        # close chromium driver
        driver.close()

        # shutdown database connection
        cursor.close()
        conn.close()
