function notFound(req, res) {
  if (req.originalUrl.startsWith('/api/')) {
    return res
      .status(404)
      .json({ status: 'error', message: 'Resource not found' });
  }

  res.status(404).render('error', {
    title: 'Page not found - OPES EDGE',
    message: 'The page you requested could not be found.',
  });
}

function errorHandler(err, req, res, next) {
  console.error(err.stack || err.message || err);
  if (res.headersSent) {
    return next(err);
  }

  if (req.originalUrl.startsWith('/api/')) {
    return res
      .status(500)
      .json({ status: 'error', message: 'Something went wrong on the server' });
  }

  res.status(500).render('error', {
    title: 'Server error - OPES EDGE',
    message: 'Something went wrong on the server.',
  });
}

module.exports = {
  notFound,
  errorHandler,
};
