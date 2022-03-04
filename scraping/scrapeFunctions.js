const engine = require('./ScrapeEngine');
const puppeteer = require('puppeteer');

module.exports = {
  getAmazonDepartments : async (scraper) => {
    return await scraper.page.evaluate(() => 
      Array.from(document.querySelectorAll('#searchDropdownBox option')).map(element => element.textContent)
    );
  }
}