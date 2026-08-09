const { findById } = require('../models/userModel');

function attachCurrentUser(req, res, next) {
  res.locals.currentUser = req.session.user || null;
  next();
}

function requireAuth(req, res, next) {
  if (!req.session.user) {
    return res.redirect(`/login?next=${encodeURIComponent(req.originalUrl)}`);
  }

  const user = findById(req.session.user.id);
  if (!user) {
    req.session.destroy(() => res.redirect('/login'));
    return;
  }

  req.user = user;
  res.locals.currentUser = user;
  next();
}

function requireRole(...allowedRoles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.redirect(`/login?next=${encodeURIComponent(req.originalUrl)}`);
    }
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).render('error', {
        title: 'Access denied - OPES EDGE',
        message: 'You do not have permission to view this area.',
      });
    }
    next();
  };
}

module.exports = {
  attachCurrentUser,
  requireAuth,
  requireRole,
};
