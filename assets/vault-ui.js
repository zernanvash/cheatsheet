(function () {
  "use strict";

  const path = location.pathname.toLowerCase();
  const isViewer = path.endsWith("/viewer.html") || path.endsWith("viewer.html");
  const isTool = /(?:ascii-code|vigenere-cipher|rot-cipher|columnar-transposition-cipher|affine-cipher)\.html$/.test(path)
    || path.includes("/cipher-identifier/");

  document.body.dataset.vaultPage = isViewer ? "viewer" : isTool ? "tool" : "index";

  function enhanceTables(root) {
    root.querySelectorAll("table").forEach((table) => {
      if (table.parentElement && table.parentElement.classList.contains("table-wrap")) return;
      const wrapper = document.createElement("div");
      wrapper.className = "table-wrap";
      table.before(wrapper);
      wrapper.appendChild(table);
    });
  }

  function enhanceCode(root) {
    root.querySelectorAll("pre").forEach((pre) => {
      if (pre.closest(".code-frame") || pre.closest(".result")) return;
      const code = pre.querySelector(":scope > code");
      if (!code) return;

      const languageClass = Array.from(code.classList).find((name) => name.startsWith("language-"));
      const language = languageClass ? languageClass.slice(9) : "text";
      const frame = document.createElement("div");
      const bar = document.createElement("div");
      const label = document.createElement("span");
      const copy = document.createElement("button");

      frame.className = "code-frame";
      bar.className = "code-frame__bar";
      label.className = "code-frame__language";
      label.textContent = language;
      copy.className = "code-frame__copy";
      copy.type = "button";
      copy.textContent = "Copy";
      copy.setAttribute("aria-label", `Copy ${language} code`);
      copy.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(code.textContent || "");
          copy.textContent = "Copied";
        } catch {
          const selection = getSelection();
          const range = document.createRange();
          range.selectNodeContents(code);
          selection.removeAllRanges();
          selection.addRange(range);
          copy.textContent = "Selected";
        }
        window.setTimeout(() => { copy.textContent = "Copy"; }, 1600);
      });

      pre.before(frame);
      bar.append(label, copy);
      frame.append(bar, pre);
    });
  }

  function enhance(root) {
    if (!(root instanceof Element)) return;
    enhanceTables(root);
    enhanceCode(root);
  }

  function start() {
    const content = document.getElementById("content");
    if (!content) return;
    enhance(content);
    new MutationObserver(() => enhance(content)).observe(content, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
}());
