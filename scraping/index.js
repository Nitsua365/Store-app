const functions = require('./scrapeFunctions');
const ScrapeEngine = require('./ScrapeEngine').ScrapeEngine;
const puppeteer = require('puppeteer');
const { storeAmazonDepartment } = require('./storeInDB');
const prompt = require("prompt-sync")();


async function main() {
  
  // create browser
  const browser = await puppeteer.launch({ headless: true });

  // create browser engine
  const browserEngine = new ScrapeEngine("http://amazon.com", browser, await browser.newPage());

  // initialize the browser engine
  await browserEngine.init();

  // prompt for department scraping
  const departmentResponse = prompt("Do you want to scrape and store amazon departments? (y/n): ");

  // check to scrape department response
  if (departmentResponse.toUpperCase() === 'Y') {
    // scrape amazon departments
    console.log("Scraping Amazon Departments...\n");
    const amazonDepartments = await functions.getAmazonDepartments(browserEngine);

    amazonDepartments.forEach(elem => storeAmazonDepartment(elem.department, elem.subDepartments, elem.departmentLink));
  }

  // close the database client
  // dbClient.end();
  
  // close browser engine
  browserEngine.close();

}

main();