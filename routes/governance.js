const express = require('express');
const { showGovernance } = require('../controllers/governanceController');

const router = express.Router();
router.get('/', showGovernance);
router.get('/schemes', showGovernance);
router.get('/grievances', showGovernance);
module.exports = router;
