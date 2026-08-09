const express = require('express');
const {
  showEducation,
  showResources,
  showCourses,
} = require('../controllers/educationController');

const router = express.Router();
router.get('/', showEducation);
router.get('/courses', showCourses);
router.get('/resources', showResources);
module.exports = router;
