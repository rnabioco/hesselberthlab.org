# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Hesselberth Lab website built with Jekyll using the [al-folio](https://github.com/alshedivat/al-folio) academic theme. The site is deployed to https://hesselberthlab.org via GitHub Pages.

## Common Commands

### Local Development (Docker - Recommended)
```bash
docker compose pull
docker compose up
```
Site runs at http://localhost:8080

### Local Development (Native Ruby)
```bash
bundle install
pip install jupyter
bundle exec jekyll serve
```
Site runs at http://localhost:4000

### Build for Production
```bash
bundle exec jekyll build
```
Output goes to `_site/`

## Architecture

### Key Content Locations
- `_pages/about.md` - Homepage content (lab mission, research focus)
- `_bibliography/papers.bib` - Publications in BibTeX format (uses jekyll-scholar)
- `_news/` - News/announcements organized by year
- `_data/repositories.yml` - GitHub repos to feature
- `_data/cv.yml` - CV data (fallback if no JSON resume)
- `assets/json/resume.json` - JSON Resume format CV data

### Configuration
- `_config.yml` - Main Jekyll config including:
  - Site metadata (`title`, `url`, `first_name`, `last_name`)
  - Jekyll Scholar settings for bibliography
  - Theme options (dark mode, masonry, math typesetting)
  - Plugin configuration

### Collections
- `news` - Lab announcements
- `projects` - Research projects
- `books` - Book collection

## Publications

Publications are managed via BibTeX in `_bibliography/papers.bib`. Supported fields include: `abstract`, `pdf`, `code`, `html`, `arxiv`, `doi`, `poster`, `slides`, `video`, `website`. Set `selected={true}` to feature on homepage.

## Deployment

Automatic deployment via GitHub Actions on push to `main` branch. The workflow builds the site and deploys to `gh-pages` branch.
