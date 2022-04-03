import sys
import time
import bs4 as bs
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


from selectorlib import Extractor, Formatter
from psycopg2 import connect

from Login import amazonLogin
from Login import chromeData

def getScrapeLinkFromDepartment(cursor, department):
    cursor.execute("SELECT scrapelink FROM amazon_department WHERE name = %s", (department,))
    return cursor.fetchone()[0]

def getAllScrapeLinks(cursor):
    cursor.execute("SELECT scrapelink FROM amazon_department WHERE scrapelink IS NOT NULL")
    return cursor.fetchall()

def scrapeProductPage(URL, driver):

    wait = WebDriverWait(driver, 10)

    affiliateLink = ''

    # navigate to product page
    driver.get(URL)

    # click amazon stripe tab
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="amzn-ss-text-link"]/span/strong')))
    getLinkButton = driver.find_element_by_xpath('//*[@id="amzn-ss-text-link"]/span/strong')
    getLinkButton.click()

    # click full link button
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="amzn-ss-full-link-radio-button"]/label/i')))
    getFullLinkButton = driver.find_element_by_xpath('//*[@id="amzn-ss-full-link-radio-button"]/label/i')
    getFullLinkButton.click()

    # get the affiliate link
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="amzn-ss-text-fulllink-textarea"]')))
    getAffiliateLink = driver.find_element_by_xpath('//*[@id="amzn-ss-text-fulllink-textarea"]')
    affiliateLink = getAffiliateLink.get_attribute('value')


    try:
        # get ASIN
        getASIN = driver.find_element_by_xpath('//*[contains(text(), "ASIN")]//following-sibling::td')
    except NoSuchElementException:
        try:
            getASIN = driver.find_element_by_xpath('//*[contains(text(), "ASIN")]//following-sibling::span')
        except NoSuchElementException:
            print("ERROR: No ASIN found", sys.stderr)

    ASIN = getASIN.get_attribute('innerHTML').strip()

    # get product name
    getProductName = driver.find_element_by_xpath('//*[@id="productTitle"]')
    productName = getProductName.get_attribute('innerHTML').strip()

    # Get product department

    # get Manufacturer
    getManufacturer = driver.find_element_by_xpath('//*[contains(text(), "Manufacturer")]//following-sibling::*')
    manufacturer = getManufacturer.get_attribute('innerHTML').trim()

    return {
        'ASIN': ASIN,
        'ProductName': productName,
        'Manufacturer': manufacturer,
        'affiliateLink': affiliateLink
    }



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

    # db client initialize
    conn = connect("dbname=americazon user=austinblanchard")
    cursor = conn.cursor()

    #  initialize driver
    options = Options()
    options.headless = False
    # options.add_argument(chromeData['data'])
    driver = webdriver.Chrome(executable_path='./webdriver/chromedriver', options=options)

    # Navigate to amazon
    driver.get('https://amazon.com')

    # login to amazon affiliate account
    loginToAmazon(driver)

    # get baby products scrape page
    scrapeLinks = getAllScrapeLinks(cursor)

    # web driver wait
    wait = WebDriverWait(driver, 10)

    for link in scrapeLinks:

        time.sleep(1)

        driver.get(link[0])

        time.sleep(1)

        # wait for elements
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-index and @data-asin and @data-component-id and @data-uuid]//h2/a')))

        productLinks = list(map(lambda x: x.get_attribute('href'), driver.find_elements_by_xpath("//div[@data-index and @data-asin and @data-component-id and @data-uuid]//h2/a")))

        for productURL in productLinks:
            print("productURL", productURL)
            scrapeProductPage(productURL, driver)


    # close chromium driver
    driver.close()

    # shutdown database connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
