const functions = require('./scrapeFunctions');
const ScrapeEngine = require('./ScrapeEngine').ScrapeEngine;
const puppeteer = require('puppeteer');
const { storeAmazonDepartment } = require('./storeInDB');

async function main() {
  
  // create browser
  const browser = await puppeteer.launch({ headless: true });

  // create browser engine
  const browserEngine = new ScrapeEngine("http://amazon.com", browser, await browser.newPage());

  // initialize the browser engine
  await browserEngine.init();

  // scrape amazon departments
  const amazonDepartments = await functions.getAmazonDepartments(browserEngine);
  console.log(amazonDepartments);

  for (let i = 0; i < amazonDepartments.length; i++) {
    storeAmazonDepartment(amazonDepartments[i].department, amazonDepartments[i].subDepartments, amazonDepartments[i].departmentLink);
  }
  
  // close browser engine
  browserEngine.close();

}

main();