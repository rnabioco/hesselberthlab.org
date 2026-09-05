# hesselberthlab.org

The Hesselberth Lab website — [Hugo](https://gohugo.io/) with the
[HugoBlox](https://hugoblox.com/) academic theme, built and deployed by Netlify.

```bash
pixi run setup     # once — installs Node dependencies
pixi run serve     # http://localhost:1313
pixi run build     # Hugo + Pagefind into public/
```

Everything below is about *where to edit what*. For the design rationale behind
particular choices, see the commit history; for agent-facing notes, see
`CLAUDE.md`.

---

## Updating content

| I want to… | Edit |
| --- | --- |
| Change the homepage hero, research areas | `content/_index.md` |
| Add a news item | new dir under `content/blog/` (see below) |
| Add or edit a lab member | `data/authors/<slug>.yaml` + `assets/media/authors/<slug>.png` |
| Add a publication | `publications.bib`, then `pixi run import-pubs` |
| Feature a publication on the homepage | add `featured: true` to its `content/publications/<slug>/index.md` |
| Edit the software list | `content/software.md` |
| Change colours | `data/themes/cu-anschutz.yaml` |
| Change layout/spacing | `assets/css/custom.css` |
| Change the nav | `config/_default/menus.yaml` |

### News

Each news item is its own directory with a one-line body:

```
content/blog/2026-01-10-short-slug/index.md
```

```markdown
---
title: "We were awarded a VISTA pilot award"
date: 2026-01-10
---

We were awarded a [VISTA](https://example.org) pilot award.
```

Items **do not get their own pages**. `content/blog/_index.md` cascades
`_build.render: never` to them, because a page holding a single sentence is not
worth having. They still appear in lists, so the homepage can show the five most
recent. The `title` is unused by the running list — the body is what renders, so
put links there.

### People

One file per person in `data/authors/`. The filename is the slug, and the
avatar must match it: `data/authors/jane-doe.yaml` ↔
`assets/media/authors/jane-doe.png`.

```yaml
name:
  given: Jane
  family: Doe
  display: Jane Doe

weight: 20          # 1 = PI, 10s = staff, 20s = students — controls order

role: Graduate Student, Molecular Biology

user_groups:
  - Graduate Students

affiliations:
  - name: University of Colorado School of Medicine
    url: https://www.cuanschutz.edu/

links:
  - icon: brands/linkedin
    url: https://www.linkedin.com/in/…
    label: LinkedIn
```

Icons are `<pack>/<name>` — packs are `brands`, `hero`, `academicons`,
`devicon`, `hb`. `brands/github`, `brands/orcid`, `brands/google-scholar`,
`hero/envelope` all work.

`content/people.md` deliberately sets **no** `user_groups`, so everyone renders
in one continuous grid ordered by `weight` rather than a row per group. Add
`user_groups` back there if you want group headings.

### Publications

`publications.bib` is the source of truth. After editing:

```bash
pixi run import-pubs      # regenerates content/publications/
```

A **nightly GitHub Action** (`.github/workflows/update-publications.yml`)
searches PubMed for new lab papers, appends them, regenerates the pages and
opens a pull request. It de-duplicates by PMID, DOI and normalised title, and
searches a 30-day window by default. Run it by hand from the Actions tab with
`days: 0` to sweep the whole record — expect it to surface older papers that
were never added.

It matches on author name, so **check for same-name authors from other labs**
before merging its PRs.

---

## How things render

The site is HugoBlox "blocks": `content/_index.md`, `content/people.md` and
`content/software.md` are `type: landing` pages that list `sections`, each a
block with `content` and `design`. Everything else is an ordinary Hugo page.

### Custom views

`design.view` on a `collection` block picks how items render. Alongside the
theme's `card`, `article-grid`, `citation` and `date-title-summary`, this repo
adds two in `layouts/_partials/views/`:

- **`citation-image`** — the dense citation with the paper's illustration
  beside it. Papers without one collapse to a single column so a mixed list
  still lines up. Used for "Selected publications".
- **`news-line`** — date and item text, no link, for the pageless news items.

A view is three files: `<name>.html`, `<name>--start.html`, `<name>--end.html`.

### Theme and CSS

Colours come from the theme pack at `data/themes/cu-anschutz.yaml`
(`config/_default/params.yaml` selects it with `theme.pack`). CU gold is only
~1.5:1 on cream, so it is used for **decoration only** — rules, motifs, fills —
and text uses the deeper gold. Dark mode swaps those roles.

`assets/css/custom.css` holds the rest. Two things there are load-bearing and
easy to break:

- The theme centres every block in a `max-w-prose` column. Sections that lay
  out their own grid opt out by putting `.wide` on their content.
- Selectors are matched against **rendered output**, not guessed. The section
  class is `hbb-section`, not `hb-section`; an earlier stylesheet targeted
  `.universal-wrapper`, `.hb-navbar` and `.card`, none of which the theme
  emits, and was silently inert.

### Images

`assets/media/` is the media library and gets processed by Hugo (resized,
converted to webp). `static/` is copied verbatim — use it when a raw HTML `<img>`
needs a URL that resolves, since raw HTML bypasses Hugo's image render hook.

- `assets/media/authors/<slug>.png` — profile avatars
- `content/publications/<slug>/featured.png` — a paper's illustration
- `assets/media/sharing.png` — the social card. The theme finds
  `media/sharing.*` automatically and it becomes `og:image` site-wide, which
  also upgrades the Twitter card to `summary_large_image`.
- `static/media/lab-logo.svg` — the logo, drawn in `currentColor` so it works
  on cream and in dark mode

### Generated illustrations

Portraits and science illustrations are generated with
[bananarama](https://hadley.github.io/bananarama/) driving Google Gemini. See
the "Site graphics" section of `CLAUDE.md` for the full details; briefly:

```bash
pixi run -e graphics graphics-setup   # once
pixi run -e graphics cu               # graphics/cu.yaml   -> graphics/out/cu/
pixi run -e graphics publications     # per-paper images
```

R lives in its own pixi environment so it never enters the one Netlify builds
with. Needs `GEMINI_API_KEY` in `~/.Renviron`. Roughly $0.07 per image, and
existing files are skipped — set `force: true` on an image to redraw it.

Renders land in `graphics/out/` (gitignored) for review; copy the ones you want
into `assets/media/`.

---

## Deploying

Netlify builds from this repo on every push to `main`. Build settings live in
`netlify.toml`, **not** in the Netlify UI — the file takes precedence. Pull
requests get a deploy preview automatically, built with `HUGO_BASEURL` set to
the preview URL.

`_headers` and `_redirects` are generated into `public/` by the HugoBlox Netlify
module; don't duplicate them in `netlify.toml`.

The domain resolves through Cloudflare to Netlify.
