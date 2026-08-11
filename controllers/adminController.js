const { getDomain } = require('../models/serviceModel');

function showAdmin(req, res) {
  res.render('admin', {
    title: 'Admin - OPES EDGE',
    domain: {
      ...getDomain('community'),
      name: 'Platform Administration',
      summary:
        'A controlled workspace for users, domain content, alerts, and future device integrations.',
      slug: 'admin',
      features: [
        {
          title: 'User oversight',
          text: 'Review authenticated accounts and roles through the shared user system.',
          icon: 'bi-people',
        },
        {
          title: 'Content management',
          text: 'Prepare controlled management for crops, resources, notices, and service content.',
          icon: 'bi-pencil-square',
        },
        {
          title: 'Device and alert readiness',
          text: 'A clear starting point for future sensor devices, reports, and unresolved alerts.',
          icon: 'bi-shield-check',
        },
      ],
      actions: [],
      note: 'Administrative workflows are intentionally limited until their data models and permissions are implemented.',
      demoLabel: 'Admin-only foundation',
    },
  });
}

module.exports = { showAdmin };
