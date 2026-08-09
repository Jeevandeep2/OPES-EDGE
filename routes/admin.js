const express = require('express');
const { requireAuth, requireRole } = require('../middleware/authMiddleware');
const { showAdmin } = require('../controllers/adminController');

const router = express.Router();
router.get('/', requireAuth, requireRole('admin'), showAdmin);
module.exports = router;
