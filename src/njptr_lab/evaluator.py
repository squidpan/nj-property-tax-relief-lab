from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class CandidateStatus(StrEnum):
    CANDIDATE = "candidate"
    NOT_CANDIDATE = "not_candidate"
    NEEDS_OFFICIAL_REVIEW = "needs_official_review"


@dataclass(frozen=True)
class ApplicantFacts:
    applicant_type: str
    age_at_end_of_2025: int
    qualifying_disability_benefit: bool
    nj_gross_income_2025: float | None = None
    total_annual_income_2024: float | None = None
    total_annual_income_2025: float | None = None
    occupied_nj_principal_residence_on_2025_10_01: bool | None = None
    owned_and_lived_since_2022_12_31: bool | None = None
    still_owned_and_lived_on_2025_12_31: bool | None = None
    owned_and_lived_full_year_2025: bool | None = None
    special_case: bool = False


@dataclass(frozen=True)
class ProgramResult:
    program_id: str
    status: CandidateStatus
    reasons: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EvaluationResult:
    filing_path: str
    programs: tuple[ProgramResult, ...]


def determine_filing_path(facts: ApplicantFacts) -> str:
    if facts.age_at_end_of_2025 >= 65 or facts.qualifying_disability_benefit:
        return "PAS-1"
    return "ANCHOR"


def _review(program_id: str, *reasons: str) -> ProgramResult:
    return ProgramResult(program_id, CandidateStatus.NEEDS_OFFICIAL_REVIEW, tuple(reasons))


def _no(program_id: str, *reasons: str) -> ProgramResult:
    return ProgramResult(program_id, CandidateStatus.NOT_CANDIDATE, tuple(reasons))


def _yes(program_id: str, *reasons: str) -> ProgramResult:
    return ProgramResult(program_id, CandidateStatus.CANDIDATE, tuple(reasons))


def evaluate_anchor(facts: ApplicantFacts) -> ProgramResult:
    program_id = "anchor"
    if facts.special_case:
        return _review(program_id, "Special situation requires official NJ guidance.")
    if facts.applicant_type not in {"homeowner", "renter", "mobile_home_owner"}:
        return _review(program_id, "Applicant type is outside the simplified MVP model.")
    if facts.occupied_nj_principal_residence_on_2025_10_01 is not True:
        if facts.occupied_nj_principal_residence_on_2025_10_01 is False:
            return _no(program_id, "Did not occupy the NJ principal residence on October 1, 2025.")
        return _review(program_id, "October 1, 2025 principal-residence status is unknown.")
    if facts.nj_gross_income_2025 is None:
        return _review(program_id, "2025 New Jersey gross income is required for the simplified check.")
    max_income = 250000 if facts.applicant_type == "homeowner" else 150000
    if facts.nj_gross_income_2025 > max_income:
        return _no(program_id, f"2025 NJ gross income exceeds the simplified {facts.applicant_type} limit of ${max_income:,.0f}.")
    return _yes(program_id, "Simplified ANCHOR residence and income checks passed.")


def evaluate_senior_freeze(facts: ApplicantFacts) -> ProgramResult:
    program_id = "senior_freeze"
    if facts.special_case:
        return _review(program_id, "Special situation requires official NJ guidance.")
    if facts.applicant_type not in {"homeowner", "mobile_home_owner"}:
        return _no(program_id, "Senior Freeze is not available to renters in the simplified model.")
    if facts.age_at_end_of_2025 < 65 and not facts.qualifying_disability_benefit:
        return _no(program_id, "Age/disability requirement not met.")
    if facts.owned_and_lived_since_2022_12_31 is not True or facts.still_owned_and_lived_on_2025_12_31 is not True:
        if False in {facts.owned_and_lived_since_2022_12_31, facts.still_owned_and_lived_on_2025_12_31}:
            return _no(program_id, "Simplified ownership/residency continuity requirement not met.")
        return _review(program_id, "Ownership/residency continuity information is incomplete.")
    if facts.total_annual_income_2024 is None or facts.total_annual_income_2025 is None:
        return _review(program_id, "2024 and 2025 total annual income are required for the simplified check.")
    if facts.total_annual_income_2024 > 168268 or facts.total_annual_income_2025 > 172475:
        return _no(program_id, "One or both simplified Senior Freeze income limits are exceeded.")
    return _yes(program_id, "Simplified Senior Freeze age/disability, continuity, and income checks passed.")


def evaluate_stay_nj(facts: ApplicantFacts) -> ProgramResult:
    program_id = "stay_nj"
    if facts.special_case:
        return _review(program_id, "Special situation requires official NJ guidance.")
    if facts.applicant_type != "homeowner":
        return _no(program_id, "Stay NJ is limited to homeowners; renters and mobile-home owners are excluded.")
    if facts.age_at_end_of_2025 < 65:
        return _no(program_id, "Stay NJ age requirement not met in the simplified model.")
    if facts.owned_and_lived_full_year_2025 is not True:
        if facts.owned_and_lived_full_year_2025 is False:
            return _no(program_id, "Full-year 2025 ownership/occupancy requirement not met.")
        return _review(program_id, "Full-year 2025 ownership/occupancy is unknown.")
    income = facts.total_annual_income_2025
    if income is None:
        return _review(program_id, "2025 income is required for the simplified Stay NJ check.")
    if income > 200000:
        return _no(program_id, "2025 income exceeds the current $200,000 Stay NJ limit.")
    return _yes(program_id, "Simplified Stay NJ homeowner, age, residency, and income checks passed.")


def evaluate(facts: ApplicantFacts) -> EvaluationResult:
    return EvaluationResult(
        filing_path=determine_filing_path(facts),
        programs=(
            evaluate_anchor(facts),
            evaluate_senior_freeze(facts),
            evaluate_stay_nj(facts),
        ),
    )
