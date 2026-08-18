from pathlib import Path

from njptr_lab.site_builder import build_site


def test_build_creates_public_pages(tmp_path: Path):
    output = build_site(tmp_path / "site")
    expected = [
        "index.html",
        "which-application/index.html",
        "programs/index.html",
        "official-resources/index.html",
        "sitemap.xml",
        "robots.txt",
        "static/css/site.css",
        "static/js/decision-tool.js",
        "static/js/decision-config.js",
    ]
    for relative in expected:
        assert (output / relative).is_file(), relative


def test_generated_decision_config_uses_structured_rule_values(tmp_path: Path):
    output = build_site(tmp_path / "site")
    config = (output / "static/js/decision-config.js").read_text(encoding="utf-8")
    assert '"homeownerIncomeMax": 250000' in config
    assert '"renterIncomeMax": 150000' in config
    assert '"income2025Max": 172475' in config
    assert '"income2025Max": 200000' in config


def test_pages_include_independent_site_disclaimer(tmp_path: Path):
    output = build_site(tmp_path / "site")
    html = (output / "index.html").read_text(encoding="utf-8")
    assert "not affiliated with the State of New Jersey" in html
    assert "does not determine final eligibility" in html


def test_sitemap_uses_requested_base_url(tmp_path: Path):
    output = build_site(tmp_path / "site", base_url="https://example.com")
    sitemap = (output / "sitemap.xml").read_text(encoding="utf-8")
    assert "https://example.com/which-application/" in sitemap

def test_official_resources_render_source_titles_not_python_methods(tmp_path: Path):
    output = build_site(tmp_path / "site")
    html = (output / "official-resources/index.html").read_text(encoding="utf-8")
    assert "ANCHOR Program - Eligibility" in html
    assert "Senior Freeze Eligibility Requirements" in html
    assert "Stay NJ - Property Tax Relief for Senior Citizens" in html
    assert "built-in method title" not in html
