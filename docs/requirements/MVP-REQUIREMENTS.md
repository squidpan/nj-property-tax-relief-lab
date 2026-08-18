---
id: NJPTR-REQ-MVP-001
type: requirements
status: draft
project: nj-property-tax-relief-lab
---

# MVP Requirements

## Epic

### EPIC-01 — Help NJ Residents Navigate 2025 Property Tax Relief

A New Jersey resident should be able to understand the major 2025 property-tax-relief programs, identify the filing path that appears relevant, and reach official State of New Jersey resources without surrendering personal information to this site.

## Features

### FEATURE-01 — Understand the programs

Explain ANCHOR, Senior Freeze, and Stay NJ using current authoritative sources.

### FEATURE-02 — Determine likely filing path

Provide a lightweight decision aid that identifies whether the visitor appears to be in the PAS-1 path or regular ANCHOR path.

### FEATURE-03 — Identify candidate programs

Return one of three states per program:

- `candidate`
- `not_candidate`
- `needs_official_review`

The site must not claim to make a final legal/tax eligibility determination.

### FEATURE-04 — Reach authoritative resources

Every result must provide a clear path to official NJ guidance or filing resources.

### FEATURE-05 — Search discovery and telemetry

Pages must be crawlable, indexable, fast, and suitable for Google Search Console measurement.

## MVP public pages

- `/`
- `/which-application/`
- `/programs/`
- `/official-resources/`

## Privacy requirements

The MVP must not collect or transmit:

- names;
- street addresses;
- SSNs or tax IDs;
- bank information;
- ID.me credentials;
- uploaded tax returns;
- login credentials.

Decision logic should execute in the browser where practical.

## Acceptance constraints

- Executable rules must trace to official NJ sources.
- Known special situations must produce `needs_official_review` rather than invented certainty.
- Conflicting official sources must be resolved explicitly using source precedence and documented rationale.
