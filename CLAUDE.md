# CLAUDE.md

Project context and working notes for **mukeshadhikari.com** — the personal
website of Mukesh Adhikari, PhD, MPH, MPA (health services researcher & health
policy analyst). This file is read by Claude Code at the start of a session; keep
it accurate so future sessions have full context.

> Change history lives in [CHANGELOG.md](CHANGELOG.md). Add an entry there for
> every substantive change.

---

## 1. What this is

A **single-page personal/academic website**, hand-built as one self-contained
`index.html` — no framework, no build step, no npm. Styling is Tailwind loaded
from a CDN; all logic is vanilla JavaScript that swaps the page content per
"section." It is deployed as a static site on **GitHub Pages**.

- **Live site:** https://mukeshadhikari.com
- **Repo:** https://github.com/adhmukesh-nepal/mukeshadhikari (public)
- **Hosting:** GitHub Pages, `main` branch, root of repo
- **Custom domain:** set via `CNAME` (`mukeshadhikari.com`)
- **Analytics:** Google Analytics (gtag `G-J176Z972QM`)

---

## 2. File tree

```
website_mukeshadhikari-main/
├── index.html                     # THE SITE — entire SPA (markup + CSS + JS) in one file
├── 404.html                       # Copy of index.html; GitHub Pages serves it for
│                                  #   unknown paths so deep links / refreshes on
│                                  #   /research etc. still load the app. KEEP IN SYNC
│                                  #   with index.html (see §5).
├── publications.json              # Publication data: { updated, us[], nepal[], other[] }.
│                                  #   Source of truth for the Research section & counts.
│                                  #   Auto-updated from ORCID via the workflow below.
├── headshot.jpg                   # Profile photo (~1 MB)
├── annualreport_dohs_2081_82.pdf  # ~19 MB PDF. No longer linked from the site
│                                  #   (removed from Resources); kept in repo for now.
├── portfolio_html.html            # LEGACY standalone portfolio page (old purple design).
│                                  #   Not linked from the site; safe to ignore/remove.
├── CNAME                          # Custom domain for GitHub Pages (mukeshadhikari.com)
├── robots.txt                     # Allows all crawlers; points to sitemap.xml
├── sitemap.xml                    # Sitemap (currently just the homepage "/")
├── README.md                      # Minimal ("mukeshadhikari")
├── .gitignore                     # Ignores .DS_Store, screenshots, local backups
├── CLAUDE.md                      # This file
├── CHANGELOG.md                   # Human-readable log of changes
├── scripts/
│   └── sync_publications.py       # Pulls works from ORCID, adds NEW ones to
│                                  #   publications.json "other" bucket. Non-destructive.
└── .github/
    └── workflows/
        └── update-publications.yml # Weekly (Mon 12:00 UTC) + manual. Runs the sync
                                     #   script and opens a PR when new pubs are found.
```

Untracked/local-only (not in the repo): `index.html.backup`, `.DS_Store`.

---

## 3. Architecture (index.html)

Everything is inside `index.html`. Mental model:

- **State:** two globals — `currentSection` (which tab is showing) and `menuOpen`
  (mobile menu). `PUBS` holds publication data loaded from `publications.json`.
- **Sections:** `SECTIONS = ['home','research','policy','teaching','resources',
  'socialmedia','about','contact']`. Each has a `render<Section>()` function that
  returns an HTML template string.
- **Rendering:** `render()` writes `renderNav() + renderSection() + footer` into
  `#app`. `renderSection()` dispatches on `currentSection`.
- **Navigation & routing:** `navigateTo(section)` updates state, pushes a clean
  URL (`/research`, `/policy`, …) via the History API, updates the tab title, and
  re-renders. `sectionFromPath()` maps the URL back to a section on load;
  `popstate` handles back/forward. See §5.
- **Design system:** custom Tailwind theme (config inline in `<head>`) — colors
  `paper/card/ink/navy/navydark/muted/rule`, fonts **Fraunces** (serif) + **Inter**
  (sans). Editorial/academic look.
- **Contact form:** posts to Web3Forms (`api.web3forms.com`).
- **Third-party embeds:** Google Analytics, Facebook Page plugin (Social Media tab).

---

## 4. Publications & the ORCID auto-sync

Publications render from `publications.json` (`us`, `nepal`, and `other` arrays).
`index.html` also contains built-in fallback arrays (`US_DEFAULT`, `NEPAL_DEFAULT`)
used only if `publications.json` fails to load (e.g. opening via `file://`).

- **Counts are dynamic.** `totalPublications()` sums `us + nepal + other`. The home
  hero stat and the About paragraph both call it — never hardcode the number.
- **Auto-sync:** `.github/workflows/update-publications.yml` runs `scripts/
  sync_publications.py` weekly (and on demand from the Actions tab). It reads
  ORCID `0000-0002-1091-328X`, adds any publication NOT already present to the
  `other` bucket (empty tags), and opens a PR titled "New publication(s) found on
  ORCID." It **never edits or removes** existing hand-curated entries.
- **After the sync opens a PR:** move each new entry into `us` or `nepal`, fix the
  title/journal if ORCID's is off, add `tags`, then merge to publish.
- ⚠️ ORCID is often behind the site's curated list — the auto-sync only helps for
  papers that are actually on ORCID. Keep ORCID updated for it to be useful.

### To add a publication by hand
Edit `publications.json` → add an object to `us` or `nepal` (newest first):
```json
{ "title": "…", "journal": "…", "year": "2026", "link": "https://doi.org/…",
  "tags": ["Medical Education", "Rural Health"] }
```
Also bump `"updated"`. The cards and all counts update automatically. If you also
want the `file://` fallback to match, add the same entry to `US_DEFAULT`/
`NEPAL_DEFAULT` in `index.html` (optional but tidy). Then re-copy to `404.html`.

---

## 5. Routing & the 404.html rule (important)

Clean URLs (`/research`, `/policy`, …) work via the History API. Because GitHub
Pages has no server-side rewrites, **`404.html` is a copy of `index.html`**: a
direct visit or refresh on `/research` has no matching file, GitHub serves
`404.html` (the full app), and the JS reads the path and shows the right section.
`<base href="/">` in the `<head>` ensures relative assets still resolve on
sub-paths.

> **RULE:** Whenever you change `index.html`'s markup/JS, re-copy it to `404.html`:
> `cp index.html 404.html`. (Publication data changes flow through
> `publications.json` at runtime and do NOT require re-copying.)

Known trade-off: sub-paths return an HTTP 404 status to crawlers even though they
render fine for visitors. The homepage `/` returns 200. This is standard for SPAs
on GitHub Pages and is acceptable here.

---

## 6. Deployment workflow

There is **no build step** — pushing to `main` deploys via GitHub Pages (live in
~1–2 minutes). Typical loop for a change:

1. Edit files in this folder.
2. Validate JS syntax: extract the main `<script>` and run `node --check`.
3. If `index.html` changed structurally: `cp index.html 404.html`.
4. Commit and push to `main` (or open a PR for review).
5. Verify on the live site after Pages redeploys.

### Git workflow

This folder **is** a git checkout tracking `origin`
(`adhmukesh-nepal/mukeshadhikari`, branch `main`). Work directly here:

```bash
git add -A
git commit -m "message"
git push
```

Pull changes made on GitHub — e.g. after **merging an ORCID auto-sync PR**:

```bash
git pull
```

Notes:
- Commit author is set locally to `adhmukesh-nepal` / `madhikari@unc.edu`.
- `index.html.backup` and other `*.backup` files are git-ignored (local only).
- For risky changes, branch and open a PR instead of pushing straight to `main`.

---

## 7. Conventions

- Match the existing code style in `index.html` (template-string render functions,
  Tailwind utility classes with the custom theme tokens).
- Never hardcode counts that can be derived (use `totalPublications()`).
- External links use `target="_blank"`; internal navigation uses
  `onclick="navigateTo('…')"`, not `<a href>`.
- Keep `index.html` and `404.html` in sync (§5).
- Add a `CHANGELOG.md` entry for every substantive change.

---

## 8. Known issues / possible follow-ups

- `annualreport_dohs_2081_82.pdf` (~19 MB) is unused/unlinked — remove if not
  needed to slim the repo.
- `portfolio_html.html` is a legacy page, not linked — candidate for deletion.
- ORCID profile is behind the curated publication list — add papers to ORCID so
  the auto-sync stays useful.
- Contact form depends on the Web3Forms access key embedded in `index.html`.
