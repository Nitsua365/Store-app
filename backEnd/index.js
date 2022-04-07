const express = require('express');
const app = express();
const endpoints = require('./API/endpoints/productEndpoints');
const cors = require('cors');

const bodyParser = require('body-parser');

const dotenv = require('dotenv');

function main() {
  dotenv.config();

  app.use((req, res, next) => {
    try {
      
      // TODO: once deployed make it a specific host
      res.header("Access-Control-Allow-Origin", "*");


      res.header("Access-Control-Allow-Methods", "POST, PUT, GET, PATCH, OPTIONS");

      next();

    } catch (error) {
      console.error(error);
    }
  })

  app.use(cors());
  app.use(express.json());
  app.use(bodyParser.json());
  // app.use(GUN.serve);
  app.use(express.static(__dirname));
  app.use(endpoints);

  app.listen(process.env.PORT, () => {
    console.log(`Listening on http://localhost:${process.env.PORT}`);
  });

}

main();