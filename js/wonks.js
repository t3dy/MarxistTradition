(async function () {
  const [wonks, thinkers, terms] = await Promise.all([
    fetch('data/wonks.json').then(r => r.json()),
    fetch('data/thinkers.json').then(r => r.json()),
    fetch('data/terms.json').then(r => r.json()),
  ]);

  let searchQuery = '';
  let activeTag = '';
  let expandedSlug = null;

  const searchEl = document.getElementById('search');
  const resultsEl = document.getElementById('results');
  const filtersEl = document.getElementById('tag-filters');

  const allTags = new Set();
  wonks.forEach(a => (a.tags || []).forEach(t => allTags.add(t)));

  const TRADITION_LABELS = {
    classical: 'Classical Marxism',
    'value-form': 'Value-Form Theory',
    harvey: 'Harvey / Geographical Materialism',
    structuralist: 'Structuralist Marxism',
  };

  function renderFilters() {
    filtersEl.innerHTML = '';
    const allChip = document.createElement('span');
    allChip.className = 'chip' + (activeTag === '' ? ' active' : '');
    allChip.textContent = 'All';
    allChip.onclick = () => { activeTag = ''; render(); };
    filtersEl.appendChild(allChip);

    for (const t of [...allTags].sort()) {
      const chip = document.createElement('span');
      chip.className = 'chip' + (activeTag === t ? ' active' : '');
      chip.textContent = t;
      chip.onclick = () => { activeTag = activeTag === t ? '' : t; render(); };
      filtersEl.appendChild(chip);
    }
  }

  function matchesSearch(a) {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      (a.title || '').toLowerCase().includes(q) ||
      (a.policy_area || '').toLowerCase().includes(q) ||
      (a.tags || []).join(' ').toLowerCase().includes(q) ||
      (a.body || '').toLowerCase().includes(q)
    );
  }

  function matchesTag(a) {
    if (!activeTag) return true;
    return (a.tags || []).includes(activeTag);
  }

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

  function renderCrossLinks(a) {
    const parts = [];
    if (a.related_terms && a.related_terms.length) {
      const links = a.related_terms.map(slug => {
        const t = terms.find(x => x.slug === slug);
        return t ? `<a href="dictionary.html">${t.term}</a>` : slug;
      }).join(' ');
      parts.push(`<strong style="font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--color-text-muted);">Related terms:</strong> ${links}`);
    }
    if (a.related_thinkers && a.related_thinkers.length) {
      const links = a.related_thinkers.map(slug => {
        const t = thinkers.find(x => x.slug === slug);
        return t ? `<a href="whos-who.html">${t.name}</a>` : slug;
      }).join(' ');
      parts.push(`<strong style="font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--color-text-muted);">Related thinkers:</strong> ${links}`);
    }
    if (!parts.length) return '';
    return `<div class="analysis-links">${parts.join('<br>')}</div>`;
  }

  function render() {
    renderFilters();
    const filtered = wonks.filter(a => matchesSearch(a) && matchesTag(a));
    resultsEl.innerHTML = '';

    if (filtered.length === 0) {
      resultsEl.innerHTML = '<p style="color: var(--color-text-muted); grid-column: 1/-1;">No entries found.</p>';
      return;
    }

    for (const a of filtered) {
      const card = document.createElement('div');
      card.className = 'card' + (expandedSlug === a.slug ? ' expanded' : '');

      const tagsHtml = (a.tags || [])
        .map(t => `<span class="tag" data-tag="${t}">${t}</span>`)
        .join('');

      const isExpanded = expandedSlug === a.slug;
      const plainText = (a.body || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();

      card.innerHTML = `
        <h3>${a.title || a.slug}</h3>
        <div class="meta">
          ${a.policy_area ? `<span class="region-badge">${a.policy_area}</span>` : ''}
        </div>
        <div class="body-preview">${plainText}</div>
        <div class="tags">${tagsHtml}</div>
        <div class="body-full" ${isExpanded ? 'style="display:block;"' : ''}>
          ${a.body || ''}
          ${renderTraditionPanels(a.traditions)}
          ${renderCrossLinks(a)}
        </div>
      `;

      card.addEventListener('click', (e) => {
        if (e.target.classList.contains('tag')) {
          activeTag = e.target.dataset.tag;
          render();
          return;
        }
        if (e.target.tagName === 'A') return;
        expandedSlug = expandedSlug === a.slug ? null : a.slug;
        render();
      });

      resultsEl.appendChild(card);
    }
  }

  searchEl.addEventListener('input', (e) => {
    searchQuery = e.target.value.trim();
    render();
  });

  render();
})();
