## Summary

DiSTAR introduces a zero-shot text-to-speech framework that operates entirely in a discrete residual vector quantization (RVQ) code space, coupling an autoregressive language model with a masked diffusion model. The system achieves blockwise parallelism by having the AR model draft compact patch-level representations, which a masked diffusion transformer then completes via iterative demasking, all without forced alignment or duration predictors. The fully discrete design enables controllable inference through classifier-free guidance, variable bitrate via RVQ layer pruning, and achieves state-of-the-art robustness and naturalness on standard benchmarks.

## Strengths

- **Novel and well-motivated architecture**: The tight coupling of AR drafting with discrete masked diffusion in RVQ space is a genuine architectural contribution. The paper clearly articulates why this combination addresses limitations of prior work—exposure bias in pure AR models, optimization fragility in continuous diffusion, and the challenge of modeling joint time-depth dependencies in RVQ codes. The design is principled and the motivation is compelling.

- **Strong empirical results**: DiSTAR achieves the lowest WER on both LibriSpeech-PC (1.66%) and SeedTTS test-en (1.32%) among all compared systems, including strong baselines like F5TTS and DiTAR. The subjective evaluation shows DiSTAR leading in both SMOS (3.31) and CMOS (0.22), with statistical significance indicated by confidence intervals. These results are achieved with a smaller parameter count (0.3B medium vs. 0.6B DiTAR), demonstrating genuine efficiency gains.

- **Practical controllability contributions**: The paper introduces several practically valuable inference-time controls that are well-engineered: (i) RVQ layer pruning for variable bitrate/compute without retraining, enabled by stochastic layer truncation during training; (ii) layer-wise and position-wise temperature shaping to address the "tail-first" bias in masked diffusion decoding; (iii) hybrid greedy/sample decoding. These are not just ablations but genuinely useful mechanisms for deployment.

- **Clean and thorough experimental design**: The evaluation uses appropriate benchmarks (LibriSpeech-PC, SeedTTS test-en), standard metrics (WER, SIM, UTMOS), and includes both objective and subjective evaluations. The ablation study on decoding strategies and the RVQ layer pruning analysis provide clear insights into the system's behavior.

## Weaknesses

### Fatal
None.

### Major

- **Missing critical baselines and comparisons**: The paper compares against DiTAR, F5TTS, E2TTS, and IndexTTS, but omits several highly relevant recent systems. Most notably, VALL-E 2 (Chen et al., 2024) is cited in the paper but not compared against, despite being a discrete RVQ-based system that achieved "human parity" on zero-shot TTS. Similarly, CosyVoice 2 appears in the subjective evaluation table but not in the objective results (Table 1), making cross-table comparisons difficult. The absence of these comparisons weakens the claim of "state-of-the-art" performance.

- **Incomplete ablation study**: The ablation study is limited to decoding strategies and RVQ layer pruning. Critical architectural choices are not ablated: (i) the effect of the masked diffusion component vs. a pure AR baseline; (ii) the impact of overlapping vs. non-overlapping patches; (iii) the contribution of the aggregator design; (iv) the effect of stochastic layer truncation during training. Without these ablations, it is difficult to attribute the performance gains to specific design choices.

- **Limited analysis of the discrete masked diffusion component**: The paper claims that discrete masked diffusion mitigates exposure bias and improves intra-patch coherence, but provides no direct evidence. There is no comparison against a variant that uses continuous diffusion over the same patch structure, nor an analysis of how the number of diffusion steps (NFE) affects quality. The paper uses NFE=24 for DiSTAR but compares against DiTAR with NFE=10—this is a significant compute difference that is not discussed.

### Minor

- **The "tail-first" bias observation is interesting but the proposed mitigation is heuristic**: The paper identifies that tokens near the end of each patch receive higher confidence early in decoding, and proposes layer-wise and position-wise temperature shaping. While these tricks work empirically, the paper does not provide a deeper analysis of why this bias occurs or whether a more principled solution (e.g., modifying the mask schedule or training objective) might be preferable.

- **Limited discussion of failure modes**: The paper presents only positive results. There is no discussion of cases where DiSTAR fails—e.g., handling of prosody, emotional expression, or rare words. The WER on LibriSpeech-PC (1.66%) is impressively low, but this is a relatively clean dataset; performance on more challenging in-the-wild data is not reported.

### Trivial
None.

## Nice-to-Haves

- A comparison against a pure AR baseline (without the masked diffusion component) would clearly demonstrate the benefit of the proposed architecture.
- An analysis of the trade-off between NFE and quality would help practitioners choose appropriate compute budgets.
- Discussion of the computational cost of the masked diffusion module relative to the AR module during inference would be useful.

## Novel Insights

The paper's key insight is that discrete RVQ codes, which have been primarily modeled with pure autoregressive or flat sequence approaches, can be effectively decomposed into a two-level hierarchy: an AR model captures coarse temporal structure across patches, while a masked diffusion model resolves the fine-grained multi-codebook dependencies within each patch in parallel. This decomposition is principled because it aligns with the natural structure of RVQ codes—the temporal axis is causal and long-range, while the depth axis (across RVQ layers) is bidirectional and local. The observation that upper RVQ layers primarily encode acoustic detail rather than linguistic content, validated by the layer pruning experiments, provides practical guidance for efficient deployment. The "tail-first" bias in masked diffusion decoding for temporally structured sequences is a subtle but important phenomenon that may generalize to other sequence generation tasks beyond speech.

## Suggestions

1. Add comparisons against VALL-E 2 and other recent discrete RVQ-based TTS systems to substantiate the state-of-the-art claim.
2. Include an ablation that replaces the masked diffusion component with a simple AR decoder (or continuous diffusion) over the same patch structure to isolate the benefit of discrete masked diffusion.
3. Report results with varying NFE values to show the quality-compute trade-off and enable fair comparison with DiTAR (NFE=10).
4. Add a discussion of failure cases or limitations, particularly for challenging acoustic conditions or out-of-domain text.

## Score and Decision

This is a strong paper with a novel architecture, well-motivated design, and convincing empirical results. The main concerns are the missing comparisons against key baselines (VALL-E 2) and the incomplete ablation study, which prevent full confidence in the claimed state-of-the-art status. However, the core contribution—tightly coupling AR drafting with discrete masked diffusion in RVQ space—is genuinely novel and practically valuable. The paper is clearly written and the experiments are otherwise thorough. With the suggested additions, this would be a clear accept. As is, the missing comparisons and ablations are significant but not fatal.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>