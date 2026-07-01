## Summary

This paper addresses the challenge of integrating score-based denoisers into the ADMM plug-and-play (PnP) framework. It identifies a key problem — that ADMM iterates (especially due to dual variables) do not lie on the noisy data manifolds that score functions are trained on — and proposes the AC-DC denoiser: a three-stage procedure (additive Gaussian noise auto-correction, conditional Langevin dynamics directional correction, and Tweedie denoising) to mitigate this mismatch. The paper provides convergence guarantees (probabilistic fixed-point ball convergence) for ADMM-PnP with the AC-DC denoiser, and demonstrates strong empirical performance across 6–7 inverse problems on FFHQ and ImageNet.

## Strengths

1. **Well-motivated method targeting a genuine architectural tension.** The observation that ADMM dual variables distort the relationship between iterates and score-function training manifolds is specific and grounded. The AC-DC denoiser — combining noise injection, conditional Langevin dynamics, and Tweedie denoising — is a coherent, non-obvious response (Algorithm 1). While components have been used separately, their assembly into a pipeline that explicitly addresses ADMM's geometry is novel.

2. **Convergence analysis for score-based denoisers in ADMM fills a real gap.** The paper correctly identifies (Section 2) that existing ADMM-PnP theory (Ryu et al., 2019; Chan et al., 2016) assumes deterministic denoisers, which score-based denoisers do not satisfy. Theorems 1–3 extend fixed-point ball convergence guarantees to a class of stochastic, score-based denoisers. Even though the guarantees are probabilistic and to a δ-ball rather than a fixed point, this is a nontrivial step beyond the prior state of knowledge.

3. **Broad and consistently strong empirical results.** The method is evaluated on super-resolution, Gaussian/motion deblurring, random/box inpainting, and phase retrieval across two datasets. In Table 1, both Ours-tweedie and Ours-ode occupy the top two positions in nearly every row, often by several dB of PSNR over the strongest baseline (e.g., 30.44 vs. 29.53 for super-resolution on FFHQ; 32.84 vs. 31.65 for random inpainting). This consistency across diverse tasks is compelling evidence of overall utility.

## Weaknesses

### Fatal
None.

### Major

1. **Ablation study is insufficient to isolate the method's specific contributions.** The paper claims that the AC-DC mechanism improves solution quality, but the ablation only varies the number of DC steps *J* for a single task (phase retrieval, Fig. 5) without quantitative metrics. The following controlled comparisons are missing and are necessary to support the central claim:
   - ADMM-PnP with a *naive score-based denoiser* (no AC, no DC — just Tweedie denoising of the ADMM iterate). This directly tests whether the AC-DC machinery helps over simply plugging a score function into ADMM.
   - ADMM-PnP with AC only (no DC), with quantitative results across multiple tasks.
   - ADMM-PnP with a non-score-based denoiser (e.g., DnCNN, BM3D) to separate the benefit of using a score model from the benefit of the AC-DC mechanism.
   
   Without these, the empirical evaluation conflates the benefit of (a) using a score-based denoiser in ADMM at all, (b) the AC correction, and (c) the DC correction. The paper's central empirical claim is underdetermined by the evidence presented.

2. **Missing controlled comparison against a naive ADMM-PnP baseline with the same score model.** The baselines (DPS, DDRM, DiffPIR, DAPS, etc.) are predominantly posterior sampling or non-ADMM methods. While comparing against strong external baselines demonstrates overall pipeline utility, it does not validate the specific ADMM + AC-DC design choices. A comparison of ADMM-PnP with the same score model, same subproblem solver, and same hyperparameters — with vs. without AC-DC — would directly isolate the benefit of the proposed mechanism. This is the single most informative control and is absent.

### Minor

3. **No variance or uncertainty reporting for quantitative results.** Table 1 reports PSNR, SSIM, and LPIPS averaged over 100 images without standard deviations, confidence intervals, or any measure of variance. Some margins are modest (e.g., box inpainting on ImageNet: Ours-tweedie PSNR 21.626 vs. DAPS 21.303 vs. DCDP 20.991; box inpainting on FFHQ: DCDP wins on PSNR 25.230 vs. Ours-tweedie 24.025). Without error bars, the reader cannot assess which differences are meaningful versus noise from the 100-image sample.

4. **The main convergence theorems assume the DC step reaches the stationary distribution, which the implemented method (J=10 Langevin steps) does not satisfy.** The paper acknowledges this and refers to Appendix E.2 for relaxed counterparts (footnote, line 207), which is commendable but means the theorems as presented in the main body prove properties of an idealized variant. For the paper's convergence claims to be fully credible as stated, the main theorems should either remove this assumption or clearly present the relaxed versions as primary. (The authors are transparent about this, but it creates a disconnect between the theoretical framing and the implemented algorithm.)

5. **The value of the decay window *W* is not specified.** The hyperparameter description (Section 6) defines σ^{(k)} over a "W decay window" and sets K = W + 10, but never provides the numerical value of W. This is a reproducibility gap.

6. **Computational cost is not discussed.** Each ADMM outer iteration involves up to 1000 Adam iterations for subproblem (7a) plus J=10 Langevin steps for the DC stage. The total number of score function evaluations per image is not reported, and no comparison of quality vs. compute with baselines is provided. The limitations section honestly notes this, but the main text does not characterize the cost.

7. **Notation in Eq. (9) and surrounding text is confusing.** The variable s^{(k)} is reused for different quantities (lines 125–129: "s^{(k)} = \tilde{z}^{(k)} - z_q^{(k)}" and then "s^{(k)} = \sqrt{2}\sigma^{(k)}\mathbf{n}_2 + \mathbf{s}^{(k)}"), making the derivation of the AC step difficult to follow. While parser artifacts may contribute, the exposition would benefit from clearer notation.

### Trivial
None.

## Nice-to-Haves

- **Add the relaxed convergence results (from Appendix E.2) as the primary theorems in the main text**, so the theoretical claims align with the actually implemented method.
- **Report NFE (number of score function evaluations)** per image for the proposed method and key baselines, to contextualize the quality-vs.-compute trade-off.
- **Add the missing controlled comparison** (ADMM-PnP with naive score denoiser without AC-DC) on at least 2–3 tasks. This single experiment would substantially strengthen the paper's central claim.

## Removed Points

- **Criticism about theory-assumption disconnect being a "structural flaw"**: The paper explicitly acknowledges this assumption and cites Appendix E.2 for relaxed counterparts. The appendix is stripped by the parser, not absent from the original submission. The concern is valid but demoted from "fatal/structural" to Minor (#4 above) since the authors anticipated and addressed it.
- **Criticism that baselines are "apples and oranges"**: While the missing within-ADMM control is a genuine issue (kept as Major #2), the suggestion that comparing against posterior sampling methods is invalid is too strong — those are legitimate state-of-the-art baselines. The criticism is reframed as "missing controlled comparison" rather than "invalid comparison."
- **Table 1 formatting issues (duplicate PMC rows, "Impainting" typo)**: Parser artifacts, not present in the original submission.
- **Criticism about Theorem 1's strongly convex ℓ assumption**: The authors are transparent about this and address it in Section 4.3. Removing convexity entirely is the point of Theorem 3.
- **Criticism that σ^{(k)} does not approach 0 in practice**: This is a genuine disconnect but is already acknowledged in the paper's limitations section ("noise schedules...currently guided by empirical heuristics"). The theoretical conditions are for the guarantee; practice may not satisfy them.
- **Several generic section-by-section observations** (e.g., abstract over-selling, convergence discussion) that are minor presentation preferences rather than substantive weaknesses.

## Novel Insights

None beyond the paper's own contributions. The reviewer's observations are largely convergent with the paper's self-assessment (the limitations section already flags the heuristic noise schedules, the computational cost, and the gap between stability guarantees and recovery quality). The most novel critical insight is that the ablation design does not isolate the AC-DC mechanism from the baseline benefit of using any score-based denoiser in ADMM — a point the paper's current experiments cannot resolve.

## Suggestions

1. Add a controlled experiment: compare ADMM-PnP with a naive score-based denoiser (just Tweedie denoising, no AC/DC) against ADMM-PnP with AC-DC, using the same score model and optimizer on 2–3 tasks. Report quantitative metrics.
2. Add standard deviations or confidence intervals to Table 1.
3. Specify the numerical value of W and report NFE per image.
4. Either (a) move the relaxed convergence theorems (from Appendix E.2) to the main text, or (b) explicitly state in Theorem 2/3 that the stationarity assumption is a simplification and summarize the relaxed result.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>