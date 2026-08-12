(() => {
  'use strict';

  const CONTROL_NAMES = [
    'NUL','SOH','STX','ETX','EOT','ENQ','ACK','BEL','BS','HT','LF','VT','FF','CR','SO','SI',
    'DLE','DC1','DC2','DC3','DC4','NAK','SYN','ETB','CAN','EM','SUB','ESC','FS','GS','RS','US'
  ];

  const FORMATS = {
    bin7: { label: 'Binary /7', base: 2, width: 7, valid: /^[01]+$/ },
    bin8: { label: 'Binary /8', base: 2, width: 8, valid: /^[01]+$/ },
    oct3: { label: 'Octal /3', base: 8, width: 3, valid: /^[0-7]+$/ },
    dec: { label: 'Decimal', base: 10, width: 0, valid: /^\d+$/ },
    dec3: { label: 'Decimal /3', base: 10, width: 3, valid: /^\d+$/ },
    hex2: { label: 'Hexadecimal /2', base: 16, width: 2, valid: /^[0-9a-f]+$/i }
  };

  function displayCharacter(code) {
    if (code < 32) return `<${CONTROL_NAMES[code]}>`;
    if (code === 32) return ' ';
    if (code === 127) return '<DEL>';
    return String.fromCharCode(code);
  }

  function encode(text, format = 'dec', separator = ' ') {
    const config = FORMATS[format];
    if (!config) throw new Error('Unknown output format.');
    const invalid = [...text].find(char => char.codePointAt(0) > 127);
    if (invalid) throw new Error(`“${invalid}” is outside 7-bit ASCII (0–127).`);
    return [...text].map(char => {
      const value = char.charCodeAt(0).toString(config.base).toUpperCase();
      return config.width ? value.padStart(config.width, '0') : value;
    }).join(separator);
  }

  function tokenize(input, config) {
    const trimmed = input.trim();
    if (!trimmed) return [];
    const separated = trimmed.split(/[\s,;:|/\\-]+/).filter(Boolean);
    if (separated.length > 1) return separated;
    const compact = trimmed.replace(/[^0-9a-f]/gi, '');
    if (!config.width) return [compact];
    if (compact.length % config.width) {
      throw new Error(`${config.label} needs groups of ${config.width} characters, or explicit separators.`);
    }
    return compact.match(new RegExp(`.{${config.width}}`, 'g')) || [];
  }

  function decode(input, format) {
    const config = FORMATS[format];
    if (!config) throw new Error('Unknown input format.');
    const tokens = tokenize(input, config);
    if (!tokens.length) throw new Error('Enter one or more ASCII values.');
    const values = tokens.map(token => {
      const normalized = token.replace(/^0x/i, '');
      if (!normalized || !config.valid.test(normalized)) throw new Error(`“${token}” is not valid ${config.label}.`);
      const value = Number.parseInt(normalized, config.base);
      if (!Number.isInteger(value) || value < 0 || value > 127) throw new Error(`${token} is outside ASCII range 0–127.`);
      return value;
    });
    return { format, label: config.label, values, text: values.map(displayCharacter).join('') };
  }

  function autoDecode(input) {
    const candidates = [];
    for (const format of ['bin7', 'bin8', 'oct3', 'dec3', 'dec', 'hex2']) {
      try {
        const result = decode(input, format);
        const key = `${result.values.join(',')}|${result.text}`;
        if (!candidates.some(item => item.key === key)) candidates.push({ ...result, key });
      } catch (_) { /* Invalid interpretations are intentionally omitted. */ }
    }
    return candidates;
  }

  function parseCsv(text) {
    const rows = [];
    let row = [], field = '', quoted = false;
    for (let index = 0; index < text.length; index += 1) {
      const char = text[index], next = text[index + 1];
      if (quoted && char === '"' && next === '"') { field += '"'; index += 1; }
      else if (char === '"') quoted = !quoted;
      else if (!quoted && char === ';') { row.push(field); field = ''; }
      else if (!quoted && (char === '\n' || char === '\r')) {
        if (char === '\r' && next === '\n') index += 1;
        row.push(field); field = '';
        if (row.some(value => value.length)) rows.push(row);
        row = [];
      } else field += char;
    }
    row.push(field);
    if (row.some(value => value.length)) rows.push(row);
    return rows;
  }

  window.H4G_ASCII = { FORMATS, encode, decode, autoDecode, parseCsv, displayCharacter };

  const byId = id => document.getElementById(id);
  if (!byId('ascii-encoder')) return;
  const escapeHtml = value => String(value || '').replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));

  function setStatus(id, message, error = false) {
    const node = byId(id);
    node.textContent = message;
    node.classList.toggle('error', error);
  }

  function runEncode() {
    try {
      byId('encode-output').value = encode(byId('plain-input').value, byId('encode-format').value, byId('separator').value);
      setStatus('encode-status', 'Converted locally in your browser.');
    } catch (error) {
      byId('encode-output').value = '';
      setStatus('encode-status', error.message, true);
    }
  }

  function renderCandidates(results) {
    const container = byId('decode-results');
    container.innerHTML = '';
    results.forEach((result, index) => {
      const card = document.createElement('article');
      card.className = 'result-card';
      card.innerHTML = `<div class="result-head"><strong>${escapeHtml(result.label)}</strong>${index === 0 ? '<span class="best-badge">best candidate</span>' : ''}</div><pre>${escapeHtml(result.text)}</pre><div class="result-values">${escapeHtml(result.values.join(' · '))}</div>`;
      container.appendChild(card);
    });
  }

  function runDecode() {
    try {
      const format = byId('decode-format').value;
      const results = format === 'auto' ? autoDecode(byId('cipher-input').value) : [decode(byId('cipher-input').value, format)];
      if (!results.length) throw new Error('No valid 7-bit ASCII interpretation was found. Check the base or separators.');
      renderCandidates(results);
      setStatus('decode-status', `${results.length} valid interpretation${results.length === 1 ? '' : 's'} found.`);
    } catch (error) {
      byId('decode-results').innerHTML = '';
      setStatus('decode-status', error.message, true);
    }
  }

  function renderTable(query = '') {
    const needle = query.trim().toLowerCase();
    const rows = [];
    for (let code = 0; code <= 127; code += 1) {
      const character = code < 32 ? CONTROL_NAMES[code] : code === 32 ? 'SPACE' : code === 127 ? 'DEL' : String.fromCharCode(code);
      const searchable = `${code} ${code.toString(8)} ${code.toString(16)} ${code.toString(2)} ${character}`.toLowerCase();
      if (!needle || searchable.includes(needle)) rows.push(`<tr><td>${String(code).padStart(3, '0')}</td><td>${code.toString(8).padStart(3, '0')}</td><td>${code.toString(16).toUpperCase().padStart(2, '0')}</td><td>${code.toString(2).padStart(7, '0')}</td><td>${escapeHtml(character)}</td></tr>`);
    }
    byId('ascii-table-body').innerHTML = rows.join('');
    byId('table-count').textContent = `${rows.length} of 128 codes`;
  }

  byId('encode-button').addEventListener('click', runEncode);
  byId('decode-button').addEventListener('click', runDecode);
  byId('plain-input').addEventListener('input', runEncode);
  byId('encode-format').addEventListener('change', runEncode);
  byId('separator').addEventListener('input', runEncode);
  byId('cipher-input').addEventListener('input', runDecode);
  byId('decode-format').addEventListener('change', runDecode);
  byId('table-search').addEventListener('input', event => renderTable(event.target.value));

  document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    const source = byId(button.dataset.copy);
    await navigator.clipboard.writeText(source.value || source.textContent || '');
    const original = button.textContent;
    button.textContent = 'Copied';
    setTimeout(() => { button.textContent = original; }, 1000);
  }));

  byId('csv-file').addEventListener('change', async event => {
    const file = event.target.files[0];
    if (!file) return;
    const rows = parseCsv(await file.text());
    byId('csv-summary').textContent = `${file.name}: ${rows.length} exported result rows. File stays in this browser tab.`;
    byId('csv-results').innerHTML = rows.map(row => `<article class="result-card"><strong>${escapeHtml(row[0] || 'Unlabelled')}</strong><pre>${escapeHtml(row.slice(1).join(';'))}</pre></article>`).join('');
  });

  byId('plain-input').value = 'dCode ASCII';
  byId('cipher-input').value = '64 43 6F 64 65 20 41 53 43 49 49';
  renderTable(); runEncode(); runDecode();
})();
