const dbClient = require('./databaseClient/dbClient');

module.exports = {
  storeAmazonDepartment : (name, subDepartments, URL) => {
    const subDepartmentsStr = subDepartments.length === 0 ? 'NULL' : subDepartments.join(';');

    const insertQuery = `INSERT INTO amazon_department(name, subdepartments, departmentLink, scrapeLink) VALUES($1,$2,$3,'NULL');`
    
    // insert into database
    dbClient.query(insertQuery, [name, subDepartmentsStr, URL], (err, res) => {
      if (err) {
        console.error(err);
      }
      else {
        console.log(res);
      }
    })

  },
  createAmazonDepartmentTable : () => {
    const checkTable = `CREATE TABLE IF NOT EXISTS amazon_department(name VARCHAR(255) PRIMARY KEY, subdepartments VARCHAR(255), departmentLink VARCHAR (500), scrapeLink VARCHAR(500));`

    dbClient.query(checkTable, [], (err, res) => {
      if (err) {
        console.error(err)
      }
      else {
        console.log(res);
      }
    });
  }
}