(async function () {
  const thinkers = await fetch('data/thinkers.json').then(r => r.json());

  let searchQuery = '';
  let activeTradition = '';
  let expandedSlug = null;

  const searchEl = document.getElementById('search');
  const timelineEl = document.getElementById('timeline');
  const filtersEl = document.getElementById('tradition-filters');

  const traditions = new Set();
  thinkers.forEach(t => t.tradition && traditions.add(t.tradition));

  // Sort by birth year
  const sorted = [...thinkers].sort((a, b) => (a.born || 0) - (b.born || 0));

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

  function matchesSearch(t) {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      (t.name || '').toLowerCase().includes(q) ||
      (t.tradition || '').toLowerCase().includes(q) ||
      (t.tags || []).join(' ').toLowerCase().includes(q) ||
      (t.body || '').toLowerCase().includes(q) ||
      (t.key_works || []).join(' ').toLowerCase().includes(q)
    );
  }

  function matchesTradition(t) {
    if (!activeTradition) return true;
    return t.tradition === activeTradition;
  }

  function render() {
    renderFilters();

    const filtered = sorted.filter(t => matchesSearch(t) && matchesTradition(t));

    timelineEl.innerHTML = '';

    if (filtered.length === 0) {
      timelineEl.innerHTML = '<p style="color: var(--color-text-muted);">No thinkers found.</p>';
      return;
    }

    for (const t of filtered) {
      const dates = t.died ? `${t.born}\u2013${t.died}` : `b. ${t.born}`;
      const worksHtml = (t.key_works || []).map(w => `<em>${w}</em>`).join(', ');
      const tagsHtml = (t.tags || [])
        .map(tag => `<span class="tag">${tag}</span>`)
        .join('');
      const isExpanded = expandedSlug === t.slug;

      const item = document.createElement('div');
      item.className = 'timeline-item';
      item.style.cursor = 'pointer';

      item.innerHTML = `
        <h3 style="font-family: var(--font-serif); font-size: 1.25rem;">${t.name}</h3>
        <div class="meta">${dates} \u00B7 ${t.nationality || ''}</div>
        <span class="tradition-badge">${t.tradition || ''}</span>
        ${worksHtml ? `<div style="margin-top: 0.5rem; font-size: 0.9rem; color: var(--color-text-muted);">Key works: ${worksHtml}</div>` : ''}
        <div class="tags">${tagsHtml}</div>
        ${isExpanded ? `<div style="margin-top: 1rem; font-size: 0.92rem; line-height: 1.6; border-top: 1px dashed var(--color-border); padding-top: 0.75rem;">${t.body || ''}</div>` : ''}
      `;

      item.addEventListener('click', () => {
        expandedSlug = expandedSlug === t.slug ? null : t.slug;
        render();
      });

      timelineEl.appendChild(item);
    }
  }

  searchEl.addEventListener('input', (e) => {
    searchQuery = e.target.value.trim();
    render();
  });

  render();
})();
