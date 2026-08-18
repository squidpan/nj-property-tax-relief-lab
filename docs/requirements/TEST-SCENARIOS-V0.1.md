---
id: NJPTR-TEST-SCENARIOS-001
type: test-scenarios
status: draft
project: nj-property-tax-relief-lab
---

# Initial Rule Test Scenarios

These are candidate-program tests, not final legal eligibility determinations.

| Case | Expected simplified result |
|---|---|
| 40-year-old renter, $80K income, qualifying NJ principal residence | ANCHOR candidate; regular ANCHOR path |
| 68-year-old renter, $80K income | ANCHOR candidate; PAS-1 path; Senior Freeze/Stay NJ not candidates |
| 68-year-old homeowner, $90K income, qualifying long-term ownership | ANCHOR + Senior Freeze + Stay NJ candidates; PAS-1 path |
| 68-year-old homeowner, $210K income | ANCHOR may remain candidate; simplified Stay NJ/Senior Freeze income tests exclude |
| 50-year-old homeowner receiving qualifying disability benefits | PAS-1 path; ANCHOR and potential Senior Freeze review; Stay NJ not candidate on age |
| 50-year-old homeowner without qualifying disability | ANCHOR path only |
| 70-year-old renter, $160K income | Simplified ANCHOR income test excludes; Senior Freeze/Stay NJ unavailable |
| 70-year-old mobile-home owner | ANCHOR renter treatment + possible Senior Freeze review; Stay NJ unavailable |

Before these become executable tests, each expected result must be tied to verified structured rules and source IDs.
