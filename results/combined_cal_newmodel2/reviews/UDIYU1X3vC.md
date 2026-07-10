Now I have everything needed to write the final review. Let me compile it.

## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), which leverage the PV space — an unconstrained coordinate representation of hyperbolic geometry isometric to the Poincaré ball — as a numerically stable alternative for building hyperbolic neural networks. The authors derive the complete Riemannian toolkit (exponential/logarithmic maps, parallel transport, geodesic distance) for PV space, construct core neural layers (MLR, FC, convolution, activation, batch normalization), and validate the framework across numerical stability benchmarks, image classification, graph node classification, and genomic sequence learning. The main empirical contribution is demonstrating that PV space avoids the vanishing/exploding gradient problems and NaN/Inf outputs that plague Poincaré ball and hyperboloid models, while matching or exceeding their performance on downstream tasks — with particularly strong gains on genomic sequence learning.

## Strengths

- **Complete Riemannian toolkit for a genuinely underexplored model.** The paper provides the first closed-form derivations of the exponential map, logarithmic map, geodesic distance, and parallel transport on the Proper Velocity space (Theorems 4.2–4.4), and leverages the isometry with the Poincaré ball in a mathematically clean way. [favorability=13.78]

- **Numerical stability advantage is convincingly demonstrated with three independent probes.** Section 6.1 provides evidence from gyro operators (Tab. 1: PV maintains zero failures at r=1000 in FP32 while hyperboloid reaches 100% failure), Riemannian round-trip error (Tab. 2: PV at 2.1×10⁻⁷ vs Poincaré at 2.1×10⁻⁴ and hyperboloid at 1.0), and gradient magnitudes (Tab. 3: PV avoids both vanishing and exploding gradients). These results are clean and unambiguous. [favorability=12.90]

- **Strong, consistent wins on genomic sequence learning.** Tab. 10 shows 6–9 MCC point improvements over both Euclidean CNN and HCNN-S across all five TEB tasks (e.g., SINEs: 93.78 vs 85.45) with non-overlapping standard deviations, indicating genuine and practically meaningful gains. [favorability=13.62]

- **Comprehensive ablation study.** Sections 6.3–6.4 include ablations on tangent vs. Riemannian layers (Tab. 6), batch statistics variants (Tab. 7), input embedding with/without Exp₀ (Tab. 8), and activation choices (Tab. 9). This thoroughness helps the reader understand where the method's advantages come from. [favorability=12.05]

- **Efficient PV MLR formulation (Theorem 5.2, Eq. 19).** The simplification replacing per-class gyroaddition with matrix multiplication via inner products is a practically meaningful efficiency improvement over the naive formulation. [favorability=12.09]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Several key experimental results lack statistical significance assessment.** In Tab. 4 (image classification), the best PV variant (95.30±0.18 on CIFAR-10) has standard deviations overlapping with top baselines (95.12±0.20). On CIFAR-100, PV (78.20±0.37) overlaps with Lorentz MLR (77.96±0.09). In Tab. 5 (graph learning), PVNN on Cora (51.42±1.33) is actually worse than LNN (53.34±1.65) with overlapping error bars. No statistical significance tests are reported anywhere. The paper's claim that PV "matches or outperforms" is technically accurate but does not distinguish genuine improvements from noise. This is the same issue that reviewers flagged in comparable hyperbolic network papers (e.g., HCNN paper at 6.00 was criticized for the same problem). [favorability=4.44]

- **The "without Exp₀" variant raises a puzzle about what drives observed gains.** In Tab. 4, the PV MLR variant that skips the exponential map (treating Euclidean features directly as PV coordinates) achieves the best results on both CIFAR-10 and CIFAR-100. Tab. 8 shows comparable performance with and without Exp₀ on graph tasks. This suggests observed gains may partly stem from PV's optimization/numerical properties rather than geometric computation. The paper discusses this briefly (lines 359–361) but does not include targeted experiments to disentangle the two factors (e.g., testing whether random Euclidean features processed through PV MLR also produce reasonable accuracy). [favorability=3.96]

- **GyroBN's practical value is undermined by its own ablation study.** Tab. 7 shows that simpler Tangent and Euclidean batch statistics variants achieve accuracy within ~0.1–0.3 points of Fréchet-based GyroBN on Disease and Airport while being ~2× faster (Airport: Tangent 98.56±0.36 at 55.48 ms/epoch vs Fréchet 10-iter 99.03±0.18 at 105.79 ms/epoch). On PubMed and Cora, Tangent variants sometimes achieve higher accuracy. The paper acknowledges this briefly (lines 357–358) but the cost-benefit tradeoff is not adequately discussed given that GyroBN is presented as a core contribution in Section 5.4. [favorability=-2.16]

- **Framing could more precisely acknowledge the isometry with the Poincaré ball.** Theorem 4.2 establishes that PV is Riemannian-isometric to the Poincaré ball — they are the same geometry in different coordinates. The paper acknowledges this (lines 64, 90, 98) but the abstract and introduction could more explicitly convey that the contribution is a more numerically stable coordinate system for hyperbolic geometry rather than a new geometric capability. The strongest evidence is numerical stability (which is a real contribution), not representational novelty. [favorability=4.60]

- **Large performance gaps in ablation tables are not explained.** Tab. 6 shows PV FC outperforms tangent-space FC by 11 points on Airport (97.93 vs 86.99) with no discussion of why the gap is so large. Tab. 9 shows Euclidean activation achieving 52.26 on Cora vs 38.10 for FC σ + Tangent Act. — a 14-point swing — while performing best on Disease and PubMed. These large dataset-dependent interactions are reported but not analyzed. [favorability=4.48]

### Trivial

- **The paper lacks a limitations section.** Important caveats implicit in the results — including (a) the isometry with Poincaré limiting geometric novelty, (b) the computational overhead of GyroBN relative to its modest gains, (c) the Cora underperformance, and (d) the large variance in some Cora results (e.g., GyroBN at 46.64±5.45 in Tab. 6) — are not explicitly discussed. [favorability=0.71]

## Nice-to-Haves

- Add a targeted experiment or discussion addressing the "without Exp₀" puzzle: test whether random Euclidean features processed through PV MLR also produce reasonable accuracy, to help disentangle geometric from optimization-driven gains.
- Explain the large Airport gap between PV FC and tangent-space FC in Tab. 6 with a brief analysis.

## Removed Points

These points from the harsh critic review were removed with justification:

- **Isometry concern framed as a "critical issue"**: Removed. The paper explicitly acknowledges the isometry (lines 64, 90, 98) and presents PV as an "alternative representation" (line 44) and "stable alternative" (line 9), not a new geometry. Retained as a minor framing weakness instead.
- **KNN baseline fairness concern**: Removed. The paper states explicitly that "All models share the same architecture consisting of two FC layers with nonlinear activations followed by an MLR classifier" (line 305). Doubting this without evidence from the paper is not a valid weakness.
- **Missing comparison with stabilized Poincaré networks**: Removed. Requesting additional baselines is a nice-to-have, not a weakness. The paper already compares against multiple Poincaré and hyperboloid baselines.
- **Speculative mentions of missing appendix content**: Removed. The parser strips appendix sections from all papers; they exist in the original submission.
- **Pure formatting/style nitpicks**: Removed per hard rules.

## Novel Insights

None beyond the paper's own contributions. The key insight from the harsh critic review — that the "without Exp₀" variant suggests gains may be optimization-driven rather than geometry-driven — is partially acknowledged in the paper but warrants deeper investigation.

## Suggestions

1. Add statistical significance discussion for the image classification and Cora graph results where error bars overlap, noting which comparisons are within noise.
2. Include a limitations paragraph explicitly addressing the isometry with Poincaré, the GyroBN cost-benefit tradeoff, and the conditions under which PV benefits are largest.
3. Address the "without Exp₀" puzzle with a targeted experiment or more detailed analysis.
4. Discuss the large Airport gap between PV FC and tangent-space FC in Tab. 6.

## Score and Decision

**Calibration summary (all anchors retrieved across rounds):**

| Path | Avg Score | Round | Itemized | Comparison to this paper |
|------|-----------|-------|----------|--------------------------|
| `/home/.../nSDOkm0SKo.md` | 1.00 | R1 | No | Unrelated topic, strong reject |
| `/home/.../Uj0h13lVrR.md` | 1.00 | R1 | No | Unrelated topic |
| `/home/.../P49gSPmrvN.md` | 1.00 | R1 | No | Unrelated topic |
| `/home/.../gwZ90hFSL2.md` | 1.00 | R1 | No | Unrelated topic |
| `/home/.../bEgDEyy2Yk.md` | 1.00 | R1 | No | Unrelated topic |
| `/home/.../u1cQYxRI1H.md` | 0.50 | R1 | No | Unrelated topic, outlier (10.0) |
| `/home/.../b2FFWnwZxl.md` | 3.40 | R1 | No | HVT paper; weaker evidence than this paper |
| `/home/.../A1JdcLawSu.md` | 3.00 | R1 | No | Unrelated (continual learning) |
| `/home/.../q6WtaLj8O1.md` | 3.00 | R1 | No | Hyperbolic hypergraph; similar topic, lower quality |
| `/home/.../WOopKWDWtS.md` | 4.40 | R1 | Yes | Hyperbolic CV improvements; weaker empirical evidence, Reject |
| `/home/.../MEnPLXJNng.md` | 4.75 | R1 | Yes | Riemannian layers for general geometries; different topic, Reject |
| `/home/.../ekz1hN5QNh.md` | 6.00 | R1 | Yes | **Most comparable anchor** — Lorentz HCNN; same isometry issue, CIFAR noise issue, but this paper has stronger ablations and genomics results |
| `/home/.../bwOndfohRK.md` | 6.00 | R1 | Yes | Symmetric spaces NN; comparable quality |
| `/home/.../TTonmgTT9X.md` | 6.60 | R2 | Yes | Hyperbolic decision trees; cleaner contribution, similar score band |
| `/home/.../zbKcFZ6Dbp.md` | 6.33 | R2 | Yes | Shadow cones; hyperbolic embeddings, Accept |

**Initial bracket (Round 1):** The paper sits between the 4.40–4.75 rejects (weaker evidence, less coherent contribution) and the 6.00–6.60 accepts (cleaner contributions, but this paper has stronger numerical stability evidence). Narrowest plausible bracket: **5.5–6.5**.

**Narrowing (Round 2):** Compared to the HCNN paper (6.00, Accept), this paper shares the same core weakness (CIFAR results within noise) but has stronger points: (a) the numerical stability evidence is much cleaner and more comprehensive, (b) the ablation study is thorough (unlike HCNN which was criticized for lacking ablations), and (c) the genomic sequence results provide a clear application where PVNNs substantially outperform both Euclidean and hyperbolic baselines. The HCNN paper's worst-rated weaknesses were at favorability −3.76 and −2.96; this paper's worst is −2.16. The overall strength profile is comparable, placing it at the same level.

Compared to the Symmetric Spaces paper (6.00, Accept), this paper has a more focused contribution and stronger empirical results in one domain (genomics), while the Symmetric Spaces paper had broader theoretical scope.

**Final score:** 6.0 — a solid, methodologically sound paper with a real practical contribution (numerical stability through coordinate reparameterization), strong evidence in one application area, and comprehensive ablations. The significance is bounded by the isometry with Poincaré and the noise-level results on several benchmarks, but the contribution is clearly above the threshold for acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>