## Summary

This paper derives observable lower bounds on precision and relative recall for unsupervised anonymous record linkage by exploiting a structural constraint (e.g., individuals can originate at most one first-lien mortgage). The bounds depend only on predicted labels and the observed rate of clusters containing multiple positive outcomes, making them method-agnostic and applicable without labeled data. The authors instantiate the framework using agglomerative clustering on HMDA mortgage data (2018–2023), reporting an estimated lower-bound precision of 92.3% at their preferred specification.

## Strengths

1. **Novel theoretical contribution (Section 2.2).** Deriving an observable lower bound on precision from the rate of clusters with multiple originations is a clean and elegant idea. The core insight — that Pr[False] = Pr[Mult] / Pr[Mult|False] with Pr[Mult|¬False] = 0 due to the structural constraint — is genuinely novel and well-derived.

2. **Simulation validates the bound against ground truth (Section 3.1).** The close correspondence between true precision (Figure 3a) and the implied lower bound (Figure 4a) provides compelling evidence that the bound is informative when its assumptions hold. The "without date" vs. "with date" comparison demonstrates how additional covariates tighten the bound.

3. **Method-agnostic framework (Remark 1, Section 2).** The bounds depend only on predicted labels, not on the specific clustering algorithm. This means the evaluation framework can be applied to any unsupervised record linkage method, extending the contribution beyond the particular agglomerative clustering implementation.

4. **Practical relevance of the application.** HMDA data is important for fair-lending analysis and lacks person-level identifiers. The conclusion sketches three concrete policy-relevant applications (measuring fairness, monitoring lending standards, studying shopping behavior) that connect to existing literature.

5. **Principled treatment of the precision-sample size trade-off (Section 4.1, Figure 5).** The use of the precision-bound frontier to select tuning parameters is clearly communicated and methodologically sound. The choice at the "knee" of the frontier is well-motivated.

## Weaknesses

### Fatal

None.

### Major

1. **The precision bound's tightness is not characterized, and the gap could be substantial in practice.** The bound states that precision ≥ 1 − Pr[Mult]/p², but the degree to which this exceeds true precision depends on how much Pr[Mult|False] exceeds p². If origination decisions are positively correlated across distinct borrowers (e.g., due to shared local housing market conditions), Pr[Mult|False] could be substantially larger than p², making the bound correspondingly loose. The simulation validates the bound under ideal conditions where assumptions hold and covariates are controlled, but it does not stress-test the bound under realistic violations of the independence assumption (Assumption 1). The paper reports "92.3% precision" as an estimate, but this is a lower bound whose distance from true precision is unquantified in the real application. This does not invalidate the method, but it means the headline empirical claim is weaker than it appears — a reader cannot gauge how far the bound is from actual performance.

### Minor

1. **No comparison against alternative record linkage methods for the clustering instantiation.** The paper presents the clustering algorithm as "state-of-the-art" and as part of the paper's contributions, but evaluates only different ε values and distance functions for the same agglomerative clustering pipeline. No baselines (e.g., deterministic matching on coarsened variables, DBSCAN, simple nearest-neighbor threshold methods) are compared. Since the main contribution is the evaluation framework, this is not fatal, but it weakens the empirical demonstration of the specific pipeline.

2. **Restriction to size-2 clusters limits scope.** The paper transparently restricts all analysis to clusters of exactly two applications (footnote 4). This means (a) cross-applicants submitting 3+ applications are undetected, (b) the bound for general cluster sizes is neither developed nor tested, and (c) the reported 314,344 clusters represent only a subset of all cross-applicants. This is stated honestly but its practical significance could be more prominently discussed.

3. **Applicant age as a partition variable.** Age is used as a partition variable (Section 4.1), meaning two applications from the same person at different ages (e.g., turning a year older between applications) would be placed in different partitions and could not be linked. Over the 2018–2023 window, this is a genuine concern that is not addressed.

4. **Lack of uncertainty quantification for the bound.** The bound estimate α̂(θ) is reported as a point estimate without confidence intervals. A bootstrap procedure would be straightforward and would help readers assess the sampling variability of the reported 92.3% figure.

### Trivial

- The adjusted bound (Equation 1) applies to the filtered set of clusters (after dropping clusters with multiple originations), but the text could be clearer about which population the headline 92.3% figure refers to.

## Nice-to-Haves

- Characterizing the looseness factor — either theoretically under relaxed assumptions or empirically on datasets with known ground truth that include realistic correlations — would directly address the central question about bound tightness.
- Comparing the clustering pipeline against at least one simple baseline (e.g., exact matching on coarsened continuous variables) would strengthen the empirical component.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Recall bound is only relative, not absolute, and the paper conflates the two"** — REMOVED because the paper explicitly calls it "relative recall" in the abstract and introduction, correctly explains the bound is proportional to the unobservable P_tot (Corollary 1), and the 92% recall figure cited by the critic appears in the simulation section where ground truth is known. The paper does not overclaim here; the criticism was about hypothetical reader confusion, not an actual error.
- **"The bound assumes Pr[Mult|¬False] = 0... what if fraud/data error?"** — REMOVED because the paper explicitly justifies this by the structural constraint ("individual can originate at most one loan"). This is a standard assumption; raising fraud edge cases without evidence is speculative.
- **"ε scaling relative to variables is unspecified"** — The paper mentions weighted ℓ₂-norm and references Appendix B for implementation details. Since the appendix is stripped by the parser, this cannot be verified from available text.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a discussion or theoretical characterization of how far Pr[Mult|False] can deviate from p² under relaxations of the independence assumption.
2. Include bootstrap confidence intervals for the precision bound estimate.
3. Add at least one simple baseline comparison (e.g., deterministic matching on coarsened variables) to ground the clustering pipeline in the existing record linkage literature.
4. Discuss the age-as-partition-variable issue and whether alternative bucketing strategies were considered.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>