function showDashboard(req, res) {
  res.render('dashboard', {
    title: 'Dashboard - OPES EDGE',
    user: req.user,
  });
}

module.exports = {
  showDashboard,
};
