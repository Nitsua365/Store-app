const puppeteer = require('puppeteer');

class ScrapeEngine {
  constructor(url, browser, page) {
    this.url = url;
    this.browser = browser;
    this.page = page;
  }

  init = async () => {
    await this.page.goto(this.url, { waitUntil : "load" });
  }

  goto = async (url) => {
    this.url = url;
    await this.page.goto(this.url, { waitUntil: "load" });
  }

  getBrowser = () => {
    return this.browser;
  }

  getPage = () => {
    return this.page;
  }

  getURL = () => {
    return this.url;
  }

  close = () => {
    this.browser.close();
  }

}

module.exports = { ScrapeEngine }