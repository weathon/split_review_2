Now I have all the evidence I need. Here is the final consolidated review.

---

## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), leveraging the Proper Velocity (PV) representation of hyperbolic space — an unconstrained alternative to the bounded Poincaré ball and hyperboloid models. The authors establish the complete Riemannian toolkit (exponential map, logarithmic map, parallel transport, geodesic distance) for PV space via isometry to the Poincaré ball (Thm. 4.2), and build core neural network layers (MLR, FC, convolution, activation, GyroBN). Experiments on numerical stability, image classification, graph node classification, and genomic sequence learning demonstrate PVNNs' numerical stability and competitive or superior performance.

## Strengths

- **First systematic treatment of PV space for deep learning.** The paper assembles a complete Riemannian toolkit (exponential map, logarithmic map, parallel transport, geodesic distance) for the PV space and builds neural network layers from it. The derivations via isometry to the Poincaré ball (Thm. 4.2, Thm. 4.3) are mathematically elegant and practically useful. **[weight=12.11]**

- **Numerical stability advantage is clearly and convincingly demonstrated.** Sec. 6.1 provides three well-designed probes (gyro operator, round-trip error, gradient behavior) with results in Tabs. 1–3 that are unambiguous: PV maintains FP32 stability where the hyperboloid model produces NaNs and the Poincaré ball suffers gradient vanishing. **[weight=10.35]**

- **Comprehensive layer suite.** The paper derives MLR (Thm. 5.2), FC (Thm. 5.3), convolutional, activation, and GyroBN layers — enough to build non-trivial architectures. The parameterization trick that reduces PV MLR to Euclidean inner products (Eq. 19) is an important practical efficiency detail. **[weight=9.22]**

- **Strong results on graph node classification and genomic sequences.** On the three most hyperbolic graph datasets (Disease, Airport, PubMed), PVNN consistently outperforms all baselines (Tab. 5). On genomic sequences (Tab. 10), PVCNN outperforms HCNN-S on all five TEB tasks, with a +9 MCC point gain on SINEs. **[weight=10.75]**

## Weaknesses

### Fatal
None.

### Major

- **The framing overstates geometric novelty because PV and the Poincaré ball are isometric (Thm. 4.2).** The paper repeatedly uses language like "alternative geometry," "alternative model," and "new alternative to classical hyperbolic models" (lines 15, 24, 44), suggesting a deeper geometric distinction than exists. The contribution is about providing a numerically better-behaved *coordinate system* for hyperbolic space, not a different hyperbolic geometry. The paper acknowledges the isometry in Sec. 4.1 but does not recalibrate its framing accordingly. This matters because accuracy differences on real tasks must come from numerical fidelity, implementation choices, or optimization dynamics — not from a different geometry — and the paper does not disentangle these. **[weight=1.12]**

- **The Airport result (+5.86% over the strongest baseline, 97.96 vs 92.10) is not explained by the paper's stated reasoning.** The paper claims PV is "more effective on strongly hyperbolic graphs" (line 307), but the most hyperbolic dataset (Disease, δ=0) shows only a +0.58% gain (80.57 vs 81.15), while the less hyperbolic Airport (δ=1) shows the largest gain. This pattern is not addressed. The paper should either analyze why Airport specifically benefits or flag the result as an unexplained outlier. **[weight=1.74]**

### Minor

- **Image classification results (Tab. 4) are marginal.** On CIFAR-10, PV MLR (95.30±0.18) vs. Unidirectional MLR (95.12±0.20) and on CIFAR-100, PV MLR (78.20±0.37) vs. Lorentz MLR (77.96±0.09) — all comparisons overlap within ~1 standard deviation. Since only the final classification head differs (backbone is a Euclidean ResNet-18), this experiment tests a narrow slice of the method and the evidence is inconclusive. **[weight=-1.22]**

- **No statistical significance testing is performed anywhere in the paper.** The paper reports means and standard deviations from 5-fold cross-validation but never performs a t-test or other significance test. This makes it difficult to distinguish systematic gains from noise, particularly for the smaller-margin comparisons in Tabs. 4, 5, and 6. **[weight=3.21]**

- **The GyroBN ablation (Tab. 7) partially undermines the practical value of the full Fréchet-based GyroBN.** On Disease and Airport, Tangent and Euclidean variants achieve similar accuracy at up to 2× lower computational cost. The paper acknowledges this (line 357) but still positions GyroBN as a core contribution without discussing when simpler variants suffice vs. when full GyroBN is genuinely needed (though GyroBN does provide clear benefits on PubMed and Cora). **[weight=4.67]**

### Trivial

- The Möbius gyration gyr_M used in the parallel transport formula (Eq. 12) is referenced to App. B.4 but not defined in the main text, making the formula difficult to parse without consulting the appendix. **[weight=3.23]**

## Nice-to-Haves

- Test whether the numerical stability advantage *causally* translates to downstream performance gains (e.g., by artificially pushing Poincaré embeddings near the boundary and measuring degradation).
- Analyze the Airport outlier: examine whether Airport's graph structure or feature distribution creates boundary-concentration issues that PV's unconstrained representation resolves.
- Include curvature sensitivity analysis beyond K=-1.
- Add a Poincaré-based CNN baseline to the genomic sequence experiments (Tab. 10) for a more complete comparison.
- Add statistical significance tests (paired t-test or bootstrap) for key comparisons.

## Removed Points

These points were raised in the input review but are removed as they do not constitute valid weaknesses:

- "Thm. 4.4 has no clear practical use" — The paper presents this as an elegant consistency result, not as a practical layer. Not a weakness.
- "PV FC layer justification is hand-wavy" — The derivation via Eq. (20)-(22) is clear and well-structured; the claim is not supported by the paper.
- "PV convolution is straightforward, not deeply novel" — The paper does not claim deep novelty here; this design is straightforward by intent given the unconstrained space. Not a weakness.
- "Dependence on Chen et al. (2026, App. C.2) for isometry properties is opaque" — Standard practice for deferring to a cited reference for known properties.
- Criticisms about missing appendix content, missing code, or formatting artifacts — These are parser artifacts or standard deferrals to supplementary material.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a useful reframing: the contribution is about a numerically stable coordinate system for hyperbolic space rather than a new geometry, but this reframing is implicit in the paper's own isometry results (Thm. 4.2) and does not constitute a novel observation beyond what the paper presents.

## Suggestions

1. **Recalibrate framing.** Lead with "a numerically stable coordinate representation for hyperbolic neural networks" rather than "an alternative geometry." The isometry with the Poincaré ball should be presented earlier and more prominently.

2. **Analyze the Airport result.** Either identify why Airport's structure specifically benefits from PV's unconstrained representation, or acknowledge the pattern is unexplained and flag it for future work.

3. **Add statistical significance tests** for the key comparisons in Tabs. 4-10 (paired t-test or bootstrap).

4. **Test the causal link** between numerical stability and downstream performance by pushing Poincaré embeddings near the boundary and comparing degradation trajectories.

5. **Add a Poincaré-based CNN baseline** to the genomic sequence experiments.

6. **Test across multiple curvatures** to ensure the stability advantage holds beyond K=-1.

## Score and Decision

**Calibration summary (all anchors retrieved):**

| File | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| Uj0h13lVrR.md | 1.00 | R1 | No | GFlowNets paper; topically unrelated |
| nSDOkm0SKo.md | 1.00 | R1 | No | Financial NLP; unrelated |
| gwZ90hFSL2.md | 1.00 | R1 | No | Cross-lingual robotics; unrelated |
| P49gSPmrvN.md | 1.00 | R1 | No | Scientometric visualization; unrelated |
| b2FFWnwZxl.md | 3.40 | R1 | No | Hyperbolic Vision Transformer; weak results |
| NYPJz0CL5X.md | 3.00 | R1 | No | Hyperdimensional computing; unrelated |
| q6WtaLj8O1.md | 3.00 | R1 | No | Hyperbolic hypergraph GNN; limited scope |
| xA25Ib7H8U.md | 2.33 | R1 | No | Ricci flows for continuous-depth nets; theoretical |
| WOopKWDWtS.md | 4.40 | R1 | No | Hyperbolic deep learning optimization; narrow |
| jzneu6AO2x.md | 4.25 | R1 | Yes | Hyperbolic prototypical networks; limited novelty (-5.09 weight weakness) |
| MEnPLXJNng.md | 4.75 | R1 | No | Riemannian transformation layers for general geometries |
| iqHh5Iuytv.md | 4.50 | R1 | No | RNNs with continuous attractors; unrelated |
| **30aSE3FB3L.md** | **5.67** | **R1** | **Yes** | **Matrix Manifold NN++; gyro layers for SPD/Grassmann. Narrower experiments. Strengths 8-11, weaknesses up to 3.0.** |
| **bwOndfohRK.md** | **6.00** | **R1** | **Yes** | **Symmetric Spaces NNs; FC/attention for hyperbolic+SPD. Strengths 8.7-9.4, weaknesses up to 8.4.** |
| **ekz1hN5QNh.md** | **6.00** | **R1** | **Yes** | **Fully Hyperbolic CNN (Lorentz). Closest contribution type. Strengths 7.2-12.3, weaknesses include -3.65 (novelty claims).** |
| YcaFqY8LWD.md | 6.25 | R1 | No | GyroAtt on matrix manifolds |
| 3i13Gev2hV.md | 8.00 | R1 | No | Hyperbolic vision-language; different task |
| Xo0Q1N7CGk.md | 8.00 | R1 | No | Grid cell theory; unrelated |
| P7KIGdgW8S.md | 8.00 | R1 | No | Graph neural network expressivity; unrelated |
| EzjsoomYEb.md | 8.00 | R1 | No | Topological deep learning; unrelated |
| NLbRvr840Q.md | 6.00 | R2 | No | Hypergraph dynamic system; unrelated |
| **TTonmgTT9X.md** | **6.60** | **R2** | **Yes** | **Fast Hyperboloid Decision Trees. Strengths 6.4-10.4, weaknesses 0.1-8.6.** |

**Round 1 bracket:** 5.5 – 7.5.

**Round 2 narrowing:** The paper's strengths (9.22–12.11) are higher than the 6.0-scoring "Symmetric Spaces NNs" (8.7–9.4) and "Fully Hyperbolic CNN" (7.2–12.3), and its weaknesses (max 4.67) are milder than both (max 8.4 and 6.9 respectively). The most directly comparable anchor is "Fully Hyperbolic CNN" (6.00), which develops layers for a different hyperbolic model (Lorentz) but shares the same contribution type and has comparable or worse weakness severity. My paper adds a clean numerical stability analysis the Lorentz paper lacks. The 6.60 "Hyperboloid Decision Tree" anchor has comparable strength weights but notably higher and more numerous weakness weights (up to 8.59). Placing above 6.0 and below 7.5, the final score is **6.5**.

**Final justification:** The paper's strengths are substantial — a complete, well-derived toolkit for a new hyperbolic coordinate system with a clearly demonstrated numerical stability advantage and strong empirical results on graphs and genomics. However, the framing of PV as an "alternative geometry" rather than a numerically stable coordinate system inflates the claims, and the unexplained Airport outlier (+5.86%) weakens the empirical narrative. These issues are addressable and do not invalidate the core contribution.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>