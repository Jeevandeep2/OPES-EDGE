const agricultureModel = require('../models/agricultureModel');

const baseView = {
  title: 'Agriculture Management - OPES EDGE',
  cropOptions: agricultureModel.getCropOptions(),
};

function showAgriculture(req, res) {
  res.render('agriculture/index', {
    ...baseView,
    tips: agricultureModel.getTips(),
    guides: agricultureModel.getCropGuides(),
  });
}

function showCropAdvisor(req, res) {
  res.render('agriculture/crop-advisor', {
    ...baseView,
    result: null,
    form: { crop: '', season: 'Kharif', soil: 'Loam' },
    error: null,
  });
}

function adviseCrop(req, res) {
  const form = {
    crop: String(req.body.crop || '').trim(),
    season: String(req.body.season || '').trim(),
    soil: String(req.body.soil || '').trim(),
  };
  const result = agricultureModel.getAdvice(form);

  res.render('agriculture/crop-advisor', {
    ...baseView,
    result: result || null,
    form,
    error: result
      ? null
      : 'We do not have a guide for that combination yet. Try another crop, season, or soil type.',
  });
}

function showWeather(req, res) {
  res.render('agriculture/weather', {
    ...baseView,
    planningRows: [
      {
        season: 'Kharif',
        timing: 'June - October',
        focus: 'Rain readiness',
        action:
          'Check drainage, bunds, seed storage, and a backup plan for heavy rainfall.',
      },
      {
        season: 'Rabi',
        timing: 'October - March',
        focus: 'Moisture timing',
        action:
          'Plan sowing after dependable moisture and track irrigation around early growth.',
      },
      {
        season: 'Summer',
        timing: 'March - June',
        focus: 'Heat protection',
        action:
          'Irrigate early, use mulch where possible, and watch plants for heat stress.',
      },
    ],
  });
}

function showMarketPrices(req, res) {
  res.render('agriculture/market-prices', {
    ...baseView,
    prices: agricultureModel.getMarketPrices(),
  });
}

module.exports = {
  showAgriculture,
  showCropAdvisor,
  adviseCrop,
  showWeather,
  showMarketPrices,
};
