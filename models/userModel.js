const db = require('../config/database');

function findByEmail(email) {
  return db
    .prepare(
      'SELECT id, full_name, email, password, role, phone, created_at FROM users WHERE email = ?',
    )
    .get(email);
}

function findById(id) {
  return db
    .prepare(
      'SELECT id, full_name, email, role, phone, created_at FROM users WHERE id = ?',
    )
    .get(id);
}

function createUser({
  fullName,
  email,
  password,
  role = 'citizen',
  phone = null,
}) {
  const result = db
    .prepare(
      `
		INSERT INTO users (full_name, email, password, role, phone)
		VALUES (?, ?, ?, ?, ?)
	`,
    )
    .run(fullName, email, password, role, phone);

  return findById(result.lastInsertRowid);
}

module.exports = {
  findByEmail,
  findById,
  createUser,
};
