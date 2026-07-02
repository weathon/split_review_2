## Summary

This paper proposes LDP, a lightweight denoising autoencoder plugin (642k params) for single-image super-resolution. LDP functions as a conditional degradation model that takes HR/SR images as input and predicts the corresponding LR image, which is then used for cycle-consistency regularization. It operates in two modes: as a training-time loss for fine-tuning existing SR models, and as an inference-time posterior sampling correction for diffusion models. The method is evaluated across four architectural families (GAN-based FeMaSR, diffusion-based StableSR, Transformer-based SwinIR, and SSM-based MambaIR) on synthetic and real-world benchmarks.

## Strengths

1. **Broad architecture coverage.** Testing on GAN, diffusion, Transformer, and SSM-based SR models (four distinct paradigms) is genuinely thorough. Most SR papers test on one or two families, making this a clear strength.

2. **Consistent synthetic improvements in fine-tuning mode (Table 3).** Every `+LDP` variant outperforms its baseline on every synthetic degradation type across PSNR, SSIM, and LPIPS — with no cherry-picked exceptions. Gains on StableSR are substantial (e.g., +2.16 dB PSNR on Hybrid, +0.1541 SSIM).

3. **Lightweight and practical.** At 642k parameters and ~16 hours training on a single GPU, LDP is usable as an add-on without requiring large compute budgets. The training-mode LDP does not need to be present at inference time.

4. **Two operational modes.** LDP can function as a training loss (fine-tuning) and as inference-time posterior sampling for diffusion models. The training mode does not require LDP at inference, which is a practical advantage.

## Weaknesses

### Major

1. **The fine-tuning experiments confound LDP with additional training on diverse degradation data.** Section 4.1 states that +LDP models are "fine-tuned... using BSRGAN degradation patterns" with LDP as an auxiliary loss. The baselines (original models) were NOT fine-tuned on BSRGAN data. This means the gains in Table 3 could partly reflect the effect of additional fine-tuning on diverse degradations rather than the LDP loss specifically. A "fine-tuned on BSRGAN data without LDP" condition is needed to isolate LDP's contribution. This is the most consequential experimental gap in the paper.

2. **No comparison to existing methods that address the same problem.** The paper frames LDP as improving generalization to unseen degradations — a problem with well-established literature. Yet Tables 3–5 contain only self-comparisons (baseline vs. baseline+LDP). There is no comparison to BSRGAN-style multi-degradation training (training the same SR models on BSRGAN patterns without LDP), DRN cycle consistency, or Lway test-time adaptation. Without such comparisons, a reviewer cannot evaluate whether LDP is additive or redundant with existing techniques.

3. **The diffusion posterior sampling results (Table 5) are overstated.** The paper claims "improvements across nearly all metrics on most datasets," but an honest read shows:
   - **LDM+LDP**: All five metrics degrade on RealSR (NIQE 6.651→6.830, MANIQA 0.2904→0.2810, CLIPIQA 0.4564→0.4319, MUSIQ 52.09→50.37, QAlign 2.685→2.610).
   - **ResShift+LDP** and **UPSR+LDP**: Changes are negligible (often in the 3rd–4th decimal place; e.g., CLIPIQA 0.5353→0.5354, MUSIQ 56.85→56.85 unchanged).
   - **StableSR+LDP** is the only model showing clear, meaningful gains (e.g., MUSIQ on DPED 45.55→49.25).
   The claim should be calibrated to reflect that only StableSR benefits substantially.

### Minor

4. **No statistical significance or variance reported.** Every numerical result (Tables 1–7) is a single point. Many improvements are small (MambaIR+LDP on Down: +0.05 dB PSNR), and for Table 5 several differences are near zero. Without error bars or multiple runs, the reader cannot distinguish genuine improvement from noise.

5. **Real-world fine-tuning results show notable regressions with insufficient analysis.** FeMaSR+LDP shows CLIPIQA drops of ~20% on RealSR (0.5645→0.4482) and ~17% on RealSRSet (0.6874→0.5683). The paper explains these as "GAN artifacts misinterpreted as texture" being suppressed, but this post-hoc explanation lacks supporting evidence (e.g., human evaluation, lesion analysis, or feature attribution). If LDP suppresses legitimate texture along with artifacts, this is a genuine limitation that needs characterization.

6. **Motivation-mechanism misalignment.** The paper invokes the DR2 diffusion-model property that "after noise is added, HR features and LR features become aligned, making denoising noisy HR features equivalent to denoising noisy LR features." However, LDP never actually uses this score-matching property — it adds noise, runs a CNN denoiser, and downsamples. The method would be described more accurately as a learned degradation predictor trained with noise injection and cycle-consistency losses. This does not invalidate the method, but the diffusion-model framing is misleading.

### Trivial

7. **Notation inconsistency.** Section 3.1 (line 76) describes "s^l"-fold downsampling/upsampling for LR high-frequency computation, while Eq. 4 uses s², and Section 4.1 reports s' = 2. These should be harmonized.

## Nice-to-Haves

- A simple ablation comparing LDP's learned degradation model against manually specified bicubic downsampling + noise for the cycle-consistency loss would isolate whether gains come from the learned degradation or merely from adding any LR-prediction loss.
- FLOPs or wall-clock overhead per training iteration would strengthen the lightweight claim.
- Visualization of the learned denoiser filters/kernels would support the claim that LDP learns interpretable degradation patterns.

## Removed Points

- **Table 1 comparison "unfairness" (Critic Issue 2):** The critic claimed evaluating DRN on non-bicubic degradations is unfair, but DRN actually achieves competitive/better PSNR on Noise (27.25 vs 26.71) and JPEG (29.65 vs 28.01). This makes the comparison informative rather than misleading, and the paper acknowledges DRN's design scope upfront. Removed because the criticism is contradicted by the data.
- **Missing related work:** Per guidelines, I cannot comment on missing references as I cannot verify their existence.
- **Missing appendix content / Table 6 column header garbling:** These are parser artifacts, not author errors.
- **Formatting nitpicks:** Per guidelines, parser-induced artifacts should not be treated as author flaws.
- **Generic area sweeps:** Speculative concerns about confounders, metric validity, or reproducibility that lack specific anchors in the paper text are removed per filtering discipline.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a control condition: fine-tune each baseline on the same BSRGAN degradation data **without** LDP, so the reader can attribute gains to the LDP loss rather than to additional training on diverse degradations.
2. Add at least one comparison to an existing generalization-improvement approach (BSRGAN training, DRN cycle consistency, or Lway test-time adaptation) to contextualize LDP's gains.
3. Calibrate the diffusion posterior sampling claims: present StableSR as the clear success case and note that LDM, ResShift, and UPSR show marginal changes.
4. Report variance (mean ± std over multiple runs) for at least the key tables.
5. Provide evidence supporting the FeMaSR CLIPIQA explanation — e.g., human evaluation, feature visualization, or an analysis of which frequency bands are suppressed.
6. Drop or soften the DR2 alignment motivation; the method stands on its own as a learned degradation predictor.

## Score and Decision

**Round 1 (Bracketing):** I searched for anchors across score bands using queries on "image super-resolution plugin lightweight degradation model" and "single image super-resolution generalization unseen degradations blind SR."

**Anchors retrieved:**

| Path | Avg Score | Round | Comparison to reviewed paper |
|------|-----------|-------|------------------------------|
| vTdwuKUc5Z (Text Prompt Diffusion) | 4.25 | R1 | Similar SR+degradation topic. Weaker architecture coverage (one framework), similar missing-baselines issue. LDP has broader evaluation. |
| JmGEZXkCH3 (Beyond Transformations) | 3.67 | R1 | Data augmentation for SR. Criticized for missing comparisons and unconventional setup. LDP has stronger experimental design. |
| my0RqY48xz (Awakening Collective Wisdom) | 6.50 | R2 | Improving SR generalization. Has theoretical proofs and cleaner ablations. LDP has broader architecture coverage but weaker causal isolation. |
| JkCJBoNUcU (RealDGen) | 6.00 | R2 | Data generation for real-world SR. Cleaner evaluation, fewer overclaiming issues. LDP has comparable scope but more framing issues. |
| BpKbKeY0La (AddSR) | 5.00 | R1 | Accelerating diffusion SR. Criticized for perception-distortion trade-off issues. LDP has similar quality of contributions. |
| ob9vuDv4yl (HAIR) | 4.67 | R1 | Plug-and-play restoration method. Similar "missing experiments" criticism. Comparable quality of empirical support. |

**Round 1 bracket:** 4.0–5.5. The paper is stronger than papers scoring <4 due to its broad architecture coverage and consistent synthetic results, but weaker than papers scoring >6 due to its confounded fine-tuning comparison, missing baselines, and overclaimed diffusion results.

**Final assessment:** The paper's core idea (lightweight learned degradation plugin) is sound and the synthetic results are consistent, but two issues prevent acceptance: (1) the fine-tuning experiments confound LDP with BSRGAN data fine-tuning, requiring a control condition, and (2) the diffusion posterior sampling results are substantially weaker than claimed. The missing comparison to existing generalization methods also limits the paper's ability to support its positioning. These are addressable gaps but significant in the current form.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>