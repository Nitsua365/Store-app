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

pool.on('error', (err, client) => {
  console.error('Unexpected error on idle client', err)
  process.exit(-1);
})

module.exports = { 
  query : (text, params, callback) => {
    return pool.query(text, params, callback)
  },
}