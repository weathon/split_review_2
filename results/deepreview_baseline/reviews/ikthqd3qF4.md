## Summary

This paper proposes a method to evaluate unsupervised anonymous record linkage without ground-truth labels by deriving observable lower bounds on precision and relative recall. The bounds exploit a structural constraint: in mortgage data, an individual can originate at most one first-lien mortgage. Using a hierarchical clustering algorithm on HMDA data, the method identifies cross-applicants (single individuals submitting multiple near-identical applications) with an estimated precision of 92.3%. The framework is presented as domain- and method-agnostic, with potential applications beyond mortgages.

## Strengths

- **Novel evaluation framework.** The idea of bounding precision and recall using only observable origination outcomes and the structural constraint (max one positive outcome per entity) is clever and practically useful. It addresses a real gap in unsupervised record linkage where no labels are available for tuning or model comparison.

- **Theoretical grounding.** The derivation is clear and the bounds are method-agnostic, applying to any label-generating algorithm. The correction for dropping clusters with multiple originations (Eq. 1) is a nice practical refinement.

- **Practical relevance.** The application to HMDA data is well-motivated, and the method scales to tens of millions of records using efficient agglomerative clustering. The precision–sample-size frontier (Figure 5) provides an actionable way to choose tuning parameters.

## Weaknesses

### Major

1. **Strong independence assumption (Assumption 1).** The bound relies on the assumption that origination decisions are independent across borrowers. In practice, origination outcomes may be correlated (e.g., due to shared lender policies, local economic conditions, or time trends). The paper acknowledges that Assumptions 1 and 2 together give `Pr[Mult|False] > p^2` (Lemma 1), but does not discuss how violations might affect the bound or whether the bound remains conservative under plausible dependence. Sensitivity analysis or a discussion of when this assumption is reasonable would strengthen the work.

2. **Recall bound is not used empirically.** Corollary 1 provides a lower bound on relative recall, but the empirical application only reports precision and sample size. Recall is mentioned in the abstract (“only minimal loss in relative recall”) but never computed or bounded on the real data. This undercuts one of the claimed contributions and makes the evaluation incomplete.

3. **Single-domain demonstration.** While the method is claimed to be domain-agnostic, it is only demonstrated on one dataset (mortgage applications under HMDA). A second application (e.g., to insurance, college admissions, or synthetic data with different structural constraints) would significantly strengthen the claim of generality.

### Minor

1. **Terminology imprecision.** The paper frequently refers to the bound as “estimated precision” (e.g., “an estimated 92.3% precision”) rather than “lower bound on precision.” In the simulation, this distinction is clear, but in the application section the language could mislead readers into thinking these are unbiased estimates rather than worst-case bounds. Consistent terminology would avoid confusion.

2. **No uncertainty quantification.** The lower bound is computed from empirical estimates `\hat{p}` and `\hat{p}_m`, which have sampling variance. The paper does not provide confidence intervals or any measure of uncertainty around the claimed 92.3% figure.

3. **Absence of baseline comparisons.** The paper does not compare against any alternative record linkage approach (e.g., deterministic rules, probabilistic linkage, or other clustering methods). While the focus is on the evaluation framework, a brief comparison would contextualize the results and show that the bound is informative relative to what is achievable with other methods.

### Trivial

None.

## Nice-to-Haves

- Release anonymized code for the bounding computation (even if the full data is confidential) to aid reproducibility.
- Test robustness of the bound under simulated violations of the independence assumption.
- Apply the recall bound in the empirical section by estimating `P_tot` (or a plausible range) to demonstrate its practical usage.
- Extend the method to clusters of size >2 (the paper restricts to size-2 clusters).

## Novel Insights

The core insight—that a structural constraint like “at most one positive outcome per entity” can transform an unobservable false-positive rate into an observable bound using only the frequency of double-success clusters—is both simple and powerful. This avoids the usual need for expensive manual labeling or synthetic ground truth. The idea connects widely-available transactional data (origination flags) to evaluation of unsupervised matching, opening the door to principled tuning in many privacy-constrained or cross-institutional settings. The paper’s demonstration on mortgage data is credible and the precision–sample-size trade-off is clearly visualized.

## Suggestions

1. Re-label the reported 92.3% figure as a “lower bound on precision” consistently throughout the text.
2. Include an empirical recall bound for the preferred specification using a conservative estimate of `P_tot` (e.g., derived from cluster counts or external benchmarks) to fully demonstrate the scope of Corollary 1.
3. Add a brief discussion on the plausibility of the independence assumption in the mortgage context and potential ways to relax it (e.g., by using cluster-level fixed effects or block bootstrap).
4. For a stronger claim of domain agnosticism, test the method on a second dataset with a different structural constraint (e.g., insurance policies, college admissions).

## Score and Decision

Score: 6  
Decision: Accept

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>