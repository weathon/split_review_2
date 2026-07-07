## Summary

This paper proposes Medix, a framework for out-of-distribution (OOD) detection that uses the element-wise median (EWM) of gradients to identify OOD samples from unlabeled "in-the-wild" data. The method works in two stages: (1) a greedy iterative algorithm that filters candidate outliers from a wild mixture by optimizing the L₂ deviation between the InD mean gradient and the EWM of the remaining set's gradients, and (2) training a binary OOD detector on the identified outliers together with labeled InD data. The paper provides theoretical bounds on inlier and outlier misclassification rates under sub-Gaussian assumptions and evaluates Medix across 11 InD-OOD pairs against 20 baselines, reporting improvements over WOODS and other methods.

## Strengths

- **Novel application of median-based filtering to OOD detection.** Using the element-wise median (EWM) of gradients to identify OOD samples from wild unlabeled data is a genuinely new idea. Most prior work on "in-the-wild" OOD detection uses constrained optimization (WOODS) or arbitrary thresholding on scores; the median provides a principled robustness anchor that is theoretically grounded. This is not an incremental modification of an existing pipeline.

- **Effective motivation experiment (Figure 1).** The demonstration that the L₂ deviation between the InD mean gradient and the EWM of the wild gradients increases monotonically as OOD samples are added provides a clear, intuitive rationale for the optimization objective in Equation 4. This well-designed sanity check makes the method's mechanism easy to grasp.

- **Strong empirical results across CIFAR-10 and CIFAR-100.** On CIFAR-100, Medix achieves an average FPR95 of 5.42% compared to WOODS's 6.74%, and on CIFAR-10, 0.80% vs. 3.40%. The improvements are consistent across challenging OOD sets like PLACES365 and TEXTURES, and the margin over methods that do not use wild data is substantial.

## Weaknesses

### Major

- **Mismatch between theoretical guarantee and experimental regime on contamination proportion π.** Theorem 4.1 requires π < 0.5 for the bound to be controlled, and the text explicitly states "as long as the contamination ratio π < 0.5." Yet every experiment in Section 5.1 (line 170) sets π = 0.5 as the "default mixing parameter." At π = 0.5, the contamination term π/(2(1-π)) = 0.5, which bounds the inlier misclassification rate at up to 50% (plus concentration terms). While this bound is not vacuous, the theorem's strict inequality means the theoretical guarantee as stated does not cover the exact regime tested. The paper's claims of robustness "up to 50% OOD contamination" (abstract, conclusion, contribution C2) are inconsistent with the theorem's π < 0.5 condition. This is not a minor parameter quibble — the central theoretical contribution (C2) is presented as a guarantee for contamination levels "below 50%" while experiments operate at the boundary.

- **Asymmetric error reporting for baselines.** Tables 1 and 2 report standard deviations (±) only for Medix (five runs). None of the 20 baselines show any variance. The caption reads "Performance averaged over five runs; best results are highlighted in bold," implying all results are averaged, but the absence of variance for baselines means the reader cannot assess whether Medix's margins over WOODS (e.g., 1.32 percentage points on CIFAR-100 FPR95 average) are statistically significant. Given that some baseline results show large variation across OOD sets (e.g., OE on CIFAR-100 ranges from FPR95 of 1.23% on LSUN-RESIZE to 40.21% on PLACES365), per-dataset variance over runs is needed for a fair comparison.

- **Computational cost of Algorithm 1 not addressed in the main text.** The algorithm computes, at each iteration, the EWM of the gradient set with each individual sample removed — for each i ∈ S, it computes EWM(G_{S \ {i}}), requiring a pass over all remaining samples and all gradient dimensions. For a wild set of size m ≈ 50,000 (25k InD + 25k OOD at π = 0.5) and gradient dimension d (at least 1,280 for CIFAR-10 penultimate-layer weights), a single iteration appears to cost O(m²·d) operations (~3.2 × 10¹²), before accounting for the outer loop that removes k samples per iteration and iterates until convergence. The paper mentions "computational efficiency" in Appendix A.6 (line 238) but provides no explanation in the main text of how this cost is mitigated. If no approximation is used, the algorithm appears infeasible at the reported dataset scales; if an approximation is used (e.g., incremental median updates), it must be described in the main text because it affects correctness.

### Minor

- **Theorem 4.1 defines ε = σ√(2 log(2d m_min)) but ε does not appear in the stated bound.** The bound has no dependence on the variance proxy σ or the dimension d, which is surprising for a result about sub-Gaussian random vectors in d dimensions. A standard union-bound argument over coordinates would introduce a log d factor. The concentration term shown, 2√(log(1/δ)/(2m_min)), is a simple Hoeffding-type bound that does not use the sub-Gaussian assumption. Since the proof is in the (parser-stripped) appendix, this cannot be resolved from the main text alone.

- **CONJ and DRL are listed as baselines but their results are absent from the main tables.** Section 5.1 lists CONJ (Peng et al., 2024) and DRL (Zhang et al., 2024) as baselines, and the conclusion claims Medix "outperformed state-of-the-art methods such as WOODS and DRL." However, neither CONJ nor DRL appears in Table 1 or Table 2. The paper defers these to the (stripped) appendix. If these methods are referenced in the conclusions, their results should appear in the main tables.

- **The "40.98%" improvement over KNN+ is stated ambiguously.** From Table 2, this is a reduction of 40.98 *percentage points* in average FPR95 (from 46.40 to 5.42), not a 40.98% relative reduction (which would be 88.3%). Similarly, the claim that "Medix reduces the average FPR95 by 1.32% on CIFAR-100 and 2.60% on CIFAR-10" compared to WOODS uses percentage points but reads as relative percentages. These should be disambiguated.

- **The convergence condition in Algorithm 1 (line 2: "while t ≤ T or |δ_max| > ε") is unusual.** It runs at least T iterations regardless of convergence (since t ≤ T is true until t > T). Additionally, δ_max is computed on line 10 after removing outliers on line 9, but uses δ_i values computed for the old set S (before removal in that iteration). This does not invalidate the algorithm but the logic should be clarified.

- **The main evaluation uses the "seen OOD" setting** where P_out^wild = P_out^test (the same OOD dataset is used for both wild mixture and test evaluation), following the WOODS protocol. While the paper mentions an "unseen OOD" setting in Appendix A.4 (stripped), the main claims are established under this weaker setting, which limits the generality of the "open-world" framing.

### Trivial

None.

## Nice-to-Haves

- A sensitivity analysis across π ∈ {0.1, 0.2, 0.3, 0.4, 0.5} would bridge the theory-experiment gap and be more informative than the current single-point evaluation at π = 0.5.
- Reporting which k values (from {4k, 7k, 10k, 20k}) were selected for each InD-OOD pair and whether results are sensitive to this choice would improve reproducibility.
- An incremental median update description would clarify the computational feasibility of Algorithm 1.

## Removed Points

These points from the input review were removed after verification against the paper:

1. **Criticism about the sub-Gaussian assumption being strong for neural network gradients** → REMOVED because the paper already addresses this in Remark 4.3 with empirical evidence (histogram and Q-Q plot) and provides a looser bounded-moments alternative (Theorem C.3).

2. **Criticism about Equation 4 not justifying why a subset whose EWM matches InD mean corresponds to the set of all inliers** → REMOVED because the paper motivates this via Figure 1's monotonic relationship, which is a reasonable justification for a greedy heuristic. The paper explicitly frames this as an approximation (line 93).

3. **Criticism that the separation condition ||μ_out − V̄_in||₂ ≥ Δ√d is stringent** → REMOVED because the paper explicitly discusses this as the "Separation Effect" (Section 4) and the √d factor is natural for d-dimensional Euclidean norm separation. This is a standard assumption in OOD theory, not a weakness.

## Novel Insights

None beyond the paper's own contributions. The analysis surfaces the theory-experiment mismatch on π = 0.5 as the most impactful issue, but this is an articulation of a gap already present in the paper rather than a novel discovery.

## Suggestions

1. **Resolve the π = 0.5 issue.** Either run experiments at π values strictly below 0.5 (e.g., 0.3, 0.4) to match the theorem's condition, or extend the theory to cover π = 0.5. A sensitivity analysis across multiple π values would strengthen both the empirical and theoretical contributions.

2. **Add error bars for all baselines** or at least the key competitors (WOODS, OE, KNN+), so readers can assess statistical significance.

3. **Address the computational complexity in the main text.** Even a brief explanation of how the EWM recomputation is optimized (e.g., incremental median updates, efficient δ_i computation without full EWM recomputation) would resolve the feasibility concern.

4. **Include CONJ and DRL in the main tables** or remove them from the conclusion's claims.

5. **Fix Theorem 4.1's unused ε** — either use it in the bound or remove the definition to avoid confusion.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>