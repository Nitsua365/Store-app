const puppeteer = require("puppeteer");
const dbClient = require("../../databaseClient/dbClient").mysqlClient;
// const gun = require('gun');

// const GUN = gun({ peers: "http://localhost:5000" });

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

    const browser = await puppeteer.launch({ path: "./backEnd/chromedriver", headless: true });

    var page = await browser.newPage();
    await page.goto("http://amazon.com", { waitUntil : "load" });

    const htmlDepartments = await page.evaluate(() => 
      Array.from(document.querySelectorAll('#searchDropdownBox option')).map(element => element.textContent)
    )

    browser.close();
        
    return htmlDepartments;
  },


}

