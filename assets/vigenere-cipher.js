(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const STANDARD = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const ENGLISH = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,.153,.772,4.025,2.406,6.749,7.507,1.929,.095,5.987,6.327,9.056,2.758,.978,2.360,.150,1.974,.074];

  function readAlphabet(id) {
    const raw = $(id).value;
    const chars = [...raw];
    if (chars.length < 2) throw new Error('Alphabet must contain at least two characters.');
    if (new Set(chars).size !== chars.length) throw new Error('Alphabet characters must be unique.');
    return chars;
  }

  function charIndex(ch, alphabet) {
    let index = alphabet.indexOf(ch);
    if (index < 0 && alphabet.join('') === STANDARD) index = alphabet.indexOf(ch.toUpperCase());
    return index;
  }

  function normalizeKey(raw, alphabet, partial = false) {
    const key = [];
    for (const ch of [...raw]) {
      if (partial && ch === '?') { key.push('?'); continue; }
      const index = charIndex(ch, alphabet);
      if (index >= 0) key.push(alphabet[index]);
      else if (!/\s/.test(ch)) throw new Error(`Key character “${ch}” is not in the alphabet.`);
    }
    if (!key.length) throw new Error('Enter a key containing alphabet characters.');
    return key;
  }

  function transform(text, key, alphabet, decrypt, preserve = true) {
    let output = '', position = 0;
    for (const ch of [...text]) {
      const input = charIndex(ch, alphabet);
      if (input < 0) { if (preserve) output += ch; continue; }
      const shift = alphabet.indexOf(key[position % key.length]);
      const index = (input + (decrypt ? -shift : shift) + alphabet.length) % alphabet.length;
      let result = alphabet[index];
      if (alphabet.join('') === STANDARD && ch === ch.toLowerCase() && ch !== ch.toUpperCase()) result = result.toLowerCase();
      output += result;
      position++;
    }
    return output;
  }

  function letters(text) { return text.toUpperCase().replace(/[^A-Z]/g, ''); }
  function requireEnglishAlphabet() {
    if ($('dec-alphabet').value !== STANDARD) throw new Error('Automatic cryptanalysis currently requires the standard A–Z alphabet. Exact keyed decryption supports custom alphabets.');
  }
  function ic(text) {
    if (text.length < 2) return 0;
    const counts = Array(26).fill(0);
    for (const ch of text) counts[ch.charCodeAt(0) - 65]++;
    return counts.reduce((sum, n) => sum + n * (n - 1), 0) / (text.length * (text.length - 1));
  }
  function averageIc(text, length) {
    let total = 0;
    for (let column = 0; column < length; column++) total += ic([...text].filter((_, i) => i % length === column).join(''));
    return total / length;
  }
  function kasiski(text, max) {
    const evidence = Array(max + 1).fill(0);
    for (let size = 3; size <= 5; size++) {
      const positions = new Map();
      for (let i = 0; i <= text.length - size; i++) {
        const gram = text.slice(i, i + size);
        if (!positions.has(gram)) positions.set(gram, []);
        positions.get(gram).push(i);
      }
      for (const list of positions.values()) for (let i = 1; i < list.length; i++) {
        const distance = list[i] - list[i - 1];
        for (let factor = 2; factor <= max; factor++) if (distance % factor === 0) evidence[factor]++;
      }
    }
    return evidence;
  }
  function rankLengths(text) {
    const max = Math.min(20, Math.max(1, Math.floor(text.length / 4)));
    const evidence = kasiski(text, max);
    return Array.from({length: max}, (_, i) => i + 1).map(length => {
      const coincidence = averageIc(text, length);
      const score = Math.max(0, 1 - Math.abs(coincidence - .0667) / .04) * 70 + Math.min(30, evidence[length] * 4);
      return {length, coincidence, kasiski: evidence[length], score};
    }).sort((a, b) => b.score - a.score);
  }
  function bestShift(sample) {
    if (!sample.length) return 0;
    const counts = Array(26).fill(0);
    for (const ch of sample) counts[ch.charCodeAt(0) - 65]++;
    let winner = 0, best = Infinity;
    for (let shift = 0; shift < 26; shift++) {
      let chi = 0;
      for (let plain = 0; plain < 26; plain++) {
        const expected = ENGLISH[plain] * sample.length / 100;
        chi += (counts[(plain + shift) % 26] - expected) ** 2 / expected;
      }
      if (chi < best) { best = chi; winner = shift; }
    }
    return winner;
  }
  function inferKey(text, length, partial = '') {
    const pattern = partial.toUpperCase();
    let key = '';
    for (let column = 0; column < length; column++) {
      const fixed = pattern[column];
      key += fixed && fixed !== '?' ? fixed : STANDARD[bestShift([...text].filter((_, i) => i % length === column).join(''))];
    }
    return key;
  }
  function englishScore(text) {
    const clean = letters(text);
    if (!clean.length) return Infinity;
    const counts = Array(26).fill(0);
    for (const ch of clean) counts[ch.charCodeAt(0) - 65]++;
    let chi = 0;
    for (let i = 0; i < 26; i++) { const expected = ENGLISH[i] * clean.length / 100; chi += (counts[i] - expected) ** 2 / expected; }
    const common = (clean.match(/THE|AND|ING|ION|TH|HE|ER|RE|AN|IN/g) || []).length;
    return chi - common * 2;
  }
  function candidate(key, note) {
    const plaintext = transform($('ciphertext').value, [...key], [...STANDARD], true, true);
    return {key, plaintext, note, score: englishScore(plaintext)};
  }
  function cribCandidates(text, crib) {
    const results = [];
    const lengths = rankLengths(text).slice(0, 8).map(row => row.length);
    for (const length of lengths) for (let start = 0; start <= text.length - crib.length; start++) {
      const pattern = Array(length).fill('?'); let consistent = true;
      for (let i = 0; i < crib.length; i++) {
        const shift = (text.charCodeAt(start + i) - crib.charCodeAt(i) + 26) % 26;
        const position = (start + i) % length;
        if (pattern[position] !== '?' && pattern[position] !== STANDARD[shift]) { consistent = false; break; }
        pattern[position] = STANDARD[shift];
      }
      if (consistent) results.push(candidate(inferKey(text, length, pattern.join('')), `crib at letter ${start + 1}, length ${length}`));
    }
    const unique = new Map();
    results.sort((a,b) => a.score - b.score).forEach(item => { if (!unique.has(item.key)) unique.set(item.key, item); });
    return [...unique.values()].slice(0, 12);
  }
  function showCandidates(items) {
    $('solutions').innerHTML = items.map((item, i) => `<article class="solution"><div><b>#${i + 1} key <code>${item.key}</code></b><span>${item.note}</span></div><pre>${escapeHtml(item.plaintext)}</pre><button type="button" data-key="${item.key}">Use this key</button></article>`).join('');
    $('decoder-output').value = items[0]?.plaintext || '';
  }
  function escapeHtml(value) { return value.replace(/[&<>]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[ch])); }
  function status(id, message, error = false) { $(id).textContent = message; $(id).className = `status${error ? ' error' : ''}`; }

  function autoDecrypt() {
    try {
      requireEnglishAlphabet();
      const text = letters($('ciphertext').value);
      if (text.length < 20) throw new Error('Automatic analysis needs at least 20 letters; 80+ is much more reliable.');
      const method = document.querySelector('input[name="method"]:checked').value;
      let items = [];
      if (method === 'key') {
        const key = normalizeKey($('known-key').value, [...STANDARD]).join(''); items = [candidate(key, 'exact supplied key')];
      } else if (method === 'length') {
        const length = Number($('known-length').value);
        if (!Number.isInteger(length) || length < 1 || length > 40) throw new Error('Key length must be between 1 and 40.');
        items = [candidate(inferKey(text, length), `frequency analysis, fixed length ${length}`)];
      } else if (method === 'partial') {
        const pattern = normalizeKey($('partial-key').value, [...STANDARD], true).join('');
        items = [candidate(inferKey(text, pattern.length, pattern), `completed partial key ${pattern}`)];
      } else if (method === 'crib') {
        const crib = letters($('crib').value); if (!crib) throw new Error('Enter a known plaintext word.');
        items = cribCandidates(text, crib); if (!items.length) throw new Error('No consistent crib placements were found.');
      } else {
        items = rankLengths(text).slice(0, 10).map(row => candidate(inferKey(text, row.length), `length ${row.length} · IC ${row.coincidence.toFixed(4)} · Kasiski ${row.kasiski}`)).sort((a,b) => a.score - b.score);
      }
      showCandidates(items);
      status('auto-status', `${items.length} ranked ${items.length === 1 ? 'result' : 'hypotheses'}. Statistical results are clues—verify readable plaintext.`);
    } catch (error) { showCandidates([]); status('auto-status', error.message, true); }
  }
  function exactDecrypt() {
    try {
      const alphabet = readAlphabet('dec-alphabet'); const key = normalizeKey($('known-key').value, alphabet);
      $('decoder-output').value = transform($('ciphertext').value, key, alphabet, true, $('dec-preserve').checked);
      status('dec-status', `Decrypted exactly with a ${key.length}-character key and ${alphabet.length}-character alphabet.`);
    } catch (error) { status('dec-status', error.message, true); }
  }
  function encrypt() {
    try {
      const alphabet = readAlphabet('enc-alphabet'); const key = normalizeKey($('enc-key').value, alphabet);
      $('encoder-output').value = transform($('plaintext').value, key, alphabet, false, $('enc-preserve').checked);
      status('enc-status', `Encrypted with a ${key.length}-character key and ${alphabet.length}-character alphabet.`);
    } catch (error) { status('enc-status', error.message, true); }
  }
  function renderTable() {
    try {
      const alphabet = readAlphabet('dec-alphabet');
      let html = `<thead><tr><th>Key \\ Plain</th>${alphabet.map(ch => `<th>${escapeHtml(ch)}</th>`).join('')}</tr></thead><tbody>`;
      alphabet.forEach((_, row) => { html += `<tr><th>${escapeHtml(alphabet[row])}</th>${alphabet.map((__, col) => `<td>${escapeHtml(alphabet[(row + col) % alphabet.length])}</td>`).join('')}</tr>`; });
      $('tabula').innerHTML = `${html}</tbody>`;
    } catch (error) { $('tabula').innerHTML = `<tbody><tr><td>${escapeHtml(error.message)}</td></tr></tbody>`; }
  }
  function updateMethod() {
    const method = document.querySelector('input[name="method"]:checked').value;
    document.querySelectorAll('.method-field').forEach(field => field.hidden = field.dataset.method !== method);
  }

  document.querySelectorAll('input[name="method"]').forEach(input => input.addEventListener('change', updateMethod));
  $('auto-decrypt').addEventListener('click', autoDecrypt);
  $('decrypt').addEventListener('click', exactDecrypt);
  $('encrypt').addEventListener('click', encrypt);
  $('dec-alphabet').addEventListener('input', renderTable);
  $('solutions').addEventListener('click', event => { if (!event.target.dataset.key) return; $('known-key').value = event.target.dataset.key; exactDecrypt(); });
  updateMethod(); renderTable();
})();
