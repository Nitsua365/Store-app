const dbClient = require('./databaseClient/dbClient');
const sql = require('sql');

sql.setDialect('postgres');

module.exports = {
  storeAmazonDepartmentBulk : (departmentList) => {

    const department = sql.define({
      name: "amazon_department",
      columns: ['name', 'subdepartments', 'departmentlink', 'scrapelink']
    });

    console.log(department.insert(departmentList).toQuery());

    dbClient.query(department.insert(departmentList).toQuery(), (err, res) => {
      if (err) {
        console.error(err);
      }
      else {
        console.log(`Successfully inserted`)
      }
    })
    
  },
  storeOneAmazonDepartment : (departmentName, subDepartments, departmentLink, scrapeLink) => {
    // const subDepartmentsStr = subDepartments.length === 0 ? null : subDepartments.join(';');

    const insertQuery = `INSERT INTO amazon_department(name, subdepartments, departmentlink, scrapelink) VALUES($1, $2, $3, $4);`
    
    // insert into database
    dbClient.query(insertQuery, [departmentName, subDepartments, departmentLink, scrapeLink], (err, res) => {
      if (err) {
        console.error(err);
      }
      else {
        console.log(res);
      }
    })

  },
  createAmazonDepartmentTable : () => {
    const checkTable = `CREATE TABLE IF NOT EXISTS amazon_department(name VARCHAR(255) PRIMARY KEY, subdepartments VARCHAR(255), departmentlink VARCHAR (500), scrapelink VARCHAR(500));`

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