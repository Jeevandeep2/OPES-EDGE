const express = require('express');
const {
  showAgriculture,
  showCropAdvisor,
  adviseCrop,
  showWeather,
  showMarketPrices,
} = require('../controllers/agricultureController');

const router = express.Router();
router.get('/', showAgriculture);
router.get('/crop-advisor', showCropAdvisor);
router.post('/crop-advisor', adviseCrop);
router.get('/market-prices', showMarketPrices);
router.get('/weather', showWeather);
module.exports = router;
