function renderDomain(res, domain) {
  res.render('domain', {
    title: `${domain.name} - OPES EDGE`,
    domain,
  });
}

module.exports = {
  renderDomain,
};
