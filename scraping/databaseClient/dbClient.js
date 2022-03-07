const Pool = require('pg').Pool;
const dotenv = require('dotenv');

dotenv.config();

const pool = new Pool({
  user: process.env.PSQL_DB_USER,
  host: process.env.PSQL_DB_HOST,
  database: process.env.PSQL_DB_DBNAME,
  password: process.env.PSQL_DB_PASSWORD,
  port: process.env.PSQL_DB_PORT
});

pool.connect();

module.exports = { pool }