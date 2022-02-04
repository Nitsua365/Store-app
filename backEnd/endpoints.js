const express = require('express');
const router = express.Router();
const service = require('./service');

router.get("/Hello", (req, res) => {
  try {

    service.hello();

    res.send("GET on /Hello");
    
  } catch (error) {
    console.error(error);
  }
})

module.exports = router;
