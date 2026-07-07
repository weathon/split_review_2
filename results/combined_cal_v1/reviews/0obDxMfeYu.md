Let me now write the final consolidated review.

Here is the verified analysis of the paper:

**Paper**: "A Median Perspective on Unlabeled Data for Out-of-Distribution Detection" (Medix)

**Core contribution**: Uses element-wise median of gradients to filter OOD samples from unlabeled wild data, then trains an OOD detector on the filtered set.

**Verification of key reviewer claims**:

1. **Theory-algorithm gap** (Issue 1): ✓ VERIFIED. Section 4 (Theorems 4.1, 4.2) bounds error of a generic "EWM filtering rule," while Algorithm 1 is an iterative greedy leave-one-out procedure. The paper states "theoretical guarantees of Medix's filtering stage" but never formally connects the theorems to the greedy algorithm. This is a real issue.

2. **40.98% framing** (Issue 2): ✓ VERIFIED. Abstract, intro, and conclusion all highlight this number. It's an absolute percentage-point difference against KNN+ (InD-only method). The WOODS comparison (1.32 pp) is also reported. The framing is not false but is potentially misleading.

3. **Numerical discrepancy** (Issue 3): ✓ VERIFIED. Table 2: 0.16+15.99+0.13+0.83+8.02=25.13, avg=5.026, but reported avg=5.42. This is a non-trivial gap (~0.4 pp).

4. **Computational cost** (Issue 4): ✓ VERIFIED. Main paper lacks any runtime characterization. Appendix A.6 is referenced but the appendix is stripped.

5. **Hyperparameter selection** (Issue 5): ✓ PARTIALLY. The paper says parameters selected "with the objective of maximizing OOD performance" without specifying validation strategy. However, the grid is small (4×4) and a sensitivity analysis is referenced in Appendix A.2.

**Filtered weaknesses**:
- REMOVED: "bounds are loose (50% baseline)" — this is standard for theoretical bounds in ML; the bounds characterize what controls error, not tight numerical predictions.
- REMOVED: "Figure 1 uses only one pair" — this is a motivating illustration, not a main result.
- REMOVED: "no analysis of optimization landscape" — scope creep; paper acknowledges exact problem is intractable and proposes greedy approximation.
- REMOVED: "batch-level mixing claim not substantiated" — claim about other works with citations.
- REMOVED: "open-world claims too broad" — standard evaluation in the field.

---

## Summary

This paper proposes Medix, a framework for OOD detection that uses the element-wise median (EWM) of gradients to filter OOD samples from unlabeled wild data. The core idea — that the median is more robust than the mean when the wild data is contaminated with OOD samples — is novel and well-motivated. The paper provides theoretical bounds on misclassification rates, an iterative greedy algorithm (Algorithm 1) for implementing the median-based filter, and empirical results comparing against 20 baselines on CIFAR-10 and CIFAR-100.

## Strengths

- **Novel median-centric filtering idea (Section 3.1).** Using the element-wise median of gradients as a robust reference for outlier detection is a genuinely fresh idea in the OOD detection literature. The insight that the median is less sensitive to OOD contamination than the mean is well-motivated and grounded in connections to data pruning work (Acharya et al., 2024).

- **Formal theoretical bounds (Section 4, Theorems 4.1 and 4.2).** The paper provides upper bounds on both inlier and outlier misclassification rates, analyzing contamination, concentration, and separation effects. This is relatively rare in the OOD detection literature for the in-the-wild setting, and the analysis of what factors control error is a meaningful contribution.

- **Strong empirical results.** On CIFAR-10 (Table 1), Medix achieves an average FPR95 of 0.80% and AUROC of 99.74%, substantially outperforming WOODS (3.40% FPR95). On individual OOD datasets like LSUN-C, LSUN-RESIZE, and SVHN, results approach near-perfect detection. The method outperforms all 20 baselines compared.

## Weaknesses

### Fatal
None.

### Major

- **Theory-algorithm gap (Section 4 vs Algorithm 1).** Theorems 4.1 and 4.2 bound the error of a generic "EWM filtering rule" — analyzing contamination, concentration, and separation effects in a one-shot median-based classification setting. However, Algorithm 1 is an iterative greedy leave-one-out procedure that removes *k* samples per step using a stopping criterion based on L2 distance change. The paper never shows that Algorithm 1's output converges to a solution of Equation 4, nor that the bounds in Theorems 4.1 and 4.2 apply to the greedy procedure's specific outputs. Contribution C2 claims "theoretical guarantees for the robustness of median-based filtering" for Medix, but the theorems and the deployed algorithm exist largely disconnected from each other. This undermines one of the paper's headline contributions.

### Minor

- **Numerical discrepancy in Table 2.** On CIFAR-100, Medix's reported average FPR95 is 5.42%, but the per-dataset FPR95 values (0.16, 15.99, 0.13, 0.83, 8.02) average to 5.026 — a ~0.4 percentage point gap that cannot be explained by rounding (max rounding error per entry is 0.005). The WOODS row in the same table checks out correctly (6.74 matches), making this discrepancy concerning for trustworthiness.

- **Selective emphasis in headline comparison.** The abstract, introduction, and conclusion highlight that Medix "outperforms KNN+ by 40.98% in terms of FPR95." This is an absolute difference (46.40 − 5.42 = 40.98 percentage points), comparing against KNN+, a method trained *only on InD data* with no access to wild data. Against WOODS — the state-of-the-art method that *also uses wild data* — the improvement is 1.32 pp on CIFAR-100 and 2.60 pp on CIFAR-10. While the WOODS comparison is fairly reported, the repeated emphasis on the KNN+ margin gives an inflated impression of the method's advance over the relevant competitor.

- **CONJ and DRL baselines listed but absent from main tables.** Section 5.1 mentions CONJ (Peng et al., 2024) and DRL (Zhang et al., 2024) as included baselines, but their results do not appear in Tables 1 or 2. The paper references Appendix A.3 for additional comparisons, but this is not made explicit in the main text, leaving the status of these comparisons ambiguous.

### Trivial
- The main text does not characterize computational cost of Algorithm 1; runtime numbers or FLOP comparisons are deferred to a stripped appendix.

## Nice-to-Haves
- Clarify the validation strategy for hyperparameter selection (*k* from {4k, 7k, 10k, 20k}, *ε* from {5e-5, 5e-4, 5e-3, 5e-2}) — specifically whether tuning was done on a held-out validation set or test OOD data.
- Include an ablation showing how iterative removal compares against a single-pass median threshold.

## Removed Points
These points were removed from the harsh critic's analysis; treat them with caution:
- **"Theoretical bounds are loose (50% baseline)"** — The ~50% contamination term at π=0.5 is standard for theoretical bounds in ML; they characterize the factors controlling error rather than providing tight numerical predictions. Not a genuine weakness.
- **"Figure 1 uses only one InD/OOD pair"** — This is a motivating illustration experiment, not a main result; the paper is transparent about this.
- **"No analysis of optimization landscape for Equation 4"** — Scope creep; the paper explicitly notes the exact problem is intractable and proposes a greedy approximation.
- **"Batch-level mixing claim not substantiated"** — This is a claim about other works with proper citations.
- **"Claims about open-world setting are too broad"** — Evaluation on 5 standard OOD test sets is standard practice in the field.
- **"Missing related works"** — Cannot verify from available sources.
- **Formatting and style nitpicks** — Parser artifacts, not author errors.

## Novel Insights
The core insight — that the element-wise median of gradients is more robust than the mean for identifying OOD points in mixed wild data, with provable guarantees tied to contamination, concentration, and separation effects — is clearly articulated and well-motivated. However, the reviewers' analyses did not surface genuinely novel insights beyond what the paper itself provides.

## Suggestions
1. **Connect theory to algorithm.** Either show that Algorithm 1 provably converges to a solution of Equation 4, or derive bounds that directly apply to the iterative greedy procedure. Alternatively, reframe the theoretical claims to be about the general median filtering principle (which the theorems actually analyze) rather than specifically about Medix.
2. **Correct the numerical discrepancy in Table 2** and verify all reported averages.
3. **Move CONJ and DRL results to the main tables** or explicitly state they are deferred to the appendix in the main text.
4. **Include runtime characterization** (wall-clock time or FLOPs vs. WOODS) in the main paper.
5. **Clarify the validation strategy** for hyperparameter selection.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>