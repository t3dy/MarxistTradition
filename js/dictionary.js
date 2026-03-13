(async function () {
  const [thinkers, texts, terms] = await Promise.all([
    fetch('data/thinkers.json').then(r => r.json()),
    fetch('data/texts.json').then(r => r.json()),
    fetch('data/terms.json').then(r => r.json()),
  ]);

  const data = { thinkers, texts, terms };
  let activeTab = 'thinkers';
  let searchQuery = '';
  let activeTradition = '';
  let expandedSlug = null;

  const searchEl = document.getElementById('search');
  const tabsEl = document.getElementById('tabs');
  const resultsEl = document.getElementById('results');
  const filtersEl = document.getElementById('tradition-filters');

  // Collect all traditions
  const traditions = new Set();
  thinkers.forEach(t => t.tradition && traditions.add(t.tradition));
  texts.forEach(t => t.tradition && traditions.add(t.tradition));

  function renderFilters() {
    filtersEl.innerHTML = '';
    const allChip = document.createElement('span');
    allChip.className = 'chip' + (activeTradition === '' ? ' active' : '');
    allChip.textContent = 'All';
    allChip.onclick = () => { activeTradition = ''; render(); };
    filtersEl.appendChild(allChip);

    for (const t of [...traditions].sort()) {
      const chip = document.createElement('span');
      chip.className = 'chip' + (activeTradition === t ? ' active' : '');
      chip.textContent = t;
      chip.onclick = () => { activeTradition = activeTradition === t ? '' : t; render(); };
      filtersEl.appendChild(chip);
    }
  }

  const TRADITION_LABELS = {
    classical: 'Classical Marxism',
    'value-form': 'Value-Form Theory',
    harvey: 'Harvey / Geographical Materialism',
    structuralist: 'Structuralist Marxism',
  };

  function renderTraditionPanels(traditions) {
    if (!traditions) return '';
    let html = '<div class="tradition-panels">';
    for (const [key, text] of Object.entries(traditions)) {
      const cssClass = key === 'value-form' ? 'value-form' : key;
      const label = TRADITION_LABELS[key] || key;
      html += `
        <div class="tradition-panel ${cssClass}">
          <div class="tradition-label">${label}</div>
          <div>${text}</div>
        </div>`;
    }
    html += '</div>';
    return html;
  }

  function getDisplayName(item) {
    return item.name || item.title || item.term || item.slug;
  }

  function getMeta(item) {
    if (activeTab === 'thinkers') {
      const dates = item.died ? `${item.born}\u2013${item.died}` : `b. ${item.born}`;
      return `${dates} \u00B7 ${item.nationality || ''} \u00B7 ${item.tradition || ''}`;
    }
    if (activeTab === 'texts') {
      return `${item.author || ''} \u00B7 ${item.year || ''} \u00B7 ${item.tradition || ''}`;
    }
    if (activeTab === 'terms') {
      const src = item.source || '';
      const german = item.german ? `(${item.german})` : '';
      return `${german} ${src}`.trim();
    }
    return '';
  }

  function matchesSearch(item) {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    const name = getDisplayName(item).toLowerCase();
    const tags = (item.tags || []).join(' ').toLowerCase();
    const body = (item.body || '').toLowerCase();
    const tradition = (item.tradition || '').toLowerCase();
    return name.includes(q) || tags.includes(q) || body.includes(q) || tradition.includes(q);
  }

  function matchesTradition(item) {
    if (!activeTradition) return true;
    return (item.tradition || '') === activeTradition;
  }

  function render() {
    renderFilters();

    // Update tabs
    tabsEl.querySelectorAll('.tab').forEach(tab => {
      tab.classList.toggle('active', tab.dataset.tab === activeTab);
    });

    const items = (data[activeTab] || []).filter(
      item => matchesSearch(item) && matchesTradition(item)
    );

    resultsEl.innerHTML = '';

    if (items.length === 0) {
      resultsEl.innerHTML = '<p style="color: var(--color-text-muted); grid-column: 1/-1;">No results found.</p>';
      return;
    }

    for (const item of items) {
      const card = document.createElement('div');
      card.className = 'card' + (expandedSlug === item.slug ? ' expanded' : '');

      const tagsHtml = (item.tags || [])
        .map(t => `<span class="tag" data-tag="${t}">${t}</span>`)
        .join('');

      const tradBadge = item.tradition
        ? `<span class="tradition-badge">${item.tradition}</span>`
        : '';

      // Strip HTML tags for preview text
      const plainText = (item.body || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();

      card.innerHTML = `
        <h3>${getDisplayName(item)}</h3>
        <div class="meta">${getMeta(item)}</div>
        ${tradBadge}
        <div class="body-preview">${plainText}</div>
        <div class="tags">${tagsHtml}</div>
        <div class="body-full">
          ${item.body || ''}
          ${renderTraditionPanels(item.traditions)}
        </div>
      `;

      card.addEventListener('click', (e) => {
        if (e.target.classList.contains('tag')) {
          searchQuery = e.target.dataset.tag;
          searchEl.value = searchQuery;
          render();
          return;
        }
        expandedSlug = expandedSlug === item.slug ? null : item.slug;
        render();
      });

      resultsEl.appendChild(card);
    }
  }

  // Event listeners
  tabsEl.addEventListener('click', (e) => {
    if (e.target.classList.contains('tab')) {
      activeTab = e.target.dataset.tab;
      expandedSlug = null;
      render();
    }
  });

  searchEl.addEventListener('input', (e) => {
    searchQuery = e.target.value.trim();
    render();
  });

  render();
})();
