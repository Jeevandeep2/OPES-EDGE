const express = require('express');
const { showHealthcare, showDoctorDirectory, showSymptomChecker } = require('../controllers/healthcareController');

const router = express.Router();
router.get('/', showHealthcare);
router.get('/doctor-directory', showDoctorDirectory);
router.get('/symptom-checker', showSymptomChecker);
module.exports = router;
