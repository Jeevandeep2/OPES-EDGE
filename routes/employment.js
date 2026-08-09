const express = require('express');
const { showEmployment } = require('../controllers/employmentController');

const router = express.Router();
router.get('/', showEmployment);
router.get('/job-listings', showEmployment);
router.get('/skill-matching', showEmployment);
module.exports = router;
