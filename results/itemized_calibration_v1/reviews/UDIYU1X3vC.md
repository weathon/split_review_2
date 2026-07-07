Now I have sufficient calibration context. Let me produce the final review.

**Bracket (Round 1):** I place this paper between 5.5 and 6.5. The closest anchors are ekz1hN5QNh.md (avg 6.00, fully hyperbolic CNNs) and bwOndfohRK.md (avg 6.00, symmetric space NNs). Our paper has comparable theoretical contribution and better numerical stability evidence than these anchors, but the unexplained Airport FC gap pulls it down relative to them. It is substantially stronger than WOopKWDWtS.md (avg 4.40) and MEnPLXJNng.md (avg 4.75).

**Narrowing:** Against ekz1hN5QNh.md (6.00): shared positive items include developing new hyperbolic operators and broad experiments; shared negative include some modest improvements within error bars. Our paper has stronger numerical stability evidence and better ablations, but also has the unexplained Airport gap which the anchor lacks. On balance, similar quality but with a notable evidential gap → 6.0.

Here is the final review:

---

## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), the first systematic treatment of the Proper Velocity (PV) model of hyperbolic geometry for deep learning. The PV model is an unconstrained representation (ℝⁿ) of hyperbolic space, unlike the bounded Poincaré ball or the constrained hyperboloid model, which suffer from numerical instabilities near boundaries. The paper derives closed-form Riemannian operators (exponential/logarithmic maps, parallel transport, geodesic distance), develops core neural network layers (MLR, FC, convolution, activation, batch normalization), and validates the framework across four tasks: numerical stability, image classification, graph node classification, and genomic sequence learning.

## Strengths

1. **Clean numerical stability demonstration (Section 6.1, Tables 1–3).** This is the paper's best-controlled contribution. The PV model shows zero failure rate up to scalar multiplier r=1000 in FP32, matching the Poincaré ball but massively outperforming the hyperboloid model (100% failure by r=200). The round-trip error in FP32 is orders of magnitude better than both competitors (2.1×10⁻⁷ for PV vs 2.1×10⁻⁴ for Poincaré vs 1.0×10⁰ for hyperboloid). The gradient stability results (Table 3) are similarly clean and informative.

2. **Sound theoretical grounding (Section 4).** The paper correctly identifies and proves the Riemannian isometry between PV space and the Poincaré ball (Theorem 4.2), derives closed-form Riemannian operators (Theorem 4.3), and obtains a simplified MLR formulation (Theorem 5.2) that replaces an O(b×C×n) intermediate tensor with a single matrix multiplication. The derivations are mathematically sound.

3. **Broad experimental evaluation with informative ablations.** The paper evaluates across four distinct tasks and includes multiple meaningful ablations: tangent vs. Riemannian FC (Table 6), GyroBN vs. tangent BN (Table 6), Fréchet iteration count (Table 7), Exp₀ vs. no Exp₀ (Table 8), and activation types (Table 9). This breadth is valuable for a first paper proposing a new hyperbolic representation.

## Weaknesses

### Fatal
None.

### Major
1. **The large Airport performance gap between Riemannian FC and tangent-space FC (Table 6) is not adequately explained and raises optimization-fairness questions.** On Airport, PVNN (Riemannian FC) achieves 97.93±0.29 while PVNN+TFC (tangent-space FC: Exp₀(A Log₀(x)+b)) achieves only 86.99±0.61 — an 11-percentage-point gap. For context, the next best baseline of any type on Airport (KNN) is 92.10±0.97, meaning the tangent-space FC variant performs *worse* than competing approaches using different geometries, despite being derived from the same PV framework. This gap is far larger than what the tangent vs. Riemannian difference produces on other datasets (e.g., Disease: 80.86 vs 81.24). The paper does not provide training curves, learning rate sweeps, or any evidence that the TFC variant received comparably tuned hyperparameters. Without such evidence, the reader cannot distinguish between a genuine architectural advantage of the Riemannian FC and an undertuned baseline. This is the paper's most significant evidential gap.

### Minor
1. **Statistical significance testing is absent for the main comparisons.** Several headline improvements are modest and fall within overlapping error bars (e.g., CIFAR-100: PV MLR at 78.20±0.37 vs. Lorentz MLR at 77.96±0.09; PubMed: PVNN at 74.33±0.22 vs. HNN++ at 73.68±0.39; Disease: PVNN at 81.15±0.23 vs. HNN++ at 80.57±0.23). Given that 5-fold cross-validation produces fold-level results, a paired test across folds would straightforwardly quantify reliability. While not universally required, the modest margins in several comparisons would benefit from such quantification.

2. **The framing in the abstract and introduction could more directly acknowledge the isometry.** Section 4.1 is transparent about the isometry between PV space and the Poincaré ball (Theorem 4.2). However, the abstract and contributions list describe PV as "a new alternative to classical hyperbolic models" without explicitly stating that the *geometry* is the same — the contribution is a coordinate representation with superior numerical properties, not a distinct geometric structure. This is a presentational issue rather than a scientific one, but addressing it would prevent expert readers from feeling the contribution is oversold.

3. **No comparison of computational cost against baseline models.** The PV exponential map, logarithmic map, and parallel transport (Eqs. 10–12) involve trigonometric/hyperbolic functions and multiple compositions. Table 7 reports GyroBN fitting time but not overall per-epoch training time compared to HNN, LNN, or other baselines. A practitioner would need to know the practical cost of adopting PVNNs.

### Trivial
- The paper does not state whether curvature is learned or fixed across experiments beyond noting K=-1 is used throughout. This is a minor clarity gap.

## Nice-to-Haves
- Provide training curves or learning rate sweeps for the TFC variant on Airport to demonstrate fair tuning.
- Include a brief limitations subsection acknowledging the isometry and that the practical benefits are primarily numerical.
- Discuss whether curvature K could be learned and the sensitivity of results to this choice.

## Removed Points
These points appeared in the harsh critic input but are removed for the following reasons:
- *"The convolution definition is essentially Euclidean concatenation followed by a PV FC layer"* — This construction is standard practice for hyperbolic CNNs (cf. Shimizu et al. 2021, Bdeir et al. 2024). The paper does not claim a novel convolution operator; the comparison with HCNN-S (which uses a similar mechanism) is fair.
- *"The parallel transport formula depends on the Möbius gyration defined in the appendix"* — Appendix content is stripped by the parser; it exists in the original submission. Not a valid criticism.
- *"The paper does not discuss whether Euclidean CNN and HCNN-S baselines were re-implemented"* — The paper states "all models share the same backbone network architecture" (line 379), which directly answers this.
- Various formatting/style observations and speculation about missing appendix details.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Investigate and report hyperparameter tuning details for the TFC variant, especially on Airport; provide training curves to demonstrate fair comparison.
2. Add paired statistical tests (e.g., across CV folds) for the main comparison tables (4, 5, 10).
3. Acknowledge the isometry more prominently in the abstract or introduction to set accurate expectations.
4. Include a per-epoch training time comparison against baseline hyperbolic models.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| ekz1hN5QNh.md — Fully Hyperbolic CNNs | 6.00 | 1 | Yes | Similar: both develop new hyperbolic operators; anchor has same weakness of modest improvements within error bars. Our paper has better numerical stability evidence but the unexplained Airport gap is a weakness not present in the anchor. |
| bwOndfohRK.md — NNs on Symmetric Spaces | 6.00 | 1 | Yes | Similar theoretical contribution level; our paper is clearer and more accessible but has a notable evidential gap. |
| TTonmgTT9X.md — Fast Hyperboloid Decision Trees | 6.60 | 1 | No | Higher-scoring but on a different topic (decision trees); less directly comparable. |
| MEnPLXJNng.md — Riemannian Transformation Layers | 4.75 | 2 | Yes | Our paper is stronger: better numerical evidence, broader evaluation, clearer presentation. |
| WOopKWDWtS.md — Robust Hyperbolic DL | 4.40 | 1 | Yes | Our paper is substantially stronger: the anchor had marginal improvements, insufficient ablation, unclear contributions. |
| KmdwGYbMv0.md — Binary Hyperbolic Embeddings | 4.50 | 2 | Yes | Different contribution type; our paper has more solid theoretical grounding. |

**Bracket (Round 1):** 5.5–6.5. The paper is clearly above the 4.4–4.75 anchors and comparable to the 6.00 anchors.

**Final Score Determination:** Against ekz1hN5QNh.md (6.00), our paper shares the positive item of developing new hyperbolic operators and the negative item of modest improvements within error bars on some comparisons. Our paper has stronger numerical stability evidence (a differentiating positive) but also has the unexplained Airport gap (a differentiating negative not present in the anchor). On balance, the paper is comparable in quality to the 6.00 anchors but with a notable evidential gap that prevents it from being scored higher.

**Final Score: 6.0 (Borderline Accept).** The paper makes a solid contribution — the first complete derivations and neural network toolkit for the PV representation of hyperbolic space — and the numerical stability advantages are convincingly demonstrated. However, the unexplained 11-point Airport gap between Riemannian and tangent-space FC variants is a significant evidential gap that needs to be resolved in the author response. The paper as submitted has the substance to warrant acceptance, contingent on a satisfactory explanation of this ablation result.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>