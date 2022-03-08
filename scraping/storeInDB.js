const dbClient = require('./databaseClient/dbClient').pool;

module.exports = {
  storeAmazonDepartment : (name, subDepartments, URL) => {
    const subDepartmentsStr = subDepartments.length === 0 ? '' : subDepartments.join(';');

    const insertQuery = {
      text: `INSERT INTO amazon_department(name,subdepartments,link) VALUES('$1','$2','$3');`,
      values: [name, subDepartmentsStr, URL]
    }

    dbClient.query(insertQuery, (err, res) => {
      if (err) {
        console.error(err);
      }
      else {
        console.log(res);
      }
    });

  }
}