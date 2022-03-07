const dbClient = require('./databaseClient/dbClient').pool;

module.exports = {
  storeAmazonDepartment : (name, subDepartments, URL) => {
    const subDepartmentsStr = subDepartments.join(';');
    dbClient.query(`INSERT INTO amazon_department(name, subdepartments, link)VALUES(${name}, ${subDepartmentsStr}, ${URL})`)
  }
}