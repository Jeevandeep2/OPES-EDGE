const userModel = require('../models/userModel');
const { hashPassword, verifyPassword } = require('../utils/helpers');
const { validateRegistration } = require('../utils/validators');

function showLogin(req, res) {
  res.render('auth/login', {
    title: 'Login - OPES EDGE',
    errors: [],
    values: { email: '' },
    next: req.query.next || '',
  });
}

function showRegister(req, res) {
  res.render('auth/register', {
    title: 'Register - OPES EDGE',
    errors: [],
    values: { fullName: '', email: '', role: 'citizen', phone: '' },
  });
}

function register(req, res) {
  const { errors, values } = validateRegistration(req.body);
  if (errors.length) {
    return res.status(400).render('auth/register', {
      title: 'Register - OPES EDGE',
      errors,
      values,
    });
  }

  if (userModel.findByEmail(values.email)) {
    return res.status(409).render('auth/register', {
      title: 'Register - OPES EDGE',
      errors: ['An account with that email already exists.'],
      values,
    });
  }

  const user = userModel.createUser({
    ...values,
    password: hashPassword(req.body.password),
  });
  req.session.regenerate((error) => {
    if (error) {
      return res.status(500).render('error', {
        title: 'Server error - OPES EDGE',
        message: 'Unable to create a secure session.',
      });
    }

    req.session.user = {
      id: user.id,
      fullName: user.full_name,
      email: user.email,
      role: user.role,
    };
    res.redirect('/dashboard');
  });
}

function login(req, res) {
  const email = String(req.body.email || '')
    .trim()
    .toLowerCase();
  const password = String(req.body.password || '');
  const user = userModel.findByEmail(email);

  if (!user || !verifyPassword(password, user.password)) {
    return res.status(401).render('auth/login', {
      title: 'Login - OPES EDGE',
      errors: ['Email or password is incorrect.'],
      values: { email },
      next: req.body.next || '',
    });
  }

  req.session.regenerate((error) => {
    if (error) {
      return res.status(500).render('error', {
        title: 'Server error - OPES EDGE',
        message: 'Unable to create a secure session.',
      });
    }

    req.session.user = {
      id: user.id,
      fullName: user.full_name,
      email: user.email,
      role: user.role,
    };
    const nextPath =
      typeof req.body.next === 'string' && req.body.next.startsWith('/')
        ? req.body.next
        : '/dashboard';
    res.redirect(nextPath);
  });
}

function logout(req, res) {
  req.session.destroy(() => res.redirect('/'));
}

module.exports = {
  showLogin,
  showRegister,
  register,
  login,
  logout,
};
