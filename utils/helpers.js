const crypto = require('crypto');

function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.scryptSync(password, salt, 64).toString('hex');
  return `scrypt:${salt}:${hash}`;
}

function verifyPassword(password, storedPassword) {
  const [algorithm, salt, storedHash] = String(storedPassword).split(':');
  if (algorithm !== 'scrypt' || !salt || !storedHash) {
    return false;
  }

  const derivedHash = crypto.scryptSync(password, salt, 64).toString('hex');
  return crypto.timingSafeEqual(
    Buffer.from(derivedHash, 'hex'),
    Buffer.from(storedHash, 'hex'),
  );
}

function renderError(res, status, message) {
  return res.status(status).render('error', {
    title: `${status} - OPES EDGE`,
    message,
  });
}

module.exports = {
  hashPassword,
  verifyPassword,
  renderError,
};
