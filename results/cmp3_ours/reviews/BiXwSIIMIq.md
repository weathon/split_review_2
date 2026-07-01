I now have sufficient calibration data. Let me produce the final consolidated review.

## Summary

This paper proposes AC-DC, a three-stage score-based denoiser designed for plug-and-play ADMM (ADMM-PnP) to address the manifold mismatch problem that arises when score functions trained on Gaussian-perturbed data are applied to ADMM iterates. The denoiser consists of: (1) an auto-correction (AC) step adding Gaussian noise, (2) a directional correction (DC) step using conditional Langevin dynamics to refine alignment toward the score-trained manifold, and (3) Tweedie-based denoising. The paper provides fixed-point convergence analysis and demonstrates consistent improvements across 7 inverse problems on FFHQ and ImageNet against 8+ baselines.

## Strengths

1. **Well-motivated problem with clear diagnosis.** The paper correctly identifies that the manifold mismatch problem is exacerbated in ADMM because dual variables distort iterate distributions beyond what simple Gaussian noise injection can correct (Section 1, Section 2 final paragraph). This diagnosis goes beyond prior work's generic framing of the manifold issue.

2. **Principled three-stage denoiser design.** The AC-DC architecture (Algorithm 1) is a genuine structural contribution. The DC step—using short conditional Langevin dynamics conditioned on the AC output to bridge the manifold gap—is novel and physically sensible. This is not merely a recombination of existing components.

3. **First fixed-point convergence analysis for score-based ADMM-PnP.** Theorem 2 extends prior ADMM-PnP convergence theory (Ryu et al., 2019; Chan et al., 2016) to score-based denoisers by establishing weak non-expansiveness with high probability, which is a nontrivial technical extension. This is the paper's clearest theoretical contribution.

4. **Broad and consistently strong empirical results.** Table 1 covers 7 inverse problems across 2 datasets with 8+ baselines. The proposed method achieves best or second-best metrics in nearly every task-dataset combination, with large margins over DPS, DDRM, and DiffPIR on several tasks (e.g., +3–6 dB PSNR on super-resolution, +4–5 dB on motion deblur). Results are averaged over 100-image test sets, lending statistical reliability.

## Weaknesses

### Fatal
None.

### Major

1. **The DC Langevin dynamics use an uncontrolled gradient approximation, creating a gap between theory and algorithm.** The DC step approximates the intractable conditional score ∇ log p(z_ac^(k) | z_σ^(k)) with a Gaussian form (Algorithm 1, line 5; Eq. 10). The justification (Section 3) appeals to "proper scheduling of σ^(k) and mild regularity conditions" but provides no quantification of the approximation error, no proof that it vanishes under the proposed schedules, and no empirical validation that the Langevin dynamics sample from the intended conditional. Theorems 2 and 3 both assume "the DC step reaches the stationary distribution for each k," but this refers to the stationary distribution of the *approximate* dynamics, not the true conditional. The convergence theory thus applies to an idealized denoiser, while the executed algorithm uses an uncontrolled distortion of the target. The footnote about Appendix E.2 (removed by the parser) does not resolve the deeper issue that the gradient itself is an uncontrolled approximation.

### Minor

2. **Convergence theory and experiments are partially decoupled.** The constant-step-size convergence (Theorems 1–2) requires ℓ to be μ-strongly convex. The paper acknowledges (Section 4.3) that this holds only for signal denoising and deblurring, *not* for super-resolution, phase retrieval, inpainting, or compression—which constitute most of the tested problems. The non-convex result (Theorem 3) requires an adaptive ρ-schedule (the "p-increasing rule") which the experiments do not use. The paper is transparent about this gap (Limitations), but it means the main theoretical result does not cover the primary experimental regime.

3. **Computational cost is unquantified.** Each ADMM outer iteration uses up to 1000 Adam iterations for subproblem (7a), J=10 Langevin steps (each requiring a score evaluation), and either a Tweedie step or 10-step ODE. The paper reports no NFEs, wall-clock time, or compute-controlled comparison with baselines. DPS, DDRM, and DiffPIR use a single diffusion pass (~100–1000 NFEs), while AC-DC's total NFEs could be substantially higher. Without compute-controlled comparison, strong metrics could partly reflect more computation rather than better algorithmic design. The paper acknowledges this in Limitations but does not provide the data needed to evaluate.

4. **Insufficient ablation study.** The only ablation (Figure 5, phase retrieval) varies the number of DC steps J=0, 10, 20. Missing: (a) isolating the AC step (no AC, no DC — naive score denoising of z̃^(k)), (b) ablation on any other inverse problem, (c) sensitivity analysis for σ^(k) schedule, η^(k), or ρ, (d) comparison to a variant using DiffPIR's stochastic regularization within the same ADMM framework. Phase retrieval may benefit most from DC, so it is unclear whether DC provides meaningful gains on Gaussian deblurring, super-resolution, or inpainting.

5. **DPIR is listed as a baseline but absent from all results.** Line 295 lists DPIR (Zhang et al., 2022) among the baselines, but it never appears in Table 1 or any figure. This is conspicuously missing from an otherwise thorough evaluation.

6. **RED-diff performs unusually poorly.** RED-diff achieves PSNR 15–17 on several tasks where others achieve 25–30+ (e.g., 15.102 on ImageNet Gaussian deblur, 16.833 on FFHQ super-resolution). The paper does not discuss whether RED-diff was misconfigured or is genuinely this fragile on these tasks.

7. **The ADMM penalty parameter ρ and its tuning are not reported.** ADMM is known to be sensitive to ρ, yet the hyperparameter section (lines 297–298) omits ρ entirely. Similarly, while the σ^(k) schedule uses range [0.1, 10], the paper does not discuss whether the pre-trained score model (Chung et al., 2023) supports σ=10.

### Trivial
None.

## Nice-to-Haves
- A compute-controlled comparison (NFEs and wall-clock time for all methods) would let the reader assess whether AC-DC's gains reflect better denoising or simply more computation.
- A 2×2 ablation (AC on/off × DC on/off) on multiple problems would isolate each component's contribution and directly substantiate the claim that AC alone is insufficient.
- Quantifying the DC approximation error, even via a numerical experiment on a tractable case (e.g., where the true conditional is known), would substantially tighten the link between theory and algorithm.
- Reporting the ρ value and how it was chosen (tuned per problem, held fixed, or rule-based) would improve reproducibility.

## Removed Points
These points are flagged for removal; treat them with caution.

- **"Section 3 notation is confusing (Eq. 9)"** — Presentation observation involving possible parser artifacts; the core algorithmic description (Algorithm 1) is clear and unambiguous.
- **"Theorem 1 condition δ² = δ²\bar{ε}/ε appears self-referential"** — Most likely a parser artifact from equation rendering; the proof in Appendix C would clarify.
- **"Table formatting issues (PMC repeated rows, empty cells)"** — Parser artifacts from PDF extraction, not errors in the original submission.
- **"Missing appendix references for convergence proofs"** — Parser strips appendices; they exist in the original submission.
- **"Abstract promises convergence with constant step size without qualifying strong convexity"** — The abstract *does* qualify: "under strongly convex losses" appears in the same sentence on line 26.

## Novel Insights

None beyond the paper's own contributions. The reviewer's observations about the theory-practice gaps (DC approximation error, strong convexity limitation) are accurate but are issues the paper itself partially acknowledges. The key meta-insight is that the paper's empirical contribution (AC-DC denoiser with strong, consistent results) is more compelling than its theoretical contribution, and the framing should reflect this asymmetry more honestly rather than implying the convergence theory directly supports the experimental regime.

## Suggestions

1. Tighten the link between theory and algorithm by either (a) bounding the DC approximation error or (b) reframing the theoretical claims to explicitly acknowledge they apply to an idealized denoiser and providing an error analysis of the approximation.
2. Add a compute-controlled comparison (NFEs and wall time) to let readers distinguish algorithmic quality from raw compute.
3. Provide a proper component ablation (2×2: AC on/off × DC on/off) on multiple problems.
4. Fill the missing DPIR results and discuss RED-diff's poor performance.
5. Report the ADMM penalty parameter ρ and how it was chosen.

## Score and Decision

**Round 1 bracket:** Based on calibration Search, the most directly comparable paper ("Prior Mismatch and Adaptation in PnP-ADMM with a Nonconvex Convergence Analysis," avg 6.25) has narrower experiments and less novel contribution. The current paper's stronger empirical scope and novel denoiser design place it above this anchor. Papers on related diffusion-based inverse problem solving score 6.5–7.5 in the calibration corpus (e.g., "Diffusion State-Guided Projected Gradient" avg 6.75, "InverseBench" avg 7.50). The AC-DC paper falls in the upper half of this range: it has a genuine architectural contribution and comprehensive experiments, but the theory-algorithm gap and missing experimental details prevent it from reaching the top tier. Final score: 7.0.

**Anchors consulted:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/HXjXPQU3yJ.md` — avg 6.25, Round 1: PnP-ADMM with prior mismatch; narrower experiments, less novel contribution.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/66arKkGiFy.md` — avg 5.75, Round 1: PnP-ULA posterior sampling; incremental contribution.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/x7d1qXEn1e.md` — avg 6.25, Round 2: Restoration network as implicit prior; limited experimental validation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/U3PBITXNG6.md` — avg 7.50, Round 2: Benchmark for diffusion PnP methods; different contribution type.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kRBQwlkFSP.md` — avg 6.75, Round 2: Diffusion state-guided projected gradient; diffusion-based IP solver.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/j8hdRqOUhN.md` — avg 7.50, Round 2: Latent diffusion for inverse problems; different methodological family.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>