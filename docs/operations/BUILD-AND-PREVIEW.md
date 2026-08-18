# Build and Preview Runbook

## Validate

Run `python scripts/validate_data.py`.

## Test

Run `pytest`.

## Build locally

Run `python scripts/build_site.py`.

The generated site is written to `site/`, which is ignored by Git.

## Preview locally

From the repository root run `python -m http.server 8000 --directory site` and open `http://127.0.0.1:8000/`.

Stop the preview server with Ctrl+C.

## Production build

Before deployment, supply the actual public URL so canonical URLs, robots.txt, and sitemap.xml are correct, for example: `python scripts/build_site.py --base-url https://your-domain.example`.
