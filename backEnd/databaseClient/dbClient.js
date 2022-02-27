const mysql = require('mysql');
const dotenv = require('dotenv');

dotenv.config();

const mysqlClient = mysql.createConnection({
  host: process.env.MYSQL_DB_HOST,
  port: 52000,
  user: process.env.MYSQL_DB_USER,
  password: process.env.MYSQL_DB_PASSWORD,
  database: process.env.MYSQL_DB_DBNAME,
});

mysqlClient.connect((err) => {
  if (err)
    console.error(err.stack);

  console.log('connected as id ' + connection.threadId);
});

module.exports = { mysqlClient }
