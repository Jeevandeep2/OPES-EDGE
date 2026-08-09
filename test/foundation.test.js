const test = require('node:test');
const assert = require('node:assert/strict');

const { hashPassword, verifyPassword } = require('../utils/helpers');
const { validateRegistration } = require('../utils/validators');
const agricultureModel = require('../models/agricultureModel');
const educationModel = require('../models/educationModel');

test('passwords can be verified without storing plaintext', () => {
  const storedPassword = hashPassword('student-password');

  assert.notEqual(storedPassword, 'student-password');
  assert.equal(verifyPassword('student-password', storedPassword), true);
  assert.equal(verifyPassword('wrong-password', storedPassword), false);
});

test('registration validation rejects invalid input', () => {
  const result = validateRegistration({
    fullName: 'A',
    email: 'invalid',
    password: 'short',
    role: 'administrator',
  });

  assert.equal(result.errors.length, 4);
});

test('agriculture provides seeded guidance and explicit market references', () => {
  assert.deepEqual(agricultureModel.getCropOptions(), [
    'Millet',
    'Rice',
    'Tomato',
    'Wheat',
  ]);
  assert.match(
    agricultureModel.getAdvice({ crop: 'Rice', season: 'Kharif', soil: 'Clay' })
      .actions,
    /bunds/,
  );
  assert.equal(
    agricultureModel.getAdvice({ crop: 'Rice', season: 'Rabi', soil: 'Sandy' }),
    undefined,
  );
  assert.equal(agricultureModel.getTips().length >= 3, true);
  assert.equal(
    agricultureModel
      .getMarketPrices()
      .every((price) => price.price === 'Update locally'),
    true,
  );
});

test('education catalog covers learning goals and uses official links', () => {
  const resources = educationModel.getResources();
  const categorySlugs = educationModel
    .getCategories()
    .map((category) => category.slug);

  assert.equal(resources.length >= 45, true);
  assert.deepEqual(categorySlugs, [
    'online-learning',
    'books',
    'institutional',
    'research',
    'video',
    'languages',
    'coding',
    'exams',
    'ai-tools',
  ]);
  assert.equal(
    resources.every((resource) => resource.url.startsWith('https://')),
    true,
  );
  assert.equal(resources.filter((resource) => resource.ai).length >= 10, true);
  assert.equal(
    resources.every((resource) =>
      ['Completely Free', 'Limited Free', 'Free + Paid', 'Paid'].includes(
        resource.access,
      ),
    ),
    true,
  );
});
