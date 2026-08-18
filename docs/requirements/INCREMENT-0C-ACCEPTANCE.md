# Increment 0C Acceptance Criteria — Static Site and Decision Aid

## Objective

Turn the validated 0B rule/data layer into a usable static website without introducing a server, database, authentication, or personal-data collection.

## Acceptance criteria

- Python builds the site into the ignored `site/` directory.
- The build fails if repository data has validation errors.
- Public pages exist for the home page, application-path decision aid, program comparison, and official resources.
- The decision aid executes in the browser and does not submit user answers to a server.
- Browser configuration values are generated from structured program/rule data rather than hand-maintained numeric constants in the page template.
- The UI uses candidate/not-candidate/official-review language and does not claim final eligibility.
- Every page displays the independent-site disclaimer.
- `sitemap.xml` and `robots.txt` are generated.
- The site is usable at mobile widths.
- Automated tests cover build output, structured configuration generation, disclaimer presence, and canonical sitemap URL generation.
