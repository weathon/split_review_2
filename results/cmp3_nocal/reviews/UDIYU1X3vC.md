Here is the final consolidated review:

---

## Summary
This paper develops Proper Velocity Neural Networks (PVNNs), a complete toolkit for building hyperbolic neural networks in the Proper Velocity (PV) representation. PV space is unconstrained (ℝⁿ), unlike the bounded Poincaré ball or constrained hyperboloid, offering inherent numerical stability advantages. The paper derives the full Riemannian toolkit (Exp, Log, parallel transport, geodesic distance), builds core neural layers (MLR, FC, convolution, activation, batch normalization), and validates the framework across numerical stability benchmarks, image classification, graph node classification, and genomic sequence learning.

## Strengths

1. **Convincing numerical stability evidence.** Section 6.1 provides three complementary measurements: Table 1 (gyromultiplication failure rates) shows PV maintains zero NaN/Inf failures up to r=1000 in FP32 while the hyperboloid fails catastrophically from r=20; Table 2 (Exp/Log round-trip error) shows PV errors ~3 orders of magnitude lower than the Poincaré ball in FP32 (2.1×10⁻⁷ vs. 2.1×10⁻⁴) and near machine epsilon in FP64; Table 3 shows PV avoids both the vanishing-gradients regime (~10⁻¹²) of Poincaré and the NaN-prone exploding regime of the hyperboloid. Together these make a compelling quantitative case for PV's numerical advantage.

2. **Rigorous geometric derivation.** The paper establishes the isometry between PV space and the Poincaré ball (Theorem 4.2), then derives closed-form expressions for all core Riemannian operators (Theorem 4.3). The approach of pulling back through the isometry is mathematically sound and provides a complete, ready-to-use toolkit.

3. **Practical MLR reparameterization (Theorem 5.2).** The paper identifies that the naive PV MLR formulation requires expensive gyro-addition per class, producing an O(b×C×n) intermediate tensor. The reparameterization via (z_k, r_k) reduces this to a matrix multiplication ⟨x, z_k⟩ — a real practical concern addressed explicitly rather than deferred.

4. **Thorough ablation study.** Tables 6–9 systematically compare Riemannian vs tangent-space formulations (FC and BN), different BN variants (tangent, Euclidean, Fréchet with varying iteration counts), whether to use Exp₀ for input embedding, and different activation strategies. These ablations give a clear picture of which design decisions matter and which are interchangeable.

5. **Diverse evaluation across four tasks.** The paper tests numerical stability, image classification (fixed backbone), graph node classification (direct geometric learning), and genomic sequence learning (convolutional architecture). The genomics results (Table 10) are particularly striking — gains of 5–9 MCC points over the hyperboloid baseline with tight standard deviations.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Several downstream comparisons lack statistical precision.** On CIFAR-10 (Table 4), PV MLR (95.30±0.18) vs. Unidirectional MLR (95.12±0.20) — the gap is 0.18 with overlapping standard deviations. On CIFAR-100 (78.20±0.37 vs. 77.96±0.09), the PV variance is large relative to the gap. On Disease (Table 5, 81.15±0.23 vs. HNN++ 80.57±0.23), the gap is 0.58 percentage points with similar standard deviations. The paper presents these as "matching or outperforming" (line 301) and "consistently achieves the best performance" (line 307) without statistical tests. The clearly significant wins are on Airport (97.96 vs. 88.40, a 9.6-point gap with tight stds) and the genomics tasks (Table 10). Adding confidence intervals or explicit discussion of statistical significance would strengthen the empirical claims.

- **Hyperparameter tuning protocol across baselines is not specified.** The paper states "All models share the same architecture... they differ only in the underlying hyperbolic model" (Section 6.3). Different hyperbolic models may require different learning rates, curvature values, or initialization schemes to reach their best performance. The paper does not clarify whether hyperparameters were tuned separately per baseline or the same settings were applied uniformly. Since the core claim is that PV's advantage stems from numerical stability during training, confirming that baselines were not disadvantaged by suboptimal tuning would strengthen this conclusion.

- **No wall-clock runtime comparison.** The paper introduces new operators (dπ_x(v), gyrations for parallel transport) with non-trivial computational cost. Aside from Table 7 (BN timing), there is no end-to-end speed comparison. Practitioners need to know whether the stability benefits carry a computational overhead.

- **Curvature treatment is underspecified.** All experiments fix K=−1 (line 233). The paper does not discuss whether curvature is learned or fixed, whether different tasks benefit from different curvatures, or how curvature interacts with numerical behavior of the operators. Since curvature scales the β_x factor and the tanh⁻¹/sinh⁻¹ functions, this is a relevant design dimension.

- **Genomics baseline set is narrow.** The genomics experiments compare only against HCNN-S (Table 10). If additional HCNN variants exist with different architectures or curvature treatments, including the strongest one would make the comparison more convincing.

### Trivial
None.

## Nice-to-Haves

- **Explicitly frame the isometry as a strength.** The paper is transparent about the isometry (Theorem 4.2), but could lean into it: "PV provides the same geometric expressiveness as the Poincaré ball, with dramatically better numerical properties." This reframes the contribution as a drop-in stable replacement.
- **Show training dynamics.** If PV's advantage is numerical stability during optimization, loss curves or gradient norm trajectories for a representative task would directly connect the Section 6.1 phenomenon to downstream performance.
- **Discuss failure modes.** When might PV not be beneficial? For tasks with inherently low-curvature data, hyperbolic machinery may be unnecessary regardless of representation.

## Removed Points

These points are flagged to be removed, treated with caution:

- **C1 from harsh critic ("The isometry theorem places a fundamental ceiling").** Removed because the paper is transparent about the isometry (Theorem 4.2), frames the contribution around numerical stability ("stable alternative"), and does not claim geometric novelty. No overstatement was found — "effectiveness" in the abstract refers to experimental performance, not geometric superiority. This is a framing suggestion, not a verifiable weakness.
- **"The comparison to baselines may not be controlled for optimization effort" (harsh critic's framing of the Airport gap as "suspiciously large").** The retained version above (hyperparameter tuning protocol) addresses the methodological concern without the speculative assertion that baselines were undertuned. The Airport gap is consistent with the paper's thesis (numerical stability → better optimization → better performance).
- **"The PV convolution is not a spatially-localized operation in the Riemannian sense."** Removed as scope creep — the paper follows the established approach in prior hyperbolic CNN work (Shimizu et al., 2021; Bdeir et al., 2024).
- **Generic "no discussion of failure modes"** — moved to Nice-to-Haves.
- **Pure formatting/style nitpicks and speculation about missing appendix content** — removed per instructions.

## Novel Insights

None beyond the paper's own contributions. The observation that the isometry between PV and the Poincaré ball implies the advantage is purely numerical/optimization-based rather than geometric is evident from Theorem 4.2 in the paper itself.

## Suggestions

1. Add statistical significance indicators (confidence intervals or paired tests) for the downstream comparisons, especially CIFAR-10/100 and Disease.
2. Report wall-clock runtime for forward/backward passes of PV operators vs. Poincaré and hyperboloid equivalents.
3. Clarify hyperparameter tuning protocol: were baselines tuned separately or with uniform settings?
4. Discuss curvature sensitivity — are results robust to K≠−1?
5. Include training curves (loss or gradient norms) for at least one graph learning task.
6. Consider expanding genomics baselines beyond HCNN-S.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>