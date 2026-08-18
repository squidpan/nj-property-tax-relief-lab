from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .loader import load_programs, load_ruleset, load_sources, repo_root
from .validator import has_errors, validate_repository


@dataclass(frozen=True)
class PageSpec:
    output: str
    template: str
    title: str
    description: str


PAGES = (
    PageSpec("index.html", "index.html", "NJ Property Tax Relief 2026", "A simplified guide to ANCHOR, Senior Freeze, Stay NJ, and the filing path that may apply to you."),
    PageSpec("which-application/index.html", "which-application.html", "Which NJ Property Tax Relief Application Do I Use?", "A simple decision aid for the ANCHOR and PAS-1 filing paths."),
    PageSpec("programs/index.html", "programs.html", "NJ Property Tax Relief Programs Compared", "Compare ANCHOR, Senior Freeze, and Stay NJ for the 2025 tax year."),
    PageSpec("official-resources/index.html", "official-resources.html", "Official NJ Property Tax Relief Resources", "Official New Jersey Division of Taxation resources for ANCHOR, Senior Freeze, Stay NJ, and PAS-1."),
)


def _public_source(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": source["source_id"],
        "title": source["title"],
        "url": source["url"],
        "authority": source["authority"],
        "verified_date": str(source["verified_date"]),
        "status": source["status"],
    }


def _decision_config(programs: dict[str, dict[str, Any]], ruleset: dict[str, Any]) -> dict[str, Any]:
    anchor = programs["anchor"]
    senior = programs["senior_freeze"]
    stay = programs["stay_nj"]
    return {
        "taxYear": ruleset["tax_year"],
        "filingDeadline": str(ruleset["filing_deadline"]),
        "anchor": {
            "referenceDate": str(anchor["reference_date"]),
            "homeownerIncomeMax": anchor["income"]["homeowner_max_nj_gross_income"],
            "renterIncomeMax": anchor["income"]["renter_max_nj_gross_income"],
        },
        "seniorFreeze": {
            "ageMin": senior["age_or_disability"]["age_at_least_on_2025_12_31"],
            "continuityDate": str(senior["ownership_and_residency"]["owned_and_lived_since_on_or_before"]),
            "income2024Max": senior["income"]["total_annual_income_2024_max"],
            "income2025Max": senior["income"]["total_annual_income_2025_max"],
        },
        "stayNJ": {
            "ageMin": stay["age"]["age_during_2025_at_least"],
            "income2025Max": stay["income"]["max"],
        },
    }


def build_site(output_dir: Path | None = None, base_url: str = "https://example.invalid") -> Path:
    root = repo_root()
    output_dir = output_dir or root / "site"

    issues = validate_repository(root)
    if has_errors(issues):
        raise RuntimeError(f"Repository validation failed with {len(issues)} issue(s)")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    programs = load_programs(root)
    ruleset = load_ruleset(root)
    sources = load_sources(root)
    public_sources = [_public_source(source) for source in sources.values() if source["status"] != "historical"]

    env = Environment(
        loader=FileSystemLoader(root / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    common = {
        "programs": programs,
        "ruleset": ruleset,
        "sources": public_sources,
        "filing_deadline": str(ruleset["filing_deadline"]),
        "base_url": base_url.rstrip("/"),
    }

    for page in PAGES:
        destination = output_dir / page.output
        destination.parent.mkdir(parents=True, exist_ok=True)
        html = env.get_template(page.template).render(
            **common,
            page_title=page.title,
            page_description=page.description,
            canonical_path="/" if page.output == "index.html" else f"/{page.output.removesuffix('index.html')}",
        )
        destination.write_text(html, encoding="utf-8")

    static_dest = output_dir / "static"
    shutil.copytree(root / "static", static_dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns("README.md"))

    config = _decision_config(programs, ruleset)
    (static_dest / "js").mkdir(parents=True, exist_ok=True)
    (static_dest / "js" / "decision-config.js").write_text(
        "window.NJPTR_CONFIG = " + json.dumps(config, indent=2) + ";\n",
        encoding="utf-8",
    )

    sitemap_urls = []
    for page in PAGES:
        path = "/" if page.output == "index.html" else f"/{page.output.removesuffix('index.html')}"
        sitemap_urls.append(f"  <url><loc>{base_url.rstrip('/')}{path}</loc></url>")
    sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(sitemap_urls) + "\n</urlset>\n"
    (output_dir / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (output_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base_url.rstrip('/')}/sitemap.xml\n", encoding="utf-8")

    return output_dir
