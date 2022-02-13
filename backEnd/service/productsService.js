const puppeteer = require("puppeteer");
const process = require('process');

var browser, amazonHomePage;

(async () => {
  browser = await puppeteer.launch({ path: "./backEnd/chromedriver", headless: true });
  amazonHomePage = await browser.newPage();

  process.on('SIGINT', () => {
    browser.close();
    console.log("exiting browser");
  })
})();


module.exports = {

  getProductsByDepartmentNameAndSubCatagory : (departmentName, subCat) => {
    
  },
  getProductByASIN : (AmazonASIN) => {

  },
  getProductByProductLink : (URL) => {

  },
  getProductsByCountryOfOrigin : (countryOfOrigin) => {

  },
  getProductsByCountryOfOriginAndDepartment : (countryOfOrigin, departmentName) => {

  },
  getProducts : (JSONdata) => {
    // pass json request body of optional params departmentName, countryOfOrigin, subCategory
  },
  getAllProductDepartments : async () => {
    

    await amazonHomePage.goto("https://amazon.com", { waitUntil: "load" });

    const htmlDepartments = await amazonHomePage.evaluate(() => 
      Array.from(document.querySelectorAll('#searchDropdownBox option')).map(element => element.textContent)
    )
        
    // browser.close();

    return htmlDepartments;
  },


}

