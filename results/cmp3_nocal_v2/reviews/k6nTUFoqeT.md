## Summary

This paper proposes FASTer, a framework for autoregressive Vision-Language-Action (VLA) models composed of two parts: FASTerVQ (a neural action tokenizer using action patchification, RVQ, and frequency-domain losses) and FASTerVLA (a policy using block-wise autoregressive decoding with a lightweight action expert). The central claim is that tokenizer quality is the primary bottleneck in autoregressive VLAs, and that a carefully designed VQ tokenizer combined with block-wise decoding can simultaneously improve task performance and inference speed. The paper backs this claim with extensive experiments across multiple embodiments, backbones, and benchmarks, achieving SOTA results (97.9% on LIBERO, 87.9% on Simpler-Bridge).

## Strengths

- **Well-motivated design rationale for action patchification (Section 3.1).** The paper correctly identifies that action dimensions carry heterogeneous distributions (binary gripper vs. continuous joints), motivating non-uniform grouping along action dimensions while grouping uniformly along time. This is not borrowed generically from image patchification; it exploits a property specific to robot action data.

- **Broad and systematic evaluation across embodiments and backbones (Table 1, Figures 4, 7, 8, 9, 10).** The evaluation covers LIBERO, VLABench, Simpler-Bridge, GalaxeaManisim, xArm, R1Lite (bimanual & whole-body), WidowX, and Franka — spanning single-arm, bimanual, and whole-body control in both simulation and on real hardware. The cross-backbone experiment (Figure 7) is particularly informative: InternVL3.5-2B goes from 79.35% (FAST) to 96.30% (FASTer w/o BAR), directly supporting the claim that tokenizer quality is the bottleneck.

- **The VRR metric (Section 4.2, Eq. 4) is a useful evaluation tool for action tokenizers.** By thresholding reconstruction error rather than using raw L2 loss, VRR focuses on task-relevant fidelity and shows clear differentiation across methods (Figure 5). This is a genuinely helpful contribution for the community.

- **Consistent SOTA results on established benchmarks (Table 1).** FASTer achieves 97.9% on LIBERO, outperforming both diffusion-based (π₀ at 94.2%, π₀.5 at 96.8%) and autoregressive (π₀-FAST-D at 94.2%) baselines. The gains on Simpler-Bridge (87.9% vs. 76.5%) are even larger.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Undiscussed training-inference discrepancy in Block-wise Autoregression (Section 3.2).** During training, teacher forcing and the block-wise causal mask (Figure 3c) allow tokens within a block to condition on ground-truth intra-block tokens. During inference, the ⟨BoBlk⟩ token is replicated B times and all B tokens in the block are generated simultaneously — the model cannot condition on real intra-block content because it hasn't been generated yet. This is a known discrepancy in multi-token prediction, and the paper neither acknowledges it nor provides evidence (e.g., comparing BAR with per-token decoding under the same training) that it is harmless. Given that the ablation (Figure 7) shows BAR provides only a small increment over the tokenizer swap alone, this does not threaten the paper's core contribution, but the silence on an acknowledged architectural issue is a clear gap.

- **The VRR metric aggregates heterogeneous physical quantities without normalization (Section 4.2, Eq. 4).** The paper states that σ corresponds to meters for translation and radians for rotation/joint positions, but the L1 norm in Eq. 4 sums all action components together — directly adding quantities in different units. The paper does not specify whether components are normalized or reweighted before the L1 sum. Additionally, the paper states "a reconstruction error on the order of 10⁻² is sufficient to cause a noticeable degradation" without justifying whether this applies to meters (1cm), radians (~0.57°), or some mixture. While this does not invalidate relative comparisons (same metric for all methods), it weakens absolute claims about reconstruction quality.

- **"Near-lossless" framing overstates what the VRR metric demonstrates (Abstract, Section 4.2).** The abstract claims "near-lossless reconstruction" and Section 4.2 states FASTerVQ-XL achieves "nearly lossless action-chunk reconstruction at σ = 10⁻³." However, VRR at a single tolerance threshold measures the fraction of actions falling within that threshold — it does not establish that reconstructions are functionally indistinguishable from originals across the full signal. "High-fidelity reconstruction within task-relevant tolerances" would be more precise and would avoid inviting unnecessary scrutiny.

- **The lightweight action expert is described only at a conceptual level (Section 3.2).** The paper states it "shares the backbone architecture but with fewer parameters" and is inspired by π₀, but gives no specifics: parameter count (relative to backbone), architecture (number of layers, cross-attention or shared hidden states to access backbone features), or training procedure (joint training or frozen backbone). This information is necessary to assess whether the action expert or the tokenizer drives the performance gain, and to reproduce the method.

- **The action patchifier introduces padding overhead that is not quantified (Section 3.1).** The paper groups action dimensions non-uniformly and pads each group to the largest group size d. This padding increases the token count, partially offsetting the advertised compression benefit. For typical configurations (e.g., a 7-DoF arm with binary gripper), the fraction of padding tokens is not reported, making the effective compression ratio unverifiable from the main text.

- **The inference speed advantage is limited on whole-body control (Table 2, Section 4.3).** The paper frames "up to 3× reduction compared to π₀," but this holds on LIBERO (112ms vs. 176ms). On WBC, FASTerVLA and π₀ converge to ~230ms, and FASTerVLA requires 12 BAR forward passes. The paper acknowledges this but the framing could be clearer about which settings enjoy the speed advantage — the primary benefit is against the autoregressive π₀-FAST (which takes 1,100–3,000ms on WBC).

### Trivial

- **Concrete tokenization parameters (m, n, h, d) are not provided for any evaluated embodiment**, making the actual token count per action chunk unverifiable from the main text. A table with these values for each setting (e.g., LIBERO, WBC) would let readers assess compression ratios directly.

## Nice-to-Haves

- **Ablation of spacing augmentation** (described in one sentence in Section 3.2 without analysis). This is a non-standard technique whose effect on performance could be reported.
- **Data budget comparison** for tokenizer training (the paper states FASTerVQ is trained on less data than baselines but does not give explicit quantities).
- **Discussion of failure cases or settings** where FASTer underperforms (e.g., the "marginal gap to π₀ on VLABench" mentioned in Section 4.3).

## Removed Points

These points were raised in the input review but are removed under the filtering rules, so treat them with caution:

- **InternVL3.5-2B FAST baseline tuning (Figure 7).** The reviewer questioned whether the 79.35% result for InternVL3.5-2B with FAST was due to hyperparameter mismatch. This is speculative — the paper reports the numbers as-is, and there is no evidence of improper tuning. [Removed: speculative criticism]
- **Cross-backbone gains might be exaggerated.** Same speculation about baseline tuning. [Removed: same reason]
- **Parker et al. (2025) reference details.** The reviewer requested more information about what is adopted from audio codecs vs. novel. This is a question, not a weakness, and the paper already describes the architectural inspiration. [Removed: not a weakness]

## Novel Insights

None beyond the paper's own contributions. The cross-backbone results (Figure 7) are the strongest evidence in the paper for the claim that tokenizer quality is the bottleneck, but this is already the paper's central thesis.

## Suggestions

1. Add an explicit discussion of the BAR training-inference discrepancy, ideally with a diagnostic experiment comparing BAR against per-token decoding at inference time under the same training procedure.
2. Clarify whether VRR normalizes action components before computing the L1 norm, or provide a reweighted variant.
3. Replace "near-lossless" with "high-fidelity reconstruction within task-relevant tolerances."
4. Provide a table with concrete tokenization parameters (m, n, h, d, token counts, padding fraction) for each evaluated embodiment.
5. Describe the action expert architecture with sufficient detail (parameter count, cross-attention or other mechanism, training procedure) to enable reproduction.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>