const Database = require('better-sqlite3');
const path = require('path');

// Database file will be created automatically in project root
const dbPath = path.join(__dirname, '..', 'opes_edge.db');

const db = new Database(dbPath);

db.pragma('foreign_keys = ON');

db.exec(`
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL COLLATE NOCASE,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'citizen',
        phone TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS agriculture_tips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS agriculture_crop_guides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        season TEXT NOT NULL,
        soil TEXT NOT NULL,
        water_need TEXT NOT NULL,
        summary TEXT NOT NULL,
        actions TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS agriculture_market_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        market TEXT NOT NULL,
        unit TEXT NOT NULL,
        price TEXT NOT NULL,
        price_date TEXT NOT NULL,
        source_note TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    CREATE INDEX IF NOT EXISTS idx_agriculture_tips_category ON agriculture_tips(category);
        CREATE INDEX IF NOT EXISTS idx_crop_guides_lookup ON agriculture_crop_guides(crop, season, soil);
        CREATE INDEX IF NOT EXISTS idx_market_prices_crop ON agriculture_market_prices(crop);
`);

const tipCount = db
  .prepare('SELECT COUNT(*) AS count FROM agriculture_tips')
  .get();
if (tipCount.count === 0) {
  db.prepare(
    `
        INSERT INTO agriculture_tips (title, content, category)
        VALUES (@title, @content, @category)
    `,
  ).run({
    title: 'Start with the soil',
    content:
      'Check moisture and drainage before changing your watering routine. Small observations early can prevent bigger crop stress later.',
    category: 'Soil health',
  });
  db.prepare(
    `
        INSERT INTO agriculture_tips (title, content, category)
        VALUES (@title, @content, @category)
    `,
  ).run({
    title: 'Keep a simple field record',
    content:
      'Note sowing dates, irrigation, pest observations, and harvest results. A small record makes the next season easier to plan.',
    category: 'Farm planning',
  });
  db.prepare(
    `
        INSERT INTO agriculture_tips (title, content, category)
        VALUES (@title, @content, @category)
    `,
  ).run({
    title: 'Inspect before treating',
    content:
      'Look across several plants before acting on a pest concern. Identify the pattern and seek local agricultural guidance when unsure.',
    category: 'Crop care',
  });
}

const guideCount = db
  .prepare('SELECT COUNT(*) AS count FROM agriculture_crop_guides')
  .get();
if (guideCount.count === 0) {
  const insertGuide = db.prepare(`
        INSERT INTO agriculture_crop_guides (crop, season, soil, water_need, summary, actions)
        VALUES (@crop, @season, @soil, @waterNeed, @summary, @actions)
    `);
  const seedGuides = db.transaction((guides) =>
    guides.forEach((guide) => insertGuide.run(guide)),
  );
  seedGuides([
    {
      crop: 'Rice',
      season: 'Kharif',
      soil: 'Clay',
      waterNeed: 'High',
      summary:
        'Rice prefers steady moisture and good field leveling. Watch standing water and drainage after heavy rain.',
      actions:
        'Level the plot where possible; check bunds; split nitrogen applications; inspect for leaf discoloration.',
    },
    {
      crop: 'Wheat',
      season: 'Rabi',
      soil: 'Loam',
      waterNeed: 'Medium',
      summary:
        'Wheat performs well in fertile, well-drained soil with timely irrigation during establishment and grain filling.',
      actions:
        'Prepare a fine seedbed; irrigate at crown-root initiation; monitor weeds early; plan harvest around dry weather.',
    },
    {
      crop: 'Tomato',
      season: 'All season',
      soil: 'Loam',
      waterNeed: 'Medium',
      summary:
        'Tomato needs consistent moisture, airflow, and support. Avoid wetting leaves late in the day.',
      actions:
        'Use stakes or trellis; mulch around plants; remove damaged leaves; check undersides for pests twice a week.',
    },
    {
      crop: 'Millet',
      season: 'Kharif',
      soil: 'Sandy',
      waterNeed: 'Low',
      summary:
        'Millet is comparatively resilient in lighter soils and lower rainfall, but early weed control is important.',
      actions:
        'Sow with the first reliable moisture; keep rows weed-free early; avoid waterlogging; save seed from healthy plants.',
    },
  ]);
}

const priceCount = db
  .prepare('SELECT COUNT(*) AS count FROM agriculture_market_prices')
  .get();
if (priceCount.count === 0) {
  const insertPrice = db.prepare(`
        INSERT INTO agriculture_market_prices (crop, market, unit, price, price_date, source_note)
        VALUES (@crop, @market, @unit, @price, @priceDate, @sourceNote)
    `);
  const seedPrices = db.transaction((prices) =>
    prices.forEach((price) => insertPrice.run(price)),
  );
  seedPrices([
    {
      crop: 'Rice',
      market: 'Planning reference',
      unit: 'per quintal',
      price: 'Update locally',
      priceDate: 'Reference only',
      sourceNote:
        'This app does not connect to a live mandi feed. Confirm current prices locally before selling.',
    },
    {
      crop: 'Wheat',
      market: 'Planning reference',
      unit: 'per quintal',
      price: 'Update locally',
      priceDate: 'Reference only',
      sourceNote:
        'This app does not connect to a live mandi feed. Confirm current prices locally before selling.',
    },
    {
      crop: 'Tomato',
      market: 'Planning reference',
      unit: 'per crate',
      price: 'Update locally',
      priceDate: 'Reference only',
      sourceNote:
        'This app does not connect to a live mandi feed. Confirm current prices locally before selling.',
    },
    {
      crop: 'Millet',
      market: 'Planning reference',
      unit: 'per quintal',
      price: 'Update locally',
      priceDate: 'Reference only',
      sourceNote:
        'This app does not connect to a live mandi feed. Confirm current prices locally before selling.',
    },
  ]);
}

module.exports = db;
