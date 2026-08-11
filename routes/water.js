const express = require('express');
const { showWater, showMonitoring } = require('../controllers/waterController');

const router = express.Router();
router.get('/', showWater);
router.get('/monitoring', showMonitoring);
module.exports = router;
