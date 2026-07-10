Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper introduces Medix, a framework for OOD detection that uses the element-wise median (EWM) of gradients to filter potential outliers from unlabeled wild data. The core idea—using the median's natural robustness to contamination as a reference point to separate InD from OOD samples—is novel and well-motivated. The method operates in two stages: (1) a greedy iterative algorithm isolates candidate OOD samples from the wild mixture based on their gradient deviation from the InD mean gradient, and (2) a binary OOD detector is trained on the identified outliers plus labeled InD data. Theoretical bounds (Theorems 4.1 and 4.2) characterize inlier/outlier misclassification rates under a Huber contamination model. Empirically, Medix achieves strong results: on CIFAR-10 an average FPR95 of 0.80% and AUROC of 99.74%, substantially beating prior wild-data methods like WOODS (3.40% FPR95).

## Strengths

- **Novel application of the element-wise median (EWM) to outlier extraction from unlabeled wild data (Section 3.1, Eq. 4).** The intuition—using the median as a robust reference point that is naturally resistant to contamination—is well motivated and cleanly formulated. This is a genuinely fresh perspective on the wild-data OOD detection problem.

- **Strong empirical results under the matched-OOD protocol.** On CIFAR-10 (Table 1), Medix achieves an average FPR95 of 0.80% and AUROC of 99.74%, substantially beating the best prior wild-data method (WOODS: 3.40% FPR95). On CIFAR-100 (Table 2), Medix achieves 5.42% average FPR95 vs. WOODS's 6.74%. Results are reported with standard deviations over 5 runs, and Medix wins on every individual OOD dataset pair across both tables.

- **Theoretical analysis with provable bounds.** Theorems 4.1 and 4.2 formalize inlier and outlier misclassification rates under the Huber contamination model, decomposing error into contamination, concentration, and separation effects. Remark 4.3 and Theorem C.3 (stripped appendix) show the sub-Gaussian assumption can be relaxed to bounded second moments.

## Weaknesses

### Fatal
None.

### Major

- **Gap between theoretical analysis and the implemented algorithm.** Theorems 4.1 and 4.2 analyze an "EWM filtering rule" that is never precisely defined, and their bounds involve oracle quantities (m_in, m_out — the true numbers of InD and OOD samples, which are unknown at run time). Algorithm 1 is a greedy, iterative leave-one-out procedure with no proven connection to these bounds. The paper claims (line 158) that the theorems "provide rigorous theoretical assurance that Medix minimizes both types of errors," but does not establish that the greedy procedure achieves, or even meaningfully approximates, the stated bounds. This is a significant disconnection between the theory and the method as actually implemented.

- **Computational cost of Algorithm 1 is substantial and its practicality is unclear.** Each iteration of Algorithm 1 computes the EWM of S (O(d·m log m)) and then, for every i ∈ S, recomputes EWM of S\{i} (O(d·m² log m) per iteration). For m=25,000 wild samples with high-dimensional penultimate-layer gradients, even a few iterations are expensive. The paper acknowledges the cost (line 93: "computationally prohibitive") but defers all analysis to Appendix A.6 (stripped). The main text gives no runtime, no complexity analysis, and no discussion of when the algorithm would become impractical for larger wild datasets.

- **Main evaluation uses matched-OOD distributions, undercutting the "open-world" claim.** The wild data construction (Section 5.1) mixes InD data with the *same* OOD dataset used at test time (e.g., PLACES365 in the wild mixture and PLACES365 as the test OOD set). This is a transductive-like setting: the model encounters unlabeled examples from the OOD distribution it will be evaluated on. An "unseen OOD" evaluation where P_out^test ≠ P_out is relegated to Appendix A.4. While the matched-OOD protocol is standard in this sub-literature (WOODS, Du et al. 2024a), the abstract's claim that Medix works "in open-world settings" is overstated for the main evidence presented.

### Minor

- **Hyperparameter k lacks a principled selection criterion.** The number of samples removed per iteration, k, is searched over {4k, 7k, 10k, 20k} on validation OOD performance, which requires labeled OOD data unavailable in practice. With k=10,000 the entire wild set is emptied in ~2–3 iterations; with k=4,000, ~6 iterations. This fundamentally determines filtering aggressiveness, yet no theoretical guidance is offered for its choice.

- **Missing comparison with the most closely related method (Du et al. 2024a).** The paper identifies Du et al. (2024a) as the only other work providing a theoretical foundation for the same in-the-wild setting and notes their thresholding approach "differs fundamentally" (line 258). A direct empirical comparison on the same benchmarks would be highly informative but is absent from Tables 1 and 2.

- **Gradient dimensionality is not reported.** The paper uses penultimate-layer gradients for computation but never states their dimensionality. This information is needed to interpret the scale of the L2-norm deviations in Figure 1 (range ~0.001–0.004) and to assess the computational cost of the leave-one-out EWM computations.

### Trivial
None.

## Nice-to-Haves

- A complexity analysis and wall-clock runtime for the CIFAR experiments in the main paper (rather than only in the appendix).
- An explicit definition of the "EWM filtering rule" that the theorems analyze, and a discussion of how Algorithm 1 approximates it.
- A calibrated description of the evaluation setting in the abstract/introduction that distinguishes the matched-OOD protocol from an "unseen OOD" setting.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"Unfair comparison with InD-only baselines due to dataset split (25K vs. 50K)."** — Removed because the asymmetry favors the baselines (they get more labeled data). The paper explicitly acknowledges this (line 182), and Medix still outperforms them, making the comparison conservative rather than unfair.

2. **"Tiny deviation signal in Figure 1 may be noise."** — Removed because the monotonic trend in Figure 1 is clearly demonstrated, and small absolute L2-norm values are expected for high-dimensional gradient vectors. The signal is not shown to be noise.

3. **"Monotonicity of addition does not imply marginal contribution of individual samples is detectable."** — Removed as speculative. The algorithm does not rely on this implication being strictly true for every single sample; it aggregates over k samples per iteration.

4. **Formatting/style nitpicks and speculation about missing appendix content.** — Removed per guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Bridge the theory-algorithm gap by formally defining the "EWM filtering rule" that the theorems analyze and explaining how Algorithm 1 relates to it, ideally with an approximation bound or a proof that the greedy procedure's output respects the same misclassification guarantees.
- Include a complexity analysis and wall-clock runtime for the main experiments in the paper body, not just the appendix.
- Calibrate the "open-world" language in the abstract and introduction to the matched-OOD setting, making clear that the unseen-OOD results are a secondary contribution.
- Report the dimensionality of the penultimate-layer gradients used.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>