---
id: NJPTR-STD-SOURCE-001
type: standard
status: draft
project: nj-property-tax-relief-lab
---

# Source Authority Standard

## Purpose

Define which sources may support executable program rules and how conflicts are handled.

## Authority classes

### AUTH-1 — Current official program page

Current operational guidance published by the New Jersey Division of Taxation or another directly responsible NJ government authority.

### AUTH-2 — Current official application/form instructions

Official instructions and forms. High authority, but may be superseded by later enacted budget or program changes when the document itself anticipates such changes.

### AUTH-3 — Current official FAQ, notice, or press release

May support interpretation, examples, timing, or process details.

### AUTH-4 — Third-party source

May support competitive or SEO research. Must never be the sole authority for executable eligibility logic.

## Executable-rule requirement

Every executable eligibility rule must reference at least one AUTH-1 or AUTH-2 source.

## Conflict handling

A conflict must be documented explicitly. Do not silently choose a value.

When an earlier official document states that later enacted changes may supersede it, a current post-enactment official program page may take precedence.

## Source lifecycle

Sources should support these statuses:

- `current`
- `superseded`
- `historical`
- `needs_review`

## Verification

Each source record should include a `verified_date` and enough metadata to explain why the source is considered current.
