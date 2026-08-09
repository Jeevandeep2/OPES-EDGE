const { getDomain } = require('../models/serviceModel');

function showCommunity(req, res) {
  res.render('community/index', { title: 'Community Services - OPES EDGE', domain: getDomain('community') });
}

function showEvents(req, res) {
  res.render('community/events', { title: 'Community Notices - OPES EDGE', domain: getDomain('community'), pageHeading: 'Keep up with local notices and community activity.' });
}

function showFeedback(req, res) {
  res.render('community/feedback', { title: 'Community Feedback - OPES EDGE', domain: getDomain('community'), pageHeading: 'Make it easier for residents to share feedback.' });
}

module.exports = { showCommunity, showEvents, showFeedback };
