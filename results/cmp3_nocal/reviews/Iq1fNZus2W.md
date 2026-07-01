## Summary

This paper proposes Patch-Wise and Keyword-Aware Attention (PKA), an efficient attention mechanism for multi-condition control in Diffusion Transformers (DiTs). PKA decomposes the standard full-attention into two specialized modules: Position-Aligned Attention (PAA), which replaces quadratic attention with one-to-one computation for spatially-aligned conditions, and Keyword-Scoped Attention (KSA), which masks attention to keyword-relevant regions for subject-driven conditions. The method also introduces a condition KV-cache and an early-timestep sampling strategy for training. Empirically, PKA achieves up to 10× inference speedup and 5.12× VRAM reduction compared to full attention, with quality metrics that are competitive or better than baselines on multi-condition tasks.

## Strengths

- **Well-diagnosed problem with empirical justification.** The paper convincingly identifies the "concatenate-and-attend" bottleneck in multi-condition DiTs and provides direct evidence of attention sparsity: Figure 2 shows diagonal-dominant attention for spatial conditions, Figure 3 shows localized activations for subject conditions. This diagnostic analysis is the strongest motivator for the method and stands on its own as a contribution.

- **Principled two-module decomposition matched to condition structure.** Rather than applying a generic sparsity technique, PAA (one-to-one spatial attention, O(N)) and KSA (keyword-masked attention) are each designed for the specific redundancy pattern of their corresponding condition type. The condition KV-cache (reusing condition projections after the first step) is a natural extension of the observation that condition tokens only self-attend.

- **Large, well-documented efficiency gains that scale with condition count.** Figures 7–8 show dramatic and clean results: PKA's inference time grows sub-linearly with condition count while UniCombine (full attention) grows steeply. At 16 conditions PKA is ~10× faster than full attention and ~1.6× faster than OminiControl2. The linear vs. quadratic complexity advantage is clearly demonstrated, and the trendlines confirm the advantage grows with condition count.

- **The PAA ablation (Figure 9) validates the core sparsity premise.** Comparing PAA against full attention and sliding-window attention on the same architecture shows that the one-to-one design reduces latency (13.63s vs. 15.38s) and VRAM (237MB vs. 308MB) while producing visually comparable quality. This internal control isolates the effect of the attention mechanism itself.

## Weaknesses

### Major

- **The quality comparison against baselines (Table 1) is confounded by unstated differences in training.** The paper states: "To ensure a fair comparison, we fine-tune the FLUX.1 model using LoRA" (Section 4.1). However, it does not specify whether the two baselines (OminiControl2 and UniCombine) were also fine-tuned under identical conditions — same LoRA rank, same 20,000 iterations, same optimizer, same data subset. Since these are *methods* rather than pretrained weights, their adaptation to FLUX.1 is nontrivial, yet the paper provides no details. This is critical because PKA shows large quality improvements (e.g., FID 52.99 vs. 61.03/72.03 on Subject-Canny), which are otherwise difficult to explain given that PKA *restricts* attention. Without clarifying whether baselines received the same LoRA fine-tuning, the quality results in Table 1 cannot be attributed to PKA's attention design versus unequal training. **The paper should either confirm that all methods were trained identically (with the only variable being the attention mechanism), or report a controlled experiment isolating the attention mechanism's effect on quality.**

- **The keyword extraction procedure for KSA is completely underspecified.** KSA uses "a small set of keyword tokens K" (1–2 tokens) to compute the relevance mask (Eq. 3). The paper mentions that each caption "contains a descriptive keyword" (Section 4.1) but provides no procedure for identifying or extracting these keywords from the text. Are they manually annotated? The first noun from a dependency parse? The token with highest attention in a warm-up pass? Without specifying this, the method cannot be independently reproduced.

### Minor

- **KSA's temporal consistency assumption is not empirically validated.** KSA computes a mask at timestep *t* and reuses it at *t*+1, citing temporal consistency (Zhou et al., 2025). However, no analysis is provided of mask stability across consecutive denoising steps. If an object's location shifts between steps, the stale mask could attend to the wrong regions. While this concern may be minor in practice (the mask is recomputed every other step), evidence of mask overlap rates across timesteps would strengthen the paper.

- **No error bars or measures of variability are reported for any quantitative result.** Given that some metric differences are small (e.g., CLIP-T: 0.349 vs. 0.352), it is impossible to assess whether differences are meaningful. This is a standard expectation for reported results.

- **The perturbation experiment motivating early-timestep sampling (Figure 5) is poorly described.** The paper says "SSIM of Visual condition perturbation" and plots SSIM vs. number of perturbation steps for "High-to-Low" and "Low-to-High" orderings. However, it does not specify: (a) what exactly is being perturbed — the condition tokens, the noisy latents, or something else; (b) between which two sets SSIM is computed. The experiment's setup and conclusions cannot be properly evaluated without this information.

- **Key training details are missing.** The paper does not specify: which FLUX.1 variant was used (dev vs. schnell), the LoRA rank, the learning rate, the size of the Subject200K subset used, nor the train/test split. The early-timestep sampling ablation (Figure 11) is a visual-only comparison on a single example with no quantitative metrics.

### Trivial

- None.

## Nice-to-Haves

- A controlled experiment where the only variable between PKA and the baselines is the attention mechanism (same LoRA, same data, same iterations) would disentangle quality improvements from training confounds.
- Analysis of KSA mask overlap rates between consecutive timesteps to validate the temporal consistency assumption.
- Failure case analysis: when does PAA break (e.g., resolution mismatch between condition and image)? When does KSA break (e.g., ambiguous keywords in multi-person scenes)?
- Evaluation on single-condition or pure text-to-image tasks to verify PKA does not degrade the base model's capability.
- Ablation isolating the effect of early-timestep sampling from PKA (i.e., does this sampling help even without PKA?).

## Removed Points

These points from the input are removed with justification:

- **"Efficiency comparison staged against uncompetitive baseline"** — The paper explicitly states the 10× figure is "compared to the full-attention mechanism in UniCombine" (Section 4.2.1). The abstract and introduction are consistent with this framing. Not misleading.
- **"Perturbation experiment tests the wrong thing"** — The critic asserted this experiment "perturbs the noisy image itself" rather than conditions. The paper states "Visual condition perturbation" (Figure 5 caption) and describes investigating the "temporal influence of visual conditions." The critic's specific claim is not verifiable from the paper; the experiment is simply underspecified (noted above as a minor weakness).
- **"What happens at the very first denoising step"** — The method is clear: the mask is computed at step *t* and reused at *t*+1. At step 0 (the first), the mask is computed from scratch.
- **"Attention module VRAM vs. end-to-end"** — The paper clearly distinguishes "inference speedup" (end-to-end, Figure 7) from "attention module VRAM" (Figure 8).
- **Strength: "Quality is not sacrificed"** — Removed because it conflicts with the verified weakness about the confounded quality comparison.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run a controlled experiment where PKA, a full-attention baseline, and OminiControl2 are all fine-tuned with the same LoRA configuration on the same data, and report quality metrics. This would cleanly isolate whether the attention mechanism itself affects quality or whether the observed improvements come from training factors.
2. Specify the keyword extraction procedure concretely.
3. Add error bars or confidence intervals to Table 1 and report the number of evaluation samples.
4. Provide a brief analysis of mask stability across consecutive denoising steps for KSA.
5. Clarify the perturbation experiment setup: what is perturbed, and between what two quantities is SSIM computed?

## Score and Decision

<score>6</score>
<decision>Borderline Accept</decision>

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>