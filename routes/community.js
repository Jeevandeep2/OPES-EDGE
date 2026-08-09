const express = require('express');
const { showCommunity, showEvents, showFeedback } = require('../controllers/communityController');

const router = express.Router();
router.get('/', showCommunity);
router.get('/events', showEvents);
router.get('/feedback', showFeedback);
module.exports = router;
