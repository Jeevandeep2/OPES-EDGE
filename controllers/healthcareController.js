const { getDomain } = require('../models/serviceModel');

function showHealthcare(req, res) {
  res.render('healthcare/index', { title: 'Healthcare Services - OPES EDGE', domain: getDomain('healthcare') });
}

function showDoctorDirectory(req, res) {
  res.render('healthcare/doctor-directory', { title: 'Doctor Directory - OPES EDGE', domain: getDomain('healthcare'), pageHeading: 'Find trustworthy care information and the right next step.' });
}

function showSymptomChecker(req, res) {
  res.render('healthcare/symptom-checker', { title: 'Health Information - OPES EDGE', domain: getDomain('healthcare'), pageHeading: 'Understand symptoms without replacing professional care.' });
}

module.exports = { showHealthcare, showDoctorDirectory, showSymptomChecker };
