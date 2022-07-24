const functions = require('./scrapeFunctions');
const ScrapeEngine = require('./ScrapeEngine').ScrapeEngine;
const puppeteer = require('puppeteer');
const { createAmazonDepartmentTable, storeAmazonDepartmentBulk } = require('./storeInDB');
const prompt = require("prompt-sync")();
const dbClient = require('./databaseClient/dbClient').pool;

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

    createAmazonDepartmentTable();

    // scrape amazon departments
    console.log("\nScraping Amazon Departments...\n");
    const amazonDepartments = await functions.getAmazonDepartments(browserEngine);

    // insert scraped departments into database
    console.log("\nInserting into DB...\n");

    // insert into DB
    storeAmazonDepartmentBulk(amazonDepartments);
  }

  // close the database client
  dbClient.end();
  
  // close browser engine
  await browserEngine.close();

}

main();