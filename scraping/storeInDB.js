const dbClient = require('./databaseClient/dbClient');

module.exports = {
  storeAmazonDepartment : (name, subDepartments, URL) => {
    const subDepartmentsStr = subDepartments.join(';');
    dbClient.pool.query(`INSERT INTO amazon_department(name, subdepartments, link)VALUES(${name}, ${subDepartmentsStr}, ${URL})`)
  }
}