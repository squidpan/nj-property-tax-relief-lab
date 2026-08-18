from njptr_lab.validator import has_errors, validate_repository


def test_repository_data_validates_without_errors():
    issues = validate_repository()
    assert not has_errors(issues), issues
