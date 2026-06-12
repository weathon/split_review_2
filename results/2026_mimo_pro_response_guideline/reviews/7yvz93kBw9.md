Now let me finalize the review.

---

## Summary

This paper proposes D²GS, a framework for improving sparse-view 3D Gaussian Splatting by addressing two spatially localized failure modes: near-field overfitting (excessive Gaussian density near the camera) and far-field underfitting (insufficient Gaussian coverage). It introduces DD-Drop, a spatially adaptive dropout strategy guided by depth and density, and DAFE, a distance-aware fidelity enhancement loss that increases supervision on far-field regions. The paper also introduces IMR, a Wasserstein-based metric to quantify stability of Gaussian distributions across training runs.

## Strengths

- **Concrete, quantitative problem diagnosis**: Section 3.1 provides specific Gaussian count comparisons grounding the two failure modes: sparse models produce 11,450 Gaussians near-field vs. 6,112 for dense models (88% excess), and only 3,082 vs. 5,224 far-field (41% deficit). This level of empirical specificity directly motivates the method design and goes beyond vague qualitative claims.

- **Consistent state-of-the-art results across two benchmarks**: Table 1 shows D²GS surpasses DropGaussian by +0.59 dB PSNR on LLFF (3-view, 1/8 resolution) and +0.55 dB at 1/4 resolution. Table 2 shows +0.35 dB improvement on Mip-NeRF360. Improvements extend across SSIM, LPIPS, and AVGE, confirming gains are not metric-specific.

- **Thorough ablation with progressive validation**: Table 4 demonstrates systematic contribution of each component: baseline (19.22 PSNR) → +density+layering (21.02) → +depth+layering (20.92) → density+depth without layering (21.10) → full DD-Drop (21.17) → +DAFE (21.35). Each addition yields measurable improvement. Table 5 provides hyperparameter sensitivity analysis.

- **Robustness to depth estimator choice**: Table 6 shows consistent gains with MiDas, DPT, and DepthAnything V2, demonstrating the method does not depend on a specific depth prior.

- **Well-motivated dual local–global dropout design**: Equations 1–2 combine continuous local scoring (depth and density) with discrete global depth-based tertile layering, addressing both fine-grained local redundancy and coarse depth-range imbalance, as validated by the ablation.

## Weaknesses

### Fatal
None.

### Major

- **No variance/error reporting despite the paper's own evidence of high run-to-run instability** — Figure 3 shows PSNR fluctuating from 14.62 to 18.63 (~4 dB range) across 10 training runs for a single method on a single scene. Yet Tables 1–2 report single-point results, and Table 3 reports IMR from 10 runs without any variance or confidence intervals. Given that the paper's central motivation is training instability, the absence of error bars makes it impossible to assess whether the reported 0.35–0.59 dB PSNR gains or IMR differences (e.g., 3.039 vs. 3.205) are statistically significant or within natural noise. This is the single highest-leverage improvement the authors could make.

- **IMR metric lacks validation of practical utility and has weak statistical support** — IMR is one of three stated contributions (Section 3.4, Table 3). However, the paper never demonstrates that IMR provides information beyond what the standard deviation of PSNR across runs would give, nor does it show correlation with any downstream metric. The weighted formulation (Eq. 14: log of S²-weighted mean of S) is not compared against simpler alternatives. With only 10 runs and no variance reported for IMR itself, the reported differences (e.g., 3.162 vs. 3.039) could easily be noise given the demonstrated instability in Figure 3. Without validation, IMR occupies a third of the paper's contribution claims without sufficient evidence.

### Minor

- **Incomplete baselines on MipNeRF360** — Table 2 compares only 4 methods (3DGS, FSGS, CoR-GS, DropGaussian) while Table 1 compares 11. Key 3DGS-based baselines present in LLFF (LoopSparseGS, DNGaussian) are absent from MipNeRF360, weakening claims about "extensive experiments on multiple datasets."

- **No computational cost analysis** — The paper does not report training time, memory overhead, or inference speed. DD-Drop introduces per-Gaussian scoring and DAFE requires monocular depth estimation as preprocessing; the overhead should be discussed.

- **Ablation design is not fully factorial** — Table 4's rows (density+layering, depth+layering, density+depth without layering, all) don't allow clean isolation of each component's individual contribution. Testing density score alone, depth score alone, and layering alone would make the ablation more informative.

- **No qualitative results on MipNeRF360** — Figure 4 shows only LLFF scenes. Since DAFE's motivation—enhancing distant regions—should be especially visible on unbounded 360° scenes, this is a missed opportunity.

- **6-view results only in IMR table** — Table 3 reports 6-view IMR but Tables 1–2 show only 3-view rendering quality. Adding 6-view PSNR/SSIM results would provide a more complete picture of how the method behaves as input density varies.

## Nice-to-Haves
- Report Gaussian counts after training for D²GS vs. baselines to support the claim of "suppressing redundant Gaussians."
- Explore whether continuous depth weighting outperforms the hard binary mask in DAFE (Eq. 4, τ=5%).
- Discuss whether the dense-view model's Gaussian distribution is necessarily the "correct" target (Section 3.1 implicitly assumes this).

## Removed Points
These points are flagged to be removed, treat them with caution:
- Criticisms about missing appendix/proofs: Appendix A derivation exists but was stripped by parser; this is standard practice.
- Formatting/typos: parser artifacts, not author errors.
- Hyperparameter disclosure: the paper discloses key hyperparameters (r_min=0.05, r_max=0.3, ω_depth=0.5, ω_density=0.5, τ=5%, λ_DAFE=1.0) in text and Table 5.
- Strength finder's claim that IMR is "novel and principled" conflicts with the verified weakness about lack of validation; the metric exists but its contribution is overstated.

## Novel Insights
The paper provides a spatial diagnosis of sparse-view 3DGS failure modes by quantifying the Gaussian count imbalance between near-field and far-field regions (88% excess vs. 41% deficit relative to dense-view baselines). While the two modules are individually incremental over DropGaussian, the dual local-global dropout framework grounded in this spatial analysis is a useful organizational contribution for thinking about sparse-view 3DGS regularization.

## Suggestions
1. **Add mean ± std from ≥3 runs for all quantitative results in Tables 1–3.** This is the single highest-leverage improvement and directly addresses the paper's own motivation.
2. **Either validate IMR against simpler robustness measures (e.g., std(PSNR)) or de-emphasize it from a core contribution to an auxiliary metric.**
3. Add LoopSparseGS and DNGaussian baselines to the MipNeRF360 evaluation.
4. Report training time and memory overhead.
5. Add 6-view PSNR/SSIM results alongside the existing 3-view results.

## Calibration Reporting

**Round 1 bracketing results (all papers retrieved):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| Distributionally Robust Surface Reconstruction | 3.00 | R1 | Different field, not comparable |
| GeoGS3D | 3.40 | R1 | Single-view 3D, different scope |
| Sparse Covariance NNs | 3.00 | R1 | Different field |
| DC3DO | 3.00 | R1 | Different field |
| FreeSplatter | 5.00 | R1 | Sparse-view GS, weaker ablation and novelty |
| Variational Bayes GS | 4.50 | R1 | Different problem (continual learning) |
| Geo-3DGS | 5.00 | R1 | 3DGS surface reconstruction |
| SCISplat | 5.00 | R1 | Different domain |
| IBGS | 5.75 | R1 | More novel technical contribution but rejected (8/6/6/3 spread) |
| RAIN-GS | 5.75 | R1 | Relaxing SfM init, rejected |
| HiSplat | 6.00 | R1 | Hierarchical GS for sparse-view, accepted (6/6/6/6) — comparable novelty |
| Lightweight Predictive 3DGS | 7.00 | R1 | More novel compact representation |
| NoPoSplat | 8.00 | R1 | Clearly stronger (pose-free, 8/8/8) |
| HQGS | 6.50 | R1 | GS for degraded scenes, similar structure, accepted (6/6/8/6) |
| FreeVS | 5.80 | R1 | Driving NVS, accepted |
| UniG | 6.00 | R1 | View-consistent GS, rejected (6/5/8/5) |
| Spiking GS | 5.25 | R1 | GS surface reconstruction, rejected |
| Scalable Benchmarking | 6.50 | R1 | Robustness benchmarking, different focus |

**Round 2 narrowing (all papers retrieved):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| RAIN-GS | 5.75 | R2 | Less clear motivation than D²GS, rejected |
| IBGS | 5.75 | R2 | More novel but worse presentation, rejected |
| Hi-Gaussian | 5.75 | R2 | Single-view, different task |
| HiSplat | 6.00 | R2 | Comparable quality, slightly more novel representation |
| Spiking GS | 5.25 | R2 | Less clear problem diagnosis |
| Scalable Benchmarking | 6.50 | R2 | Different focus (noise robustness) |
| HQGS | 6.50 | R2 | Similar structure, broader problem |
| FreeVS | 5.80 | R2 | Different domain |
| UniG | 6.00 | R2 | Rejected despite consistent 6s |

**Bracket**: 5.5 – 6.5. D²GS is comparable to HiSplat (6.00, Accept) in overall quality: it has clearer motivation and better problem diagnosis, but HiSplat's hierarchical representation is arguably more novel. D²GS is slightly below HQGS (6.50, Accept) which addresses a broader problem space. D²GS has stronger ablation and clearer motivation than IBGS (5.75, Reject) and RAIN-GS (5.75, Reject), but those papers have more technical novelty. The IMR weakness is notable but does not invalidate the core DD-Drop+DAFE contribution.

**Final score: 6.0**. D²GS is a solid incremental contribution with clear spatial motivation, consistent gains, and good ablation. It sits at the level of HiSplat (6.00): well-executed and clearly above the rejected papers at 5.75, but not reaching the 6.5+ tier of papers addressing broader or more novel problems. The main drag on the score is the unvalidated IMR metric (one of three contributions) and the absence of variance reporting, both of which are addressable.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept