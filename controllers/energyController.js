const { getDomain } = require('../models/serviceModel');

function showEnergy(req, res) {
  res.render('energy/index', { title: 'Energy Management - OPES EDGE', domain: getDomain('energy') });
}

function showMonitoring(req, res) {
  res.render('energy/monitoring', { title: 'Energy Monitoring - OPES EDGE', domain: getDomain('energy'), pageHeading: 'See energy patterns clearly before making a change.' });
}

module.exports = { showEnergy, showMonitoring };
