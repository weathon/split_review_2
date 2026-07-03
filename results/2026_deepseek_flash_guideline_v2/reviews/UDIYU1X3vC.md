Now let me write the final consolidated review.

## Summary

The paper introduces Proper Velocity Neural Networks (PVNNs), leveraging the Proper Velocity (PV) model — an unconstrained parametrization of hyperbolic space from special relativity — as an alternative to the constrained Poincaré ball and hyperboloid models for building hyperbolic neural networks. The authors establish the complete Riemannian toolkit for PV space (exponential/log maps, parallel transport, geodesic distance) via isometry with the Poincaré ball, then construct core neural network layers (MLR, FC, convolutional, activation, batch normalization) in this space. Experiments across numerical stability, image classification, graph node classification, and genomic sequence learning demonstrate improved numerical stability and competitive or superior performance compared to existing hyperbolic models.

## Strengths

1. **Closed-form Riemannian operators derived via isometry (Theorems 4.2–4.3):** The paper proves PV space is isometric to the Poincaré ball and uses this to derive closed-form expressions for the exponential map, logarithmic map, parallel transport, and geodesic distance in PV coordinates. This is a clean, efficient approach that provides the theoretical foundation for constructing neural networks in PV space.

2. **Efficient PV MLR parametrization avoiding memory blowup (Theorem 5.2):** The paper identifies that a naive PV MLR formulation would require explicit gyroaddition per class, producing a b×C×n intermediate tensor. The proposed (z_k, r_k) parametrization reduces computation to a matrix multiplication via Eq. (19), a practical engineering contribution that makes PV MLR feasible at scale.

3. **Quantitative numerical stability evidence across three metrics (Section 6.1, Tables 1–3):** PV achieves zero failure rate up to r=1000 in FP32, and its round-trip error (2.1×10⁻⁷ in FP32) is three orders of magnitude smaller than Poincaré (2.1×10⁻⁴) and seven orders smaller than hyperboloid (1.0×10⁰). These results directly and convincingly support the paper's central claim about numerical stability.

4. **Consistent across-task validation with strong gains on hyperbolic-rich datasets (Tables 5 and 10):** On graph node classification, PVNN achieves 81.15% on Disease (vs. 80.57% best baseline) and 97.96% on Airport (vs. 92.10% best baseline). On genomic sequence learning, PVCNN outperforms HCNN-S on all five TEB tasks with gains of 5.71–8.33 MCC points (e.g., SINEs: 93.78 vs. 85.45). The breadth of tasks and consistency of results (best on 3/4 graph datasets, 5/5 genomic datasets) strengthen the case for practical usefulness.

5. **Ablation isolating the benefit of Riemannian PV layers over tangent-space alternatives (Table 6):** The comparison of PV FC vs. tangent-space FC shows a 10.94% gap on Airport (97.93% vs. 86.99%), directly attributing performance gains to the gyro-vector construction rather than just the PV coordinate space.

6. **Principled PV Batch Normalization with homogeneity guarantees (Theorem 5.4):** The extension of GyroBN to PV space with proven homogeneity properties (Eqs. 26–27) provides theoretical grounding that goes beyond prior Riemannian BN approaches, as noted in the related work.

## Weaknesses

### Fatal
None.

### Major

- **The graph learning comparison (Table 5) requires better justification of the large baseline spread.** On Airport, the spread among hyperbolic models is over 22 points (LNN: 75.20, HNN: 82.16, HNN++: 88.40, KNN: 92.10, PVNN: 97.96). The paper states (line 305) that all models share "the same architecture consisting of two FC layers with nonlinear activations followed by an MLR classifier" and differ only in the underlying hyperbolic model. While different hyperbolic parametrizations can indeed yield different optimization landscapes, the magnitude of the gap — especially LNN (75.20) vs. the rest — is large enough to raise questions about whether all baselines received comparable hyperparameter tuning. The paper does not report per-model tuning budgets, learning rate schedules, or optimization details in the main text (these may be in the stripped appendix). This does not invalidate the paper's core contribution (PV as a numerically stable parametrization) but it weakens the claim that "PVNN consistently achieves the best performance" in graph learning and makes the comparison uninterpretable as evidence of PV's superiority. **This is a significant concern that the authors must address in rebuttal.**

### Minor

- **Cora results show unusual volatility in the batch statistics ablation (Table 7).** Tangent gets 33.10%, Euclidean gets 32.62%, while Fréchet 5 iter reaches 49.50%. This extreme sensitivity on a relatively simple dataset like Cora — with standard deviations up to 6.15 for Fréchet 1 iter — suggests the experimental setup may be fragile on this particular dataset. A brief discussion of why Cora is particularly sensitive would improve the paper.

- **No discussion of limitations or settings where PV may not be advantageous.** The paper is notably silent on this. Given that PVNN underperforms LNN on Cora (Table 5: 51.42 vs. 53.34), the image classification gains are marginal (Table 4: 95.30 vs. 95.12 on CIFAR-10), and the Fréchet-based GyroBN introduces 2–3× slowdown (Table 7), a limitations paragraph acknowledging when the PV parametrization may not help would strengthen credibility.

- **Computational cost of PV core layers is not analyzed.** The PV FC layer involves sinh computations (Eq. 22), which are more expensive than a Euclidean FC layer. Only GyroBN timing is reported (Table 7). A wall-time comparison between PVNN and Poincaré/hyperboloid counterparts would help practitioners assess the practical tradeoff.

- **Curvature K setting not explicitly reported for downstream experiments.** Line 233 states K = −1 for the numerical stability experiments in Section 6.1, but it is not stated whether the same value is used in Sections 6.2–6.4 or whether curvature was tuned per task. (The appendix, which was stripped by the PDF parser, may contain these details.)

### Trivial
None.

## Nice-to-Haves

- Connecting the numerical stability advantage more directly to training outcomes (e.g., training loss curves or gradient norms during actual training for PVNN vs. Poincaré networks).
- Reporting hyperparameter tuning budgets and search ranges for all graph learning baselines in the main text.

## Removed Points

These points were raised by one or both input reviewers but are removed as invalid, misinformed, or outside the paper's scope:

1. **"Contribution is about numerical parametrization, not a new geometry" (Harsh Critic Issue 2):** Removed as a strawman. The paper is transparent throughout that PV is a parametrization of hyperbolic space. The abstract states "an unconstrained representation of hyperbolic space... as a stable alternative." The contributions (lines 24–26) describe "the complete Riemannian geometric toolkit" for PV. The paper never claims a fundamentally different geometry — the numerical stability advantage of an unconstrained parametrization is the explicit contribution. This criticism misreads the paper's claims.

2. **"Numerical stability experiments evaluate edge cases not relevant in practice" (Harsh Critic Issue 3, partial):** Removed because the downstream experiments (especially genomic sequence learning with ~9 MCC point gains on SINEs, Table 10) directly validate the practical relevance of the PV parametrization. Numerical stress-testing (r=1000, ‖v‖=10) is a standard technique to demonstrate stability bounds and does not require claiming these exact values occur during training. The paper's comparison is fair: all models are tested under the same conditions.

3. **Missing appendix, proofs, or references:** Removed as a parser artifact — these sections exist in the original submission. The reproducibility statement (line 387) explicitly states "complete proofs in App. E" and "experimental details in App. C."

4. **Generic formatting/style nitpicks:** Removed as not substantive.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Address the graph learning comparison fairness.** For the rebuttal, provide per-model hyperparameter tuning details (search budgets, ranges, number of trials) for Table 5. If all models used the same hyperparameters without per-model tuning, acknowledge this and either provide evidence that the results are robust to hyperparameter choices (e.g., learning rate sweeps) or temper the claim from "consistently achieves the best performance" to "performs competitively."

2. **Add a brief discussion of Cora sensitivity** in Table 7, explaining why this dataset is particularly volatile under different batch statistics approximations.

3. **Include a limitations paragraph** in the conclusion acknowledging when the PV parametrization may not outperform baselines and discussing the computational overhead of PV layers.

4. **Report the curvature K value(s) used** for the downstream experiments (image classification, graph learning, genomic sequence learning) in the main text.

## Score and Decision

**Calibration:** The calibration corpus was unavailable for querying. Score is based on direct assessment of the paper against ICLR standards.

**Reasoning:** This paper makes a genuine contribution — it provides the first systematic treatment of the Proper Velocity model for hyperbolic neural networks. The theoretical derivations are sound, the numerical stability evidence is strong (3+ orders of magnitude improvement in round-trip error), the practical MLR optimization (Theorem 5.2) is non-trivial, and the genomic sequence learning results demonstrate substantial real-world value (up to +8.33 MCC). The ablations (Table 6) convincingly isolate the benefit of Riemannian PV layers. However, the graph learning comparison (Table 5) has a significant fairness concern: the 22-point spread among hyperbolic models on Airport with ostensibly the same architecture demands explanation. This weakens the performance superiority claims but does not undermine the core contribution — the first PV Riemannian toolkit, numerical stability evidence, and genomic results stand on their own. The paper is clearly above the borderline threshold and warrants acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>