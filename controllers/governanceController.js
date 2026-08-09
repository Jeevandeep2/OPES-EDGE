const { renderDomain } = require('./domainController');

function showGovernance(req, res) {
  renderDomain(res, {
    name: 'Governance',
    summary:
      'A clear starting point for schemes, civic information, and grievance support.',
    features: ['Public schemes', 'Civic information', 'Grievance support'],
  });
}

module.exports = { showGovernance };
