const db = require('../config/database');

function getTips(limit = 3) {
  return db
    .prepare(
      `
		SELECT id, title, content, category, created_at
		FROM agriculture_tips
		ORDER BY id DESC
		LIMIT ?
	`,
    )
    .all(limit);
}

function getCropGuides() {
  return db
    .prepare(
      `
		SELECT id, crop, season, soil, water_need, summary, actions
		FROM agriculture_crop_guides
		ORDER BY crop
	`,
    )
    .all();
}

function getCropOptions() {
  return db
    .prepare('SELECT DISTINCT crop FROM agriculture_crop_guides ORDER BY crop')
    .all()
    .map((row) => row.crop);
}

function getAdvice({ crop, season, soil }) {
  return db
    .prepare(
      `
		SELECT crop, season, soil, water_need, summary, actions
		FROM agriculture_crop_guides
		WHERE crop = ? AND season = ? AND soil = ?
	`,
    )
    .get(crop, season, soil);
}

function getMarketPrices() {
  return db
    .prepare(
      `
		SELECT crop, market, unit, price, price_date, source_note
		FROM agriculture_market_prices
		ORDER BY crop
	`,
    )
    .all();
}

module.exports = {
  getTips,
  getCropGuides,
  getCropOptions,
  getAdvice,
  getMarketPrices,
};
