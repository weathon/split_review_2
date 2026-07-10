Now I have all the information I need. Let me produce the final consolidated review.

---

## Summary

The paper introduces ARSS, the first decoder-only autoregressive transformer framework for novel view synthesis (NVS) from a single image with camera control. The system combines a video tokenizer (VidTok) for temporally consistent visual tokens, a camera autoencoder that converts Plücker raymaps into 3D positional guidance tokens, and a causal transformer trained with a hybrid spatial-permutation/temporal-preservation strategy. Experiments on RealEstate10K, ACID, and DL3DV benchmark the approach against diffusion-based and feed-forward NVS baselines. The paper's core idea — adapting the GPT-style AR visual generation paradigm to multi-view sequences with explicit 3D camera conditioning — is genuinely novel and fills a clearly identifiable gap.

## Strengths

- **First application of decoder-only AR to NVS with camera control.** Prior AR visual generation work focused on single-image synthesis; extending this to multi-view generation with precise 3D camera conditioning is a nontrivial extension that the paper designs end-to-end, from tokenization through camera encoding to shuffled-sequence training. This directional novelty is the paper's strongest asset.

- **Elegant dual-role camera autoencoder design.** Encoding Plücker raymaps into camera tokens that simultaneously serve as camera pose conditioning and 3D positional instruction tokens during spatial permutation (Section 3.2.2) is a clean solution. Because the Plücker raymap retains spatial resolution matching the latent grid, each visual token receives its own ray-direction+momentum descriptor that slots naturally into the token-shuffling training paradigm.

- **Hybrid permutation strategy is well-motivated and convincingly ablated.** The choice to shuffle spatial order while preserving temporal order (Section 3.2.3) is clearly reasoned, and the ablation (Table 2) shows it outperforms both raster-order and full spatiotemporal shuffle across all reported metrics, providing concrete evidence that the design choice is sound.

- **Error accumulation analysis across long trajectories.** Figure 6's per-frame metrics across 17-frame sequences offer informative evidence about long-horizon degradation behavior that most NVS papers omit. This is valuable regardless of the absolute numbers.

## Weaknesses

### Fatal
None.

### Major

- **The quantitative evidence does not support the paper's headline claims.** The abstract claims "overall comparable to SOTA" (line 9), while the introduction claims "out-performs current state-of-the-art methods" (line 88) and the discussion claims "outperforms state-of-the-art methods leveraging diffusion models and transformers" (line 281). Against the strongest baseline (SEVA): on RealEstate10K, ARSS wins on PSNR (+1.5%), LPIPS (-23%), and FVD (-12%) but loses on SSIM (-6.9%) and FID (+1.3%); on ACID, ARSS wins on PSNR (+0.7%) and LPIPS (-19%) but loses on SSIM (-6.2%), FID (+44% relative — 47.76 vs 33.16), and FVD (+1.7%). The paper dismisses the 44% FID gap on ACID as "minor geometric inconsistencies" (line 231), which is a significant understatement. A method that degrades FID by 44% on one of two primary evaluation datasets cannot credibly claim to "outperform" SOTA. The paper needs to either calibrate its claims to match the evidence or address why the FID gap is so large.

- **Ablation metrics are inconsistent with main-table metrics and the discrepancy is never explained.** Table 1 reports "Ours" on RealEstate10K as PSNR 19.02, SSIM 0.624, LPIPS 0.269, FID 47.60. Tables 2 and 3 (ablation studies) report "ours" on the same dataset as PSNR 19.22, SSIM 0.565, LPIPS 0.294, FID 60.11. SSIM differs by 0.059 (10% relative) and FID differs by 12.51 (26% relative). The paper provides no explanation — different checkpoint, evaluation subset, or random seed? This inconsistency undermines trust in all reported numbers, as the reader cannot determine which evaluation protocol is correct.

- **The paper's core differentiating advantage — causal incremental generation — is motivated but never tested.** The introduction (line 13) argues that AR models can "incrementally extend and reuse existing generations when the trajectory changes" — a clear advantage over joint-generation diffusion models. However, every evaluation uses fixed, pre-defined trajectories where causal structure provides no measurable benefit. The paper's most distinctive claimed advantage is left entirely unvalidated. This gap between motivation and evaluation weakens the paper's argument for why the AR paradigm is preferable for this task.

- **Genwarp listed as a baseline but excluded from quantitative comparison.** Genwarp (Seo et al., 2024) is introduced in Section 4.1, shown in qualitative comparisons (Figures 3, 4), and discussed in the text (lines 229–230), but never appears in Table 1. No reason is given for this omission. Since Genwarp is a published NVS method, its exclusion from quantitative comparison weakens the evaluation's completeness.

### Minor

- **Unsupported claim about SEVA's training requirements.** The paper states that SEVA "benefits from large-scale, high-resolution training data and heavy computational resources" (line 241) without providing any evidence, citation, or compute-budget comparison. This reads as post-hoc rationalization for underperformance on ACID FID and should either be supported or removed.

- **No variance or significance estimates.** All quantitative results are single-run point estimates with no standard deviations, confidence intervals, or significance tests. Given that PSNR differences between ARSS and SEVA are within 0.3 dB on both datasets, the reader cannot assess whether these differences reflect meaningful improvement or random variation.

### Trivial

- **Equation 5 naming error.** In the camera loss description (line 153), both the ray direction and the momentum term are labeled as "d" ("d is the normalized camera ray direction, d is the momentum term"), but the equation uses "m" for the momentum term. The second "d" should be "m".

## Nice-to-Haves

- A demonstration of the causal advantage (e.g., mid-trajectory modification where the AR model reuses prior views while diffusion baselines regenerate) would transform a purely motivational claim into a compelling experimental result.
- Adding Genwarp to Table 1, or explicitly explaining why it was excluded, would improve evaluation completeness.
- Reporting results over 3 seeds with standard deviations for the main SEVA comparison would help interpret the small-margin metric differences.

## Removed Points

The following concerns raised in the input reviews were filtered out as unverifiable, speculative, or not substantive:

- **ViewCrafter/RayZer numbers claimed as "anomalously low":** This criticism relies on external knowledge of these methods' published results that cannot be verified from the paper alone. While the reported PSNR values (12.67, 12.97) are low, whether they are incorrect relative to published numbers is not verifiable from the paper's content. Better framed as a question for the authors.
- **Equation 7 "garbled":** Likely a PDF extraction artifact; the parser strips appendix content.
- **"SEVA also trained from scratch" counter-claim:** Not verifiable from the paper under review, which does not describe SEVA's training protocol.
- **Causal video tokenizer needing more detail:** A presentation preference, not a substantive weakness; the description in lines 127–135 is adequate for a conference paper.
- **Per-frame claim in Error Accumulation Analysis cannot be assessed without figure:** The figure is included in the submission; the text describes what it depicts.
- **Missing related works / baselines:** Cannot be independently verified; all cited references are assumed to exist.

## Novel Insights

None beyond the paper's own contributions. The analysis primarily identifies gaps between the paper's claims and its evidence base, rather than surfacing new technical insights about the method itself.

## Suggestions

1. **Reconcile the inconsistent numbers** between Tables 1 and 2/3. State whether they come from different checkpoints, evaluation subsets, or random seeds; then use a consistent evaluation protocol across all experiments.
2. **Calibrate the claims** to match the evidence. Replace "outperforms SOTA" language with a precise statement of where the method wins (LPIPS, PSNR), where it loses (SSIM, FID on ACID), and an honest discussion of why.
3. **Either demonstrate or retract the causal advantage.** Run a simple experiment: modify a trajectory mid-generation and show that the AR model reuses prior views while a diffusion baseline cannot. If this cannot be demonstrated, remove the claim from the motivation.
4. **Add Genwarp to the quantitative comparison** or explicitly state why it was excluded (e.g., could not produce comparable numbers under the same evaluation protocol).
5. **Add variance estimates** for the main comparison with SEVA.

## Score and Decision

**Score: 4.0**

**Decision: Reject**

This paper brings a genuinely novel idea to novel view synthesis — applying decoder-only autoregressive transformers — and demonstrates a competent system design with clear ablations. The camera autoencoder and hybrid permutation strategy are technically sound contributions. However, the evaluation as presented does not adequately support the paper's central claims. Three issues are decisive: (1) the headline "outperforms SOTA" claim is contradicted by the paper's own data (44% FID degradation on ACID is not minor); (2) the ablation and main-table numbers are inconsistent without explanation, undermining trust in the reported metrics; and (3) the paper's most distinctive claimed advantage (causal incremental generation) is motivated but never tested. These are fixable shortcomings, and the core contribution is worth pursuing, but in its current form the evaluation rigor is insufficient to recommend acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>