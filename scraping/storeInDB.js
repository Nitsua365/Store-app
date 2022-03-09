const dbClient = require('./databaseClient/dbClient').pool;

module.exports = {
  storeAmazonDepartment : (name, subDepartments, URL) => {
    const subDepartmentsStr = subDepartments.length === 0 ? 'NULL' : subDepartments.join(';');

    const insertQuery = `INSERT INTO amazon_department(name, subdepartments, link) VALUES($1,$2,$3);`
    
    dbClient.query(insertQuery, [name, subDepartmentsStr, URL]).then((err, res) => {
      if (err) {
        console.error(err);
      }
      else {
        console.log(res);
      }
    })

  }
}