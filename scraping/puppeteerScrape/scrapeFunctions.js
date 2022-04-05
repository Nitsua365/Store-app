module.exports = {
  getAmazonDepartments : async (scraper) => {

    const page = scraper.getPage();

    // get the department names
    const htmlDepartments = await page.evaluate(() => 
      Array.from(document.querySelectorAll('#searchDropdownBox option')).map(element => element.textContent)
    );

    const htmlDepartmentsValues = await page.evaluate(() => 
      Array.from(document.querySelectorAll('#searchDropdownBox option')).map(element => element.getAttribute("value"))
    );

    // initialize the dictionary
    let dict = [];
    let prevNonSpaceNdx;

    // add the department name 
    for (let i = 0; i < htmlDepartments.length; i++) {

      // check if the department starts with space
      if (!(/^\s/.test(htmlDepartments[i]))) {
        dict.push({
          name: htmlDepartments[i],
          subdepartments : [],
          htmlValue : htmlDepartmentsValues[i],
          departmentlink : null,
          scrapelink : null
        });

        prevNonSpaceNdx = i;
      }
      else {
        dict[prevNonSpaceNdx].subdepartments.push(htmlDepartments[i].trim());
      }

    }

    // scrape department URLs
    for (let i = 0; i < dict.length; i++) {

      // click on drop down card
      await page.waitForSelector('#nav-search-dropdown-card')
      await scraper.getPage().click('#nav-search-dropdown-card');
      
      // select the current drop down box
      await page.waitForSelector('select#searchDropdownBox');
      await page.select('select#searchDropdownBox', dict[i].htmlValue);

      delete dict[i].htmlValue;
      
      // click on the search button for the search dropdown option
      // await page.waitForSelector('input#nav-search-submit-button');
      await page.click('input#nav-search-submit-button');

      // wait for the navigation
      await page.waitForNavigation();

      // Set departmentURL
      dict[i]["departmentlink"] = await page.url();
      console.log(`got departmentLink: ${dict[i].departmentlink}`);

      // get href element for scrape link
      const [elem] = await page.$x("//a[@class='a-link-normal']/span[contains(text(), 'Amazon.com') and @class='a-size-base a-color-base']/parent::a")
      
      if (elem != undefined) {

        // get the scrape link from href value
        const scrapeAttr = await elem.getProperty('href');

        // store scrape Link
        dict[i]["scrapelink"] = await scrapeAttr.jsonValue();

        console.log(`Scrape Link: ${dict[i]["scrapelink"]}`)
      }


      // go back to the first page
      await page.goBack();
    }

    // make subdepartments a string field
    for (let i = 0; i < dict.length; i++) {
      if (dict[i]['subdepartments'].length > 0) {
        dict[i]['subdepartments'] = dict[i]['subdepartments'].join(";");
      }
      else {
        dict[i]['subdepartments'] = null;
      }
    }


    return dict;

  }
}