## Summary

This paper identifies two failure modes in sparse-view 3D Gaussian Splatting—near-field overfitting (excessive Gaussians) and far-field underfitting (too few Gaussians)—and proposes D²GS, a framework with two complementary modules: DD-Drop (depth-and-density guided dropout) to suppress overfitting in dense near-field regions, and DAFE (distance-aware fidelity enhancement) to boost supervision in under-fitted distant regions using monocular depth priors. The paper also introduces IMR (Inter-Model Robustness), a Wasserstein-based metric for measuring distribution-level stability across independent training runs.

## Strengths

1. **Problem diagnosis with concrete quantitative evidence.** Section 3.1 provides a specific numerical comparison: in near-field regions, prior methods produce 11,450 Gaussians vs. 6,112 for a dense-view model (overfitting), while far-field regions have only 3,082 vs. 5,224 (underfitting). This empirically grounds the motivation rather than relying on intuition alone.

2. **Coherent design mapping diagnosis to method.** The two identified failure modes map directly onto the two proposed modules. DD-Drop targets near-field overfitting; DAFE targets far-field underfitting. The DD-Drop design combines a local continuous score (Eq. 1) with global depth-based layering (Eq. 2), which is internally consistent.

3. **Thorough hyperparameter ablations.** Table 5 reports sensitivity to four key parameters (r_min, r_max, ω_depth:ω_density, τ, λ_DAFE). Table 6 ablates three different monocular depth estimators. This level of ablation is more thorough than typical for this area and provides practical deployment guidance.

4. **Novel distribution-level stability perspective.** The IMR metric (Section 3.4), grounded in 2-Wasserstein distance and optimal transport over Gaussian mixtures, addresses a genuine gap: standard image-space metrics cannot detect whether the underlying 3D representation is stable across training runs.

## Weaknesses

### Fatal
None.

### Major

1. **No uncertainty quantification on any performance metric, despite the paper's own emphasis on instability.** Every result in Tables 1, 2, 4, 5, and 6 reports only a single point estimate with no standard deviation, standard error, or confidence interval. This is a serious omission for two reasons: (a) improvement margins over strong baselines are modest (0.35–0.92 dB PSNR), and (b) the paper's own motivation (Figure 3 left, showing PSNR varying from ~14.6 to ~18.6 across runs of a prior method) argues that inter-run variance is large enough to matter. The authors already run 10 independent models for IMR computation (Table 3 caption), so multi-run data exists but is not reported for the main results. Without variance estimates, the reader cannot assess whether the reported improvements are robust or reflect a single favorable run.

2. **The IMR metric is presented as a third contribution but is not validated as a useful measure.** IMR is reported in Table 3 (LLFF only), but there is no analysis showing what it correlates with or what insight it provides beyond image-space metrics. Does lower IMR imply lower PSNR variance across runs? More consistent 3D geometry? Better downstream task performance? The paper merely asserts that D²GS has the lowest IMR and concludes this is good. The metric's functional form (Eq. 14: ln(∑S²_ij / ∑S_ij)) is given without justification or intuition. The depth-stratified importance sampling (lines 176–177) introduces a systematic bias toward far-field Gaussians without sensitivity analysis. IMR is only reported on LLFF, not on MipNeRF360, which limits the evidence for its general usefulness. As presented, IMR is an interesting mathematical construction but not a validated evaluation tool.

### Minor

3. **Evaluation is limited to two datasets (LLFF, MipNeRF360).** While these are standard for this sub-area, many related sparse-view works (e.g., FreeNeRF, SparseNeRF, FSGS, DropGaussian) also evaluate on DTU, Tanks and Temples, or BlendedMVS. Adding another dataset would strengthen claims of generalization beyond the two environments where hyperparameters were tuned.

4. **DAFE's reliance on monocular depth estimation is under-analyzed.** The paper ablates which depth estimator to use (MiDas, DPT, DepthAnything V2) but does not analyze when depth estimation systematically fails (e.g., reflective surfaces, transparent objects) and how that affects results. The τ=5% threshold means only the farthest 5% of pixels receive the DAFE loss—it is unclear whether the improvement truly comes from boosting distant supervision or from acting as a general regularizer. Training time and computational overhead of running a monocular depth estimator are not reported.

5. **No clean ablation isolating adaptive dropout from uniform dropout.** The paper states it builds on DropGaussian (line 196), which already uses uniform dropout. The ablation in Table 4 compares against vanilla 3DGS (no dropout), but a direct comparison of DD-Drop (adaptive) vs. uniform dropout (as in DropGaussian) while holding all other components equal would isolate whether adaptivity itself is the source of improvement.

### Trivial
None.

## Nice-to-Haves

- Report mean ± std for Tables 1 and 2 by running each method 3–5 times.
- Validate IMR by correlating it with PSNR variance or showing it distinguishes methods in ways image-space metrics cannot.
- Add evaluation on at least one additional benchmark (e.g., DTU).
- Clarify whether depth tertiles for DD-Drop's global layering are fixed at initialization or recomputed during training.
- Report training time and the computational overhead of the monocular depth estimator.

## Removed Points

These points are flagged to be removed, treat them with caution:

- "The first-order Taylor approximation (Eq. 11) is not validated against the exact closed-form" — this is a standard computational approximation used in the OT literature; the paper cites Appendix A for the derivation (stripped by the parser). Not a substantive weakness.
- "Mixing NeRF-based and 3DGS-based baselines makes comparison unfair" — the paper already labels baseline families clearly in Tables 1 and 2. Separating them would be a presentation improvement but does not affect validity.
- "Overclaiming in conclusion" — the conclusion language ("extensive experiments on standard benchmarks") matches standard academic writing conventions for this venue. Not a specific weakness.
- "Far-field multiplier analysis (λ_far=0.3 × r_max=0.3 → at most 0.09 dropout probability)" — this is an intentional design choice consistent with the paper's stated motivation (don't suppress already-underfitted regions). The design is coherent, not a flaw.
- "The IMR metric is a mathematical curiosity rather than a useful tool" — this is editorial phrasing; the substantive concern (lack of validation) is kept in Major weakness #2.

## Novel Insights

The harsh critic's key insight—that the paper's own emphasis on instability (Figure 3, showing large PSNR variance across runs) undermines its lack of variance reporting on the main results—is penetrating and correct. This is a self-inflicted credibility gap. A second important observation is that the IMR metric, while potentially interesting, is presented as a contribution without any validation that it measures something useful; this makes the paper's third claimed contribution unsubstantiated as written.

## Suggestions

1. Report mean ± standard deviation for all main results (Tables 1 and 2) using at least 3–5 independent runs. The authors already have the infrastructure for this (IMR requires N independently trained models).
2. Either validate IMR (e.g., show its correlation with PSNR variance or geometric consistency across runs) or de-emphasize it as a claimed contribution.
3. Add evaluation on at least one additional dataset (e.g., DTU) to support generalization claims.
4. Include a direct ablation: DD-Drop vs. uniform dropout with all other components held equal.
5. Analyze DAFE failure cases when monocular depth estimation produces inaccurate depth maps.

## Calibration

**Calibration Anchors (all rounds):**

| Paper | Score | Round | Comparison |
|-------|-------|-------|------------|
| NoPoSplat | 8.00 | R1 | Strongly above D²GS; clean pose-free 3DGS with no evidential gaps |
| HiSplat | 6.00 | R1 | Above D²GS; similar sparse-view 3DGS topic, minor weaknesses only |
| RAIN-GS | 5.75 | R2 | Above D²GS; more datasets, fewer evidential gaps, but weaker practical motivation |
| Injecting Inductive Bias | 5.75 | R2 | Comparable; mixed reviews (8,6,6,3) |
| Hi-Gaussian | 5.75 | R2 | Comparable; single-view 3DGS |
| FreeSplatter | 5.00 | R1/R2 | Comparable; weaker ablations but similar overall quality |
| SCISplat | 5.00 | R2 | Comparable; all 5s |
| Geo-3DGS | 5.00 | R2 | Comparable; all 5s |
| studentSplat | 4.25 | R1 | Below D²GS; questionable claims, unconvincing evaluation |

**Bracket (Round 1 → Round 2 → Final):**
- R1 bracket: Between FreeSplatter (5.00) and HiSplat (6.00)
- R2 narrowing: Compared to RAIN-GS (5.75) and Injecting Inductive Bias (5.75), D²GS has better method design and ablations but worse evidential support (no variance, unvalidated IMR, fewer datasets)
- Final: Score 5.0 — the method is sound and well-motivated, but the evidential gaps (especially missing variance estimates despite the paper's own framing) are significant enough to prevent acceptance

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>