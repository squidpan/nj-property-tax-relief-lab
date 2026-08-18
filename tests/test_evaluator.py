from njptr_lab.evaluator import ApplicantFacts, CandidateStatus, evaluate


def status_map(result):
    return {item.program_id: item.status for item in result.programs}


def test_40_year_old_renter_anchor_candidate_only():
    result = evaluate(
        ApplicantFacts(
            applicant_type="renter",
            age_at_end_of_2025=40,
            qualifying_disability_benefit=False,
            nj_gross_income_2025=80000,
            occupied_nj_principal_residence_on_2025_10_01=True,
        )
    )
    assert result.filing_path == "ANCHOR"
    statuses = status_map(result)
    assert statuses["anchor"] == CandidateStatus.CANDIDATE
    assert statuses["senior_freeze"] == CandidateStatus.NOT_CANDIDATE
    assert statuses["stay_nj"] == CandidateStatus.NOT_CANDIDATE


def test_68_year_old_homeowner_can_be_candidate_for_all_three():
    result = evaluate(
        ApplicantFacts(
            applicant_type="homeowner",
            age_at_end_of_2025=68,
            qualifying_disability_benefit=False,
            nj_gross_income_2025=90000,
            total_annual_income_2024=90000,
            total_annual_income_2025=90000,
            occupied_nj_principal_residence_on_2025_10_01=True,
            owned_and_lived_since_2022_12_31=True,
            still_owned_and_lived_on_2025_12_31=True,
            owned_and_lived_full_year_2025=True,
        )
    )
    assert result.filing_path == "PAS-1"
    statuses = status_map(result)
    assert all(status == CandidateStatus.CANDIDATE for status in statuses.values())


def test_68_year_old_homeowner_income_210k_only_anchor_candidate():
    result = evaluate(
        ApplicantFacts(
            applicant_type="homeowner",
            age_at_end_of_2025=68,
            qualifying_disability_benefit=False,
            nj_gross_income_2025=210000,
            total_annual_income_2024=210000,
            total_annual_income_2025=210000,
            occupied_nj_principal_residence_on_2025_10_01=True,
            owned_and_lived_since_2022_12_31=True,
            still_owned_and_lived_on_2025_12_31=True,
            owned_and_lived_full_year_2025=True,
        )
    )
    statuses = status_map(result)
    assert statuses["anchor"] == CandidateStatus.CANDIDATE
    assert statuses["senior_freeze"] == CandidateStatus.NOT_CANDIDATE
    assert statuses["stay_nj"] == CandidateStatus.NOT_CANDIDATE


def test_under_65_qualifying_disability_routes_to_pas1():
    result = evaluate(
        ApplicantFacts(
            applicant_type="homeowner",
            age_at_end_of_2025=50,
            qualifying_disability_benefit=True,
            nj_gross_income_2025=70000,
            total_annual_income_2024=70000,
            total_annual_income_2025=70000,
            occupied_nj_principal_residence_on_2025_10_01=True,
            owned_and_lived_since_2022_12_31=True,
            still_owned_and_lived_on_2025_12_31=True,
            owned_and_lived_full_year_2025=True,
        )
    )
    assert result.filing_path == "PAS-1"
    statuses = status_map(result)
    assert statuses["anchor"] == CandidateStatus.CANDIDATE
    assert statuses["senior_freeze"] == CandidateStatus.CANDIDATE
    assert statuses["stay_nj"] == CandidateStatus.NOT_CANDIDATE


def test_mobile_home_owner_can_be_anchor_and_senior_freeze_but_not_stay_nj():
    result = evaluate(
        ApplicantFacts(
            applicant_type="mobile_home_owner",
            age_at_end_of_2025=70,
            qualifying_disability_benefit=False,
            nj_gross_income_2025=80000,
            total_annual_income_2024=80000,
            total_annual_income_2025=80000,
            occupied_nj_principal_residence_on_2025_10_01=True,
            owned_and_lived_since_2022_12_31=True,
            still_owned_and_lived_on_2025_12_31=True,
            owned_and_lived_full_year_2025=True,
        )
    )
    statuses = status_map(result)
    assert statuses["anchor"] == CandidateStatus.CANDIDATE
    assert statuses["senior_freeze"] == CandidateStatus.CANDIDATE
    assert statuses["stay_nj"] == CandidateStatus.NOT_CANDIDATE


def test_special_case_returns_official_review():
    result = evaluate(
        ApplicantFacts(
            applicant_type="homeowner",
            age_at_end_of_2025=70,
            qualifying_disability_benefit=False,
            special_case=True,
        )
    )
    statuses = status_map(result)
    assert all(status == CandidateStatus.NEEDS_OFFICIAL_REVIEW for status in statuses.values())
