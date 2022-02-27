const puppeteer = require('puppeteer');

class ScrapeEngine {
  constructor(url) {
    this.browser = await puppeteer.launch({ path: "./scraping/chromedriver", headless: true });
    this.page = await this.browser.newPage();

    await this.page.goto(url, { waitUntil : "load" });
  }

  getPage = () => {
    return this.page;
  }

  getBrowser = () => {
    return this.browser;
  }

  closeEngine = () => {
    this.browser.close();
  }

}

module.exports = { ScrapeEngine }