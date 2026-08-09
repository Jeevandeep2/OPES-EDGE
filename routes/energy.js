const express = require('express');
const { showEnergy, showMonitoring } = require('../controllers/energyController');

const router = express.Router();
router.get('/', showEnergy);
router.get('/monitoring', showMonitoring);
module.exports = router;
