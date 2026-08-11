(() => {
  const page = document.querySelector('.resources-page');
  if (!page) return;

  const searchInput = document.querySelector('#resource-search');
  const categoryFilter = document.querySelector('#category-filter');
  const accessFilter = document.querySelector('#access-filter');
  const sortSelect = document.querySelector('#sort-resources');
  const grid = document.querySelector('[data-resource-grid]');
  const cards = [
    ...document.querySelectorAll(
      '[data-resource-grid]:not(.education-ai-section__grid) [data-resource-card]',
    ),
  ];
  const emptyState = document.querySelector('[data-empty-state]');
  const resultCount = document.querySelector('[data-result-count]');
  const savedCount = document.querySelector('[data-saved-count]');
  const savedSection = document.querySelector('[data-saved-section]');
  const savedGrid = document.querySelector('[data-saved-grid]');
  const noSaved = document.querySelector('[data-no-saved]');
  const recentSection = document.querySelector('[data-recent-section]');
  const recentList = document.querySelector('[data-recent-list]');
  const directorySection = document
    .querySelector('[data-resource-grid]')
    ?.closest('section');
  const aiSection = document.querySelector('.education-ai-section');
  const savedKey = 'opes-edge-saved-resources';
  const recentKey = 'opes-edge-recent-resources';
  const themeKey = 'opes-edge-theme';

  const readList = (key) => {
    try {
      const value = JSON.parse(localStorage.getItem(key) || '[]');
      return Array.isArray(value) ? value : [];
    } catch (error) {
      return [];
    }
  };

  const writeList = (key, value) =>
    localStorage.setItem(key, JSON.stringify(value));
  const saved = () => readList(savedKey);
  const resourceByName = (name) =>
    cards.find((card) => card.dataset.name === name);

  function updateFavoriteButtons() {
    const savedNames = new Set(saved());
    document.querySelectorAll('[data-favorite]').forEach((button) => {
      const isSaved = savedNames.has(button.dataset.favorite);
      button.setAttribute('aria-pressed', String(isSaved));
      button.setAttribute(
        'aria-label',
        `${isSaved ? 'Remove' : 'Save'} ${button.dataset.favorite}`,
      );
      button.innerHTML = `<i class="bi ${isSaved ? 'bi-bookmark-fill' : 'bi-bookmark'}" aria-hidden="true"></i>`;
      button.classList.toggle('is-saved', isSaved);
    });
    if (savedCount) savedCount.textContent = savedNames.size;
  }

  function toggleFavorite(name) {
    const names = saved();
    const next = names.includes(name)
      ? names.filter((item) => item !== name)
      : [name, ...names];
    writeList(savedKey, next.slice(0, 50));
    updateFavoriteButtons();
    if (!savedSection.classList.contains('d-none')) renderSaved();
  }

  function renderSaved() {
    const names = saved();
    savedGrid.innerHTML = '';
    const uniqueCards = [];
    names.forEach((name) => {
      const card = resourceByName(name);
      if (card && !uniqueCards.some((item) => item.dataset.name === name))
        uniqueCards.push(card);
    });
    uniqueCards.forEach((card) => savedGrid.appendChild(card.cloneNode(true)));
    noSaved.classList.toggle('d-none', uniqueCards.length > 0);
    savedGrid.classList.toggle('d-none', uniqueCards.length === 0);
    updateFavoriteButtons();
  }

  function renderRecent() {
    const names = readList(recentKey).filter((name) => resourceByName(name));
    if (!names.length) {
      recentSection.classList.add('d-none');
      return;
    }
    recentSection.classList.remove('d-none');
    recentList.innerHTML = names
      .map((name) => {
        const card = resourceByName(name);
        return `<a class="recent-resource" href="${card.querySelector('.resource-visit').href}" target="_blank" rel="noopener noreferrer"><span class="resource-logo resource-logo--tiny">${card.querySelector('.resource-logo').textContent}</span><span><strong>${name}</strong><small>${card.querySelector('.resource-best').textContent}</small></span><i class="bi bi-arrow-up-right" aria-hidden="true"></i></a>`;
      })
      .join('');
  }

  function trackRecent(name) {
    const next = [
      name,
      ...readList(recentKey).filter((item) => item !== name),
    ].slice(0, 5);
    writeList(recentKey, next);
    renderRecent();
  }

  function sortCards(cardList) {
    const sort = sortSelect.value;
    return [...cardList].sort((first, second) => {
      if (sort === 'featured')
        return first.dataset.name.localeCompare(second.dataset.name);
      if (sort === 'name')
        return first.dataset.name.localeCompare(second.dataset.name);
      if (sort === 'access')
        return (
          first.dataset.access.localeCompare(second.dataset.access) ||
          first.dataset.name.localeCompare(second.dataset.name)
        );
      return (
        first.dataset.category.localeCompare(second.dataset.category) ||
        first.dataset.name.localeCompare(second.dataset.name)
      );
    });
  }

  function applyFilters() {
    const query = searchInput.value.trim().toLowerCase();
    const category = categoryFilter.value;
    const access = accessFilter.value;
    const matches = cards.filter((card) => {
      const searchMatch =
        !query || card.dataset.search.toLowerCase().includes(query);
      return (
        searchMatch &&
        (!category || card.dataset.category === category) &&
        (!access || card.dataset.access === access)
      );
    });
    sortCards(cards).forEach((card) => grid.appendChild(card));
    cards.forEach((card) =>
      card.classList.toggle('d-none', !matches.includes(card)),
    );
    emptyState.classList.toggle('d-none', matches.length > 0);
    resultCount.textContent = `${matches.length} resource${matches.length === 1 ? '' : 's'} shown`;
    document
      .querySelectorAll('[data-category-pill]')
      .forEach((pill) =>
        pill.classList.toggle('active', pill.dataset.categoryPill === category),
      );
  }

  function showSavedResources() {
    directorySection.classList.add('d-none');
    aiSection.classList.add('d-none');
    recentSection.classList.add('d-none');
    savedSection.classList.remove('d-none');
    renderSaved();
    savedSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function showDirectory() {
    directorySection.classList.remove('d-none');
    aiSection.classList.remove('d-none');
    savedSection.classList.add('d-none');
    recentSection.classList.toggle('d-none', readList(recentKey).length === 0);
  }

  document.addEventListener('click', (event) => {
    const favoriteButton = event.target.closest('[data-favorite]');
    if (favoriteButton) toggleFavorite(favoriteButton.dataset.favorite);
    const resourceLink = event.target.closest('[data-resource-link]');
    if (resourceLink) trackRecent(resourceLink.dataset.resourceLink);
    const categoryPill = event.target.closest('[data-category-pill]');
    if (categoryPill) {
      categoryFilter.value = categoryPill.dataset.categoryPill;
      applyFilters();
    }
  });

  searchInput.addEventListener('input', applyFilters);
  categoryFilter.addEventListener('change', applyFilters);
  accessFilter.addEventListener('change', applyFilters);
  sortSelect.addEventListener('change', applyFilters);
  document
    .querySelector('[data-clear-search]')
    .addEventListener('click', () => {
      searchInput.value = '';
      applyFilters();
      searchInput.focus();
    });
  document
    .querySelector('[data-reset-filters]')
    .addEventListener('click', () => {
      searchInput.value = '';
      categoryFilter.value = '';
      accessFilter.value = '';
      sortSelect.value = 'featured';
      applyFilters();
    });
  document
    .querySelector('[data-show-saved]')
    .addEventListener('click', showSavedResources);
  document
    .querySelector('[data-close-saved]')
    .addEventListener('click', showDirectory);

  const themeButton = document.querySelector('[data-theme-toggle]');
  const storedTheme = localStorage.getItem(themeKey);
  if (storedTheme === 'dark') document.documentElement.dataset.theme = 'dark';
  themeButton.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    localStorage.setItem(themeKey, dark ? 'dark' : 'light');
    themeButton.innerHTML = `<i class="bi ${dark ? 'bi-sun' : 'bi-moon-stars'} me-2" aria-hidden="true"></i>${dark ? 'Light mode' : 'Dark mode'}`;
  });

  const initialCategory = page.dataset.initialCategory;
  const initialSearch = page.dataset.initialSearch;
  if (initialCategory) categoryFilter.value = initialCategory;
  if (initialSearch) searchInput.value = initialSearch;
  updateFavoriteButtons();
  applyFilters();
  renderRecent();
})();
