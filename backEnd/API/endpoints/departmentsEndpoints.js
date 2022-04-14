const express = require('express');
const router = express.Router();
const service = require('../service/departmentsService');


router.get(`/departments/getAllDepartments`, async (req, res) => {
    try {
  
      res.send(await service.getAllProductDepartments());
  
    } catch (error) {
      console.error(error);
    }
})