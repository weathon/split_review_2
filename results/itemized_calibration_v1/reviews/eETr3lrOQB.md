Now I have all the calibration data I need. Let me write the final review.

## Summary

The paper proposes VQ-Transplant, a framework for swapping new VQ modules into a frozen, pre-trained visual tokenizer (VAR) while preserving its encoder and decoder, then briefly adapting the decoder (5 epochs on ImageNet-1k) to resolve the resulting distribution mismatch. The method is evaluated across five VQ algorithms × two quantization scales × four datasets with thorough metric reporting. A secondary contribution, MMD-VQ, uses Maximum Mean Discrepancy for distribution alignment between features and codebook.

## Strengths

- **Practical and clearly motivated core idea.** Decoupling VQ algorithm development from full tokenizer retraining is a genuine bottleneck in visual tokenization research (Section 1). The two-stage design (substitution then decoder adaptation) is clean and easy to understand.

- **Strong internal validation of the two-stage logic.** The paper convincingly demonstrates that after Stage I (VQ substitution only), even VQ methods with *lower* quantization error than the original VAR produce worse reconstruction metrics (Tables 3 and 7, Substitution rows vs. original VAR). Stage II (decoder adaptation) closes this gap, validating the core thesis.

- **Broad empirical coverage.** Experiments cover 5 VQ algorithms (Vanilla, EMA, Online, Wasserstein, MMD) × 2 quantization scales (multi-scale and fixed-scale) × 4 datasets (ImageNet-1k, FFHQ, CelebA-HQ, LSUN-Churches) with 7 metrics, providing a thorough characterization.

## Weaknesses

### Major

- **MMD-VQ's advantage over Wasserstein VQ is marginal and inconsistent, undermining its status as a separate contribution.** The paper presents MMD-VQ as a novel VQ method motivated by overcoming Wasserstein VQ's Gaussian assumptions. However, the empirical evidence does not support a meaningful advantage:
  - Multi-scale (Table 3, Adaptation): MMD beats Wasserstein by r-FID margins of 0.02 (K=4096: 0.91 vs. 0.93; K=8192: 0.81 vs. 0.83) — noise-level differences.
  - FFHQ (Table 8, Adaptation, K=32768): Wasserstein *outperforms* MMD (1.21 vs. 1.37 r-FID).
  - LSUN-Churches (Table 10, Adaptation): Wasserstein *outperforms* MMD (1.79 vs. 1.87 r-FID).
  No diagnostic experiment demonstrates a case where non-Gaussian feature distributions cause Wasserstein VQ to fail while MMD succeeds, despite this being the stated motivation. This makes MMD-VQ more appropriate as an ablation within the VQ-Transplant framework than as a standalone contribution.

- **The headline efficiency numbers conflate multiple uncontrolled factors, inflating the apparent gain.** The abstract's "95% cost reduction" and Table 1's "21.8× speedup" compare decoder-only fine-tuning from a pre-trained backbone (2×A100, 22 hours, ImageNet-1k) against full from-scratch pre-training with a different GPU count and dataset (VAR: 16×A100, 60 hours, OpenImages). The ratio mixes dataset differences, GPU-count differences, and the fundamental asymmetry between fine-tuning and pre-training. While VQ-Transplant is clearly cheaper, the specific multiplicative speedup figure is not a clean measure.

### Minor

- **No downstream generation evaluation.** The paper evaluates reconstruction metrics only (r-FID, PSNR, SSIM, LPIPS, r-IS). For a visual tokenization paper whose ultimate application is generative modeling, showing downstream generation (e.g., class-conditional ImageNet 256×256) is the community standard and would substantially strengthen the practical claim. This limitation is not acknowledged.

- **Frame around adversarial training is inconsistent.** The paper motivates VQ-Transplant by characterizing adversarial training as "computationally intensive" and "inherently unstable" (Section 1), yet Stage II uses the same GAN loss with a DINO-S discriminator, DiffAug, consistency regularization, and LeCAM regularization. The savings come from not training the encoder and from fewer training epochs, not from avoiding adversarial training. The paper should acknowledge this honestly.

- **From-scratch comparison in Table 6 is only partially informative.** Comparing VQ-Transplant (22 hours) against 5–7 epoch from-scratch training (25–35 hours) shows much worse performance for the latter, but as the paper itself notes, "discrete tokenizers typically require hundreds of epochs." The question of *how much compute would be needed to match VQ-Transplant's performance from scratch* is unanswered, which would be the more informative comparison.

- **Cross-dataset "state-of-the-art" claim is not tightly controlled.** The baselines in Tables 8–10 (FFHQ, CelebA-HQ, Churches) use different token counts (256 vs. 512), codebook sizes, and architectures. While this is standard ML benchmarking practice, the "state-of-the-art" framing should acknowledge these confounds.

- **Decoder adaptation protocol lacks some specification.** The paper does not clarify whether the discriminator is initialized from the pre-trained tokenizer or from scratch, and whether the same learning rate schedule as the original training is used (reference to Tian et al. (2024) provides partial but incomplete detail). The weaker LDM-16 results are deferred entirely to the appendix (Appendix D), limiting assessment of the method's generality.

### Trivial

- Notation inconsistency: Equation (2) uses $\mathcal{L}_{\text{Perf}}$ while Equation (4) uses $\mathcal{L}_{\text{Per}}$ for the perceptual loss.

## Nice-to-Haves

- Ablate decoder adaptation with L2 + perceptual loss only (no GAN) to clarify what the adversarial component contributes.
- Diagnose the MMD advantage over Wasserstein VQ with a synthetic experiment using explicitly non-Gaussian feature distributions.
- Compare against training the new VQ module + decoder from scratch for the same compute budget to isolate the transplant benefit from pre-trained initialization.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Fundamentally unfair comparisons" (claimed as Structural/Fatal):** Weakened to Major. The efficiency comparison mixes confounds (GPU count, dataset, paradigm) but does not invalidate the core contribution. The paper's main claim — that VQ-Transplant saves substantial compute — remains true.
- **"Adversarial training undermines own motivation" (claimed as Structural):** Weakened to Minor framing issue. The savings come from fewer epochs and frozen encoder, not from avoiding adversarial training.
- **"Table 6 comparison staged" (claimed as Evidential):** Weakened to Minor. The paper is transparent about the limitation.
- **"L_unique defined only by example":** Removed. The paper defines it clearly in Section 4.2 as MMD distance for MMD-VQ.
- **"r-FID discrepancy 0.806 vs. 0.81":** Removed. These differ only by rounding (0.806 → 0.81).
- **Missing statistical significance / confidence intervals:** Removed as a nitpick. Single-run evaluation is standard for large-scale vision benchmarks.
- **Strengths about "problem is well-motivated" / "two-stage design is clean":** These are generic and filtered per instructions; the remaining strengths above are specific and evidence-grounded.

## Novel Insights

The most interesting finding from the review synthesis is the paper's own strongest internal result: the Stage I substitution experiment showing that reduced quantization error does *not* translate to better reconstruction (Tables 3 and 7), which cleanly isolates and validates the decoder-quantization mismatch problem. This is a non-obvious diagnostic result that independently motivates the decoder adaptation stage. The calibration comparison reveals that the paper shares a structural pattern with other borderline VQ papers (RAQ-VAE at 5.50): a practical contribution that reviewers find useful, but whose presentation overstates the advance and whose secondary methodological contribution (MMD-VQ) lacks sufficient empirical support.

## Suggestions

1. **Reframe the efficiency comparison** to explicitly separate the factors: report GPU-hours directly and note the confounds. Replace "21.8× faster" with a more precise claim like "achieving better reconstruction using 22 GPU-hours versus VAR's 960 GPU-hours, while noting that this comparison is between decoder-only fine-tuning and full from-scratch pre-training."
2. **Either strengthen or downgrade MMD-VQ.** Either provide a diagnostic experiment (e.g., synthetic non-Gaussian features) showing MMD's advantage over Wasserstein VQ, or reposition MMD-VQ as an ablation within VQ-Transplant rather than a separate contribution.
3. **Add a downstream generation experiment.** Even a single setup (e.g., class-conditional ImageNet 256×256 generation with the transplanted tokenizer) would significantly strengthen the practical claims.
4. **Acknowledge limitations explicitly** in the conclusion: (a) the method still requires adversarial training in Stage II, (b) reconstruction-only evaluation, (c) the efficiency comparison is not controlled.
5. **Include LDM-16 results in the main paper** rather than deferring to appendix, since they reveal important boundary conditions for the method's generality.

## Score and Decision

**Calibration Anchors Used:**
| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| yGnsH3gQ6U.md (BSQ: Binary Spherical Quantization) | 5.75 | R1 | Yes | Stronger novel quantization method, similar comparison fairness concerns; VQ-Transplant is slightly weaker due to marginal MMD-VQ contribution |
| mb2ryuZ3wz.md (How many tokens) | 5.75 | R1 | Yes | Novel variable-length token concept, limited to ImageNet-100; VQ-Transplant is comparable but with broader evaluation |
| GMwRl2e9Y1.md (Rotation Trick) | 8.00 | R1 | Yes | Clearly stronger — principled method, rigorous theory, extensive ablations; VQ-Transplant is well below this bar |
| YlWvQSBCgl.md (Channel-wise Quantization) | 4.00 | R1 | Yes | Weaker — novelty concerns, limited resolution, weak theoretical justification; VQ-Transplant is clearly stronger |
| iqqpx8hgSQ.md (RAQ-VAE) | 5.50 | R2 | Yes | Most comparable anchor — both are practical extensions to VQ-VAE without retraining, both criticized for weak baselines and limited evaluation; VQ-Transplant matches this profile closely |
| 8ishA3LxN8.md (FSQ) | 6.50 | R2 | Yes | Much cleaner and stronger contribution; VQ-Transplant is clearly below this |

**Round 1 bracket:** 5.0–6.0 (between borderline reject and borderline accept).

**Round 2 narrowing:** The shared heavy-weight items with RAQ-VAE (5.50) — practical contribution but insufficiently controlled comparisons and limited evaluation scope — establish the closest anchor. VQ-Transplant shares RAQ-VAE's pattern of a useful but overclaimed practical contribution. The missing heavy-weight positive items (no strong novelty anchor like FSQ's simplicity, no principled method like BSQ's quantization) and the presence of a marginal secondary contribution (MMD-VQ) place this paper at 5.5.

**Final Score: 5.5.** The core VQ-Transplant idea is pragmatic and well-validated internally, and the empirical breadth is commendable. However, the inflated efficiency framing, the marginal and inconsistent evidence for MMD-VQ as a separate contribution, and the absence of generative evaluation prevent a clear acceptance. The paper would benefit substantially from: (a) honest reframing of efficiency comparisons, (b) either strengthening or downgrading MMD-VQ, and (c) adding downstream generation results.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>