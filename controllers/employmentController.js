const { renderDomain } = require('./domainController');

function showEmployment(req, res) {
  renderDomain(res, {
    name: 'Employment',
    summary:
      'A future-ready space for local opportunities and skill development.',
    features: ['Job listings', 'Skill matching', 'Career guidance'],
  });
}

module.exports = { showEmployment };
