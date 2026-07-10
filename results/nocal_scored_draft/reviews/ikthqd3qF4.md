Now let me write the final consolidated review.

## Summary

This paper introduces a novel method for deriving observable lower bounds on precision and recall in unsupervised record linkage without labeled data, exploiting a structural constraint (e.g., at most one mortgage origination per person). The core idea is elegant: clusters with multiple originations are guaranteed false positives, and their rate can be used to bound the false positive rate overall. The method is demonstrated on HMDA mortgage data using hierarchical clustering, identifying cross-applicants with an estimated 92.3% precision lower bound.

## Strengths

- **Genuinely novel theoretical connection.** The core insight — that a structural constraint (at most one origination per person) allows identifying a subset of guaranteed false positives and extrapolating a precision lower bound — is clever and clearly formalized in Theorem 1 and its corollaries. This appears to be a genuinely new contribution to the unsupervised record linkage literature.

- **Convincing simulation validation.** The side-by-side comparison of true precision (Figure 3a) and the implied precision bound (Figure 4a) shows that the bound closely tracks true precision in a realistically structured simulation (1M census tracts, realistic application distributions). At ε=0.06, true precision is ~95% and the bound is ~93.7% — a conservative 1.3 pp gap in the right direction.

- **Domain- and method-agnostic framing.** The bounds (Theorem 1, Corollaries 1–2) depend only on predicted labels and the structural constraint, not on the specific clustering algorithm. The paper correctly notes that the same structural constraint applies to insurance, college admissions, job offers, and other settings, giving the framework reach beyond the HMDA application.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Restriction to size-2 clusters is under-discussed.** The paper drops all clusters with more than two applications (footnote 4), limiting empirical findings to pairs of applications. The theoretical framework (Theorem 1) does not require this restriction, but the paper provides no analysis of what fraction of cross-applicants are excluded or how this might bias the resulting sample. The representativeness of the identified sample for downstream applications is not discussed.

- **No validation of proposed downstream applications.** The conclusion lists three significant applications (fairness measurement, monitoring lending standards, studying shopping behavior) but none are executed or validated. While the paper appropriately frames these as future work, some basic face-validity checks on the identified cross-applicants using only observable data patterns (e.g., time-between-applications distribution, approval rate patterns) would strengthen the claim that the clusters capture meaningful shopping behavior. The paper mentions additional diagnostics in the appendix but these cannot be evaluated from the main text.

- **Abstract blurs simulation and real-data claims.** The abstract states "92.3% precision with only minimal loss in relative recall" without distinguishing that the precision figure is a lower bound from the real-data application while the recall claim is validated only in the simulation. The main text correctly explains the recall bound's dependence on the unknown P_tot (Corollary 1) and provides a valid workaround for relative comparisons across tuning parameters, but the abstract's framing could mislead a casual reader.

- **Robustness of assumptions not analyzed.** The paper states that Assumptions 1–2 "do not appear very strong to us" but does not analyze how their violation could affect the bound. Lemma 1 (appendix) shows the assumptions are sufficient, but the paper would benefit from discussing what kinds of dependence structures (e.g., correlated origination outcomes within the same census tract) could threaten the bound and whether the empirical setting is plausibly robust.

### Trivial

- The paper lacks an explicit limitations section that acknowledges the size-2 restriction, the need for P_tot to compute absolute recall, and the bounding (rather than point-estimate) nature of the reported precision figure.

## Nice-to-Haves

- Confidence intervals or standard errors for the 92.3% precision lower bound would strengthen the real-data results.
- A histogram of time-between-applications for identified pairs would provide a simple face-validity check without requiring ground-truth labels.
- Basic descriptive statistics of the identified cross-applicant clusters (e.g., average within-cluster distance, distribution across partitions, demographic composition) would help readers assess face validity.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Criticism about the "individual" definition (borrower-property pair):** The critic claimed this was under-discussed, but the paper explicitly defines it in Section 2 (line 39): "If the same person applies for a mortgage for two distinct properties, we would count this as two distinct individuals." REMOVED — the paper already addresses this.
- **Strength about "method addresses a real bottleneck":** Generic praise about the problem being important rather than a specific strength of the paper's execution. REMOVED per filtering rules.
- **Criticism about missing confidence intervals:** A reasonable suggestion but standard for large-scale single-run benchmarks in this field. MOVED to Nice-to-Haves.
- **Speculative claim that the bound could fail entirely under violated assumptions:** The critic speculates about correlation structures making Pr[Mult|False] < p² but provides no concrete example. The paper's Lemma 1 provides the sufficiency argument. WEAKENED to Minor (above).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a dedicated limitations section discussing the size-2 restriction, bounding nature of precision estimates, dependence on assumptions, and the distinction between simulation-based and real-data claims.
2. Include at least one face-validity check on identified cross-applicants using observable patterns (e.g., time-between-applications distribution, concentration at 1–7 day intervals consistent with shopping).
3. Clarify in the abstract that the 92.3% figure is a lower bound on precision and that the recall figure is from the simulation.
4. Analyze sensitivity of the bound to modest violations of Assumption 1.

## Score and Decision

The paper's core theoretical contribution is genuinely novel and well-supported by a carefully designed simulation. The weaknesses are all minor and relate to presentation completeness rather than methodological soundness. The theoretical framework is sound, the simulation provides strong evidence that the bound tracks true precision, and the real-data application demonstrates practical feasibility at scale. The paper would be strengthened by additional face-validity checks and clearer communication of what is bound vs. point estimate, but these do not undermine the central contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>