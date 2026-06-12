## Summary

This paper proposes Medix, a median-based framework for OOD detection that filters outliers from unlabeled wild data. The method uses the element-wise median (EWM) of gradients as a robust reference and greedily removes samples whose gradient deviations are largest. It provides two-sided theoretical bounds on inlier and outlier misclassification rates and evaluates against 20 baselines on CIFAR-10 and CIFAR-100, achieving the best average FPR95 and AUROC in both settings.

## Strengths

1. **Novel median-based filtering approach.** The use of element-wise median on gradients as a robust reference for outlier detection is a clean, well-motivated departure from prior threshold-based or mean-based methods. The motivating experiment (Figure 1) showing monotonic increase in L2 deviation as OOD samples accumulate provides clear intuition for why the median works.

2. **Meaningful theoretical guarantees.** Theorems 4.1 and 4.2 provide two-sided misclassification bounds decomposed into contamination, concentration, and separation effects. The contamination term π/(2(1−π)) cleanly captures why median-based filtering is robust up to 50% OOD contamination — a threshold that emerges naturally from the mathematics rather than being chosen heuristically. The paper also provides a looser bound (Theorem C.3) that drops the sub-Gaussian assumption, which is good practice.

3. **Consistently strong empirical results.** On CIFAR-10 (Table 1), Medix achieves an average FPR95 of 0.80% vs. WOODS at 3.40% — a large margin. On CIFAR-100 (Table 2), Medix achieves 5.42% FPR95 vs. WOODS at 6.74%. Standard deviations across 5 runs are small, indicating stable performance. The improvements over the best prior wild-data methods are clear and consistent across all five OOD test sets.

## Weaknesses

### Major

- **CONJ and DRL results are claimed but not shown in the main tables.** Section 5.1 states that CONJ (Peng et al., 2024) and DRL (Zhang et al., 2024) were included "to provide a more thorough evaluation," and the conclusion claims Medix "outperformed state-of-the-art methods such as WOODS and DRL." However, neither CONJ nor DRL appears in Tables 1 or 2, nor is there a pointer in the main text to where these results can be found. If they are in the appendix, a forward reference is needed. As written, a reader cannot verify the claim against DRL. The authors should either include these results in the main tables or remove the claim.

### Minor

- **Algorithm 1's convergence criterion is inconsistently specified.** The pseudo-code (line 110) uses `while t ≤ T or |δ_max| > ε`. With OR, the ε threshold has no effect until after T iterations, which defeats its purpose as a convergence criterion. The intended logic is almost certainly AND. Additionally, the prose (line 95) describes the criterion as "the change in the L2 distance between two iterations," but δ_max measures the maximum per-sample drop within a single iteration — these are different quantities. Neither issue invalidates the method, but a reader trying to re-implement from the pseudo-code alone would get different behavior than described.

- **Percentage improvements over InD-only methods are framed ambiguously.** The abstract (line 27) claims an improvement of "40.98% in terms of FPR95" over KNN+ on CIFAR-100, and Section 5.3 claims reductions of "52.31% on PLACES365 and 38.24% on TEXTURES." These are absolute percentage-point differences (e.g., KNN+ avg FPR95 = 46.40, Medix = 5.42; difference = 40.98 pp), not relative percentages. Additionally, KNN+ uses the full 50k labeled InD samples while Medix uses 25k labeled + 50k wild samples (acknowledged at line 182). The cross-category comparison conflates method improvement with additional data access. The paper would benefit from clearer disambiguation.

- **The 2D synthetic experiment (Figure 2) is too simple to be probative.** OOD points are placed ~20 units from the nearest InD cluster center (with covariance 0.25·I), making the detection task trivially easy. The paper acknowledges this simulation is "designed to be simple," but a more realistic high-dimensional demonstration would better connect the theory to practice.

- **No analysis of greedy approximation quality.** The optimization problem (Eq. 4) is combinatorial, and Algorithm 1 is a greedy leave-one-out approximation with no analysis of how far the output could deviate from the optimal subset. This is a gap, though it does not threaten the core contribution.

### Trivial

- Typo "ReaT" in Table 1 (line 198) should be "ReAct."

## Nice-to-Haves

- A direct empirical evaluation of the filtering stage against the theoretical bounds (e.g., a plot of empirical inlier/OOD misclassification rate vs. π with the theoretical bound overlaid) would connect the two halves of the paper more convincingly than the current 2D synthetic experiment.
- A brief runtime estimate in the main text (currently deferred to Appendix A.6) would help readers assess practicality.

## Removed Points

- **Criticism of the matched-OOD evaluation setting.** The paper clearly describes its matched protocol (Section 5.1), this is the standard protocol in the sub-field (WOODS, Du et al. 2024a), and the paper includes an unseen-OOD experiment in Appendix A.4. Demanding a different primary protocol is scope creep.
- **Criticism that sub-Gaussian assumption is unverified.** The paper provides empirical validation in Remark 4.3 (Figure 4) and offers a looser bound (Theorem C.3) without the assumption.
- **Criticism about pseudo-label noise for OOD samples not being discussed in main text.** An appendix study (A.5) exists; this is a nice-to-have acknowledgment at most.
- **Criticism about unfair comparison with InD-only methods.** The paper explicitly acknowledges the data-size difference (line 182). The comparison is valid as a demonstration of wild data's value, even if the framing could be clearer.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix Algorithm 1's convergence criterion to use AND semantics and clarify what quantity is being compared to ε.
2. Include CONJ and DRL results (or a pointer to where they appear in the appendix) or remove the claim from the conclusion.
3. Disambiguate percentage-point differences from relative percentages throughout the paper.
4. Add a brief acknowledgment in Section 3.1 that pseudo-labels for OOD samples introduce noise into gradient computation (the appendix study shows resilience, but the concern should be surfaced earlier).

## Score and Decision

**Calibration anchors (all rounds combined):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| *How Does Unlabeled Data Provably Help OOD Detection?* (Du et al. 2024a, SAL) | 6.50 | R1/R2 | Direct predecessor; same two-stage pipeline, different filtering criterion (top singular vector vs. median), similar theory, comparably strong results. Medix's median-based filtering is more principled and achieves better results. |
| *Geometric Median Matching for Robust Data Pruning* | 3.00 | R2 | Also uses median concepts but for data pruning, not OOD. Weak theory and results. Not comparable in scope. |
| *Guaranteed OOD Detection with Diverse Auxiliary Set* (ProMix) | 6.00 | R2 | Mixup-based OOD detection with theoretical guarantees. Comparable rigor but different problem framing (auxiliary set vs. wild data). |
| *Pathologies of OOD Detection* | 4.75 | R1 | Critical analysis paper without new method. Significantly weaker technical contribution. |
| *Gradient-based OOD Detection (GradRect)* | 4.20 | R2 | Uses gradients for OOD but not in wild-data setting. Struggles with over-parameterization issues. |

**Round-1 bracket:** 5.5–7.5. **Narrowing:** Medix is comparable to the SAL paper (6.50, Accept) — both provide novel filtering methods with theoretical guarantees for the wild-data setting. Medix's median-based approach is cleaner and its empirical results are stronger, but it shares the same two-stage pipeline structure and has some presentation issues (missing CONJ/DRL results, algorithm pseudo-code ambiguity). It clearly exceeds the borderline-reject papers in the 4–5 range. I place it at the same level as SAL, possibly slightly higher due to stronger results, but tempered by the missing baseline data.

**Final score:** 6.5 — a solid accept with fixable weaknesses.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>