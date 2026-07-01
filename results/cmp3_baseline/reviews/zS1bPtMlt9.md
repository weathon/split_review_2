## Summary

This paper introduces REPL, a semi-supervised learning framework for LiDAR semantic segmentation that directly refines noisy pseudo-labels rather than discarding or reweighting them. REPL uses a teacher-student architecture with a pseudo-label refiner that identifies unreliable predictions via confidence-based agreement and corrects them through masked reconstruction, supported by a theoretical analysis establishing conditions for beneficial refinement. The method achieves state-of-the-art results on nuScenes-lidarseg and SemanticKITTI across various label ratios.

## Strengths

- **Novel and well-motivated approach to a chronic problem**: Instead of post-hoc filtering or loss reweighting of noisy pseudo-labels (the dominant paradigm), REPL directly refines them through masked reconstruction. This is a principled shift in how the confirmation bias issue is tackled in semi-supervised LiDAR segmentation, and the idea is cleanly executed.

- **Strong empirical results with thorough analysis**: The method achieves the highest average mIoU on both benchmarks (71.3 on nuScenes, 61.6 on SemanticKITTI) and is consistently among the best at every label ratio. The paper goes beyond reporting final numbers by showing pseudo-label quality improvement throughout training (Figure 5), analyzing the benefit region for refinement (Figure 2), and providing a detailed component ablation (Tables 2, 3).

- **Theoretical grounding with practical verification**: Proposition 2 formalizes the trade-off between error correction and error introduction, providing a concrete condition (ζ > 0) for when refinement helps. The empirical analysis at two label ratios (Figure 2) confirms that REPL operates well within the benefit region, bridging theory and practice.

- **Principled handling of limited supervision for the refiner**: The combination of random masking (making reconstruction harder), scene mixing (exposing the refiner to diverse errors), and negative learning on unlabeled data addresses the fundamental challenge of training a refiner when ground truth is scarce. This is a thoughtful design.

## Weaknesses

### Fatal
None.

### Major

- **Claim of state-of-the-art is slightly overstated**: On SemanticKITTI, REPL is best at 1% and 50% but is outperformed by AIScene at 10% (62.5 vs 63.3) and 20% (63.2 vs 63.7). While the average is highest, the paper should acknowledge this nuance rather than claiming SOTA without qualification. The abstract and conclusion claim "state of the art" without caveats.

- **Theoretical novelty is modest**: Proposition 1 (H(Y|X,T) ≤ H(Y|X)) is a direct consequence of the data processing inequality—conditioning on additional information cannot increase entropy. This shows the refinement task is "easier" in an information-theoretic sense, but it is a standard fact rather than a substantive new insight. Proposition 2 is the more useful contribution, but the analysis would be strengthened by deriving tighter bounds or connecting it to the learning dynamics.

### Minor

- **No error bars or confidence intervals**: The main results (Table 1) and ablation studies report single mIoU values without variance. Given that semi-supervised methods can have non-trivial run-to-run variance, especially at low label ratios, the absence of uncertainty quantification weakens the reliability claims. Results should be reported as mean ± std over multiple seeds.

- **Limited hyperparameter sensitivity analysis**: κ (confidence percentile) is tested at only three values (0.2, 0.4, 0.6). The negative learning top-k is fixed at 3 without ablation. The random masking probability σ is set to 0.15 without sensitivity study. More thorough exploration would increase confidence in the robustness of the method.

- **Computational overhead is non-trivial but under-discussed**: Adding 0.25s (58% increase) and 396MB (32% increase) per scene is moderate but not negligible. The paper correctly notes the +9.1 mIoU gain, but in deployment-critical settings this trade-off deserves more discussion (e.g., whether the refiner can be distilled or applied selectively).

- **Large gap between heuristic and oracle error masks**: Table 4 shows the oracle mask achieves 67.3 mIoU vs 60.0 for REPL's heuristic. This 7.3-point gap indicates substantial room for improvement in error detection. The paper acknowledges this but does not analyze what kinds of errors the heuristic misses or how to close this gap.

### Trivial

- The notation in Section 3.3 uses $\mathcal{L}_{\text{runl}}$ but Equation 5 uses $\mathcal{L}_{\text{runl}}$ while Table 2 uses $\mathcal{L}_{\text{runi}}$; this inconsistency is likely a parser artifact.

## Nice-to-Haves

- An analysis of which classes benefit most from refinement (e.g., rare vs. frequent classes) would provide insight into when the refiner is most effective.
- Comparison against a baseline that applies the same refiner architecture but trained only with supervised data (without the semi-supervised training strategy) would isolate the value of the negative learning and mixing components more clearly.
- Discussion of whether the refiner could be applied at test time for models deployed without retraining, or if it is only useful during training.

## Novel Insights

Beyond the paper's own contributions, the key insight is that pseudo-label quality can be improved through reconstruction-based correction rather than just selection, and that this correction is feasible even with limited labeled data when combined with random masking and scene mixing. The analysis of the ζ condition reveals that refinement can tolerate a surprisingly high error introduction rate (up to ~11× the correction rate at π=0.917) and still be beneficial, which explains why even a simple heuristic error detector works well in practice. This suggests that the community may be over-investing in complex filtering mechanisms when simpler correction strategies could be equally or more effective.

## Suggestions

- Rephrase the "state-of-the-art" claim to acknowledge the per-ratio results (e.g., "achieves the best average performance across all label ratios and is SOTA at most ratios").
- Add standard deviations over 3-5 runs for the main results and key ablations.
- Conduct a sensitivity analysis on the random masking probability σ (e.g., {0.05, 0.10, 0.15, 0.20}) and the top-k parameter for negative learning.
- Discuss why REPL underperforms AIScene at 10% and 20% on SemanticKITTI—is this a dataset-specific issue or a more fundamental limitation of the refinement approach at certain label ratios?

## Score and Decision

**Score**: 7.5  
**Decision**: Accept

The paper presents a well-motivated, novel framework for a known problem in semi-supervised LiDAR segmentation, with solid theoretical grounding, thorough ablation, and strong empirical results. The weaknesses are addressable and do not invalidate the core contributions. This work will be valuable to the community as a new direction for pseudo-label quality improvement.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>