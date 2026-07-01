## Summary

This paper introduces a method for evaluating unsupervised anonymous record linkage without labeled data. By exploiting a structural constraint—that each individual can have at most one positive outcome (e.g., originate at most one first-lien mortgage)—the authors derive observable lower bounds on precision and relative recall. They demonstrate the approach on HMDA mortgage data, using hierarchical clustering to detect “cross‑applicants” (individuals submitting multiple near‑identical applications) and achieve an estimated 92.3% precision at their preferred specification.

## Strengths

- **Novel theoretical framework.** The paper provides the first derivation (to my knowledge) of observable lower bounds on precision and relative recall in unsupervised record‑linkage settings. The bounds rely only on the observed origination rate and the fraction of clusters with multiple originations, making them practical and adversary‑robust.
- **Broad applicability.** The method is domain‑agnostic and algorithm‑agnostic; it applies to any label‑generating model. The structural constraint it exploits (one positive outcome per individual) appears in many settings: secured loans, insurance, college admissions, job offers, etc.
- **Clear exposition and demonstration.** The intuition behind the bounds is clearly explained, the hierarchical clustering algorithm is well described, and the simulated experiment validates that the feasible lower bound closely tracks the true (infeasible) precision. The real‑world application to 65.5 million HMDA applications demonstrates the method’s scalability and utility.
- **Practical impact.** The identified cross‑applicants enable downstream analyses of fairness, lending standards, and shopping behavior that are otherwise impossible without person‑level identifiers. The paper connects its contribution to concrete, important research questions.

## Weaknesses

### Fatal
None.

### Major
- **Assumption 1 (independence of origination decisions across borrowers) is strong.** Loan approvals are plausibly correlated through macroeconomic conditions, lender‑specific policies, or geographical shocks. While the bound might remain useful under mild violations, the paper does not analyze sensitivity to this assumption. A violation that systematically increases co‑origination among distinct applicants would loosen the bound; one that decreases it would potentially make the bound invalid (over‑optimistic). Some discussion or simulation under correlated approvals would strengthen the work.
- **Recall bound depends on the unknown total number of cross‑applicants \(P_{tot}\).** Corollary 1 gives a bound that is proportional to \(\hat{\alpha}(\theta)N^+(\theta)\), but the constant of proportionality \(1/P_{tot}\) is unknown. The authors note that ranking specifications by \(\hat{\alpha}(\theta)N^+(\theta)\) is valid, but this yields only a relative ordering, not an absolute lower bound on recall. The paper would benefit from at least discussing how \(P_{tot}\) might be approximated or bounded using domain knowledge.
- **The method is demonstrated only on clusters of size 2** (footnote 4). The theoretical bounds are derived for arbitrary cluster sizes, but the empirical implementation discards larger clusters. The paper does not justify this restriction or discuss how the method would extend to clusters of size 3 or more. For many applications, individuals may submit more than two applications; this limitation reduces generality.

### Minor
- **The simulation design closely matches the assumptions**, making the tight alignment between feasible and true precision less surprising. A simulation that relaxes Assumptions 1 or 2 would better test the robustness of the bounds.
- **Uncertainty in the estimated bounds is not discussed.** Both \(\hat{p}\) and \(\hat{p}_m\) are sample quantities; the paper presents point estimates without confidence intervals. Given the large dataset, variability may be small, but a brief treatment (e.g., bootstrap intervals) would improve rigor.
- **The choice of distance weights (over 96 combinations) is treated as a grid search**, but the paper does not explain whether some distance functions are a priori preferable or how to interpret the resulting frontier beyond picking the “knee.” Some guidance for practitioners would be helpful.

### Trivial
None of consequence.

## Nice-to-Haves

- Sensitivity analysis (simulations) for violations of Assumptions 1 and 2.
- A practical recommendation on how to estimate or bound \(P_{tot}\) for the recall bound.
- Extension to clusters of arbitrary size, or a clear justification for restricting to pairs.
- Uncertainty quantification (e.g., bootstrap) for the reported precision lower bound.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that a ubiquitous structural constraint (“at most one positive outcome per entity”) suffices to turn the unobservable false‑positive rate into an observable quantity via the multiple‑origination rate. This principle is simple yet powerful: it transforms an otherwise unsupervised evaluation problem into a supervised‑like assessment using only the outcome labels that are already present in the data. The idea that one can get *guaranteed lower bounds* without any ground‑truth labels is likely to find applications well beyond mortgage data.

## Suggestions

- Provide a simulation where the independence assumption is broken (e.g., by adding a common lender‑level shock to acceptance probabilities) and show that the bound still holds or degrades gracefully.
- Discuss how to obtain a usable lower bound on recall when \(P_{tot}\) is unknown (e.g., by using a conservative upper bound from the data, such as the number of partitions).
- Clarify why clusters larger than size 2 are dropped and whether the same bounds apply if they were retained.

## Score and Decision

The paper makes a genuinely novel theoretical contribution with clear practical value. The weaknesses are not fatal—they point to natural extensions rather than fundamental flaws. The work is well written, the experiments support the claims, and the application is timely and impactful. I recommend acceptance.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>