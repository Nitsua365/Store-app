from selenium import webdriver


def main():
    #  initialize driver
    driver = webdriver.Chrome(executable_path='./webdriver/chromedriver')

    # get amazon driver
    driver.get('https://www.amazon.com')



    # close chromium driver
    driver.close()

if __name__ == "__main__":
    main()
