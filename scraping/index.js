const functions = require('./scrapeFunctions');
const ScrapeEngine = require('./ScrapeEngine').ScrapeEngine;
const puppeteer = require('puppeteer');

async function main() {
  
  const browser = await puppeteer.launch({ headless: true });

  const browserEngine = new ScrapeEngine("http://amazon.com", browser, await browser.newPage());

  await browserEngine.init();

  console.log(await functions.getAmazonDepartments(browserEngine));  

  browserEngine.close();

}

main();