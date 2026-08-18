# Architecture v0.3 — Progressive Decision UX

Increment 0D keeps the static architecture established in v0.2.

The UX now treats the questionnaire as a decision tree rather than a flat government-style form. JavaScript derives which program-specific questions are relevant from residence type, age, and qualifying-disability answers. Irrelevant sections are hidden and their inputs disabled.

The result vocabulary remains aligned with the Python domain model:

- `candidate`
- `not_candidate`
- `needs_official_review`

This increment does not introduce server-side processing or persistence. Numeric thresholds continue to be generated from validated YAML during the Python/Jinja build.

The public application remains intentionally simpler than a future Motorweb-style full-stack application. Server/API/database architecture should be introduced only when a demonstrated requirement needs it.
