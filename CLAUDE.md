# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Hesselberth Lab website built with [Hugo](https://gohugo.io/) using the [HugoBlox](https://hugoblox.com/) academic theme. The site is deployed to https://hesselberthlab.org via GitHub Pages. Dependencies are managed with [pixi](https://pixi.sh/).

## Common Commands

### Setup

```bash
pixi run setup
```

Installs Node.js dependencies via pnpm (corepack + pnpm install).

### Local Development

```bash
pixi run serve
```

Site runs at http://localhost:1313

### Build for Production

```bash
pixi run build
```

Builds with Hugo + Pagefind search index. Output goes to `public/`.

### Import Publications

```bash
pixi run import-pubs
```

Converts `publications.bib` to individual Hugo publication pages in `content/publications/` using the `academic` CLI.

## Architecture

### Key Content Locations

- `content/_index.md` - Homepage (HugoBlox block-based landing page)
- `content/publications/` - Publication pages (auto-generated from BibTeX)
- `content/blog/` - News/announcements as blog posts
- `content/software.md` - Software and tools page
- `content/people.md` - Lab members page
- `content/authors/` - Author profiles (one directory per person)
- `publications.bib` - Publications in BibTeX format (source of truth)
- `assets/media/` - Images and media files
- `assets/css/custom.css` - Custom CSS (Crimson Pro font)

### Configuration

- `config/_default/hugo.yaml` - Main Hugo config (baseURL, build settings)
- `config/_default/params.yaml` - HugoBlox theme params (identity, theme, typography, header, footer)
- `config/_default/menus.yaml` - Navigation menu
- `config/_default/module.yaml` - Hugo module imports (HugoBlox)
- `config/_default/languages.yaml` - Language settings

### Dependencies

- `pixi.toml` - pixi workspace (Hugo, Go, Node.js, Python, academic CLI)
- `package.json` - Node.js dependencies (Tailwind CSS, Pagefind, Preact)
- `go.mod` - Go module for HugoBlox theme
- `hugoblox.yaml` - HugoBlox version and deploy config

## Publications

Publications are managed via BibTeX in `publications.bib` at the repo root. The `academic` CLI converts BibTeX entries to individual Hugo content pages. Set `featured: true` in a publication's front matter to show on homepage. A GitHub Actions workflow auto-creates a PR when `publications.bib` changes.

## Deployment

Automatic deployment via GitHub Actions on push to `main` branch. The workflow uses pixi to install dependencies, builds with Hugo + Pagefind, and deploys to GitHub Pages via `actions/deploy-pages`.
