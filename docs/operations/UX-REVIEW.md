# Increment 0D UX Review

After applying the increment:

1. Run `python scripts/validate_data.py`.
2. Run `pytest`.
3. Run `python scripts/build_site.py`.
4. Preview with `python -m http.server 8000 --directory site`.
5. Check `/` and confirm the deadline reads `November 2, 2026`.
6. Check `/which-application/`.
7. Choose renter, age 40, no disability and confirm Senior Freeze and Stay NJ detail questions are hidden.
8. Choose homeowner, age 68 and confirm both program-specific sections appear.
9. Choose a special circumstance and confirm the result routes the visitor toward official review.
10. Narrow the browser window to a phone-like width and confirm cards/actions become single-column.

Stop the local server with Ctrl+C when finished.
