const express = require('express');
const router = express.Router();
const service = require('../service/productsService');

router.get(`/products/getAllDepartments`, async (req, res) => {
  try {

    res.send(await service.getAllProductDepartments());

  } catch (error) {
    console.error(error);
  }
})

module.exports = router;
