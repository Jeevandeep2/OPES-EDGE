function validateRegistration({ fullName, email, password, role, phone }) {
  const errors = [];
  const normalizedEmail = String(email || '')
    .trim()
    .toLowerCase();
  const normalizedRole = String(role || 'citizen')
    .trim()
    .toLowerCase();

  if (String(fullName || '').trim().length < 2) {
    errors.push('Full name must contain at least 2 characters.');
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizedEmail)) {
    errors.push('Enter a valid email address.');
  }
  if (String(password || '').length < 8) {
    errors.push('Password must contain at least 8 characters.');
  }
  if (!['citizen', 'farmer', 'student', 'patient'].includes(normalizedRole)) {
    errors.push('Select a valid account role.');
  }
  if (phone && !/^[0-9+()\-\s]{7,20}$/.test(String(phone))) {
    errors.push('Enter a valid phone number.');
  }

  return {
    errors,
    values: {
      fullName: String(fullName || '').trim(),
      email: normalizedEmail,
      role: normalizedRole,
      phone: String(phone || '').trim(),
    },
  };
}

module.exports = {
  validateRegistration,
};
