---
id: NJPTR-ARCH-001
type: architecture
status: draft
project: nj-property-tax-relief-lab
---

# Architecture v0.1

## Context

The MVP requires authoritative structured content, deterministic validation, a small decision aid, and inexpensive public hosting. It does not require accounts, persistence, server-side sessions, or private user data.

## Logical flow

Authoritative NJ sources
→ structured source registry
→ structured program/rule data
→ Python validation/tests
→ Python/Jinja2 static build
→ HTML/CSS/vanilla JavaScript
→ static hosting
→ Google Search Console
→ analysis and iteration

## Components

### `data/`

Structured source-of-truth data for programs, rules, and source provenance.

### `src/njptr_lab/`

Reusable Python domain/build/validation code.

### `scripts/`

Thin executable entry points for build, validation, and later operational checks.

### `templates/`

Jinja2 templates.

### `content/`

Human-authored page content.

### `static/`

Browser assets: CSS, JavaScript, and images.

### `tests/`

Table-driven rule and validation tests.

### `docs/`

Obsidian-compatible engineering knowledge base.

## Deferred architecture

FastAPI, PostgreSQL, authentication, server-side persistence, and richer application behavior are intentionally deferred. They may be introduced later using Motorweb-style patterns if product requirements justify them.
