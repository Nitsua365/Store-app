const express = require('express');
const app = express();
const endpoints = require('./endpoints/productEndpoints');
const cors = require('cors');

const bodyParser = require('body-parser');

const dotenv = require('dotenv');
dotenv.config();

// const Gun = require('gun');

function main() {
  app.use((req, res, next) => {
    try {
      
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

  var server = app.listen(process.env.PORT, () => {
    console.log(`Listening on http://localhost:${process.env.PORT}`);
  });

  // GUN({ server : server })

}

main();