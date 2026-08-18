# Architecture v0.2 — Static Site Application Layer

## Flow

Official NJ sources → YAML program/rule/source data → Python validation → Python/Jinja2 site build → static HTML/CSS/JavaScript → static host → Google Search Console.

## Decision-tool boundary

Python remains the source-side validation/build language. The public questionnaire executes entirely in browser JavaScript because the MVP has no requirement for server-side processing or persistence.

Numeric rule configuration used by the browser is generated during the Python build from the structured YAML program data. This reduces drift between displayed decision logic and the source-of-truth data.

## Deliberately absent

- FastAPI/Django
- PostgreSQL
- authentication
- server-side sessions
- user profiles
- submission of questionnaire answers
- personally identifying information

A Motorweb-style server/application architecture remains an evolution path only when a concrete requirement justifies it.
