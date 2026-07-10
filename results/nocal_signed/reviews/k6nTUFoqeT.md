Now let me compile the final review with all verified, filtered points.

## Summary

This paper introduces FASTer, a unified framework for autoregressive Vision-Language-Action (VLA) models with two components: FASTerVQ (a neural action tokenizer using residual vector quantization with patchification and DCT-based reconstruction losses) and FASTerVLA (an autoregressive policy with block-wise decoding and a lightweight action expert). The key idea is to design a compact, high-fidelity discrete action representation that enables efficient autoregressive decoding. The paper evaluates across nine benchmarks covering five embodiments in both simulation and real-world settings, demonstrating improved inference speed and competitive or state-of-the-art task performance.

## Strengths

- **Broad and demanding evaluation across diverse benchmarks (Section 4, Tables 1–2, Figures 4–10):** The paper evaluates across nine benchmarks covering five distinct embodiments, including both simulation and real-world settings (LIBERO, VLABench, GalaxeaManisim, xArm, R1Lite, Bridge, Droid). This scope substantially exceeds most VLA papers and includes challenging settings like whole-body control with 21 DoF and bimanual manipulation.

- **Cross-backbone validation across three different VLM backbones (Figure 7):** Consistent improvement across PaliGemma2-3B, Qwen2.5-3B, and InternVL3.5-2B strengthens the claim that gains come from the tokenization and decoding design, not from backbone-specific tuning.

- **Clear, well-motivated problem framing (Section 1, lines 16–18):** The paper identifies four concrete desiderata for action tokenizers (high compression, robust reconstruction, 2D structural modeling, flexibility) and systematically argues why existing methods fall short, providing a principled basis for evaluating the proposed method.

- **Meaningful inference speed gains with detailed latency breakdown (Table 2, Section 4.3):** FASTerVLA achieves 112ms on single-arm settings (vs. 176ms for π₀ and 197–556ms for π₀-FAST), with the BAR module reducing forward passes from 21 to 3 on LIBERO. The latency analysis is usefully decomposed by component.

## Weaknesses

### Major

- **No variance or statistical significance reporting anywhere in the main results.** All results in Table 1, Figures 4, 7, 9, and 10 are reported as point estimates with no error bars, standard deviations, or confidence intervals. No mention is made of the number of random seeds, trials per task, or any measure of variance. In robotic manipulation, success rates can vary by 5–15% across runs due to stochasticity in object placement, policy noise, and hardware variation. Without this information, it is impossible for the reader to assess whether reported improvements (e.g., 97.9% vs. 97.1% on LIBERO, or 87.9% vs. 76.5% on Simpler-Bridge) are statistically reliable or within the noise floor. This does not invalidate the method, but it weakens every comparative claim in the paper.

### Minor

- **LIBERO benchmark near saturation limits discriminative value.** FASTerVLA achieves 97.9% on LIBERO while several baselines (π₀ at 94.2%, π₀₅ at 96.8%, OpenVLA-OFT at 97.1%) also cluster in the mid-to-high 90s. The 0.8% gap over OpenVLA-OFT on this near-saturated benchmark is not the strongest evidence of superiority; the paper's harder benchmarks (Simpler-Bridge: 87.9% vs. 76.5%; VLABench generalization) provide more meaningful comparisons.

- **No discussion of limitations or failure modes.** Section 5 (Conclusion) is entirely positive with no discussion of when the method might not work well, what its failure modes are, or the computational cost of tokenizer pretraining (data requirements, GPU-hours). Given the scope of the contribution, a limitations paragraph would substantially strengthen the paper.

- **Baseline initialization ambiguity.** The paper states baselines are "initialized from checkpoints pretrained on large-scale robotics data (e.g., from π₀-FAST)" (line 198). The "e.g." makes it unclear which specific checkpoint was used for each baseline, which matters for fairness and reproducibility since different baselines have different architectures and pretraining procedures.

- **VRR metric norm inconsistency.** Equation (4) defines VRR using the L1 norm (‖·‖₁), but the accompanying description (line 222) states "σ corresponds to the Euclidean distance error measured in meters" — Euclidean distance is the L2 norm, not L1. It is unclear which norm is actually used in the reported VRR figures.

- **Lightweight action expert underspecified.** The paper states it "shares the backbone architecture but with fewer parameters" but does not provide the parameter count, its size relative to the backbone, or whether it is trained jointly with or separately from the backbone.

### Trivial

None.

## Nice-to-Haves

- Move key ablation studies (patchifier design, BAR block size, codebook size effects) from the appendix into the main text, as these directly support the claimed contributions.
- Provide specific σ values used for the VRR metric in each figure that reports it, beyond the multiple-σ sweep in Figure 5.

## Novel Insights

None beyond the paper's own contributions. The central tension surfaced by the reviews is that the paper has a genuinely strong methodological contribution with unusually broad empirical validation, yet its reporting standards (no variance information, no limitations section) lag behind the ambition of the claims. This is a gap in presentation discipline, not in technical soundness.

## Suggestions

1. Report all main results with error bars or confidence intervals from multiple runs (at least 3 seeds) — this is the single highest-leverage improvement.
2. Clarify whether VRR uses L1 norm or Euclidean distance (L2) and ensure consistency between the formula and text description.
3. Add a limitations paragraph discussing failure modes, settings where the method may struggle, and tokenizer pretraining cost.
4. Specify the action expert's parameter count and training protocol.
5. Clarify baseline initialization by specifying which specific checkpoint was used for each baseline.
6. Move key ablation results from the appendix to the main text.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>