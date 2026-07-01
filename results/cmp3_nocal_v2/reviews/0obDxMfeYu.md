## Summary

This paper introduces Medix, a framework that uses element-wise median (EWM) of gradients to identify and filter OOD samples from unlabeled "in-the-wild" mixtures, then trains an OOD detector on the identified outliers and labeled InD data. The core idea is that the median is a robust central estimator, making it suitable for detecting outliers in contaminated mixtures. The paper provides theoretical bounds on inlier/outlier misclassification under a Huber contamination model with sub-Gaussian gradient assumptions, and reports strong empirical results across CIFAR-10 and CIFAR-100 against 20 baselines.

## Strengths

- **Novel application of median to OOD detection.** Using the element-wise median of gradients as a robust estimator to identify outliers in unlabeled mixtures is a genuinely new idea in the OOD detection literature. The motivation (Section 3.1, Figure 1) is clearly supported by a preliminary experiment showing monotonic deviation as OOD samples increase.

- **Consistently strong empirical results.** Tables 1 and 2 show Medix dominates all 20 baselines across both CIFAR-10 and CIFAR-100. On CIFAR-10, Medix achieves an average FPR95 of 0.80% (vs. WOODS at 3.40%, OE at 6.16%), with small standard deviations (≤0.75%). On CIFAR-100, Medix achieves 5.42% average FPR95 vs. WOODS at 6.74%. The margins are large enough that they cannot be dismissed as noise.

- **Theorems provide coherent robustness bounds for median-based filtering under a contamination model.** Theorems 4.1 and 4.2 give formal bounds on inlier and outlier misclassification under sub-Gaussian gradient assumptions, cleanly separating contamination, concentration, and separation effects. The assumptions are partially validated empirically (Q-Q plot, Figure 4), and a looser version under bounded second moments (Theorem C.3) is noted.

## Weaknesses

### Fatal
None.

### Major
- **The theoretical analysis does not analyze the presented algorithm.** Theorems 4.1 and 4.2 are framed as providing guarantees for "Medix's filtering stage" (Section 4) and "the EWM filtering rule," but the bounds contain no parameters of Algorithm 1 — not the greedy leave-one-out selection, not the number of samples *k* removed per iteration, not the stopping threshold *ε*, and not the iterative nature of the procedure. The bounds are statements about the robustness of the *static* median as a central estimator under the Huber contamination model (Theorem 4.1 bounds `ERR_in` by a concentration term plus `π/[2(1-π)]`; Theorem 4.2 is analogous). Algorithm 1, by contrast, is an iterative greedy procedure that recomputes the median on a reduced set at each iteration, selects the *k* samples with the largest drop in L2 distance, and stops based on a convergence criterion. None of this machinery appears in the theory. The paper needs to either (a) connect the iterative algorithm to these bounds (e.g., show that the greedy procedure converges to a set whose misclassification rates satisfy the theorems), or (b) honestly delimit the theory as providing *motivation* for median-based filtering rather than a guarantee for Algorithm 1. As written, the text in Section 4 and the conclusion (line 262) overclaims what the theory establishes.

### Minor
- **CONJ and DRL baselines are claimed but absent from the main tables.** The baselines paragraph (lines 174–175) lists CONJ (Peng et al., 2024) and DRL (Zhang et al., 2024) among the compared methods. The conclusion (line 262) states Medix "outperformed state-of-the-art methods such as WOODS and DRL." Yet neither CONJ nor DRL appears in Tables 1 or 2, where 20 other baselines are shown. If these results exist only in the appendix, the main text and conclusion should not claim superiority over DRL without showing the supporting numbers.

- **Computational cost of Algorithm 1 is not characterized in the main paper.** The greedy algorithm requires computing the EWM for each leave-one-out subset at each iteration — O(d × m × log m) per median, times up to *m* per iteration, times up to *T* iterations. For 25,000 wild samples, this is expensive. The paper defers efficiency analysis to Appendix A.6 (line 238), but the main text should at least state actual wall-clock times or complexity for the reported experiments so readers can assess practicality.

- **Synthetic 2D example (Figure 2) uses an unrealistically easy separation.** The OOD Gaussian mean is at [20, 2√3] while the nearest InD cluster is centered near [0, 2√3], making OOD points roughly 40 standard deviations away on the x-axis. The paper acknowledges this is "simple to facilitate better understanding," but the example does not test the method's limits.

### Trivial
- The data split (25k labeled InD for Medix vs. 50k for InD-only baselines) is acknowledged by the paper (lines 170, 182) and does not affect the fair comparison against wild-data methods (WOODS, OE). Minor note worth mentioning for clarity.

## Nice-to-Haves

- **Well-posedness of the optimization (Section 3.1).** When π < 0.5, the EWM of the full wild set is already close to ∇̄_in, meaning many subsets may have EWMs near ∇̄_in. The paper does not analyze whether the δ_i values (drops in distance from removing a single sample) are reliably distinguishable from numerical noise. An analysis or empirical characterization of the δ_i distribution would strengthen confidence in the greedy selection.

- **Unseen-OOD evaluation should be given more prominence.** The main evaluation uses the same OOD distribution for wild data and testing (the standard protocol from Katz-Samuels et al., 2022a). Appendix A.4 evaluates the harder unseen-OOD setting, but this is arguably the more practically relevant result. Leading with it or giving it equal weight in the main paper would strengthen the practical claims.

## Removed Points

These points are flagged to be removed; treat them with caution.
- *"The theoretical analysis does not analyze the algorithm presented" was downgraded from the reviewer's "Critical Issues" framing.* Kept as Major per verification — the reviewer's core claim is correct (the bounds are static, not algorithmic). Not removed.
- *"The evaluation uses the same OOD distribution for wild data and test data" — weakened from a "Critical Issue" to Minor* because this is the standard protocol in the WOODS line of work, all baselines use it, and the paper does include unseen-OOD evaluation in the appendix.
- *"Section 3.1 — Well-posedness of the optimization problem" — moved to Nice-to-Haves* because it is speculative (the paper does not analyze this, but the reviewer's concern about flat optimization landscape is not verified as an actual failure).
- *"Section 5.1 — Data asymmetry" — downgraded to Trivial* because the paper explicitly acknowledges this asymmetry (lines 170, 182), and the comparison against wild-data methods (WOODS, OE) is fair.
- *Strengths about "novel application" and "strong empirical results" retained; generic framing removed.*

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Align the theory with the algorithm.** Either prove that Algorithm 1's iterative procedure satisfies bounds analogous to Theorems 4.1 and 4.2, or clearly delimit the theory as motivation for why median-based filtering *in principle* can work, rather than claiming it guarantees Medix's performance.
2. **Include CONJ and DRL results in the main tables** (or remove claims about outperforming them from the main text and conclusion).
3. **Report wall-clock time or FLOPs for Algorithm 1** in the main paper, given its computational expense.
4. **Give the unseen-OOD evaluation (Appendix A.4) more prominence** — the matched-OOD main evaluation does not test generalization to genuinely novel OOD distributions at test time.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Reject</decision>