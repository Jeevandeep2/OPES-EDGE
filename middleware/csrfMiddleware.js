const crypto = require('crypto');

function csrfProtection(req, res, next) {
  if (!req.session.csrfToken) {
    req.session.csrfToken = crypto.randomBytes(32).toString('hex');
  }
  res.locals.csrfToken = req.session.csrfToken;

  if (!['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method)) {
    return next();
  }

  const submittedToken = String(
    req.body._csrf || req.get('x-csrf-token') || '',
  );
  const expectedToken = String(req.session.csrfToken);
  const validToken =
    submittedToken.length === expectedToken.length &&
    crypto.timingSafeEqual(
      Buffer.from(submittedToken),
      Buffer.from(expectedToken),
    );

  if (!validToken) {
    return res.status(403).render('error', {
      title: 'Request rejected - OPES EDGE',
      message:
        'This form is no longer valid. Please refresh the page and try again.',
    });
  }

  next();
}

module.exports = csrfProtection;
