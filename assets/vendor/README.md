# Vendored browser dependencies

These pinned files are stored locally so opening the vault never downloads runtime code from a third party.

| File | Upstream | Version | License |
| --- | --- | --- | --- |
| `marked-15.0.12.min.js` | [marked](https://github.com/markedjs/marked/tree/v15.0.12) | 15.0.12 | MIT (`LICENSE.marked.md`) |
| `purify-3.2.6.min.js` | [DOMPurify](https://github.com/cure53/DOMPurify/tree/3.2.6) | 3.2.6 | MPL-2.0 OR Apache-2.0 (`LICENSE.DOMPurify.txt`) |

When updating either dependency, pin an exact upstream release, replace its license copy, update `viewer.html`, and rerun the protected-server and browser smoke tests.

