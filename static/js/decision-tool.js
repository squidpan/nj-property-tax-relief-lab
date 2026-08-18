(() => {
  "use strict";

  const form = document.querySelector("#decision-form");
  if (!form) return;

  const result = document.querySelector("#decision-result");
  const errorBox = document.querySelector("#form-error");
  const freezeSections = [...form.querySelectorAll('[data-for="senior-freeze"]')];
  const staySections = [...form.querySelectorAll('[data-for="stay-nj"]')];

  const radioValue = (name) => {
    const selected = form.querySelector(`input[name="${name}"]:checked`);
    return selected ? selected.value : null;
  };

  const numberValue = (name) => {
    const input = form.elements[name];
    if (!input || input.value === "") return null;
    const value = Number(input.value);
    return Number.isFinite(value) ? value : null;
  };

  const setVisible = (elements, visible) => {
    elements.forEach((el) => {
      el.hidden = !visible;
      el.querySelectorAll("input").forEach((input) => {
        input.disabled = !visible;
      });
    });
  };

  function candidatePaths() {
    const type = radioValue("applicant_type");
    const age = numberValue("age");
    const disability = radioValue("disability") === "yes";
    const seniorOrDisabled = age !== null && (age >= 65 || disability);

    return {
      seniorOrDisabled,
      freeze: seniorOrDisabled && (type === "homeowner" || type === "mobile_home_owner"),
      stay: age !== null && age >= 65 && type === "homeowner",
    };
  }

  function updateProgressiveQuestions() {
    const paths = candidatePaths();
    setVisible(freezeSections, paths.freeze);
    setVisible(staySections, paths.stay);
  }

  function validateVisibleQuestions() {
    errorBox.hidden = true;
    errorBox.textContent = "";

    const requiredGroups = [
      ["applicant_type", "Choose whether you are a homeowner, renter, or mobile-home owner."],
      ["age", "Enter your age on December 31, 2025."],
      ["disability", "Answer the disability-benefit question."],
      ["nj_income", "Enter your approximate 2025 NJ gross income."],
      ["anchor_residence", "Answer the October 1, 2025 residence question."],
      ["special_case", "Answer the special-circumstance question."],
    ];

    for (const [name, message] of requiredGroups) {
      const element = form.elements[name];
      const missing = element instanceof RadioNodeList ? !radioValue(name) : numberValue(name) === null;
      if (missing) {
        errorBox.textContent = message;
        errorBox.hidden = false;
        errorBox.focus();
        return false;
      }
    }

    const paths = candidatePaths();
    if (paths.freeze) {
      if (!radioValue("freeze_history") || numberValue("income_2024") === null || numberValue("income_2025_total") === null) {
        errorBox.textContent = "Complete the Senior Freeze questions shown for your path, or choose Not sure where available.";
        errorBox.hidden = false;
        errorBox.focus();
        return false;
      }
    }
    if (paths.stay && !radioValue("stay_history")) {
      errorBox.textContent = "Answer the Stay NJ full-year ownership/residence question shown for your path.";
      errorBox.hidden = false;
      errorBox.focus();
      return false;
    }
    return true;
  }

  const statusCard = (name, status, explanation) => {
    const labels = {
      candidate: "Worth checking",
      not_candidate: "Not indicated by this simplified check",
      needs_official_review: "Official review needed",
    };
    return `<article class="result-card status-${status}">
      <div class="result-card-heading"><h3>${name}</h3><span class="status-badge">${labels[status]}</span></div>
      <p>${explanation}</p>
    </article>`;
  };

  function evaluate() {
    const cfg = window.NJPTR_CONFIG;
    const type = radioValue("applicant_type");
    const age = numberValue("age");
    const disability = radioValue("disability") === "yes";
    const njIncome = numberValue("nj_income");
    const anchorResidence = radioValue("anchor_residence") === "yes";
    const special = radioValue("special_case") === "yes";
    const paths = candidatePaths();

    const filingPath = paths.seniorOrDisabled ? "PAS-1" : "ANCHOR";
    const statuses = {};

    if (special) {
      ["anchor", "senior_freeze", "stay_nj"].forEach((key) => statuses[key] = "needs_official_review");
    } else {
      const anchorMax = type === "homeowner" ? cfg.anchor.homeownerIncomeMax : cfg.anchor.renterIncomeMax;
      statuses.anchor = anchorResidence && njIncome <= anchorMax ? "candidate" : "not_candidate";

      if (!paths.freeze) {
        statuses.senior_freeze = "not_candidate";
      } else if (radioValue("freeze_history") === "unsure") {
        statuses.senior_freeze = "needs_official_review";
      } else {
        statuses.senior_freeze =
          radioValue("freeze_history") === "yes" &&
          numberValue("income_2024") <= cfg.seniorFreeze.income2024Max &&
          numberValue("income_2025_total") <= cfg.seniorFreeze.income2025Max
            ? "candidate" : "not_candidate";
      }

      if (!paths.stay) {
        statuses.stay_nj = "not_candidate";
      } else if (radioValue("stay_history") === "unsure") {
        statuses.stay_nj = "needs_official_review";
      } else {
        statuses.stay_nj =
          radioValue("stay_history") === "yes" && njIncome <= cfg.stayNJ.income2025Max
            ? "candidate" : "not_candidate";
      }
    }

    return { filingPath, statuses, special };
  }

  function render(outcome) {
    const filingDescription = outcome.filingPath === "PAS-1"
      ? "Your answers point toward the PAS-1 filing path used for seniors and qualifying disability-benefit recipients."
      : "Your answers point toward the regular ANCHOR filing path rather than PAS-1.";

    const officialReview = Object.values(outcome.statuses).includes("needs_official_review");
    result.innerHTML = `
      <p class="eyebrow">YOUR SIMPLIFIED RESULT</p>
      <h2>Likely filing path: ${outcome.filingPath}</h2>
      <p class="result-summary">${filingDescription}</p>
      ${officialReview ? '<div class="notice warning"><strong>Some answers need official review.</strong> This tool intentionally does not guess when a special situation or uncertain rule is involved.</div>' : ""}
      <div class="result-grid">
        ${statusCard("ANCHOR", outcome.statuses.anchor, "Based on the residence type, October 1 residence answer, and simplified income check you entered.")}
        ${statusCard("Senior Freeze", outcome.statuses.senior_freeze, "Based on age/disability, residence type, ownership/residency history, and the simplified income checks when applicable.")}
        ${statusCard("Stay NJ", outcome.statuses.stay_nj, "Based on age, homeowner status, full-year ownership/residency, and the simplified income check when applicable.")}
      </div>
      <div class="official-next-step">
        <h3>Official next step</h3>
        <p>Use this result as a starting point only. The New Jersey Division of Taxation makes the final eligibility and benefit determination.</p>
        <a class="button primary" href="../official-resources/">Go to official NJ resources</a>
      </div>`;
    result.hidden = false;
    result.focus();
    result.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  form.addEventListener("change", updateProgressiveQuestions);
  form.addEventListener("input", updateProgressiveQuestions);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    updateProgressiveQuestions();
    if (!validateVisibleQuestions()) return;
    render(evaluate());
  });
  form.addEventListener("reset", () => {
    window.setTimeout(() => {
      result.hidden = true;
      errorBox.hidden = true;
      updateProgressiveQuestions();
    }, 0);
  });

  updateProgressiveQuestions();
})();
