const engine = require('./ScrapeEngine');
const puppeteer = require('puppeteer');

module.exports = {
  getAmazonDepartments : async (scraper) => {

    // const browser = await puppeteer.launch({ path: "./scraping/chromedriver", headless: true });

    // console.log(browser);

    // var page = await browser.newPage();

    // await page.goto("http://amazon.com", { waitUntil : "load" });

    // const htmlDepartments = await page.evaluate(() => 
    //   Array.from(document.querySelectorAll('#searchDropdownBox option')).map(element => element.textContent)
    // )

    // browser.close();
        
    // return htmlDepartments;

    const htmlDepartments = await scraper.page.evaluate(() => {
      Array.from(document.querySelectorAll('#searchDropdownBox option')).map(element => element.textContent);
    })

    return htmlDepartments;

  }
}