from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from .loader import load_programs, load_ruleset, load_sources


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    code: str
    message: str


def validate_repository(root: Path | None = None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    sources = load_sources(root)
    programs = load_programs(root)
    ruleset = load_ruleset(root)

    if len(sources) != len(set(sources)):
        issues.append(ValidationIssue("ERROR", "duplicate-source-id", "Duplicate source IDs found."))

    if len(programs) != len(set(programs)):
        issues.append(ValidationIssue("ERROR", "duplicate-program-id", "Duplicate program IDs found."))

    for source_id, source in sources.items():
        url = source.get("url", "")
        parsed = urlparse(str(url))
        if parsed.scheme != "https":
            issues.append(ValidationIssue("ERROR", "source-url-not-https", f"{source_id}: source URL must use HTTPS"))
        if not source.get("verified_date"):
            issues.append(ValidationIssue("ERROR", "missing-verification-date", f"{source_id}: verified_date is required"))
        if source.get("authority_level") not in {"AUTH-1", "AUTH-2", "AUTH-3", "AUTH-4"}:
            issues.append(ValidationIssue("ERROR", "invalid-authority-level", f"{source_id}: invalid authority level"))

    for program_id, program in programs.items():
        if program.get("tax_year") != 2025:
            issues.append(ValidationIssue("ERROR", "unexpected-tax-year", f"{program_id}: tax_year must be 2025 for this ruleset"))
        if not program.get("filing_deadline"):
            issues.append(ValidationIssue("ERROR", "missing-deadline", f"{program_id}: filing_deadline is required"))
        source_refs = program.get("sources", [])
        if not source_refs:
            issues.append(ValidationIssue("ERROR", "missing-program-sources", f"{program_id}: at least one source is required"))
            continue
        missing = [source_id for source_id in source_refs if source_id not in sources]
        for source_id in missing:
            issues.append(ValidationIssue("ERROR", "unknown-source-reference", f"{program_id}: unknown source {source_id}"))
        executable_authorities = {
            sources[source_id].get("authority_level")
            for source_id in source_refs
            if source_id in sources
        }
        if not executable_authorities.intersection({"AUTH-1", "AUTH-2"}):
            issues.append(ValidationIssue("ERROR", "no-primary-authority", f"{program_id}: executable rules need AUTH-1 or AUTH-2 support"))

    for source_id in ruleset.get("sources", []):
        if source_id not in sources:
            issues.append(ValidationIssue("ERROR", "unknown-ruleset-source", f"Ruleset references unknown source {source_id}"))

    expected_statuses = {"candidate", "not_candidate", "needs_official_review"}
    statuses = set(ruleset.get("status_values", []))
    if statuses != expected_statuses:
        issues.append(ValidationIssue("ERROR", "invalid-status-vocabulary", f"Expected status vocabulary {sorted(expected_statuses)}"))

    today = date.today()
    for source_id, source in sources.items():
        verified = source.get("verified_date")
        if isinstance(verified, date) and (today - verified).days > 90:
            issues.append(ValidationIssue("WARNING", "stale-source-verification", f"{source_id}: verified more than 90 days ago"))

    return issues


def has_errors(issues: list[ValidationIssue]) -> bool:
    return any(issue.severity == "ERROR" for issue in issues)
