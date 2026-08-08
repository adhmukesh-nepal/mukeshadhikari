# Changelog

Human-readable log of substantive changes to mukeshadhikari.com. Newest first.
Dates are the date the change was made.

## 2026-08-08 (fifth pass — CV published; Resources back in the nav)

- **Added `Adhikari_Mukesh_CV_2026.pdf`** (2 pages, 179 KB) and a Resources card for it.
  The "Resources coming soon" empty state no longer renders — the section has content.
  **This is the public build of the CV, with the phone number stripped.** It is generated
  by `../../consulting_practice/build_cv.py`, which emits two PDFs from one HTML source: a
  full version carrying the phone (for direct sending) and this web version without it. The
  phone is a personal mobile, and a number on a public page gets scraped and cached
  permanently. **Never overwrite this file with the full version** — rerun the build script
  and copy `Adhikari_Mukesh_CV_2026_web.pdf` here.
- **"Download CV" button in the homepage hero**, between View Research and Get in Touch.
  Added a `download` icon to the shared `icons` object (the existing one was local to
  `renderResources`).
- **`resources` returned to `NAV_SECTIONS`** — it came out earlier today only because it had
  nothing in it.
- **`/resources` added to `sitemap.xml`**, now that indexing it is worth doing.
  `/socialmedia` stays out: it's a Facebook embed with no indexable content.

## 2026-08-08 (fourth pass — evaluation split, casing consistency)

- **"Evaluation" → "Program evaluation", plus a new "Economic evaluation" group**
  (cost-effectiveness analysis, costing of service delivery and program implementation,
  cost outcomes estimated alongside effectiveness). "Evaluation" alone was vague and
  overlapped the new group; "Program evaluation" is the term US funders and RFPs use, and
  it covers both the effectiveness and implementation work. `cost` moved out of the
  implementation-evaluation phrase so the two groups don't duplicate it.
- **Casing made consistent** across the block. Each `·`-separated entry now starts with a
  capital, matching the Research Focus Areas list convention elsewhere in About — the
  lists previously capitalised only the first entry. Group labels now use `&`
  consistently ("Tools & reproducibility", "US administrative & survey data"), matching
  the "Methods & Data" heading rather than mixing "and" with "&".
- Seven groups now, so Tools & reproducibility takes `md:col-span-2` again: three even
  rows plus a full-width closer.
- `<noscript>` methods sentence updated in step, per §3.

## 2026-08-08 (third pass — trim Methods & Data to demonstrated experience)

- **Removed the "Robustness practice" group** from Methods & Data. The causal-inference
  line already implies it, and itemising honest-DiD bounds and wild cluster bootstrap
  invited scrutiny with no upside.
- **Removed `small-area estimation`** from Other methods.
- **Removed `CMS Payroll-Based Journal`, `Care Compare and Provider Information`, and
  `BLS OES/QCEW`** from US administrative data — and PBJ from the `<noscript>` block,
  keeping it in sync as §3 requires. These are datasets for planned work, not completed
  work; listing them read as experience. They go back once the analysis exists.
- **Added `Health Professional Shortage Area designations`, `Federally Qualified Health
  Center program data`, and the `Medical Expenditure Panel Survey (MEPS)`** to the US
  data group (and to the `<noscript>` block). All three are demonstrated work, unlike
  the datasets removed above.
- **Removed `natality files` and `BRFSS`** — not worked in.
- **Relabelled the group "US administrative & survey data."** MEPS and ACS/PUMS are
  surveys, not administrative files, and the label now matches the hero tagline
  ("national administrative and survey data").
- Tools and reproducibility lost its `md:col-span-2`, so the six remaining groups form
  an even 3×2 grid.

## 2026-08-08 (second pass — positioning, social previews, crawlability)

- **New "Methods & Data" block in About.** Seven labelled groups: causal inference,
  evaluation, other methods, robustness practice, US administrative data,
  international data, tools and reproducibility. The site previously named no
  method or dataset anywhere — it listed research *topics* only.
- **`headshot.jpg` is now a real JPEG.** It was PNG data (872×872, 1.0 MB) served
  with a `.jpg` extension, which failed in headless Chrome and risked rejection by
  strict social-card validators. Now genuine JPEG, 400×400, 44 KB — a 96% saving on
  a file that displays at 176px. The 872px original is kept locally as
  `headshot-872-original.png.backup` (git-ignored), not committed.
- **Dedicated `og-image.jpg` (1200×630).** `og:image` and `twitter:image` pointed at
  the square headshot, wrong for a `summary_large_image` card. Added a proper card —
  name, credentials, eyebrow, tagline, site — with `og:image:width/height` and alt
  text. `og-image-source.html` is the committed source; regenerate with:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless
  --disable-gpu --hide-scrollbars --force-device-scale-factor=2
  --window-size=1200,630 --screenshot=og.png file://$(pwd)/og-image-source.html`
  then `sips -s format jpeg -s formatOptions 90 -z 630 1200 og.png --out og-image.jpg`.
  JSON-LD `image` still points at the headshot, which is correct for a Person photo.
- **`<noscript>` fallback added.** All content is JS-injected into `#app`; extracting
  text from the raw HTML previously yielded only the `<title>`. Google runs JS, but
  LinkedIn's preview fetcher and archiving tools don't. The block carries name, role,
  tagline, journals, methods, and Scholar/ORCID/LinkedIn/email links. **Keep it in
  sync with About when the bio changes.**
- **Meta and JSON-LD repositioned** to match the new hero: `description`,
  `og:description`, `twitter:description`, and JSON-LD `jobTitle` and `description`
  now lead with health economist and causal policy evaluation. Added Causal
  Inference, Program Evaluation, and Health Workforce to `knowsAbout`. `<title>`,
  `og:title`, `twitter:title`, and the `<h1>` are unchanged.
- **Nav trimmed to six tabs.** Introduced `NAV_SECTIONS` (home, research, policy,
  teaching, about, contact) separate from `SECTIONS`, which still governs routing.
  `/resources` and `/socialmedia` continue to resolve and render — they are just no
  longer top-level tabs. Resources has no content yet (its "coming soon" placeholder
  read as an abandoned site in the nav), and Social Media reads personal-brand beside
  the research sections. Contact now carries a "Social media feed" link so the
  section stays reachable. **Put Resources back in `NAV_SECTIONS` once the CV and
  working papers are there.**
- **`sitemap.xml` expanded** from the homepage alone to the six nav routes, with
  `lastmod` 2026-08-08. `/resources` and `/socialmedia` are deliberately excluded;
  a comment in the file explains when to add them.

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
