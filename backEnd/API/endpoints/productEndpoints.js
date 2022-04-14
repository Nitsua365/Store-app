const express = require('express');
const router = express.Router();
const service = require('../service/productsService.js');

router.get(`/products/getProducts`, async (req, res) => {
  try {
    res.send(await service.getProducts(req.body));
  }
  catch (error) {
    console.error(error);
  }
})

module.exports = router;
