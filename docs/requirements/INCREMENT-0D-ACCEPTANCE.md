# Increment 0D — UX Refinement Acceptance Criteria

## Goal

Refine the functional 0C vertical slice into a small public-facing decision aid that is easier to use before deployment.

## Acceptance criteria

- The homepage presents the filing deadline in human-readable form.
- The decision tool hides Senior Freeze questions when the applicant cannot be a simplified Senior Freeze candidate.
- The decision tool hides Stay NJ questions when the applicant cannot be a simplified Stay NJ candidate.
- Hidden conditional inputs are disabled so they do not participate in validation.
- Required visible questions receive clear validation feedback.
- Results distinguish `candidate`, `not_candidate`, and `needs_official_review`.
- Results emphasize that the output is a simplified filing-path/candidate-program check rather than a final eligibility determination.
- A clear CTA sends the visitor to the site's curated official NJ resources.
- Result changes are announced through an `aria-live` region.
- Keyboard focus is moved to validation errors or results when appropriate.
- Mobile layouts collapse multi-column cards and actions into a single-column presentation.
- No personal data collection, persistence, API call, database, or authentication is introduced.
- Existing structured YAML remains the source for executable numeric thresholds.
