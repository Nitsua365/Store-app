import signal
import sys
import time

from selenium import webdriver

from AmazonScraper import Login

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException

def cleanAttribute(string):
    return string.strip().encode("ascii", "ignore").decode().replace(',', ' ').replace('  ', ' ').replace('&amp;', '&').replace('&nbsp;', ' ').strip()

def loginToAmazon(driver):
    loginButton = driver.find_element_by_xpath("//*[@id='nav-link-accountList']")
    loginPage = loginButton.get_attribute('href')

    driver.get(loginPage)

    # enter email
    emailPrompt = driver.find_element_by_xpath("//*[@id='ap_email']")
    emailPrompt.send_keys(Login.amazonLogin['email'])

    # click continue
    continueButton = driver.find_element_by_xpath("//*[@id='continue']")
    continueButton.click()

    # enter password
    password = driver.find_element_by_xpath("//*[@id='ap_password']")
    password.send_keys(Login.amazonLogin['password'])

    # click login
    signIn = driver.find_element_by_xpath("//*[@id='signInSubmit']")
    signIn.click()

def scrapeAffiliate(URL, driver):
    affiliateWait = WebDriverWait(driver, 10)

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
        affiliateLink = cleanAttribute(getAffiliateLink.get_attribute('value'))

    except ElementNotInteractableException:
        print("ERROR: cannot get affiliate link ELEMENT", file=sys.stderr, end='')
        return None
    except TimeoutException:
        print("ERROR: cannot get affiliate link TIMEOUT", file=sys.stderr, end='')
        return None

    return affiliateLink