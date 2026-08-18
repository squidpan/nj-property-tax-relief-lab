from pathlib import Path

from njptr_lab.site_builder import build_site


def test_homepage_uses_human_readable_deadline(tmp_path: Path):
    output = build_site(tmp_path / "site")
    html = (output / "index.html").read_text(encoding="utf-8")
    assert "November 2, 2026" in html
    assert "Current filing deadline:</strong> 2026-11-02" not in html


def test_decision_page_has_progressive_sections_and_accessible_result(tmp_path: Path):
    output = build_site(tmp_path / "site")
    html = (output / "which-application/index.html").read_text(encoding="utf-8")
    assert 'data-for="senior-freeze"' in html
    assert 'data-for="stay-nj"' in html
    assert 'aria-live="polite"' in html
    assert 'role="alert"' in html


def test_decision_script_contains_progressive_logic_and_official_cta(tmp_path: Path):
    output = build_site(tmp_path / "site")
    js = (output / "static/js/decision-tool.js").read_text(encoding="utf-8")
    assert "updateProgressiveQuestions" in js
    assert "Go to official NJ resources" in js
    assert "needs_official_review" in js

def test_decision_page_loads_decision_scripts(tmp_path: Path):
    output = build_site(tmp_path / "site")
    html = (output / "which-application/index.html").read_text(encoding="utf-8")
    assert "../static/js/decision-config.js" in html
    assert "../static/js/decision-tool.js" in html
