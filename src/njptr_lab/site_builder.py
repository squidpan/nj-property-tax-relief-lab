from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .loader import load_programs, load_sources

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = REPO_ROOT / "templates"
STATIC_DIR = REPO_ROOT / "static"


def _display_date(value: str | date) -> str:
    parsed = value if isinstance(value, date) else date.fromisoformat(str(value))
    return f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}"


def _environment() -> Environment:
    return Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "xml"]),
    )


def _decision_config(programs: dict) -> dict:
    anchor = programs["anchor"]
    freeze = programs["senior_freeze"]
    stay = programs["stay_nj"]
    return {
        "anchor": {
            "homeownerIncomeMax": anchor["income"]["homeowner_max_nj_gross_income"],
            "renterIncomeMax": anchor["income"]["renter_max_nj_gross_income"],
        },
        "seniorFreeze": {
            "income2024Max": freeze["income"]["total_annual_income_2024_max"],
            "income2025Max": freeze["income"]["total_annual_income_2025_max"],
        },
        "stayNJ": {"income2025Max": stay["income"]["max"]}, 
    }


def build_site(output_dir: Path | None = None, base_url: str = "https://example.com") -> Path:
    output = output_dir or (REPO_ROOT / "site")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    programs = load_programs()
    sources = load_sources()
    env = _environment()

    deadline = programs["anchor"]["filing_deadline"]
    common = {
        "root": "/",
        "programs": programs,
        "sources": sources,
        "filing_deadline": deadline,
        "filing_deadline_display": _display_date(deadline),
    }

    pages = {
        "index.html": "index.html",
        "which-application/index.html": "which-application.html",
        "programs/index.html": "programs.html",
        "official-resources/index.html": "official-resources.html",
    }
    for relative, template_name in pages.items():
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        page_context = dict(common)
        page_context["root"] = "../" if relative.count("/") else "./"
        target.write_text(env.get_template(template_name).render(**page_context), encoding="utf-8")

    shutil.copytree(STATIC_DIR, output / "static", dirs_exist_ok=True)
    config = "window.NJPTR_CONFIG = " + json.dumps(_decision_config(programs), indent=2) + ";\n"
    (output / "static/js/decision-config.js").write_text(config, encoding="utf-8")

    base = base_url.rstrip("/")
    paths = ["", "which-application/", "programs/", "official-resources/"]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{base}/{path}</loc></url>\n" for path in paths)
    sitemap += "</urlset>\n"
    (output / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (output / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + base + "/sitemap.xml\n", encoding="utf-8")
    return output
