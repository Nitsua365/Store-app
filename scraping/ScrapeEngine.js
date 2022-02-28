const puppeteer = require('puppeteer');

class ScrapeEngine {
  constructor(url) {
    this.url = url;
  }

  init = async () => {

    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    // await page.goto(this.url, { waitUntil : "load" });

    const engine = {
      browser : browser,
      page : page
    }

    await engine.page.goto(this.url, { waitUntil : "load"});

    return engine;
  }

}

module.exports = { ScrapeEngine }