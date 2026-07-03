Now I have all the evidence I need. Let me write the final consolidated review.

---

## Summary

This paper derives observable lower bounds on precision and relative recall for unsupervised record linkage without labeled data. The key insight exploits a structural constraint — each individual can originate at most one first-lien mortgage — to bound precision using only the fraction of predicted clusters with multiple originations (Pr[Mult]) and the unconditional origination probability (p): Precision ≥ 1 − Pr[Mult]/p². The paper extends this to relative recall and weighted summaries (Corollaries 1–2), enabling model tuning without ground-truth labels. The method is instantiated via hierarchical agglomerative clustering on 65.5 million HMDA mortgage records, identifying 314,344 cross-applicant clusters at an estimated 92.3% precision.

## Strengths

1. **Novel theoretical bounds using structural constraints (Theorem 1, Section 2.2)**. The paper exploits a real-world constraint (one origination per individual) to derive Precision ≥ 1 − Pr[Mult]/p² from two observable quantities. Lemma 1 (appendix) establishes the bound is conservative, which is the correct direction for a lower bound. This is a genuinely clever theoretical contribution — using a domain restriction to bound clustering quality without labels — and it is cleanly presented.

2. **Simulation evidence that the bound is practically tight (Section 3, Figures 3a vs. 4a)**. At the preferred specification (ε = 0.06, with date), the observable bound gives ~93.7% precision while the infeasible true precision is ~95%. The bound captures the same ordering across tuning parameters, demonstrating it is not merely theoretically valid but tight enough to guide hyperparameter selection. The close resemblance between Figures 3a and 4a is concrete evidence of practical utility.

3. **Extension to relative recall and weighted summaries without additional assumptions (Corollaries 1–2)**. The paper shows that ranking specifications by the fully observable quantity α̂(θ)N⁺(θ) is equivalent to ranking by a lower bound on recall, and extends this to Fβ-scores and weighted precision-recall sums. This makes the framework directly usable for model selection without any labeled holdout set.

4. **Computationally feasible implementation on massive data (Section 2.1)**. The use of O(ℓ²) nearest-neighbor chain agglomerative clustering (Müllner, 2011/2013) and the insight that the inverse tree structure allows different ε values to be evaluated without recomputing clusters (line 57) are essential engineering contributions that make the method viable on 65.5 million records.

5. **Practical refinement by dropping known false positives (Equations 1–2)**. The paper recognizes that clusters with multiple originations are *known* false positives and derives a tighter bound after removing them (line 140–146). This is a simple but effective engineering insight.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Key assumption about false-positive clusters is not empirically tested.** The precision bound relies on the claim (Lemma 1, appendix) that Pr[Mult|False] > p² under Assumptions 1–2. The critic raises a plausible concern: false-positive clusters are formed precisely because applications are *similar on observables* (same census tract, similar income, similar date, similar credit score). If those observables correlate with lower origination probability — and applicants who file multiple near-identical applications may be shopping because they expect rejection — then the conditional origination probability within false-positive clusters could systematically differ from the population mean. The paper claims Lemma 1 addresses this, but the simulation does *not* include a scenario where false-positive clusters have non-representative origination probabilities, so the robustness of the bound to this concern is untested. [Evidence: lines 136–138 show the paper relies on Lemma 1; the simulation (Section 3) does not test correlated origination probabilities within specific cluster types.]

2. **Claim of "cross-model comparison" is unsupported.** The paper states its bounds enable "hyper-parameter tuning and cross-model comparisons" (line 15), but the empirical evaluation compares only two variants of the *same* agglomerative clustering algorithm (with date vs. without date). No genuinely different methods are compared — no DBSCAN, spectral clustering, Fellegi-Sunter, embedding-based approaches, or even a simple thresholding baseline. All 96 combinations explored (Section 4.1) vary only the distance function and ε within the same agglomerative clustering framework. The theoretical claim is plausible, but the paper provides no evidence that the bounds work for comparing fundamentally different algorithms. [Evidence: lines 15, 178–179, Section 4.1.]

3. **Restriction to size-2 clusters is uncharacterized.** Footnote 4 drops all clusters with more than two applications without explaining what fraction of data this affects, whether the dropped clusters differ in properties, or whether the precision bound generalizes to larger clusters. Since the structural constraint (one origination per individual) should be *even more* informative for larger clusters, this restriction seems unnecessary and should at least be characterized. [Evidence: line 186 (footnote 4).]

4. **No uncertainty quantification.** The headline precision estimate of 92.3% (line 240) is a point estimate without confidence intervals. Both p̂ and p̂_m are estimated from finite samples, so the precision bound has sampling variance. Confidence intervals or bootstrap standard errors would strengthen the empirical claims.

### Trivial

- The paper lists application domains where the structural constraint applies (college admissions, job offers) but does not discuss that when p is small (e.g., p ≈ 0.05–0.20 in college admissions), p² is tiny and the bound would be extremely weak. A brief caveat would be helpful. [Evidence: line 13.]

## Nice-to-Haves

- Test the bound's sensitivity to correlated origination outcomes within partitions (violating Assumption 1). This would directly address the most serious concern about the method's validity.
- Report how many size-3+ clusters were dropped and extend the analysis to at least characterize them.
- Add a comparison with at least one genuinely different clustering or record-linkage approach to support the cross-model comparison claim.

## Removed Points

These points were flagged for removal. Treat with caution if referencing them:

- **"The recall bound is not truly observable — the paper's framing overstates it"** (Harsh Critic #1). REMOVED because the paper is transparent: the abstract says "relative recall" (not absolute recall), Corollary 1 explicitly states the absolute bound requires the unknown P_tot and that only the *ranking* is fully observable via α̂(θ)N⁺(θ), and the 92% recall figure (line 216) is reported in the *simulation section* where ground truth is known — it is not claimed to come from the bound. No conflation exists.

- **"The bound's usefulness in college admissions / job offers"** (Harsh Critic section-by-section). REMOVED from weaknesses and moved to Trivial. The paper lists these as examples of domains where the structural constraint *applies*, not where the method performs best. The critic is demanding the paper address scope outside its stated application.

- **"The 96 combinations are not individually described / non-reproducible"** (Harsh Critic). REMOVED — the paper states implementation details are in Appendix B (which was stripped by the parser). Standard practice.

- Generic strengths from Strength Finder about "addressing an important problem" or "well-motivated" — REMOVED. Kept only concrete, evidence-grounded strengths.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a simulation scenario where false-positive clusters have systematically different origination probabilities to test the bound's robustness to this plausible violation.
2. Include at least one genuinely different algorithm (e.g., a simple embedding-based matching baseline) to support the cross-model comparison claim the paper makes.
3. Report bootstrapped confidence intervals for the headline precision estimate of 92.3%.
4. Characterize the size-3+ clusters dropped by the size-2 restriction and discuss how the bound might generalize to larger clusters.

## Score and Decision

The calibration tool was unavailable due to a path error, so I rely on my judgment calibrated against the ICLR scoring scale.

This paper presents a genuinely novel theoretical contribution: using a structural constraint (one origination per individual) to derive observable lower bounds on precision and relative recall for unsupervised record linkage. The theoretical framework is sound and cleanly presented. The simulation provides credible evidence that the bound is tight enough to be practically useful, and the HMDA application demonstrates real-world feasibility on a large-scale dataset.

However, the empirical validation has meaningful gaps: (1) the key assumption underlying the precision bound is not tested for robustness against plausible violations (systematically different origination probabilities in false-positive clusters); (2) the paper's claim of enabling "cross-model comparisons" is not supported by any cross-method comparison in the evaluation; and (3) the restriction to size-2 clusters is uncharacterized. These are addressable issues that weaken but do not invalidate the core contribution.

The paper is above the reject threshold — the theoretical idea is genuinely novel and the simulation provides reasonable evidence of practical utility. It is below a clear accept because the validation is too narrow to fully support the scope of the claims made. I rate this paper at the borderline accept level.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>