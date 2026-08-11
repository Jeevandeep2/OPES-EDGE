const educationModel = require('../models/educationModel');

function showEducation(req, res) {
  res.render('education/index', {
    title: 'Education - OPES EDGE',
    categories: educationModel.getCategoryCounts(),
    featured: educationModel.getFeaturedResources(),
  });
}

function showResources(req, res) {
  res.render('education/resources', {
    title: 'Educational Resources - OPES EDGE',
    categories: educationModel.getCategories(),
    resources: educationModel.getResources(),
    aiResources: educationModel
      .getResources()
      .filter((resource) => resource.ai),
    initialCategory: req.query.category || '',
    initialSearch: req.query.q || '',
  });
}

function showCourses(req, res) {
  res.render('education/resources', {
    title: 'Online Learning - OPES EDGE',
    categories: educationModel.getCategories(),
    resources: educationModel.getResources(),
    aiResources: educationModel
      .getResources()
      .filter((resource) => resource.ai),
    initialCategory: 'online-learning',
    initialSearch: '',
  });
}

module.exports = { showEducation, showResources, showCourses };
