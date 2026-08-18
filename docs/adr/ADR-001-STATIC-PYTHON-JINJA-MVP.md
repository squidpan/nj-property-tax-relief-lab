---
id: NJPTR-ADR-001
type: adr
status: accepted
project: nj-property-tax-relief-lab
---

# ADR-001 — Use Static Python/Jinja Architecture for MVP

## Decision

Build the MVP as a statically generated website using Python 3.13 and Jinja2, with browser-side JavaScript for the decision aid.

## Drivers

- Lowest practical hosting cost
- Small attack surface
- No requirement for authentication or persistence
- No requirement to collect private user data
- Strong fit for deterministic validation and testing
- Easy migration to a fuller Python application later if necessary

## Alternatives considered

### WordPress

Rejected for MVP because its CMS/plugin/runtime overhead is not required for the initial four-page/tool experiment.

### FastAPI

Deferred because the MVP has no server-side API requirement.

### Django

Deferred because the MVP does not require an admin application, ORM, authentication, or dynamic server rendering.

## Consequences

Positive:

- simple deployment;
- low operating cost;
- deterministic builds;
- version-controlled content and rules.

Tradeoff:

- publishing/admin conveniences normally supplied by a CMS must be implemented only if later required.
