(() => {
  "use strict";
  const form = document.getElementById("relief-form");
  const result = document.getElementById("result");
  if (!form || !result || !window.NJPTR_CONFIG) return;
  const cfg = window.NJPTR_CONFIG;
  const value = (name) => form.elements[name].value;
  const yes = (name) => value(name) === "yes";
  const money = (name) => Number(value(name));
  const statusLabel = { candidate: "Candidate under simplified checks", not_candidate: "Not a candidate under simplified checks", needs_official_review: "Official review recommended" };

  function specialReview() { return { status: "needs_official_review", reason: "Your situation includes an exception that this simplified tool intentionally does not adjudicate." }; }
  function anchor(f) {
    if (f.special) return specialReview();
    if (!f.octResidence) return { status: "not_candidate", reason: "The simplified ANCHOR check requires the NJ home to have been your principal residence on October 1, 2025." };
    const limit = f.type === "homeowner" ? cfg.anchor.homeownerIncomeMax : cfg.anchor.renterIncomeMax;
    if (f.njIncome > limit) return { status: "not_candidate", reason: `2025 NJ gross income is above the simplified ${f.type === "homeowner" ? "homeowner" : "renter/mobile-home"} limit of $${limit.toLocaleString()}.` };
    return { status: "candidate", reason: "The simplified residence and income checks passed." };
  }
  function seniorFreeze(f) {
    if (f.special) return specialReview();
    if (f.type === "renter") return { status: "not_candidate", reason: "Renters are not included in the simplified Senior Freeze model." };
    if (f.age < cfg.seniorFreeze.ageMin && !f.disability) return { status: "not_candidate", reason: "The simplified age/disability requirement is not met." };
    if (f.continuity === "unknown") return { status: "needs_official_review", reason: "Ownership/residency continuity is uncertain." };
    if (f.continuity !== "yes") return { status: "not_candidate", reason: "The simplified ownership/residency continuity requirement is not met." };
    if (f.income2024 > cfg.seniorFreeze.income2024Max || f.income2025 > cfg.seniorFreeze.income2025Max) return { status: "not_candidate", reason: "One or both simplified Senior Freeze income limits are exceeded." };
    return { status: "candidate", reason: "The simplified age/disability, continuity, and income checks passed." };
  }
  function stayNJ(f) {
    if (f.special) return specialReview();
    if (f.type !== "homeowner") return { status: "not_candidate", reason: "The simplified Stay NJ model is for homeowners." };
    if (f.age < cfg.stayNJ.ageMin) return { status: "not_candidate", reason: "The simplified Stay NJ age requirement is not met." };
    if (f.fullYear === "unknown") return { status: "needs_official_review", reason: "Full-year 2025 ownership/occupancy is uncertain." };
    if (f.fullYear !== "yes") return { status: "not_candidate", reason: "The simplified full-year 2025 ownership/occupancy requirement is not met." };
    if (f.income2025 > cfg.stayNJ.income2025Max) return { status: "not_candidate", reason: `2025 income is above the current simplified $${cfg.stayNJ.income2025Max.toLocaleString()} limit.` };
    return { status: "candidate", reason: "The simplified homeowner, age, residency, and income checks passed." };
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const facts = {
      type: value("applicantType"), age: Number(value("age")), disability: yes("disability"), njIncome: money("njIncome"),
      octResidence: yes("octResidence"), continuity: value("continuity"), income2024: money("income2024"), income2025: money("income2025"),
      fullYear: value("fullYear"), special: yes("specialCase")
    };
    const filingPath = facts.age >= 65 || facts.disability ? "PAS-1" : "ANCHOR";
    const programs = [["ANCHOR", anchor(facts)], ["Senior Freeze", seniorFreeze(facts)], ["Stay NJ", stayNJ(facts)]];
    result.innerHTML = `<h2>Your simplified result</h2><p><strong>Likely filing path to investigate: ${filingPath}</strong></p><div class="result-grid">${programs.map(([name, r]) => `<div class="status"><h3>${name}</h3><p><strong>${statusLabel[r.status]}</strong></p><p>${r.reason}</p></div>`).join("")}</div><p>This result is informational only. Continue with the <a href="/official-resources/">official New Jersey resources</a> for current instructions and final eligibility.</p>`;
    result.hidden = false;
    result.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
