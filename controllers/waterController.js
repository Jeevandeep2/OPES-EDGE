const { getDomain } = require('../models/serviceModel');

function showWater(req, res) {
  res.render('water/index', { title: 'Water Management - OPES EDGE', domain: getDomain('water') });
}

function showMonitoring(req, res) {
  res.render('water/monitoring', { title: 'Water Monitoring - OPES EDGE', domain: getDomain('water'), pageHeading: 'Make every drop visible and easier to protect.' });
}

module.exports = { showWater, showMonitoring };
