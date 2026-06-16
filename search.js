(function () {
  const INDEX_URL = "search-index.json";
  const MIN_QUERY_LENGTH = 2;
  const MAX_RESULTS = 12;

  let indexPromise;

  function normalize(value) {
    return String(value || "")
      .toLowerCase()
      .replace(/[^a-z0-9+#._/-]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(INDEX_URL)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Search index unavailable: ${response.status}`);
          }
          return response.json();
        })
        .then((entries) =>
          entries.map((entry) => ({
            ...entry,
            searchTitle: normalize(entry.title),
            searchPath: normalize(entry.path),
            searchCategory: normalize(entry.category),
            searchHeadings: normalize((entry.headings || []).join(" ")),
            searchText: normalize(entry.text),
          }))
        );
    }
    return indexPromise;
  }

  function scoreEntry(entry, terms, phrase) {
    let score = 0;

    if (entry.searchTitle === phrase) score += 120;
    if (entry.searchTitle.includes(phrase)) score += 70;
    if (entry.searchPath.includes(phrase)) score += 45;
    if (entry.searchHeadings.includes(phrase)) score += 32;
    if (entry.searchText.includes(phrase)) score += 12;

    for (const term of terms) {
      if (!term) continue;
      if (entry.searchTitle.includes(term)) score += 20;
      if (entry.searchPath.includes(term)) score += 14;
      if (entry.searchCategory.includes(term)) score += 10;
      if (entry.searchHeadings.includes(term)) score += 9;
      if (entry.searchText.includes(term)) score += 2;
    }

    return score;
  }

  function makeSnippet(entry, terms, phrase) {
    const source = entry.text || "";
    const lower = source.toLowerCase();
    const needles = [phrase, ...terms].filter(Boolean);
    let index = -1;

    for (const needle of needles) {
      index = lower.indexOf(needle);
      if (index !== -1) break;
    }

    if (index === -1) {
      return source.slice(0, 180).trim();
    }

    const start = Math.max(0, index - 70);
    const end = Math.min(source.length, index + 140);
    const prefix = start > 0 ? "... " : "";
    const suffix = end < source.length ? " ..." : "";
    return `${prefix}${source.slice(start, end).trim()}${suffix}`;
  }

  function resultUrl(path) {
    return `viewer.html?file=${encodeURIComponent(String(path || "").replace(/\\/g, "/"))}`;
  }

  function renderResults(results, nodes, queryData) {
    const { resultsNode, countNode } = nodes;

    if (!results.length) {
      resultsNode.innerHTML = '<div class="search-empty">No matching vault pages.</div>';
      resultsNode.hidden = false;
      countNode.textContent = "No results";
      return;
    }

    resultsNode.innerHTML = results
      .map((result) => {
        const snippet = makeSnippet(result.entry, queryData.terms, queryData.phrase);
        return `
          <a class="search-result" href="${resultUrl(result.entry.path)}">
            <span class="search-result-title">${escapeHtml(result.entry.title)}</span>
            <span class="search-result-path">${escapeHtml(result.entry.category)} / ${escapeHtml(result.entry.path)}</span>
            <span class="search-result-snippet">${escapeHtml(snippet)}</span>
          </a>
        `;
      })
      .join("");

    resultsNode.hidden = false;
    countNode.textContent = `${results.length} result${results.length === 1 ? "" : "s"}`;
  }

  async function runSearch(rawQuery, nodes) {
    const phrase = normalize(rawQuery);
    const { resultsNode, countNode } = nodes;

    if (phrase.length < MIN_QUERY_LENGTH) {
      resultsNode.hidden = true;
      resultsNode.innerHTML = "";
      countNode.textContent = `Type at least ${MIN_QUERY_LENGTH} characters.`;
      return [];
    }

    countNode.textContent = "Searching...";
    const terms = phrase.split(" ").filter(Boolean);
    const entries = await loadIndex();
    const results = entries
      .map((entry) => ({ entry, score: scoreEntry(entry, terms, phrase) }))
      .filter((result) => result.score > 0)
      .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title))
      .slice(0, MAX_RESULTS);

    renderResults(results, nodes, { terms, phrase });
    return results;
  }

  function initSearch(root) {
    const scope = root || document;
    const input = scope.querySelector("[data-search-input]");
    const resultsNode = scope.querySelector("[data-search-results]");
    const countNode = scope.querySelector("[data-search-count]");
    const clearButton = scope.querySelector("[data-search-clear]");

    if (!input || !resultsNode || !countNode) return;

    const nodes = { resultsNode, countNode };
    let latestResults = [];
    let timer;

    input.addEventListener("input", () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(async () => {
        try {
          latestResults = await runSearch(input.value, nodes);
        } catch (error) {
          resultsNode.hidden = false;
          resultsNode.innerHTML = '<div class="search-empty">Search index could not be loaded.</div>';
          countNode.textContent = "Search unavailable";
          console.error(error);
        }
      }, 80);
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && latestResults.length) {
        event.preventDefault();
        window.location.href = resultUrl(latestResults[0].entry.path);
      }

      if (event.key === "Escape") {
        input.value = "";
        input.dispatchEvent(new Event("input"));
      }
    });

    if (clearButton) {
      clearButton.addEventListener("click", () => {
        input.value = "";
        input.focus();
        input.dispatchEvent(new Event("input"));
      });
    }
  }

  window.H4GSearch = { initSearch, loadIndex };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => initSearch(document));
  } else {
    initSearch(document);
  }
})();
