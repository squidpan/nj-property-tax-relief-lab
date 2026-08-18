---
id: NJPTR-REQ-INC-0B
status: active
type: requirements
---

# Increment 0B Acceptance Criteria

Increment 0B is complete when:

- authoritative sources are represented in machine-readable YAML;
- ANCHOR, Senior Freeze, and Stay NJ have separate program records;
- executable records cite official source IDs;
- repository validation fails on unknown source references or missing primary authority;
- simplified candidate vocabulary is limited to `candidate`, `not_candidate`, and `needs_official_review`;
- filing path differentiates PAS-1 from the under-65/non-disability ANCHOR path;
- executable tests cover renter, homeowner, disability, income-limit, mobile-home, and special-case scenarios;
- no UI or public claim presents the evaluator as a final eligibility determination;
- `pytest` and `python scripts/validate_data.py` pass before commit.
