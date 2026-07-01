## Summary

This paper introduces ARSS, the first decoder-only (GPT-style) autoregressive model for novel view synthesis (NVS) from a single image with camera control. The method uses a video tokenizer for temporally consistent discrete tokenization, a camera autoencoder that encodes Plücker raymaps into 3D positional tokens, and a spatial-permutation strategy that preserves temporal causality while enabling the transformer to handle bi-directional spatial context. Evaluated on RealEstate10K, ACID, and DL3DV (zero-shot), ARSS achieves results competitive with diffusion-based methods like SEVA.

## Strengths

1. **First causal AR approach to NVS with camera control.** The paper is genuinely the first to apply decoder-only autoregressive modeling to NVS from a single view. This is a non-trivial extension because NVS requires precise 3D camera awareness that prior AR visual generation work (LlamaGen, VAR, etc.) did not address. The novelty is specific and defensible (lines 86, 281).

2. **Component-level design is coherent and ablated cleanly.** Each of the three challenges identified (temporal consistency via video tokenization, 3D guidance via camera autoencoder, bi-directional spatial context via permutation) maps to a distinct module, and the ablations in Tables 2–3 and Figure 7 convincingly show that each choice matters. The ablation on permutation strategies (raster vs. full-perm vs. spatial-only) is particularly informative.

3. **Error accumulation analysis (Figure 6) provides partial evidence for the core motivation.** The paper's argument that causal AR models can condition on previously generated frames is tested via per-frame metrics along camera trajectories. This analysis is a meaningful addition that goes beyond aggregate metrics.

## Weaknesses

### Fatal
None.

### Major

1. **Inconsistent claims about outperforming SOTA.** The abstract truthfully states that ARSS achieves results "comparable to state-of-the-art" (line 9), but the introduction claims it "out-performs current state-of-the-art methods" (line 88) and the discussion repeats this (line 281). Against the strongest competitor (SEVA), the results are genuinely mixed:

   | Metric | Re10K (ARSS vs SEVA) | ACID (ARSS vs SEVA) |
   |--------|---------------------|---------------------|
   | PSNR ↑ | **19.02** vs 18.73 | **21.93** vs 21.77 |
   | SSIM ↑ | 0.624 vs **0.670** (−7%) | 0.623 vs **0.664** (−6%) |
   | LPIPS ↓ | **0.269** vs 0.349 | **0.265** vs 0.326 |
   | FID ↓ | 47.60 vs **46.98** | 47.76 vs **33.16** (+44%) |
   | FVD ↓ | **50.51** vs 57.56 | 54.60 vs **53.69** |

   ARSS wins on PSNR and LPIPS consistently but loses on SSIM (~7% on both datasets) and, on ACID, loses badly on FID (+44%). The paper's own Section 4.2 acknowledges these gaps (line 231–232), yet the discussion overrides this nuance with a blanket "outperforms" claim. The inconsistency between the evidence and the headline framing is the paper's most significant weakness.

2. **Ablation results diverge from main results without explanation.** The ablation tables report PSNR 19.22 / SSIM 0.565 (Tables 2–3), while the main results in Table 1 report PSNR 19.02 / SSIM 0.624 on RealEstate10K. These differences — particularly the SSIM gap of 0.059 — are non-trivial and no explanation is given (different subset? different seed? different hyperparameters?). Readers cannot determine whether the ablations are commensurable with the main evaluation.

### Minor

3. **SEVA excluded from the error accumulation analysis (Figure 6).** The paper's central claim — that causal AR models degrade more slowly over long trajectories — is demonstrated against LVSM, MotionCtrl, RayZer, and ViewCrafter, but not against SEVA, the strongest competitor. Since SEVA is the primary point of comparison in the main tables, its absence from this analysis weakens what would otherwise be the strongest argument for the AR approach.

4. **Systematic SSIM deficit is noted but not analyzed.** The ~7% SSIM gap appears consistently across both datasets. The paper describes this as "minor geometric inconsistencies" (line 231), but a consistent gap of this magnitude on a structural similarity metric suggests a systematic issue (likely rooted in discrete tokenization or the causal attention mask) that deserves frank analysis. The paper would be stronger if it investigated the root cause rather than labeling it as minor without evidence.

5. **SEVA absent from DL3DV zero-shot evaluation.** The paper explains that DL3DV was part of SEVA's training data, so excluding it is justified. However, this means the only out-of-distribution evaluation lacks the strongest baseline, leaving the reader unable to assess whether the generalization gap to SEVA narrows or widens on unseen data.

6. **No ablation of the camera autoencoder.** The camera autoencoder is a core contribution, but there is no ablation that removes or degrades it (e.g., a "no camera tokens" baseline). Without this, the contribution of the 3D positional guidance is asserted but not independently verified.

### Trivial

7. **Parallel decoding claim is not substantiated.** Line 177 states that the system "has the capacity to predict multiple tokens at one time," but the inference procedure (line 210) is entirely sequential. No parallel decoding is implemented or evaluated. This should be clarified as a theoretical advantage or future direction.

8. **"World models" framing is dropped after the introduction.** The abstract and introduction invoke world models (lines 9, 13–15), but the paper is about NVS along fixed camera trajectories with no planning, interaction, or dynamics modeling. This framing sets expectations the paper does not fulfill and is never substantiated.

## Nice-to-Haves

- An ablation that removes the camera tokens would establish whether the camera autoencoder contributes meaningfully beyond what the visual tokens alone provide.
- Error bars or multiple-seed runs would help determine whether the small PSNR margins are meaningful.
- The resolution limitation (256×256 vs. higher-resolution baselines) and training data disparity are acknowledged but not quantified; a rough comparison of compute/data budgets would help readers calibrate.
- Implementing a simple version of parallel decoding (predicting k tokens at once) and measuring the speed–quality tradeoff would either substantiate or retire the claim in point 7 above.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Typo in Eq. 5 description (second "d" should be "m")** — removed per policy on typographical criticisms; these are parser artifacts or minor author errors.
- **"No error bars or statistical significance"** — not standard practice for large-scale generative model evaluations in this subfield; downgraded to a nice-to-have.
- **"Resolution limitation should be foregrounded earlier"** — the paper already acknowledges this limitation in Section 5; the timing of disclosure is a presentation preference, not a weakness.
- **"Training data discrepancy not quantified"** — the paper states SEVA uses "large-scale, high-resolution training data" (line 241); the critic asks for quantification of data the authors may not have access to from the SEVA publication.

## Novel Insights

The most interesting observation from the review meta-analysis is that the method's mixed results relative to SEVA are themselves informative: ARSS systematically wins on PSNR and LPIPS while losing on SSIM and (on ACID) FID. This pattern suggests that AR and diffusion approaches have complementary failure modes — AR methods may sacrifice structural fidelity for sharper per-pixel accuracy. This is a potentially valuable insight that the paper could foreground but currently does not. The error accumulation analysis points in the right direction but is incomplete without SEVA.

## Suggestions

1. **Align claims with evidence.** Replace "outperforms" with "achieves competitive results with complementary strengths and weaknesses" in the introduction and discussion. The mixed metric profile (better PSNR/LPIPS, worse SSIM/FID) is actually interesting and should be discussed as a finding, not masked.
2. **Explain the ablation/main result discrepancy.** Clarify whether the ablations use a subset, a different seed, or different settings.
3. **Include SEVA in the error accumulation analysis** if the per-frame metrics are available, or explicitly discuss its absence as a limitation.
4. **Investigate the SSIM gap.** A brief analysis of whether it comes from the video tokenizer, the causal mask, or the permutation strategy would deepen the contribution.
5. **Add a camera autoencoder ablation** to independently validate its contribution.
6. **Either implement parallel decoding or remove the claim** from the method section (it is fine as a future-work mention).

## Score and Decision

**Score:** 6  
**Decision:** Accept

The paper's core contribution — demonstrating that a causal decoder-only AR model can achieve competitive results on NVS with camera control — is novel, the method is well-designed, and the ablations are informative. The main issue is a mismatch between the cautiously mixed quantitative evidence and the overly strong claims in the introduction and discussion. This is fixable with revisions and does not invalidate the underlying contribution. The paper would be stronger if it reframed its headline finding as "AR models are viable for NVS and have complementary strengths to diffusion models" rather than "outperforms SOTA."

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>