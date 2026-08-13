(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const DIGITS = '0123456789';
  const EN = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,.153,.772,4.025,2.406,6.749,7.507,1.929,.095,5.987,6.327,9.056,2.758,.978,2.360,.150,1.974,.074];
  const printable = Array.from({length:94}, (_, i) => String.fromCharCode(i + 33)).join('');
  const ascii = Array.from({length:128}, (_, i) => String.fromCharCode(i)).join('');

  function selected(prefix) { return document.querySelector(`input[name="${prefix}-alphabet"]:checked`).value; }
  function groups(prefix) {
    const mode = selected(prefix);
    if (mode === 'letters') return [AZ];
    if (mode === 'split') return [AZ, DIGITS];
    if (mode === 'alnum') return [AZ + DIGITS];
    if (mode === 'base36') return [DIGITS + AZ];
    if (mode === 'printable') return [printable];
    if (mode === 'ascii') return [ascii];
    const custom = $(`${prefix}-custom`).value;
    if ([...custom].length < 2) throw new Error('Custom alphabet must contain at least two characters.');
    if (new Set([...custom]).size !== [...custom].length) throw new Error('Custom alphabet characters must be unique.');
    return [custom];
  }
  function rotate(text, amount, alphabets, insensitive, decrypt) {
    return [...text].map(ch => {
      for (let groupIndex = 0; groupIndex < alphabets.length; groupIndex++) {
        const alphabet = alphabets[groupIndex];
        let index = alphabet.indexOf(ch), lower = false;
        if (index < 0 && insensitive) {
          const upper = ch.toUpperCase(); index = alphabet.toUpperCase().indexOf(upper);
          lower = ch !== upper && ch === ch.toLowerCase();
        }
        if (index >= 0) {
          const groupAmount = alphabets.length === 2 && amount === 13 && groupIndex === 1 ? 5 : amount;
          const shift = ((decrypt ? -groupAmount : groupAmount) % alphabet.length + alphabet.length) % alphabet.length;
          let output = [...alphabet][(index + shift) % [...alphabet].length];
          if (lower) output = output.toLowerCase();
          return output;
        }
      }
      return ch;
    }).join('');
  }
  function scoreEnglish(text) {
    const clean = text.toUpperCase().replace(/[^A-Z]/g, '');
    if (!clean.length) return Infinity;
    const counts = Array(26).fill(0); for (const ch of clean) counts[ch.charCodeAt(0) - 65]++;
    let chi = 0; for (let i = 0; i < 26; i++) { const expected = EN[i] * clean.length / 100; chi += (counts[i] - expected) ** 2 / expected; }
    const words = (text.toUpperCase().match(/\b(THE|AND|THAT|THIS|YOU|FOR|WITH|CODE|ROT|IS|TO|OF|IN)\b/g) || []).length;
    return chi - words * 12;
  }
  function escapeHtml(value) { return value.replace(/[&<>]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[ch])); }
  function setStatus(id, text, error = false) { $(id).textContent = text; $(id).className = `status${error ? ' error' : ''}`; }
  function updateCustom(prefix) {
    const mode = selected(prefix); const field = $(`${prefix}-custom-field`);
    field.hidden = mode !== 'custom-i' && mode !== 'custom-s';
  }
  function run(prefix, decrypt) {
    try {
      const amount = Number($(`${prefix}-rotation`).value);
      if (!Number.isInteger(amount)) throw new Error('Rotation N must be an integer.');
      const mode = selected(prefix), alphabets = groups(prefix), insensitive = mode !== 'custom-s' && mode !== 'printable' && mode !== 'ascii';
      $(`${prefix}-output`).value = rotate($(`${prefix}-input`).value, amount, alphabets, insensitive, decrypt);
      setStatus(`${prefix}-status`, `${decrypt ? 'Decrypted' : 'Encrypted'} with ROT-${amount}.`);
    } catch (error) { setStatus(`${prefix}-status`, error.message, true); }
  }
  function bruteForce() {
    const input = $('dec-input').value;
    if ((input.match(/[A-Za-z]/g) || []).length < 4) { setStatus('auto-status', 'Enter at least four letters for useful English ranking.', true); return; }
    const results = Array.from({length:25}, (_, i) => i + 1).map(rotation => ({rotation, text: rotate(input, rotation, [AZ], true, true)}));
    results.sort((a,b) => scoreEnglish(a.text) - scoreEnglish(b.text));
    $('auto-results').innerHTML = results.map((item, i) => `<article class="result"><div><b>#${i+1} ROT-${item.rotation}</b><button type="button" data-rotation="${item.rotation}">Use rotation</button></div><pre>${escapeHtml(item.text)}</pre></article>`).join('');
    $('dec-output').value = results[0].text; $('dec-rotation').value = results[0].rotation;
    setStatus('auto-status', 'All 25 rotations tested and ranked using English letter/word statistics. Verify the readable candidate.');
  }
  ['dec','enc'].forEach(prefix => {
    document.querySelectorAll(`input[name="${prefix}-alphabet"]`).forEach(input => input.addEventListener('change', () => updateCustom(prefix)));
    updateCustom(prefix);
  });
  $('auto-decrypt').addEventListener('click', bruteForce);
  $('decrypt').addEventListener('click', () => run('dec', true));
  $('encrypt').addEventListener('click', () => run('enc', false));
  $('auto-results').addEventListener('click', event => { if (!event.target.dataset.rotation) return; $('dec-rotation').value = event.target.dataset.rotation; run('dec', true); });
})();
