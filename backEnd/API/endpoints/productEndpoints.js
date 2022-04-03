const { response } = require('express');
const express = require('express');
const router = express.Router();
const service = require('../../service/productsService');

const products = "/products";

router.get(`${products}/getAllDepartments`, async (req, res) => {
  try {
    
    const response = await service.getAllProductDepartments();

    res.send(response);

  } catch (error) {
    console.error(error);
  }
})

module.exports = router;
