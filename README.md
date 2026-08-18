# NJ Property Tax Relief SEO Lab

A small, production-oriented experiment for publishing trustworthy New Jersey property-tax-relief guidance and a browser-side decision aid.

## Current objective

Prove an end-to-end reusable pipeline:

1. Authoritative source research
2. Structured program/rule data
3. Python validation and build tooling
4. Jinja2 static-site generation
5. Browser-side decision logic with no personal-data collection
6. Static deployment
7. Google Search Console measurement
8. Python-assisted analysis and iteration

## Architectural constraints for MVP

- Python 3.13
- Static site first
- Jinja2 for page generation
- YAML/JSON/Markdown for source data and content
- Vanilla JavaScript for browser interaction
- No database
- No FastAPI/Django server
- No authentication
- No collection of names, addresses, SSNs, tax IDs, banking data, ID.me credentials, or tax-return uploads
- Official NJ sources are authoritative for executable eligibility rules

## Status

Foundation scaffold only. Program rules are not yet implemented.

See:

- `docs/context/PROJECT-CONTEXT.md`
- `docs/requirements/MVP-REQUIREMENTS.md`
- `docs/architecture/ARCHITECTURE-V0.1.md`
- `docs/adr/ADR-001-STATIC-PYTHON-JINJA-MVP.md`
- `docs/standards/SOURCE-AUTHORITY-STANDARD.md`
- `docs/research/OFFICIAL-SOURCE-REGISTRY.md`
