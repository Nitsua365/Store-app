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
          department: htmlDepartments[i],
          subDepartments : [],
          htmlValue : htmlDepartmentsValues[i],
          scrapeLink : null
        });

        prevNonSpaceNdx = i;
      }
      else {
        dict[prevNonSpaceNdx].subDepartments.push(htmlDepartments[i].trim());
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
      
      // click on the search button for the search dropdown option
      // await page.waitForSelector('input#nav-search-submit-button');
      await page.click('input#nav-search-submit-button');

      // wait for the navigation
      await page.waitForNavigation();

      // Set departmentURL
      dict[i]["departmentLink"] = await page.url();
      console.log(`got departmentLink: ${dict[i].departmentLink}`);

      // get href element for scrape link
      const [elem] = await page.$x("//a[@class='a-link-normal']/span[contains(text(), 'Amazon.com') and @class='a-size-base a-color-base']/parent::a")
      
      if (elem != undefined) {

        // get the scrape link from href value
        const scrapeAttr = await elem.getProperty('href');

        // store scrape Link
        dict[i]["scrapeLink"] = await scrapeAttr.jsonValue();

        console.log(`Scrape Link: ${dict[i]["scrapeLink"]}`)
      }


      // go back to the first page
      await page.goBack();
    }


    return dict;

  }
}