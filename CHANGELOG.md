# Changelog

Human-readable log of substantive changes to mukeshadhikari.com. Newest first.
Dates are the date the change was made.

## 2026-08-08

- **Accuracy pass on About and the homepage stat cards** (three text edits; no
  structural or JS changes). Re-copied `index.html` to `404.html`.
  - **Journal names made precise.** "peer-reviewed publications in top-tier journals
    including JAMA, The Lancet, and BMJ" → "peer-reviewed publications, including in
    JAMA Health Forum, JAMA Internal Medicine, The Lancet Global Health, and BMJ
    Global Health." The compressed form read as the flagship titles; the actual
    venues are the family journals.
  - **Career stat card reconciled with the Education timeline.** "15 Years —
    Teaching & Research Career (2010–present)" → "14 Years — Public Health Practice,
    Research & Teaching (2012–present)". The old card dated the career two years
    before the BPH (2012) listed in About, and "Teaching & Research" excluded the
    Nepal practice years it was counting.
  - **Hero repositioned.** Eyebrow "Researcher · Science Communicator · Educator" →
    "Health Economist · Health Services Researcher · Policy Analyst". Tagline
    "Turning public health research into clear public communication and measurable
    policy impact." → "Causal policy evaluation using national administrative and
    survey data — health workforce, access, and health systems in the United States
    and South Asia." The old tagline repeated the unsupported policy-impact claim
    removed from About below, and led with communication rather than capability.
    `<h1>` and the meta/JSON-LD descriptions are unchanged.
  - **Removed an unsubstantiated impact claim.** "My work has influenced policy
    decisions at both national and international levels…" → a factual statement of
    what the published work covers. The subject areas are unchanged; the assertion
    of policy influence is gone, since no specific citation backs it.

## 2026-07-13

- **Add project documentation.** Added `CLAUDE.md` (project context, file tree,
  architecture, conventions) and this `CHANGELOG.md`.
- **Clean URL routing.** Each section now has its own URL (`/research`, `/policy`,
  `/teaching`, `/resources`, `/socialmedia`, `/about`, `/contact`) via the History
  API; the tab title updates per section and back/forward works. Added
  `<base href="/">` so relative assets resolve on sub-paths. Replaced the stale
  `404.html` (it was still the old purple-gradient design) with a copy of the
  current `index.html` so deep links and refreshes on sub-paths load the app.
- **Resources tab.** Removed the "Annual Report of DOHS: 2081/82" download; the
  tab stays live with a "Resources coming soon" placeholder. (The PDF file remains
  in the repo but is no longer linked.)
- **Sitemap.** Bumped `sitemap.xml` `<lastmod>` to 2026-07-13.
- **New publication + dynamic counts.** Added "Health Resources and Services
  Administration and Veterans Affairs Funding Intersections Expand Graduate Medical
  Education Training Opportunities in Rural and Underserved Areas" (The Journal of
  Rural Health, 2026) to the US list. Replaced hardcoded "24"/"over 24" counts with
  a `totalPublications()` helper so the number updates automatically as papers are
  added. Refactored the fallback publication arrays to global scope so the counter
  and Research section share one source. Total is now 25.
- **Fixed ORCID sync workflow.** The Python-setup step was mistakenly using
  `peter-evans/create-pull-request@v7` with a `python-version` input; switched it
  to `actions/setup-python@v5` and bumped the PR step to `@v7`. Delivered via PR #1
  and merged. (Before this fix the weekly ORCID sync would not run correctly.)
- **Synced local folder** to match the GitHub repo (the local copy had drifted to
  an older design).

## 2026-07-02 (pre-existing, before these sessions)

- Site redesign to the current editorial/academic look (paper/navy palette,
  Fraunces + Inter fonts).
- Added full SEO: `<title>`, meta description, Open Graph + Twitter cards, JSON-LD
  Person structured data, `robots.txt`, `sitemap.xml`.
- Moved publications into `publications.json` (data-driven Research section).
- Added ORCID auto-sync (`scripts/sync_publications.py` +
  `.github/workflows/update-publications.yml`).
