const functions = require('./scrapeFunctions');
const ScrapeEngine = require('./ScrapeEngine').ScrapeEngine;

async function main() {
  
  const browserEngine = new ScrapeEngine("http://amazon.com");

  const engine = await browserEngine.init();

  console.log(await functions.getAmazonDepartments(engine));

  // engine.browser.close();
  // engine.page.close();
}

main();