Now let me produce the final consolidated review.

## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), which use the Proper Velocity (PV) space — an unconstrained coordinate representation of hyperbolic geometry — as a foundation for building hyperbolic neural network layers. The authors derive the Riemannian operators (exponential/logarithmic maps, parallel transport, geodesic distance) on PV space via its isometry to the Poincaré ball, develop core neural layers (MLR, FC, convolution, activation, and batch normalization), and validate them across numerical stability experiments, image classification, graph node classification, and genomic sequence learning.

## Strengths

1. **Sound theoretical derivation with clean proofs.** Section 4 establishes the Riemannian operators on PV space by leveraging the isometry with the Poincaré ball (Theorem 4.2). The derivation strategy is mathematically rigorous and produces usable closed-form expressions. The isometry is explicitly proven, providing a principled foundation.

2. **Numerical stability is convincingly demonstrated.** Section 6.1 (Tables 1–3) provides clear, well-designed evidence that PV avoids catastrophic numerical failures that plague the hyperboloid model (100% NaN at r=200 in FP32) and the gradient vanishing that affects the Poincaré ball. The round-trip error (Table 2) shows 3–5 orders of magnitude improvement over Poincaré in FP32. This is the paper's strongest and most distinctive contribution.

3. **Elegant MLR parameterization.** Theorem 5.2 gives a closed-form PV MLR score that (a) avoids Riemannian optimization by depending only on inner products ⟨x, z_k⟩, (b) can be implemented as a matrix multiply rather than requiring explicit gyroaddition per class, and (c) correctly recovers Euclidean MLR as K→0⁻. This is a genuine engineering improvement over the naive formulation.

4. **Diverse experimental validation and extensive ablations.** The paper evaluates on four substantially different tasks (stability, vision, graphs, genomics) and provides ablations on tangent vs. Riemannian layers (Table 6), batch normalization variants (Table 7), exponential map usage (Table 8), and activation choices (Table 9). This is appropriate for a foundational-layer paper.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Image classification gains are marginal and not tested for significance.** On CIFAR-10, the best PV variant (without Exp₀, 95.30%) differs from the strongest baseline (Unidirectional MLR, 95.12% ± 0.20) by only 0.18 pp — well within one standard deviation of the baseline. On CIFAR-100, PV's best (78.20%) vs. Lorentz MLR (77.96% ± 0.09) is a 0.24 pp difference, which is more notable but still small. No statistical significance tests are reported. The paper's claim that PV "matches or outperforms" baselines is technically accurate, but a reader could overinterpret this as a meaningful improvement when the evidence only supports a tie with a slight directional advantage.

2. **The origin of large graph learning gains is not analyzed.** The Airport result (PVNN 97.96 vs. KNN 92.10, a 5.86% absolute improvement) is striking, but the paper provides no training dynamics analysis — convergence curves, gradient norms, or loss trajectories — that would help establish why PV outperforms isometric baselines by such a margin. Since PV is isometric to Poincaré, the gains presumably come from optimization dynamics rather than representational capacity, but this is never verified. The ablations (Tables 6–9) provide partial insight but do not directly address this mechanism.

3. **Curvature handling is under-specified in the main text.** Curvature K is a critical hyperparameter. It is fixed to K=−1 for the stability experiments (Sec. 6.1). The genomic learning section says "a single curvature shared for all layers" but does not state the value or how it was chosen. For image and graph experiments, curvature treatment is not discussed at all in the main text. While details may reside in the appendix (App. C, which is standard), the main text should provide enough information for readers to assess whether curvature choices systematically favor PVNN.

4. **No end-to-end computational cost comparison.** The paper reports internal timing for GyroBN variants (Table 7) but does not compare training time or FLOPs of PVNN against Poincaré or hyperboloid baselines on any task. Since PV operations involve hyperbolic functions (sinh, sinh⁻¹, tanh⁻¹), readers need to know whether the numerical stability benefits come at a computational premium.

### Trivial
None.

## Nice-to-Haves

- Provide training dynamics (convergence curves, gradient norms) for the Airport graph task to clarify the mechanism behind the large gains.
- Report a computational cost comparison (wall-clock time per epoch) against at least one baseline on one task.
- Include a brief limitations paragraph acknowledging that PV is isometric to Poincaré, so advantages stem from optimization stability rather than geometric expressiveness.

## Removed Points

These points from the input review were removed; treat them with caution.

- **"Core contribution is a numerically stable coordinate parameterization, not new geometric capability."** The paper explicitly proves the isometry (Theorem 4.2) and frames PV as an "alternative representation" throughout. It does not claim new geometric capabilities; the claims are about numerical stability and practicality. The isometry implication is already established mathematically in the paper. This is a framing preference, not a factual weakness.

- **"Hyperparameter tuning imbalance and architecture differences confound graph learning comparison."** This is speculative ("If the paper tuned hyperparameters for PVNN but not for the baselines…"). The paper states "All models share the same architecture" and cites appendix details. No concrete evidence of an actual imbalance is provided.

- **"Poorly implemented Poincaré layer could underperform."** Entirely speculative — no evidence or concrete concern is given.

- **"Missing discussion of prior attempts to address numerical stability."** This is a related-work suggestion, not a weakness.

- **"No limitations section."** The paper has standard conclusion and reproducibility/ethics statements. The absence of an explicit limitations section is a formatting preference.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a sentence or two in the introduction or conclusion acknowledging that PV's advantages stem from numerical stability in an unconstrained coordinate system of the **same** hyperbolic geometry (isometric to Poincaré), not from greater geometric expressiveness.
2. Report at least a simple indication of statistical significance (e.g., "the difference is not significant at α=0.05 given the observed variance") for the image classification results.
3. Add training loss curves or gradient norm trajectories for the Airport graph task to clarify the mechanism behind the 5.86% improvement.
4. State curvature values used for each method and dataset in the main text.

---

**Calibration.** Round 1 queried the calibration corpus for topically similar papers. The strongest anchors were:

| Path | Avg Human Score | Comparison Summary |
|------|----------------|-------------------|
| ekz1hN5QNh.md (Fully Hyperbolic CNNs) | 6.00 | Very similar HNN paper; accepted despite marginal vision gains and limited mechanistic analysis. PVNN has stronger theory and clearer stability evidence. |
| bwOndfohRK.md (Symmetric Spaces) | 6.00 | Related non-Euclidean NN paper; accepted with similar presentation/analysis weaknesses. |
| WOopKWDWtS.md (Optimizing Hyperbolic Learning) | 4.40 | Rejected; its contributions were less grounded and its gains more marginal than PVNN's. |
| fJNnerz6iH.md (Magnitude Invariant Parametrizations) | 6.25 | Less topically related but similar in making numerical stability the core contribution. |

**Round-1 bracket:** [5.5, 7.5]. The paper is clearly stronger than the 4.4-level rejections (which had unsupported claims and no theoretical grounding) and comparable to the 6.0-level accepted hyperbolic NN papers, with slightly stronger theoretical contributions and clearer empirical differentiation on numerical stability. A score of **7.0** reflects that the paper makes a solid, well-grounded contribution with clear practical value (numerical stability), where the main limitations are modest downstream gains and missing mechanistic analysis — issues that do not undermine the core contribution.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>