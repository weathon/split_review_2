## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), which use the Proper Velocity (PV) model — an unconstrained coordinate representation of hyperbolic space rooted in special relativity — as an alternative to the constrained Poincaré ball and hyperboloid models for hyperbolic neural networks. The authors derive the complete Riemannian toolkit (exponential/logarithmic maps, parallel transport, geodesic distance) for PV space, develop core neural network layers (MLR, FC, convolution, activation, batch normalization), and demonstrate through four tasks that PVNNs provide superior numerical stability while matching or exceeding the performance of prior hyperbolic models.

## Strengths

1. **Well-motivated problem with clean theoretical foundation.** The numerical instability of constrained hyperbolic models (Poincaré ball near its boundary, hyperboloid under large gyromultiplication) is a genuine practical concern documented in prior work. The paper correctly identifies PV as an unconstrained alternative, provides a complete Riemannian treatment (Exp, Log, parallel transport, geodesic distance in Section 4.2), and proves PV is isometric to the Poincaré ball (Theorem 4.2). The theory is sound and the derivations are non-trivial.

2. **Comprehensive layer development.** The paper builds a full neural toolkit: MLR (Theorem 5.2 with a crucial simplification replacing per-class gyroaddition with matrix multiplication), FC layer (Theorem 5.3), convolution, activation, and batch normalization (Section 5.4, with homogeneity guarantees in Theorem 5.4). The parameterization trick replacing $(p_k, a_k)$ with $(z_k, r_k)$ in Theorem 5.2 avoids Riemannian optimization and has clear practical value.

3. **Clear and convincing numerical stability advantage.** Section 6.1 provides strong evidence: Tables 1–3 show that PV maintains zero NaN/Inf outputs up to $r=1000$ in FP32 while the hyperboloid model fails completely beyond $r=20$; round-trip Exp/Log error for PV ($2.1\times10^{-7}$ in FP32) is three orders of magnitude better than the Poincaré ball ($2.1\times10^{-4}$); and gradient magnitudes in PV stay in $[10^{-6}, 10^{-4}]$ while Poincaré gradients vanish to $10^{-13}$ and hyperboloid gradients explode to NaN.

## Weaknesses

### Fatal
None.

### Major

1. **Missing Poincaré CNN baseline in genomic sequence experiments (Table 10).** The genomic sequence experiments compare PVCNN against Euclidean CNN and HCNN-S (hyperboloid CNN). Since PV is isometric to the Poincaré ball (Theorem 4.2), the natural baseline to establish that gains come from PV *specifically* — rather than from any numerically stable hyperbolic model — is a Poincaré convolutional network on the same architecture. Tables 1–2 already show the hyperboloid model is the most numerically fragile; the large gains over HCNN-S (e.g., +9 MCC on SINEs) could simply reflect the hyperboloid's instability rather than a property of PV. Without this comparison, the reader cannot determine whether the gains reflect PV's unconstrained nature or merely the fact that the hyperboloid baseline is numerically fragile for this task.

### Minor

1. **The isometry between PV and the Poincaré ball bounds the scope of the contribution, and the paper could be more precise about this.** Theorem 4.2 establishes that PV and the Poincaré ball are Riemannian isometric — they are the same manifold in different coordinates. Any network expressible in PV space is expressible, with identical representational capacity, in the Poincaré ball. The paper correctly acknowledges this ("By Thm. 4.2, we can readily obtain the counterparts on PV space via properties of isometries," line 98), but occasional language ("new alternative to classical hyperbolic models," "PV geometry is more effective on strongly hyperbolic graphs") implies a stronger distinction than the geometry supports. The empirical gains should be interpreted as numerical/practical benefits of an unconstrained coordinate chart, not as evidence that PV captures structure that other models cannot. The paper would be strengthened by stating this distinction explicitly.

2. **Gradient range notation in Table 3 is ambiguous.** Table 3 reports the Poincaré gradient range as $[1.1\times10^{-11}, 7.6\times10^{-13}]$ and PV as $[1.1\times10^{-4}, 2.1\times10^{-6}]$. In both cases the first value is *larger* than the second, which suggests either $[\text{max}, \text{min}]$ ordering (unusual and unexplained) or a formatting/typographical error. The authors should clarify the intended ordering.

3. **No overall training throughput reported.** The paper notes that PV GyroBN is slower than tangent-space approximations (Table 7) but does not report overall training throughput for any main experiment. Since numerical stability is the core advantage, the reader needs to know whether PV layers introduce overhead that offsets their stability benefits in wall-clock time.

4. **Curvature sensitivity unexplored.** All experiments fix $K=-1$. Since curvature interacts with the constraint boundary in the Poincaré ball (the ball radius is $1/\sqrt{-K}$), testing whether tuning $K$ per task narrows the gap between Poincaré and PV performance would strengthen the empirical picture.

### Trivial
None.

## Nice-to-Haves

- A controlled experiment testing whether the same empirical gains on graph/sequence tasks can be reproduced by running Poincaré-ball operations through the isometry (Eq. 4) with careful numerics. This would isolate whether the contribution is purely about numerical convenience or whether the unconstrained optimization landscape offers additional benefits.
- Reporting overall training throughput (not just normalization fit time) for the main experiments.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **"Metric definition deferred to appendix."** REMOVED (factual error): The metric IS given in the main text (Eq. 1 on line 46). The paper says "given by App. E.1" and then immediately states the full expression. The critic misread this.

2. **"Code not yet released."** REMOVED per hard rules: criticisms about the release status or availability of code/models are excluded. The paper states "code will be released upon acceptance," which is standard practice for conference submissions.

3. **"Missing related works."** REMOVED per hard rules: cannot confirm missing references without external sources.

4. **"Hyperboloid vs PV comparison in gradients" framing.** REMOVED: The critic's claim that the paper's language implies a stronger-than-guaranteed distinction is partially addressed — the paper is transparent about the isometry and frames PV primarily as a practical/numerical alternative. This is moved to a Minor weakness (point #1 above) for the specific instances where language could be more precise.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a Poincaré CNN baseline to the genomic sequence experiments (Table 10), or explain why this comparison cannot be performed.** This is the single highest-leverage improvement and would address the most significant evidential gap.

2. Clarify the gradient range notation in Table 3 — specify whether the bracketed values are $[\text{min}, \text{max}]$ or $[\text{max}, \text{min}]$.

3. Include an explicit discussion in the conclusions or a limitations paragraph that squarely addresses what the isometry (Theorem 4.2) does and does not imply about the contribution's scope, distinguishing representational equivalence from numerical/practical advantages.

4. Report training throughput for the main experiments to allow readers to assess the practical cost of PV layers.

## Score and Decision

**Calibration anchors (retrieved from human-review corpus):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ekz1hN5QNh.md` (Fully Hyperbolic CNNs) | 6.00 | R1/R2 | Similar scope (hyperbolic NN layers); weaker numerical evidence, similar empirical pattern — this paper is slightly stronger |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bwOndfohRK.md` (NN on Symmetric Spaces) | 6.00 | R1/R2 | Similar methodology (geometric ML); comparable theoretical depth and empirical rigor |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/WOopKWDWtS.md` (Optimizing Hyperbolic DL) | 4.40 | R1 | Less rigorous theory, more marginal results — this paper is clearly stronger |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/30aSE3FB3L.md` (Matrix Manifold NN++) | 5.67 | R2 | Similar in being a toolkit paper; this paper has clearer numerical advantages |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/zbKcFZ6Dbp.md` (Shadow Cones) | 6.33 | R2 | Different topic but same evaluation bar; comparable quality |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TTonmgTT9X.md` (Fast Hyperboloid Decision Trees) | 6.60 | R2 | Stronger empirical results than this paper but narrower scope |

**Bracketing:** Round 1 suggested the paper sits between 5.5 and 7.5. Round 2 narrowed the range by showing the paper is clearly stronger than papers scoring ~4.4 and slightly stronger than papers scoring ~6.0, while not reaching the ~8.0 level of top hyperbolic papers (which typically offer deeper theoretical novelty beyond a single coordinate change).

**Final score:** 6.5 — solid Accept. The paper has correct theory, comprehensive layer development, and convincing numerical stability evidence. The main weakness (missing Poincaré CNN baseline) is addressable, and the isometry-bound scope is a framing issue rather than a technical flaw. The contribution is practically useful and the paper is well-executed.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>