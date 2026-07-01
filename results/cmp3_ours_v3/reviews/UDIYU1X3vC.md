Now I have a clear calibration picture. Let me produce the final review.

## Summary

This paper introduces Proper Velocity (PV) Neural Networks, a framework for hyperbolic deep learning based on the PV model — an unconstrained coordinate representation of hyperbolic space rooted in special relativity. The authors derive the full Riemannian toolkit (exponential/logarithmic maps, parallel transport, geodesic distance) for PV space, build fundamental neural network layers (MLR, FC, convolution, activation, batch normalization), and evaluate across numerical stability, image classification, graph node classification, and genomic sequence learning tasks. The key contribution is a numerically stable coordinate representation of hyperbolic geometry that avoids the boundary-related instabilities of the Poincaré ball and hyperboloid models.

## Strengths

1. **Complete derivation of the PV Riemannian toolkit.** The paper provides closed-form expressions for Exp, Log, parallel transport, and geodesic distance on PV space (Thm. 4.3), along with the isometry proof linking PV to the Poincaré ball (Thm. 4.2). This is the first systematic treatment of this representation for deep learning, and the derivations are mathematically sound.

2. **Compelling and well-designed numerical stability experiments (Sec. 6.1, Tabs. 1–3).** Across gyro operations (zero NaN/Inf for PV vs. 100% failure for hyperboloid at r=200), Riemannian round-trip error (PV at 2.1×10⁻⁷ in FP32 vs. 2.1×10⁻⁴ for Poincaré and 1.0×10⁰ for hyperboloid), and gradient behavior (PV gradients stay in [1.1×10⁻⁴, 2.1×10⁻⁶] vs. Poincaré vanishing to 10⁻¹¹–10⁻¹³ and hyperboloid going 0-to-NaN), the PV model dramatically outperforms both standard models. This is the paper's clearest and most impactful finding.

3. **Strong empirical results on strongly hyperbolic graph benchmarks and genomic sequence learning.** PVNN achieves the best results on Airport (97.96 vs. 92.10 for the next-best Klein model) and Disease (81.15 vs. 80.57 for HNN++), and PVCNN shows large gains on genomic SINEs (93.78 MCC vs. 85.45 for HCNN-S). These improvements are substantial and consistent.

## Weaknesses

### Fatal
None.

### Major

1. **Downstream gains are not cleanly attributed to numerical stability vs. architectural differences.** Since PV and Poincaré are Riemannian isometric (Thm. 4.2), any performance gap on downstream tasks must come from numerical effects, optimization dynamics, or architectural differences. The ablation study (Tab. 6) compares PVNN to PVNN+TFC (tangent FC within PV), which controls for the FC construction but does **not** compare against a *Poincaré Riemannian FC layer* — the directly analogous baseline under isometry. Without this comparison, it is unclear whether PVNN's large gains on Airport (97.96 vs. Poincaré HNN's 82.16) stem from numerical stability or from different network design principles. The paper's framing conflates these factors.

2. **Missing Poincaré CNN baseline in genomic sequence learning (Sec. 6.4).** Tab. 10 compares PVCNN against only Euclidean CNN and HCNN-S (hyperboloid). Despite Poincaré convolutional networks being well-established (Shimizu et al., 2021), no Poincaré-based CNN is included. Without this baseline, it is impossible to tell whether PVCNN's large gains (e.g., +8.3 MCC on SINEs over HCNN-S) are specific to the PV representation or achievable with any well-designed hyperbolic architecture.

### Minor

3. **The paper does not discuss the relationship between PV and the Beltrami-Klein model.** KNN (Mao et al., 2024) is included as a baseline in Tab. 5 and achieves the second-best results on Airport (92.10). However, the paper never discusses whether PV and Klein are isometric, how their numerical properties differ, or what distinguishes the two unconstrained representations. This omission weakens the positioning of PV as the natural unconstrained alternative.

4. **Framing overstates geometric novelty given the isometry.** The paper establishes that PV and the Poincaré ball are Riemannian isometric (Thm. 4.2) — the same manifold in different coordinates. While the paper accurately describes the numerical benefits, portions of the framing (e.g., "new alternative to classical hyperbolic models" in the contributions list) could be more precise: the novelty is in the coordinate representation and its numerical properties, not in a geometrically distinct space. The paper is transparent about the isometry but does not fully discuss what this implies for the nature of the contribution.

5. **Curvature sensitivity is not explored.** All experiments fix K = -1 (Sec. 6.1). Since hyperbolic model performance can be sensitive to curvature, the paper should either study this or justify the choice.

6. **Computational cost of the PV Riemannian FC layer is not discussed.** The PV FC layer requires computing sinh(√(-K)·v_k(x)) per output dimension, but the paper does not analyze its cost relative to simpler tangent-space alternatives. Tab. 7 shows 2× slowdowns for Fréchet GyroBN, suggesting cost could be nontrivial, but no runtime comparison is provided for the FC layer itself.

### Trivial
None.

## Nice-to-Haves

- Add a Poincaré Riemannian FC baseline to the graph learning ablation to isolate numerical stability effects from architectural differences.
- Add a Poincaré CNN baseline to the genomic sequence learning experiment.
- Discuss the relationship between PV space and the Beltrami-Klein model.
- Include a brief curvature sensitivity study or justify the fixed K = -1 choice.
- Report the relative computational cost of the PV FC layer versus tangent-space alternatives.

## Removed Points

- **Code release criticism** ("The code is promised 'upon acceptance'"): Removed per hard rules — this is a standard practice and constitutes a nitpick about reproducibility. The paper includes a reproducibility statement describing what will be released.
- **Section-by-Section Notes from the harsh critic**: These are commentary and not structured weaknesses (e.g., "Clear and well-structured," "No issues"). They add no actionable criticism.
- **Generic or speculative concerns**: Any criticism that reads as an area-of-concern sweep without a specific anchor in the paper text has been removed per filtering discipline.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. For the graph learning experiments, add a Poincaré version of the Riemannian FC/MLR layers (easily obtained via the isometry mapping from PV) to directly compare PV's numerical stability advantages under architectural equivalence.
2. For the genomic experiments, include at least one Poincaré-based convolutional network as a baseline.
3. Add a brief section or paragraph discussing the relationship between PV and the Beltrami-Klein model, clarifying whether they are isometric and what distinguishes their numerical properties.
4. Include a curvature ablation (e.g., K ∈ {-0.1, -0.5, -1, -5}) on at least one dataset.
5. Add a simple runtime comparison for the FC layer constructions (PV Riemannian FC vs. tangent-space FC).

---

## Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ekz1hN5QNh.md` (Fully Hyperbolic CNNs) | 6.00 | 1 | Similar hyperbolic network contribution with Lorentz model; weaker numerical evidence but comparable theoretical depth |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bwOndfohRK.md` (Symmetric Spaces) | 6.00 | 1 | Similar theoretical derivation of neural network layers for non-Euclidean spaces; comparable rigor and evaluation breadth |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TTonmgTT9X.md` (Fast Hyperboloid Decision Trees) | 6.60 | 1 | Stronger algorithmic contribution with clear practical advantages; PV paper has stronger numerical evidence but weaker attribution of downstream gains |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/WOopKWDWtS.md` (Optimizing Learning for Robust Hyperbolic DL) | 4.40 | 1 | Rejected paper with marginal improvements and missing ablations; PV paper has much stronger numerical evidence and clearer contribution |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jzneu6AO2x.md` (Riemannian Optimization for Hyperbolic Prototypical Networks) | 4.25 | 1 | Rejected paper with weaker theoretical grounding; PV paper has stronger theory, experiments, and numerical validation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KmdwGYbMv0.md` (Binary Hyperbolic Embeddings) | 4.50 | 1 | Different setting (embeddings vs. networks); PV paper has broader contribution |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/feZ7RpTLRy.md` (Bridging ML and algorithms) | 4.25 | 1 | Survey/comparison paper; very different contribution type |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Iy0WQ0c75x.md` (Alignment and Outer Shell Isotropy) | 4.75 | 1 | Hyperbolic graph contrastive learning; different sub-area |

**Round 1 bracket:** [4.5, 7.0] — the paper sits clearly above rejected hyperbolic papers (3.0–4.5) due to solid theory and compelling numerical evidence, but below the strongest accepted papers (7.0+) due to missing baselines and attribution issues.

**Final score determination:** The paper is most comparable to the Fully Hyperbolic CNNs paper (avg 6.00) and the Symmetric Spaces paper (avg 6.00) — all three have solid theoretical foundations, novel layer derivations, and experiments with some gaps. The PV paper's numerical stability evidence is stronger than either anchor, but its attribution of downstream gains is weaker and it has missing baselines. This places it at the same level: a clear accept with bounded, addressable weaknesses.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>