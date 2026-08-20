# Experiment 0 Status — NJ Property Tax Relief

## Purpose

Experiment 0 tests whether Number Eleven Works can turn a real, complicated information problem into a useful, trustworthy, inexpensive web utility that can be discovered through search and eventually contribute to monetization.

Immediate evidence goals:
- Google discovery/indexing
- impressions and clicks
- site visits
- tool usage
- eventually monetizable actions and revenue

## Current product

Public site: `https://nj-property-tax-relief-lab.pages.dev`

Public pages:
- `/`
- `/which-application/`
- `/programs/`
- `/official-resources/`

## Architecture

- Python 3.13
- Jinja2 static generation
- YAML-backed program/source/rule data
- Python validation
- JavaScript decision-tool behavior
- generated `robots.txt`
- generated `sitemap.xml`
- `public/` copied to generated site root
- Cloudflare Pages deployment from GitHub `main`

Static-first remains intentional. Add server/API/database capability only when an observed requirement justifies it.

## Current deployment / telemetry state

Repository: `squidpan/nj-property-tax-relief-lab`
Production branch: `main`
Cloudflare Pages project: `nj-property-tax-relief-lab`
Automatic GitHub deployments: enabled
Cloudflare Web Analytics: enabled

Recent production work:
- `85544f4` — Harden Cloudflare deployment and fix official resource rendering
- `d009066` — Document NJ Cloudflare web analytics activation
- `a4a6cc3` — Publish root verification assets for Search Console

Current validation:
- repository validation: 0 issues
- automated tests: 18 passing

## Local development lesson

For active development use an editable install:

    python -m pip install -e .

A normal `python -m pip install .` can leave repository scripts importing a stale installed copy from `.venv/site-packages`.

Check import location when needed:

    python -c "import njptr_lab.site_builder as s; print(s.__file__)"

It should resolve into the repository `src/` tree during development.

## Google Search Console

Property type: URL prefix
Property: `https://nj-property-tax-relief-lab.pages.dev/`
Ownership: verified by HTML file

Verification artifact:
- source: `public/googlee4acd0bdef57edbb.html`
- production URL: `/googlee4acd0bdef57edbb.html`

Do not remove it.

## Sitemap / robots state

Sitemap: `https://nj-property-tax-relief-lab.pages.dev/sitemap.xml`

Independent checks:
- browser-accessible
- HTTP 200
- `Content-Type: application/xml`
- expected four URLs present

Robots: `https://nj-property-tax-relief-lab.pages.dev/robots.txt`

Observed content:

    User-agent: *
    Allow: /
    Sitemap: https://nj-property-tax-relief-lab.pages.dev/sitemap.xml

Search Console currently reports the sitemap as `Couldn't fetch` / `Sitemap could not be read`, despite independent checks being healthy.

Decision: do not modify the sitemap merely because of that Search Console status. Observe first.

## Google crawl/indexing observations

Homepage:
- Google has crawled it
- crawl allowed: Yes
- page fetch: Successful
- indexing allowed: Yes
- Google-selected canonical: inspected URL
- current state: `Crawled – currently not indexed`

A manual Request Indexing attempt hit Google's daily quota.

Decision:
- do not repeatedly resubmit
- let natural indexing behavior become part of the experiment
- use manual indexing sparingly

## Current experiment status

`observing`

The current question is:

> Will Google naturally index, surface, and send traffic to a brand-new, useful, low-cost utility with no established authority?

## Monetization / experiment role

Direct monetization is weak for this first experiment. Its primary economic value is:
- SEO/discovery laboratory
- proof of the reusable Number Eleven Works build/deploy/telemetry pipeline

## Immediate next actions

1. Recheck Search Console without changing the site.
2. Recheck sitemap processing status.
3. Recheck homepage indexing state.
4. If manual Request Indexing is available, make at most one deliberate homepage request.
5. Observe natural discovery/indexing for the other pages.
6. Record first meaningful Search Console and Cloudflare telemetry.
7. Do not expand the product merely because traffic has not appeared immediately.

## Resume instruction

A fresh chat should read this document plus existing architecture, operations, requirements, and source-authority docs before changing code.
