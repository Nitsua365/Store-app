const express = require('express');
const router = express.Router();
const service = require('../service/productsService.js');

router.get(`/departments/getAllDepartments`, async (req, res) => {
  try {

    res.send(await service.getAllProductDepartments());

  } catch (error) {
    console.error(error);
  }
})

router.get(`/products/getProducts`, async (req, res) => {
  try {
    res.send(await service.getProducts(req.body));
  }
  catch (error) {
    console.error(error);
  }
})

module.exports = router;
