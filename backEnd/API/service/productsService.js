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

  },


}

