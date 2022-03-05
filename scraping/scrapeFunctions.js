const engine = require('./ScrapeEngine');
const puppeteer = require('puppeteer');

module.exports = {
  getAmazonDepartments : async (scraper) => {
    const htmlDepartments = await scraper.getPage().evaluate(() => 
      Array.from(document.querySelectorAll('#searchDropdownBox option')).map(element => element.textContent)
    );

    const SPACE = " ";

    let dict = [];
    let prevNonSpaceNdx;

    for (let i = 0; i < htmlDepartments.length; i++) {

      if (!(/^\s/.test(htmlDepartments[i]))) {

        dict.push({
          department: htmlDepartments[i],
          subDepartments : []
        });

        prevNonSpace = htmlDepartments[i];
        prevNonSpaceNdx = i;
      }
      else {
        dict[prevNonSpaceNdx].subDepartments.push(htmlDepartments[i].trim());
      }

    }

    return dict;

  }
}