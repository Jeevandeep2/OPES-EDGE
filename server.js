// ============================================
// OPES EDGE - Main Server File
// One Platform For Every Solution
// ============================================

// Step 1: Load environment variables from .env file
// This keeps secrets (passwords, keys) out of our code
require('dotenv').config(); // Database connection
// Step 2: Import required packages
const crypto = require('crypto');
const express = require('express');
const path = require('path');
const session = require('express-session');
require('./config/database');
const logger = require('./middleware/logger');
const csrfProtection = require('./middleware/csrfMiddleware');
const { attachCurrentUser } = require('./middleware/authMiddleware');
const { notFound, errorHandler } = require('./middleware/errorMiddleware');

const app = express();
const isProduction = process.env.NODE_ENV === 'production';
const port = Number(process.env.PORT) || 5000;
const sessionSecret =
  process.env.SESSION_SECRET ||
  (isProduction ? null : crypto.randomBytes(32).toString('hex'));

if (!sessionSecret) {
  throw new Error('SESSION_SECRET must be configured in production.');
}

app.disable('x-powered-by');
app.set('trust proxy', isProduction ? 1 : 0);
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.set('views', path.join(__dirname, 'views'));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.get('/favicon.ico', (req, res) =>
  res.sendFile(path.join(__dirname, 'public', 'favicon.svg')),
);
app.use(logger);
app.use(
  session({
    secret: sessionSecret,
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      sameSite: 'lax',
      secure: isProduction,
      maxAge: 24 * 60 * 60 * 1000,
    },
  }),
);
app.use(attachCurrentUser);
app.use(csrfProtection);

app.get('/', (req, res) => res.render('index', { title: 'OPES EDGE' }));
app.get('/about', (req, res) =>
  res.render('about', { title: 'About - OPES EDGE' }),
);
app.get('/help', (req, res) =>
  res.render('help', { title: 'Help - OPES EDGE' }),
);

app.get('/api/health', (req, res) => {
  res.json({
    status: 'success',
    message: 'OPES EDGE server is healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
  });
});

app.get('/api/db-status', (req, res) => {
  const db = require('./config/database');
  const users = db.prepare('SELECT COUNT(*) AS count FROM users').get();
  res.json({
    status: 'success',
    database: 'SQLite',
    users_count: users.count,
    message: 'Database is working',
  });
});

app.use('/', require('./routes/auth'));
app.use('/agriculture', require('./routes/agriculture'));
app.use('/education', require('./routes/education'));
app.use('/healthcare', require('./routes/healthcare'));
app.use('/community', require('./routes/community'));
app.use('/energy', require('./routes/energy'));
app.use('/water', require('./routes/water'));
app.use('/employment', require('./routes/employment'));
app.use('/governance', require('./routes/governance'));
app.use('/admin', require('./routes/admin'));
app.use('/dashboard', require('./routes/dashboard'));

app.use(notFound);
app.use(errorHandler);

if (require.main === module) {
  app.listen(port, () => {
    console.log(`OPES EDGE running at http://localhost:${port}`);
  });
}

module.exports = app;
