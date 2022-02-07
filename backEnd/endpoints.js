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

router.post("/insert/:path", (req, res) => {
  try {
    
    service.insert(req.params.path, req.body);

    res.send(`inserted ${req.body} at path ${req.params.path}`);

  } catch (error) {
    console.error(error);
  }
})

router.get("/getAll", (req, res) => {
  try {

    console.log(service.getAll());

    res.send(JSON.stringify(service.getAll()));
    
  } catch (error) {
    console.error(error);
  }
})

module.exports = router;
