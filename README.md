# Contributing to H4G CTF Vault

Welcome! Thank you for considering contributing to the H4G CTF Vault & Cheatsheet repository. Whether you are adding new tool cheatsheets, fixing typos, or documenting CTF challenge walkthroughs, your contributions are welcome.

This repository follows the standard GitHub Forking Workflow. Below is a step-by-step guide on how to contribute using a fork.

---

## Run the Vault Locally Offline

The repository's local HTML interfaces can be served without an internet connection or build step. You need Python 3 and a web browser.

Open PowerShell in the repository root:

```powershell
Set-Location G:\HackForGov2025\h4g
python -m http.server 8080
```

If Windows provides the `py` launcher instead of `python`, use:

```powershell
py -m http.server 8080
```

On Linux or macOS, open a terminal in the cloned repository root:

```bash
python3 -m http.server 8080
```

Keep the terminal open, then use these local URLs:

| Interface | URL |
| --- | --- |
| Vault home | `http://localhost:8080/` |
| Zen CTF Notes | `http://localhost:8080/zen-ctf-notes/` |
| Web Exploit Checklist | `http://localhost:8080/zen-ctf-notes/#web-exploit-checklist` |
| Writeup browser | `http://localhost:8080/writeups.html` |
| 0xrefs cheatsheet | `http://localhost:8080/0xrefs.html` |

Stop the server with `Ctrl+C`.

### Local Viewer Troubleshooting

- Use `python -m http.server 8080`, not `python http.server 8080`.
- If port 8080 is busy, replace it with another port such as `8081` in both the command and URL.
- Use `Ctrl+F5` if recent local changes do not appear.
- Python's built-in server is read-only. The Zen CTF Notes Edit button requires an optional `/api/zen-notes` backend and remains disabled on the static server.
- Open the HTML interface rather than a `.md` file directly when you want rendered Markdown.

After editing the derived Zen Web Exploit Checklist, rebuild its embedded note data from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-zen-ctf-notes.ps1
```

---

## Workflow Overview

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch
4. Make your edits and test
5. Commit and push your changes
6. Open a Pull Request (PR)

---

### Step 1: Fork the Repository

1. Go to the main repository page on GitHub: https://github.com/zernanvash/cheatsheet
2. Click the Fork button in the top-right corner of the page.
3. Select your GitHub account to create your personal copy of the repository (`https://github.com/YOUR-USERNAME/cheatsheet`).

---

### Step 2: Clone Your Fork Locally

Open your terminal or command prompt and clone your forked repository to your local machine:

```bash
git clone https://github.com/YOUR-USERNAME/cheatsheet.git
cd cheatsheet
```

Add the original repository as an `upstream` remote to keep your fork in sync:

```bash
git remote add upstream https://github.com/zernanvash/cheatsheet.git
```

---

### Step 3: Create a Feature Branch

Always create a new branch for your edits. Keeping your `main` branch clean makes updating your fork much simpler.

```bash
git fetch upstream
git checkout main
git merge upstream/main

git checkout -b feature/my-new-cheatsheet
```

---

### Step 4: Make Your Edits

Make your changes using your code editor of choice.

#### Editing Guidelines
* Cheatsheets: Save new tool cheatsheets in `tools/` and link them in `tools/Tools Index.md`.
* Playbooks & Blueprints: Place new guides in `guides/` or `blueprints/`.
* Code Formatting: Use standard GitHub-Flavored Markdown. Wrap all commands in code blocks specifying the language (`bash`, `python`, `powershell`).
* Environment Variables: Use variables like `$TARGET` (IP), `$URL` (web endpoint), `$LHOST` (attacker IP), and `$LPORT` instead of hardcoded IPs.

If you added or updated markdown writeups, run the enrichment script to verify index building:

```bash
python tools/enrich_writeups.py
```

---

### Step 5: Commit & Push Your Changes

Stage your files, write a concise commit message, and push the branch to your GitHub fork:

```bash
git status
git add .
git commit -m "Add new cheatsheet for Go binary analysis"
git push origin feature/my-new-cheatsheet
```

---

### Step 6: Create a Pull Request (PR)

1. Navigate to your fork on GitHub (`https://github.com/YOUR-USERNAME/cheatsheet`).
2. Click Compare & pull request for your recently pushed branch.
3. Review your changes in the diff view.
4. Add a brief title and description explaining what your PR adds or fixes.
5. Click Create Pull Request.

---

## Keeping Your Fork Up to Date

Before starting a new feature in the future, sync your local copy with the main repository:

```bash
git checkout main
git pull upstream main
git push origin main
```
