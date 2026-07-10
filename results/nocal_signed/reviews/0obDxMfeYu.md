Now let me write the final consolidated review.

## Summary

This paper introduces Medix, a framework for OOD detection that uses median-based gradient filtering to extract OOD samples from unlabeled wild-data mixtures. The approach has two stages: (1) an iterative outlier-extraction algorithm (Algorithm 1) that finds candidate OOD samples by tracking how the element-wise median of wild-data gradients deviates from the mean InD gradient, and (2) training a binary OOD detector on the extracted outliers plus labeled InD data, following the protocol of Du et al. (2024a). The paper provides theoretical guarantees (Theorems 4.1 and 4.2) bounding inlier and outlier misclassification rates via contamination, concentration, and separation effects, and reports strong empirical results on CIFAR-10 and CIFAR-100.

## Strengths

- **Theoretical framing is a genuine contribution.** The paper is one of the few works in wild-data OOD detection to provide formal guarantees. Theorems 4.1 and 4.2 decompose misclassification risk into contamination, concentration, and separation effects, and the analysis identifies the π < 0.5 threshold where median-based filtering remains stable. This theoretical scaffolding is a meaningful addition to a literature that has been mostly empirical.

- **Strong empirical results, especially in the matched-OOD setting.** On CIFAR-10 (Table 1), Medix achieves 0.80% average FPR95 compared to WOODS's 3.40% — a substantial improvement. Results on CIFAR-100 (Table 2: 5.42% vs. WOODS's 6.74%) are more modest but still positive. The gap over InD-only methods like KNN+, CSI, and ASH is very large in most cases.

- **Novel median-based filtering approach.** The median-centric perspective for outlier extraction from unlabeled mixtures is conceptually clean and distinct from prior threshold-based filtering methods. The contamination-effect analysis (π < 0.5) provides useful insight into when the method can be expected to be stable.

## Weaknesses

### Major

- **The filtering mechanism computes gradients using predicted (argmax) labels for wild/OOD samples, but neither the method analysis nor the theory accounts for this.** In Equation 4 and Algorithm 1, the gradient for a wild sample is computed as ∇ℓ(f_{φ}(x̃_i), ŷ_{x̃_i}), where ŷ is the predicted label from the InD classifier. For an OOD sample, this predicted label is essentially arbitrary — the model was trained on K InD classes and is processing an input from a completely different distribution. Theorem 4.2 assumes OOD gradients are i.i.d., sub-Gaussian, and have a well-separated mean (‖μ_out − ∇̄_in‖₂ ≥ Δ√d), but the paper never justifies why gradients computed with predicted (essentially meaningless) labels for OOD data would satisfy these properties. Remark 4.3 empirically verifies the sub-Gaussian assumption only for InD gradients; no such verification is provided for OOD gradients. A looser bound (Theorem C.3) that drops the sub-Gaussian assumption is relegated to the appendix with no discussion in the main text. This creates a gap between what the method actually computes and what the theory assumes.

- **CONJ and DRL are listed as baselines and DRL is claimed as outperformed in the conclusion, yet neither appears in the main results tables.** Section 5.1 states: "Finally, we included more recent baselines, including CONJ (Peng et al., 2024) and DRL (Zhang et al., 2024), to provide a more thorough evaluation." The Conclusion (Section 7) claims to outperform "state-of-the-art methods such as WOODS and DRL." But neither CONJ nor DRL appears in Table 1 or Table 2. The main paper makes empirical claims without presenting the corresponding evidence in the main text.

### Minor

- **The "40.98%" improvement over KNN+ is stated ambiguously.** The paper says "outperforming it by an average of 40.98% in terms of FPR95" (Section 1) and "reduced the average FPR95 by 40.98%" (Section 7). From Table 2: KNN+ achieves 46.40% FPR95 and Medix achieves 5.42%; the absolute difference is 40.98 percentage points, while the relative improvement is (46.40−5.42)/46.40 ≈ 88.3%. A reader naturally interprets "X% improvement" as relative, making this phrasing ambiguous at best.

- **Hyperparameter selection for ϵ and k is described as "with the objective of maximizing OOD performance" (Section 5.2) without specifying whether this uses a validation split or test set.** If test-performance-based selection is used, the comparison may not reflect a realistic deployment scenario.

- **Theorem 4.1's bound at the default experimental setting π=0.5 yields a contamination term of 0.5/(2×0.5)=0.5, guaranteeing ≤50% inlier misclassification even with infinite data.** The paper claims the rates are "tightly controlled" (Section 1, contribution C2), which overstates the practical tightness of these worst-case bounds. The bounds are mathematically valid but too loose to be informative about why Medix works well in practice. The paper would benefit from a clearer discussion of the gap between the worst-case theoretical guarantee and empirical performance.

- **The computational complexity of Algorithm 1 is acknowledged as prohibitive (line 93) but the main paper provides no runtime analysis or quantification.** With a starting N≈25,000 and k up to 20,000, the greedy leave-one-out procedure's per-iteration cost is significant, and readers evaluating practical deployment cannot assess feasibility from the main paper.

### Trivial

None.

## Nice-to-Haves

- Including Du et al. (2024a) as an experimental baseline would strengthen the empirical comparison, since the paper repeatedly cites it as the closest prior work with theoretical foundations and follows its protocol for stage 2.

## Removed Points

These points from the input review were removed with justification:

- **Computational cost "not acknowledged"**: The paper does acknowledge computational cost is prohibitive (line 93: "Solving the optimization problem... can be computationally prohibitive"). The criticism was reframed as a Minor weakness about lack of quantification.
- **Synthetic 2D example critique**: The paper states this simulation is "designed to be simple to facilitate better understanding." It is a pedagogical illustration, not a claim of general robustness.
- **Figure 1 only uses one InD-OOD pair**: Presented as a motivating experiment, not rigorous proof; appropriately scoped.
- **FPR notation concern**: The critic acknowledges the notation is consistent with OOD detection conventions.
- **"20 baselines" count discrepancy**: The appendix (stripped by parser) may contain additional baselines; cannot verify from the main paper alone.

## Novel Insights

None beyond the paper's own contributions. The key insight from the review process is the identification of a substantive gap between the gradient computation mechanism (using predicted labels for OOD data) and the theoretical assumptions (sub-Gaussian, well-separated OOD gradients), which is partially bridged by the paper's appendix references to pseudo-label quality analysis and the looser bound without sub-Gaussian assumptions.

## Suggestions

1. Provide empirical verification that OOD gradient coordinates (as computed by the method using predicted labels) are sub-Gaussian and that their mean is well-separated from the InD gradient mean — analogous to what Remark 4.3 does for InD gradients, but applied to OOD gradients.
2. Include DRL and CONJ in the main results tables, or remove claims about outperforming them from the main paper's narrative and conclusion.
3. Clarify whether the "40.98%" figure is an absolute percentage-point difference or a relative improvement.
4. Specify whether hyperparameter selection uses a validation split or the test set.
5. Provide a runtime/scalability estimate for Algorithm 1.

## Score and Decision

This paper addresses an important problem with a novel median-based filtering approach backed by theoretical guarantees that are rare in this sub-area. The empirical results on CIFAR-10 are compelling, and the theoretical decomposition into contamination, concentration, and separation effects is a genuine contribution. However, the paper has two significant issues: (1) a gap between the gradient computation mechanism (using predicted labels for OOD data) and the theoretical assumptions (sub-Gaussian, well-separated OOD gradients) that is not addressed in the main text, and (2) missing experimental baselines (DRL, CONJ) that are cited and claimed without appearing in the main results tables. These issues weaken the paper as presented but are addressable. The core contribution — median-based filtering with theoretical guarantees for wild-data OOD detection — is solid.

**MY FINAL SCORE:** <score>6</score>
**MY FINAL DECISION:** <decision>Borderline Accept</decision>