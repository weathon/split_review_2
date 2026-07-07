## Summary
The paper proposes a joint Pixel-Token (P-T) compression strategy for Video Large Language Models. Pixel-level compression iteratively compares consecutive frames via L1 pixel distance and drops frames below a similarity threshold. Token-level compression uses cosine similarity between corresponding token positions across frames (and intra-frame pairwise similarity for the anchor frame) to prune redundant tokens with a dynamic pruning ratio. The method is evaluated on MVBench, VideoMME, and NextQA under both training-free and fine-tuning settings using LLaVA-Video and Qwen2.5-VL as backbones.

---

## Strengths
- **Practical plug-and-play design**: The method integrates into existing VLLMs without architectural changes, making it broadly applicable. Experiments on two diverse baselines (LLaVA-Video, Qwen2.5-VL) confirm generalizability.
- **Comprehensive ablation**: Sections 4.3.1–4.3.3 systematically ablate compression strategy, ratio, and similarity measure, providing useful empirical guidance for practitioners on threshold and ratio selection.
- **Consistent training-free gains over DyCoke**: Table 1 shows that pixel-token (75%) outperforms DyCoke (77%) on all three benchmarks under LLaVA-OV 7B, providing a clear head-to-head comparison against the closest baseline.

---

## Weaknesses

### Fatal
None.

### Major
1. **Pixel-level compression is a very basic heuristic with no semantic grounding.** Using raw L1 pixel differences to decide frame importance is a decades-old technique (pre-deep-learning video processing). It is sensitive to global illumination changes and camera motion without reflecting semantic content variation. There is no justification for why this should be preferred over learned or feature-level alternatives, nor any analysis of failure cases (e.g., fast camera pans discarding semantically similar but important content, or slow-motion scenes with nearly identical pixels but critical semantic change).

2. **The joint method does not consistently outperform its individual components.** In Table 2 (training-based, the paper's main contribution setting), joint Pixel-Token (75%) scores 63.9% on MVBench/LLaVA-Video — lower than Pixel alone (64.5%) and Token alone (64.0%). Under Qwen2.5-VL, joint (75%) scores 68.3% vs. Token alone (69.0%). The paper's claim that "joint compression is superior" is only supported by Table 3 (training-free, single benchmark), while the broader training-based results contradict it. This inconsistency is not discussed.

3. **No computational efficiency measurements are reported.** The paper's primary motivation is reducing computational cost, yet there are no FLOPs, latency, throughput, or GPU memory measurements anywhere. Without these, it is impossible to assess whether the approach actually delivers the promised efficiency gains in practice. DyCoke, the main comparison, reports concrete speed numbers; this paper does not.

4. **The gains are marginal and sometimes within noise.** Most improvements are 0.4–1.7%. Some "improvements" from compression over the full 64-frame baseline (e.g., Table 1 pixel-level on NextQA: 82.5 vs 81.5) suggest the baseline may be over-sampling rather than the method actively preserving useful content. No statistical significance is reported.

### Minor
1. **Inconsistency between abstract and results.** The abstract highlights "0.9% gain on MVBench" from the joint method. In the tables, this appears to correspond to the Qwen2.5-VL τ=0.5 configuration in Table 1 (68.1 vs 67.2), but that row is labeled "τ=0.5 (50%–70%)" not "Pixel-Token joint." The exact configuration being referenced is ambiguous.

2. **The dynamic pruning ratio is under-explained.** Equation (2) says tokens with sim < τ are retained and ρ ∈ [ρ_min, ρ_max], but it is unclear how the dynamic ρ is actually computed. Is it simply clipping the empirical ratio? The mechanism for "dynamic" adjustment is never explicitly stated as an algorithm.

3. **Anchor frame selection is fixed (always first frame of window).** No justification is provided for why the first frame of each window is necessarily the best anchor, and no ablation is done on anchor selection strategy.

### Trivial
- Table 3's caption says "MVBench" but does not specify training-free vs. training-based context (it is training-free per Section 4.3).

---

## Nice-to-Haves
- Report wall-clock inference speedups and GPU memory reduction alongside accuracy, which is essential for an efficiency paper.
- Include failure-case analysis for pixel-level compression (fast camera motion, scene cuts, fade transitions).
- Provide a proper mechanism for dynamic pruning ratio computation (pseudocode or formula).

---

## Novel Insights
The combination of coarse pixel-difference frame gating with fine-grained inter-frame token cosine-similarity pruning as a unified pipeline is a reasonable engineering contribution. However, neither component is technically novel on its own, and the joint design does not consistently demonstrate synergy beyond either component alone. The observation that 50–75% of video tokens can be removed with minimal or no loss is consistent with and not materially beyond existing findings in the literature (FastV, DyCoke, LLaVA-PruMerge).

---

## Suggestions
- Add wall-clock latency and memory benchmarks to substantiate efficiency claims.
- Address the contradiction in training-based results where the joint method underperforms individual components; discuss when joint compression helps vs. hurts.
- Consider replacing raw pixel L1 with feature-space (e.g., CLIP embedding) frame similarity for the pixel-level stage, which would be more semantically grounded and potentially more robust.
- Clarify the dynamic pruning ratio mechanism with a concrete formula or algorithm.

---

## Score and Decision
The paper addresses a real, important problem and is easy to read. However, pixel-level compression is technically trivial, the joint method does not consistently outperform its parts, and no efficiency numbers (the core motivation) are reported. The empirical gains are marginal throughout. As an ICLR submission, the technical novelty and empirical rigor fall below the acceptance bar.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>