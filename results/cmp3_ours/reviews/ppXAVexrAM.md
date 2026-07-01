## Summary

ARSS is the first application of a GPT-style decoder-only autoregressive transformer to novel view synthesis (NVS) from a single image with camera trajectory control. The method uses a video tokenizer for temporally consistent discrete tokenization, a camera autoencoder that encodes Plücker raymaps into camera tokens for 3D positional guidance, and an autoregressive transformer with a spatial-permutation-while-temporal-order strategy. The model is trained from scratch on RealEstate10K and ACID, with zero-shot evaluation on DL3DV.

## Strengths

1. **First causal AR model for NVS with explicit camera control.** The paper is genuinely the first to apply a GPT-style decoder-only autoregressive transformer to novel view synthesis with camera trajectory conditioning integrated into the token sequence. The authors identify three specific obstacles (temporal consistency in tokenization, camera conditioning, mismatch between unidirectional attention and bidirectional images) and design components to address each one. This is a legitimate architectural contribution.

2. **Principled camera token design.** The camera autoencoder that maps Plücker raymaps into latents with matching spatial-temporal dimensions as visual tokens (Eq. 5) is well-conceived. The geometric regularization losses (unit-norm rays, orthogonality of ray direction and momentum) are physically grounded and likely prevent degenerate camera representations.

3. **Clean ablation on token permutation strategies.** Figure 7 and Table 2 cleanly isolate the effect of the spatial-permutation-within-temporal-order design. The ablations show that both "raster" ordering and "full perm." degrade quality, with clear explanations for each failure mode. The ablation on tokenization (Table 3, VQ vs. video tokenizer) showing ~62% FVD improvement is similarly informative.

## Weaknesses

### Fatal
None.

### Major
1. **Central motivation (AR's sequential/causal advantages) is not evaluated.** The Introduction (paragraphs 1–2) and Related Work (line 92) argue that diffusion-based NVS methods are limited because they "generate all the images simultaneously," making it "less straightforward to impose a strictly causal structure along a camera path or to incrementally extend and reuse existing generations when the trajectory changes." The paper situates itself in the context of world models requiring "sequential and causal" processing (line 13). However, every experiment evaluates ARSS in the standard setting where all target views are known and the full trajectory is fixed — exactly the setting that does not differentiate AR models from joint-generation diffusion models. There is no experiment on incrementally adding views to an already-generated trajectory, adapting to trajectory changes after some views have been generated, or using previously generated views as additional conditioning beyond the fixed training setup. The paper either needs to add experiments demonstrating these claimed advantages or substantially revise its framing to match what is actually shown. As it stands, the motivation and the evidence are misaligned.

2. **Results are mixed but portrayed overly positively.** On ACID, ARSS's FID (47.76) is 44% worse than SEVA's (33.16). On RealEstate10K, ARSS trails SEVA on SSIM (0.624 vs. 0.670, ~7% deficit). The Discussion (line 281) states that "our method outperforms state-of-the-art methods leveraging diffusion models and transformers" as a blanket statement, which is not supportable across all metrics — ARSS is better on PSNR and LPIPS but clearly worse on SSIM and FID. The paper also understates the FID gap (claiming "+22% FID" while the actual gap is ~44%). The results should be characterized as **competitive but mixed**, with specific strengths (PSNR, LPIPS) and weaknesses (SSIM, FID) relative to SEVA.

### Minor
3. **Ablation table numbers do not match main table numbers without explanation.** Main Table 1 reports "Ours" on RealEstate10K with PSNR=19.02, SSIM=0.624, LPIPS=0.269, FVD=50.51. Ablation Tables 2 and 3 report "ours" with PSNR=19.22, SSIM=0.565, LPIPS=0.294, and FVD=52.56 (Table 3). The SSIM and LPIPS differences are substantial (0.624→0.565 and 0.269→0.294). The paper does not specify whether ablations are on a different validation split, a different random seed, or a different experimental setting. These discrepancies need to be reconciled.

4. **Missing implementation details.** The camera autoencoder loss weights λ₁–λ₄ in Eq. 5 are never specified. Whether the video tokenizer (VidTok) is frozen or finetuned during ARSS training is not stated. These details matter for reproducibility.

5. **Notation issues.** Equation 7 is incomplete — it shows only one argument to the cross-entropy loss (the input sequence) but omits the target sequence that the CE is computed against (compare with Eq. 3 which clearly shows both arguments). Figure 6 legend says "L2SM" which should be "LVSM."

### Trivial
6. **Line 153 notation error:** "d is the normalized camera ray direction, d is the momentum term" — the second "d" should be "m" (the momentum).

## Nice-to-Haves

- **Parallel decoding speed.** The paper notes (line 177) that spatial permutation allows parallel decoding but provides no wall-clock measurements. A speed comparison against diffusion baselines (which typically require 20–50 denoising steps) would be a strong practical result.
- **Codebook/vocabulary size.** The FSQ vocabulary size for the video tokenizer is not reported, which directly affects the difficulty of the next-token prediction task.
- **Zero-shot baseline coverage on DL3DV** is limited to 3 methods (MotionCtrl, Genwarp, LVSM). While the exclusion of SEVA, ViewCrafter, and RayZer is justified (DL3DV was in their training data), the comparison set is thin.

## Removed Points

- **"Parallel decoding speed claimed but never measured"** → Moved to Nice-to-Have. The paper states an architectural capability ("has the capacity to predict multiple tokens at one time"), not a measured speed claim. Not measuring it is a missed opportunity, not a flaw in claimed results.
- **"Tokenizer codebook size not reported"** → Moved to Nice-to-Have. A standard reporting detail that is nice to have but not a core weakness.
- **"DL3DV thin coverage"** → Moved to Nice-to-Have. The paper provides a reasonable justification for the exclusions (training data overlap).
- **"Camera autoencoder architecture not specified"** → Merged into Minor #4 as part of missing implementation details.
- **"Notation error d→m"** → Kept as Trivial #6 (genuine typo but inconsequential).

## Novel Insights

The harsh critic insight that the paper's central motivation (AR sequential advantages) is never tested is the most penetrating observation. The critic correctly identifies that the paper critiques diffusion models for their inability to incrementally extend or reuse generations, but then evaluates ARSS in the same static, full-sequence setting. This is not a minor omission — it is a structural mismatch between how the paper frames its contribution and what it actually demonstrates. The critic's suggested experiment (extending trajectories beyond training length at test time) would directly validate or refute a core claimed advantage of the AR paradigm for NVS. The critic also correctly identifies that the paper understates the FID gap (44% worse on ACID, not the "22%" the paper claims) and that the blanket "outperforms" language is unsupported.

## Suggestions

1. **Either add experiments demonstrating the claimed sequential-generation advantages** (e.g., extending trajectories beyond the training length at test time, modifying the camera trajectory mid-generation) or **revise the framing** to match the standard NVS evaluation setting actually used.
2. **Characterize results honestly** as "competitive but mixed" with specific strengths (PSNR, LPIPS) and weaknesses (SSIM, FID) rather than claiming to "outperform" baselines.
3. **Reconcile the ablation table numbers** with the main table by specifying the evaluation split and experimental conditions used for ablations.
4. **Report camera autoencoder loss weights** (λ₁–λ₄) and state whether the video tokenizer is frozen or finetuned during training.
5. **Fix Equation 7** to include the target sequence argument for the CE loss, and fix the "L2SM" typo in Figure 6.

## Score and Decision

**Bracket (Round 1):** 5.0–6.0 (between AR-1-to-3 at 5.0 and GST/ControlAR at 6.25).

**Anchor papers retrieved:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pOcGFvfgjS.md` — AR-1-to-3, avg 5.0. Similar autoregressive NVS approach but with narrower evaluation (Objaverse only). ARSS has broader evaluation but shares the "AR motivation untested" issue.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NuHYh4YKNe.md` — GST, avg 6.25. Autoregressive model for pose+view prediction. Mixed reviews (3,8,6,8). Stronger demonstrated performance than ARSS.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BWuBDdXVnH.md` — ControlAR, avg 6.25. Controllable AR image generation. Cleaner results presentation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QQBPWtvtcn.md` — LVSM, avg 7.67. Non-AR transformer NVS, stronger quantitative results.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/zDJf7fvdid.md` — Zero-shot NVS via Video Diffusion, avg 6.00. All reviewers gave 6.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/hWlCc7Iksi.md` — ARVideo, avg 3.40. Autoregressive video pretraining, weaker contribution.

**Final reasoning:** ARSS has genuine novelty as the first AR model for NVS with camera control and clean architectural design. However, the paper's framing claims advantages for the AR paradigm (sequential/causal generation) that are never evaluated, and the quantitative results are more mixed than the paper portrays (notably 44% worse FID on ACID vs. SEVA). These are substantive issues that prevent a clear acceptance. The paper sits above AR-1-to-3 (5.0, Reject) due to broader evaluation and cleaner architecture, but below the 6+ range where papers typically demonstrate clearer advantages.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>