---
id: NJPTR-STD-RULE-DATA-001
type: standard
status: active
---

# Rule and Program Data Standard

## Purpose

Keep executable public-policy facts separate from presentation and preserve source traceability.

## Principles

1. A program or executable ruleset must cite source IDs from `data/sources/sources.yaml`.
2. Executable eligibility rules require at least one AUTH-1 or AUTH-2 source.
3. The evaluator returns `candidate`, `not_candidate`, or `needs_official_review`; it does not declare legal eligibility.
4. Special/complex situations are routed to official review rather than guessed.
5. Current post-enactment official program pages take precedence over older instructions when the older source explicitly states that later appropriations may change eligibility or benefits.
6. Presentation templates and browser code must not become alternate sources of truth for program thresholds.
7. Rule changes require corresponding tests and source-registry updates.

## Current conflict note

The 2025 PAS-1 instructions were prepared before final FY2027 appropriations. The current Stay NJ program page reflects the June 30, 2026 appropriations and therefore controls the MVP's current $200,000 income threshold.
