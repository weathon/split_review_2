Now let me produce the final consolidated review.

## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), leveraging the unconstrained PV representation of hyperbolic space (derived from Einstein's special relativity) as a numerically stable alternative to the constrained Poincaré ball and hyperboloid models. The authors derive closed-form Riemannian operators (exponential/logarithmic maps, parallel transport, geodesic distance) in PV coordinates, build core neural network layers (MLR, FC, convolutional, activation, batch normalization), and validate the framework through experiments on numerical stability, image classification, graph node classification, and genomic sequence learning.

## Strengths

- **Thorough derivation of PV Riemannian operators (Sec. 4).** The paper derives closed-form expressions for the exponential map, logarithmic map, geodesic distance, and parallel transport in PV coordinates via the isometry to the Poincaré ball. The derivations are explicit and complete, providing a toolkit that prior machine learning work had not worked out. [Impact: +9.5]

- **Numerical stability is convincingly demonstrated (Sec. 6.1, Tables 1–3).** The synthetic benchmarks are well-designed: PV achieves zero NaN/Inf failure and violation rates at all tested radii in FP32 (Table 1), round-trip error of 2.1×10⁻⁷ vs. Poincaré's 2.1×10⁻⁴ in FP32 (Table 2), and maintains gradients in a healthy 10⁻⁴–10⁻⁶ range while Poincaré gradients vanish to 10⁻¹¹–10⁻¹³ (Table 3). These are concrete, measurable advantages. [Impact: +9.3]

- **Comprehensive layer design (Sec. 5).** The paper covers MLR (with a clever reparameterization that avoids costly gyroaddition — Eq. 19 reduces to matrix multiplication), FC, convolutional, activation, and batch normalization layers in PV space. The normalization theorem (Thm. 5.4) providing homogeneity guarantees for GyroBN is a useful theoretical contribution. [Impact: +8.6]

- **Strong results on genomic sequence learning (Sec. 6.4, Table 10).** PVCNN substantially outperforms HCNN-S on all TEB datasets, with margins of ~8.33 MCC points on SINEs and ~5.71 points on LINEs — large, consistent improvements on a non-synthetic task. [Impact: +9.2]

## Weaknesses

### Fatal
None.

### Major

- **The causal link between numerical stability and improved learning performance is not demonstrated.** The paper's core narrative — that PV's numerical stability drives better results — lacks direct evidence. On image classification (Table 4), PV MLR gains are only 0.18 points on CIFAR-10 and 0.24 points on CIFAR-100, within one standard deviation of baselines, while all baselines train without NaN collapse. On genomics (Table 10), the only non-PV hyperbolic baseline is HCNN-S (hyperboloid), which Tables 1–2 show has catastrophic numerical issues (100% failure rates at large radii). Thus PV's advantage on genomics may simply reflect "not being numerically broken" rather than any specifically desirable geometric property. The paper would be substantially strengthened by analyzing training dynamics (gradient norms, NaN frequencies, constraint-violation rates) across tasks to establish whether PV's stability actually drives the observed performance. [Impact: -7.2]

### Minor

- **Missing Poincaré-ball CNN baseline in the genomics experiment (Table 10).** The paper compares against the Poincaré ball in every other experiment (Tables 1, 2, 3, 4, 5) but omits this baseline from the key genomics task where the largest gains appear. Since the Poincaré ball is the most popular hyperbolic model and does not share the hyperboloid's catastrophic numerical failures, its inclusion would substantially strengthen the claim that PV offers practical advantages beyond "not being the hyperboloid." [Impact: -5.6]

- **Framing inflation relative to the isometry result.** Theorem 4.2 proves that PV space and the Poincaré ball are Riemannian isometric — the same underlying geometry in different coordinate charts. The paper is transparent about this fact, yet its abstract, introduction, and conclusion systematically frame PV as a "new alternative geometry" rather than as an isometric coordinate representation with different numerical properties. This inflates the perceived contribution: the value is real (numerical stability, closed-form operators in PV coordinates) but stems from the coordinate representation, not from discovering a distinct geometric space. The framing should explicitly acknowledge that PV and the Poincaré ball represent the same hyperbolic geometry. [Impact: -4.5]

- **Tangent-space ablations suggest the full Riemannian machinery is often unnecessary.** Table 6 shows that a simple tangent-space FC (PVNN+TFC) achieves nearly identical or better results than the full Riemannian PVNN on 3 of 4 graph datasets (PubMed: 74.40 vs 74.16; Cora: 53.58 vs 52.26). Only on Airport does the Riemannian formulation dominate massively (97.93 vs 86.99). This undercuts the practical case for the Riemannian layers as a general-purpose contribution. The paper acknowledges this pattern in partial terms ("especially in strongly hyperbolic settings") but the positioning still emphasizes the Riemannian constructions as the primary deliverable. [Impact: -8.3]

### Trivial
None.

## Nice-to-Haves

- Explore whether tuning the curvature parameter K (fixed at K=-1 throughout) provides additional benefits, or whether PV's numerical stability allows more extreme curvatures to be used safely.
- Report wall-clock training times for the main comparisons to accompany the accuracy results.

## Removed Points

- **Conflation of "numerical instability" with "gradient vanishing":** The critic claimed the paper conflates NaN/Inf failures with gradient vanishing under one term. However, the paper explicitly distinguishes these in Sec. 6.1 — Table 1 measures NaN/failure rates, Table 3 separately measures gradient behavior — and the introduction (line 13) cites gradient vanishing specifically for the Poincaré ball. This criticism is not supported by the actual paper content.
- **Inconsistent performance across graph datasets:** The critic noted that PVNN is worse than LNN on Cora. The paper itself addresses this pattern (line 307: "PV geometry is more effective on strongly hyperbolic graphs," with δ values in Table 5), so this is adequately discussed.
- **No limitations section or curvature exploration:** These are nice-to-have additions, not core weaknesses. The paper provides substantial experimental coverage across four tasks.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a Poincaré-ball CNN baseline to the genomics experiment (Table 10).** This would directly address the most conspicuous experimental gap and clarify whether PV's advantages extend beyond "not being the hyperboloid."
2. **Analyze training dynamics across tasks.** Report gradient norm statistics, NaN frequencies, or constraint-violation rates during training for each baseline to directly connect numerical stability to observed performance differences.
3. **Reframe the contribution language.** Explicitly state in the abstract and conclusion that PV provides an *isometric coordinate representation* of hyperbolic space with superior numerical properties, rather than a "new alternative geometry."
4. **Reposition the tangent-space results.** Acknowledge that the simple tangent approach often suffices, and position the Riemannian toolkit as: (a) providing the theoretical foundation that the tangent approach rests on, and (b) being beneficial specifically for strongly hyperbolic settings.

## Score and Decision

This paper makes a legitimate, well-supported contribution to hyperbolic deep learning. The derivation of closed-form Riemannian operators in PV coordinates is genuinely useful, the numerical stability advantages are convincingly demonstrated through well-designed synthetic benchmarks, and the neural layer designs are technically sound and comprehensive. The genomics results demonstrate practical value. The weaknesses are primarily about framing and incomplete causal evidence between stability and performance — they are addressable and do not undermine the core contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>