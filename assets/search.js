(() => {
  'use strict';

  const state = {
    all: [],
    byId: new Map(),
    results: [],
    engine: null,
    category: 'all',
    origin: 'all',
    concept: 'all',
    query: '',
    visible: 30,
    concepts: []
  };

  const categoryKeys = {
    'Reverse Engineering': 'rev',
    'Machine Exploitation': 'machine',
    'Web Exploitation': 'web',
    'PWN / Binary Exploit': 'pwn',
    'Steganography': 'steg',
    'Cryptography': 'crypto',
    'OSINT': 'osint',
    'Forensics': 'forensics',
    'General': 'general'
  };

  const originClasses = {
    TryHackMe: 'origin-thm', HackMyVM: 'origin-hmv', picoCTF: 'origin-pico',
    'crackmes.one': 'origin-crackme', HackTheBox: 'origin-htb', Vulnyx: 'origin-vulnyx',
    'Proving Grounds': 'origin-pg', PwnTillDawn: 'origin-ptd', 'Sec-Fortress': 'origin-secfortress',
    ruycr4ft: 'origin-ruycr4ft', Other: 'origin-other'
  };

  const dom = {
    input: document.getElementById('writeups-search'),
    clear: document.getElementById('search-clear'),
    count: document.getElementById('search-count'),
    stats: document.getElementById('search-stats'),
    cards: document.getElementById('writeups-container'),
    moreWrap: document.getElementById('load-more-wrap'),
    more: document.getElementById('load-more-btn'),
    concepts: document.getElementById('concept-tags-container')
  };

  const escapeHtml = value => String(value || '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

  const cleanTitle = value => String(value || '').replace(/\*\*/g, '').replace(/\|\|/g, '').replace(/::.*/, '').trim();
  const categoryKey = item => categoryKeys[item.category] || 'general';
  const hasConcept = (item, concept) => concept === 'all' || (item.tags || []).includes(concept);
  const matchesCategory = (item, category) => category === 'all' || categoryKey(item) === category;
  const matchesOrigin = (item, origin) => origin === 'all' || (item.origin || 'Other') === origin;

  function regexTerms(terms) {
    return [...new Set(terms.filter(Boolean).map(String))]
      .sort((a, b) => b.length - a.length)
      .map(term => term.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&'));
  }

  function highlight(value, terms) {
    const safe = escapeHtml(value);
    const patterns = regexTerms(terms);
    if (!patterns.length) return safe;
    try {
      return safe.replace(new RegExp(`(${patterns.join('|')})`, 'gi'), '<mark>$1</mark>');
    } catch (_) {
      return safe;
    }
  }

  function matchedTerms(result) {
    const queryTerms = state.query.toLowerCase().split(/\s+/).filter(Boolean);
    return [...new Set([...queryTerms, ...Object.keys(result?.match || {})])];
  }

  function contextualSnippet(item, terms) {
    const source = item.body || item.snippet || '';
    const lower = source.toLowerCase();
    let at = -1;
    for (const term of terms) {
      at = lower.indexOf(term.toLowerCase());
      if (at >= 0) break;
    }
    if (at < 0) return item.snippet || source.slice(0, 220);
    const start = Math.max(0, at - 85);
    const end = Math.min(source.length, at + 140);
    return `${start ? '... ' : ''}${source.slice(start, end).trim()}${end < source.length ? ' ...' : ''}`;
  }

  function baseSearchResults() {
    if (!state.query) return state.all.map(item => ({ item, match: {}, score: 0 }));
    let hits = state.engine.search(state.query, { fuzzy: false });
    if (!hits.length) {
      hits = state.engine.search(state.query, {
        fuzzy: term => term.length >= 4 ? 0.2 : false,
        maxFuzzy: 1,
        weights: { prefix: 0.8, fuzzy: 0.55 }
      });
    }
    return hits.map(hit => ({ item: state.byId.get(hit.id), match: hit.match, score: hit.score }));
  }

  function filtered(base, { ignoreCategory = false, ignoreOrigin = false, ignoreConcept = false } = {}) {
    return base.filter(result => {
      const item = result.item;
      return item &&
        (ignoreCategory || matchesCategory(item, state.category)) &&
        (ignoreOrigin || matchesOrigin(item, state.origin)) &&
        (ignoreConcept || hasConcept(item, state.concept));
    });
  }

  function countBy(items, selector) {
    const counts = { all: items.length };
    items.forEach(result => {
      const key = selector(result.item);
      counts[key] = (counts[key] || 0) + 1;
    });
    return counts;
  }

  function updateFacetCounts(base) {
    const categories = countBy(filtered(base, { ignoreCategory: true }), categoryKey);
    document.getElementById('cc-all').textContent = categories.all;
    Object.values(categoryKeys).forEach(key => {
      const el = document.getElementById(`cc-${key}`);
      if (el) el.textContent = categories[key] || 0;
    });

    const origins = countBy(filtered(base, { ignoreOrigin: true }), item => item.origin || 'Other');
    document.querySelectorAll('.origin-btn[data-origin]').forEach(button => {
      const key = button.dataset.origin;
      const el = button.querySelector('.origin-count');
      if (el) el.textContent = origins[key] || 0;
    });

    const concepts = countBy(filtered(base, { ignoreConcept: true }), item => item.tags || []);
    const tagCounts = { all: concepts.all };
    filtered(base, { ignoreConcept: true }).forEach(({ item }) => {
      (item.tags || []).forEach(tag => { tagCounts[tag] = (tagCounts[tag] || 0) + 1; });
    });
    dom.concepts.querySelectorAll('.concept-pill').forEach(button => {
      const count = button.querySelector('.concept-count');
      if (count) count.textContent = tagCounts[button.dataset.concept] || 0;
    });
  }

  function renderConcepts() {
    const counts = {};
    state.all.forEach(item => (item.tags || []).forEach(tag => { counts[tag] = (counts[tag] || 0) + 1; }));
    state.concepts = Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 18).map(([tag]) => tag);
    dom.concepts.innerHTML = '<button class="concept-pill active" data-concept="all">All Concepts</button>' +
      state.concepts.map(tag => `<button class="concept-pill" data-concept="${escapeHtml(tag)}">${escapeHtml(tag)} <span class="concept-count">${counts[tag]}</span></button>`).join('');
    dom.concepts.querySelectorAll('.concept-pill').forEach(button => button.addEventListener('click', () => selectConcept(button.dataset.concept)));
  }

  function selectConcept(concept) {
    state.concept = concept;
    dom.concepts.querySelectorAll('.concept-pill').forEach(button => button.classList.toggle('active', button.dataset.concept === concept));
    apply();
  }

  function renderStats() {
    const matched = state.results.length;
    dom.count.textContent = state.query
      ? `${matched} result${matched === 1 ? '' : 's'} for “${state.query}”`
      : `Displaying ${matched} of ${state.all.length} writeups`;
    const parts = [];
    if (state.origin !== 'all') parts.push(`Origin: ${state.origin}`);
    if (state.category !== 'all') parts.push(`Type: ${Object.entries(categoryKeys).find(([, key]) => key === state.category)?.[0] || state.category}`);
    if (state.concept !== 'all') parts.push(`Concept: ${state.concept}`);
    dom.stats.textContent = parts.length ? `Filters: ${parts.join(' · ')}` : '';
  }

  function renderCards() {
    dom.cards.replaceChildren();
    if (!state.results.length) {
      dom.cards.innerHTML = '<div class="empty-state"><div class="empty-icon">🔍</div><h3>No writeups found</h3><p>Try clearing your search, or pick a different origin / challenge type.</p></div>';
      dom.moreWrap.hidden = true;
      return;
    }
    state.results.slice(0, state.visible).forEach(result => {
      const item = result.item;
      const terms = matchedTerms(result);
      const card = document.createElement('a');
      card.className = `card cat-${categoryKey(item)}`;
      card.href = `viewer.html?id=${encodeURIComponent(item.id)}`;
      const primaryTitle = item.context_title || cleanTitle(item.title);
      const subtitle = item.context_title ? `<span class="card-title-sub">${highlight(cleanTitle(item.title), terms)}</span>` : '';
      const tags = (item.tags || []).map(tag => `<span class="tag-badge" data-tag="${escapeHtml(tag)}">${highlight(tag, terms)}</span>`).join('');
      const snippet = state.query ? contextualSnippet(item, terms) : item.snippet;
      card.innerHTML = `<div class="card-content"><span class="${item.context_title ? 'card-title-context' : 'card-title'}">${highlight(primaryTitle, terms)}</span>${subtitle}<span class="card-desc">${highlight(snippet, terms)}</span>${tags ? `<div class="card-tags">${tags}</div>` : ''}</div><div class="card-footer"><span class="badge badge-category">${escapeHtml(item.category)}</span><span class="badge badge-origin ${originClasses[item.origin] || 'origin-other'}">${escapeHtml(item.origin || 'Other')}</span></div>`;
      card.querySelectorAll('.tag-badge').forEach(badge => badge.addEventListener('click', event => {
        event.preventDefault(); event.stopPropagation(); selectConcept(badge.dataset.tag);
      }));
      dom.cards.appendChild(card);
    });
    dom.moreWrap.hidden = state.results.length <= state.visible;
  }

  function apply() {
    const base = baseSearchResults();
    state.results = filtered(base);
    state.visible = 30;
    updateFacetCounts(base);
    renderStats();
    renderCards();
  }

  function bindControls() {
    document.querySelectorAll('.chip[data-cat]').forEach(button => button.addEventListener('click', () => {
      document.querySelectorAll('.chip[data-cat]').forEach(node => node.classList.remove('active'));
      button.classList.add('active'); state.category = button.dataset.cat; apply();
    }));
    document.querySelectorAll('.origin-btn[data-origin]').forEach(button => button.addEventListener('click', () => {
      document.querySelectorAll('.origin-btn[data-origin]').forEach(node => node.classList.remove('active'));
      button.classList.add('active'); state.origin = button.dataset.origin; apply();
    }));
    let debounce;
    dom.input.addEventListener('input', () => {
      clearTimeout(debounce);
      debounce = setTimeout(() => { state.query = dom.input.value.trim(); apply(); }, 160);
    });
    dom.input.addEventListener('keydown', event => {
      if (event.key === 'Escape') { dom.input.value = ''; state.query = ''; apply(); }
    });
    dom.clear.addEventListener('click', () => { dom.input.value = ''; state.query = ''; apply(); dom.input.focus(); });
    dom.more.addEventListener('click', () => { state.visible += 30; renderCards(); });
  }

  async function boot() {
    try {
      dom.count.textContent = 'Loading writeups database…';
      const response = await fetch('writeups-index.json');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      state.all = await response.json();
      state.byId = new Map(state.all.map(item => [item.id, item]));
      renderConcepts();
      bindControls();
      dom.count.textContent = `Indexing ${state.all.length} writeups…`;
      await new Promise(resolve => setTimeout(resolve, 0));
      state.engine = new MiniSearch({
        fields: ['title', 'tags', 'headings', 'snippet', 'body', 'path'],
        idField: 'id',
        searchOptions: {
          boost: { title: 5, tags: 3, headings: 2, snippet: 2, body: 1, path: 1 },
          prefix: term => term.length >= 2,
          fuzzy: false,
          weights: { prefix: 0.8, fuzzy: 0.55 },
          combineWith: 'AND'
        }
      });
      state.engine.addAll(state.all.map(item => ({
        ...item,
        tags: (item.tags || []).join(' '),
        headings: (item.headings || []).join(' ')
      })));
      apply();
    } catch (error) {
      console.error('Writeup search initialization failed:', error);
      dom.count.textContent = 'Could not load the writeups database.';
      dom.cards.innerHTML = '<div class="empty-state"><h3>Search unavailable</h3><p>Reload the page or verify writeups-index.json is present.</p></div>';
    }
  }

  boot();
})();
