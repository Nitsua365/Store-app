import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



from selectorlib import Extractor, Formatter
from psycopg2 import connect

from Login import amazonLogin

def getScrapeLinkFromDepartment(cursor, department):
    cursor.execute("SELECT scrapelink FROM amazon_department WHERE name = %s", (department,))
    return cursor.fetchone()[0]

def getAllScrapeLinks(cursor):
    cursor.execute("SELECT scrapelink FROM amazon_department WHERE scrapelink != 'NULL'")
    return cursor.fetchall()

def scrapeProductPage(URL, driver):

    affiliateLink = ''

    # navigate to product page
    driver.get(URL)

    time.sleep(3)

    # get affiliate link
    getLinkButton = driver.find_element_by_xpath('//*[@id="amzn-ss-text-link"]/span/strong')
    getLinkButton.click()

    getFullLinkButton = driver.find_element_by_xpath('//*[@id="amzn-ss-full-link-radio-button"]/label/i')
    getFullLinkButton.click()

    getAffiliateLink = driver.find_element_by_xpath('//*[@id="amzn-ss-text-fulllink-textarea"]')
    affiliateLink = getAffiliateLink.get_attribute('value')

    print(affiliateLink)



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
    driver = webdriver.Chrome(executable_path='./webdriver/chromedriver', options=options)

    # Navigate to amazon
    driver.get('https://amazon.com')

    # login to amazon affiliate account
    loginToAmazon(driver)

    # get baby products scrape page
    scrapeLinks = getAllScrapeLinks(cursor)


    for link in scrapeLinks:

        # thread has
        time.sleep(3)

        scrapePage = driver.get(link[0])

        productLinks = map(lambda x: x.get_attribute('href'), driver.find_elements_by_xpath("//div[@data-index and @data-asin and @data-component-id and @data-uuid]//h2/a"))


        for productURL in productLinks:
            print("productURL", productURL)
            scrapeProductPage(productURL, driver)
            driver.get(scrapePage)
            time.sleep(3)


    # close chromium driver
    driver.close()

    # shutdown database connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
