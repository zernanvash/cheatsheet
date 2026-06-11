# Notion Sync

This repo can publish selected vault pages into a Notion workspace through GitHub Actions.

## Required Notion Setup

1. Create a Notion integration.
2. Copy the integration secret.
3. Open the Notion parent page where the vault pages should be created.
4. Share that page with the integration.
5. Copy the parent page ID from the page URL.

## Required GitHub Secrets

Add these under repository settings:

- `NOTION_TOKEN`: Notion integration secret.
- `NOTION_PARENT_PAGE_ID`: target parent page ID.

Optional repository variable:

- `NOTION_TITLE_PREFIX`: prefix for synced page titles, such as `H4G - `.

## How It Works

- Workflow: `.github/workflows/sync-notion.yml`
- Script: `scripts/sync_notion.py`
- Page list: `notion-sync-manifest.txt`

The workflow runs on pushes to `main` that touch vault Markdown files, and it can also be run manually with `workflow_dispatch`.

The sync creates or updates Notion child pages by title. It replaces each synced page's existing blocks with the current Markdown content.

## Scope

The manifest intentionally focuses on the PDA/databank route, machine blueprints, core path guides, key tool sheets, and references. Source folders such as `_source_*` are not synced.
