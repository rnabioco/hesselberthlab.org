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

## Site graphics

Illustrations and headshots are generated with [bananarama](https://hadley.github.io/bananarama/), which drives Google Gemini from a YAML file.

```bash
pixi run -e graphics graphics-setup   # once — installs the R package
export GEMINI_API_KEY=...             # or GOOGLE_API_KEY
pixi run -e graphics graphics         # graphics/site.yaml   -> assets/media/generated/
pixi run -e graphics headshots        # graphics/headshots.yaml -> assets/media/authors/
```

R lives in a separate pixi environment (`[feature.graphics]`), so it never enters the default environment that Netlify builds with.

- Each image's `name` becomes `<name>.png` in the config's `output-dir`. Existing files are skipped; set `force: true` on an image to redraw it. Roughly $0.07 per image.
- `[somename]` in a description is a reference image: bananarama looks for `graphics/somename.png` and passes it to the model.
- Headshot `name`s must match the profile slug in `data/authors/<slug>.yaml`, since that is how `team-showcase` resolves avatars.
- The `style` block in each config mirrors the CU palette in `data/themes/cu-anschutz.yaml`; keep them in step.
- Commit generated images — regenerating costs money and is not deterministic.

## Publications

Publications are managed via BibTeX in `publications.bib` at the repo root. The `academic` CLI converts BibTeX entries to individual Hugo content pages. Set `featured: true` in a publication's front matter to show on homepage. A GitHub Actions workflow auto-creates a PR when `publications.bib` changes.

## Deployment

Deployed by [Netlify](https://www.netlify.com/), which builds from the repo on every push to `main`. Build settings live in `netlify.toml` (not the Netlify UI — the file takes precedence): it bootstraps pixi, then runs `pixi run setup && pixi run build`, publishing `public/`.

Pull requests get a deploy preview automatically; previews and branch deploys build with `HUGO_BASEURL` set to the generated Netlify URL so links resolve.

HTTP headers and redirects are generated into `public/_headers` and `public/_redirects` by the HugoBlox Netlify integration module (`config/_default/module.yaml` plus the `headers`/`redirects` outputs in `hugo.yaml`) — don't duplicate them in `netlify.toml`.

The domain hesselberthlab.org resolves through Cloudflare to Netlify.
