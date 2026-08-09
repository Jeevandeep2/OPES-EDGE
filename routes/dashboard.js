const express = require('express');
const { requireAuth } = require('../middleware/authMiddleware');
const { showDashboard } = require('../controllers/dashboardController');

const router = express.Router();

router.get('/', requireAuth, showDashboard);

module.exports = router;
