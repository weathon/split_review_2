Now I have all the information I need. Let me compile the final review.

## Summary

This paper proposes Augmented Intermediate Representations (AIR), a method for defending LLMs against indirect prompt injection attacks by injecting instruction hierarchy (IH) signals into every decoder layer (via small trainable embedding tables), rather than only at the input layer as prior work does. The core insight — that input-only IH signals degrade as they propagate through the decoder stack — is supported by cosine similarity analysis (Figure 3). Empirically, AIR achieves a 1.6× to 9.2× reduction in ASR against gradient-based attacks (GCG, Astra) compared to existing IH injection mechanisms (Delimiters, ISE), with <2% utility degradation across three model families (3B–8B) and two training methods (SFT, DPO).

## Strengths

- **Well-motivated and clean idea.** The paper identifies a genuine structural limitation of input-only IH injection and demonstrates it empirically via rising cosine similarity between privilege-level representations across layers (Figure 3). The proposed fix — adding small, trainable, layer-specific embedding tables (0.4M extra params for an 8B model, 0.005% increase) — is simple, principled, and incurs negligible overhead. The parallel to the evolution from input-level positional encodings to RoPE provides useful intuition.

- **Consistent and substantial improvements across diverse settings.** In Table 1, AIR achieves the lowest ASR among all IH injection mechanisms across three model families (Llama-3.2-3B, Qwen-2.5-7B, Llama-3.1-8B), two training procedures (SFT, DPO), and two gradient-based attacks (GCG, Astra). For GCG, the reduction relative to the next-best defense ranges from ~1.6× to ~9.2×. For Astra in the SFT setting, improvements are dramatic (e.g., 14.5% → 0.1% on Llama-3.2-3B). Utility degradation is consistently <2%.

- **Good evaluation breadth.** The paper evaluates across three model sizes, two training methods, two evaluation datasets (AlpacaFarm and SEP), and both static and optimization-based attacks. The inclusion of SEP as a complementary robustness benchmark and the loss curves in Figure 7 (with per-instance variance) provide useful fine-grained analysis beyond single ASR numbers.

## Weaknesses

### Fatal
None.

### Major

- **No variance reporting for the central ASR results.** Table 1 reports all ASR values as single point estimates with no standard deviations, confidence intervals, or information about how many independent attack runs were performed. For gradient-based attacks (GCG and Astra) involving random initialization of the adversarial prefix and stochastic optimization, run-to-run variance could be significant. The standard deviation shown in Figure 7 is across test instances, not across independent attack runs — these are different quantities. Without variance information, the reader cannot assess whether the observed differences (e.g., 4.1% vs. 38% for Llama-3.2-3B GCG SFT) are statistically stable. That said, the consistency of AIR's advantage across all configurations (3 models × 2 training methods × 2 attacks) provides some confidence that the pattern is real.

### Minor

- **No discussion of adaptive attacks.** AIR modifies the model architecture by adding layer-specific trainable embeddings. In the white-box setting assumed for gradient-based attacks, an adversary aware of AIR could potentially design an attack that accounts for the IH embeddings (e.g., by explicitly suppressing their effect in the loss function). The paper evaluates only against standard GCG and Astra, which were designed without knowledge of AIR's mechanism, and does not acknowledge this limitation or discuss whether adaptive attacks might reduce the advantage. This is a gap common in the defense literature but worth noting.

- **Uneven distribution of headline improvement.** The 1.6×–9.2× range is accurate, but the largest gains (9.2×) come from the smallest model (Llama-3.2-3B) with SFT (the weaker training method). For larger models with DPO, improvements are more modest (e.g., 4.0% → 2.8% for Llama-3.1-8B DPO GCG, ~1.4×). The paper does not discuss this pattern or offer a hypothesis for why AIR's relative advantage narrows. This does not invalidate the contribution but would benefit from explanation.

### Trivial
None.

## Nice-to-Haves

- Include variance information for ASR values (multiple independent attack runs with different random seeds) and significance tests — this would substantially increase confidence in the central empirical claims.
- Discuss adaptive attacks explicitly, even if only to argue why standard attacks are a reasonable proxy or to flag it as future work.
- Provide a hypothesis for why AIR's relative advantage shrinks with larger models and DPO training (e.g., do larger models already maintain better input-layer IH signal propagation?).
- Clarify in the Figure 3 analysis that for Delim, the IH signal is encoded via attention patterns around delimiter tokens, not in content token representations, so the high cosine similarity (~1.0) reflects a fundamentally different mechanism rather than signal loss.

## Removed Points

- **"Table 1 formatting and readability"** and similar presentation nitpicks: removed per instructions (formatting/style nitpicks).
- **"The parameter count is negligible but learning dynamics could differ"**: speculative alternative explanation without supporting evidence; removed per filtering discipline.
- **"SEP separation score formula property"**: a minor observation about the metric's definition, not a weakness of the paper; moved to nice-to-have.
- **"Adversarial training dataset compatibility confound"**: concerns about whether the adversarial dataset was constructed compatibly with all IH injection methods — the paper states "all models undergo the same training procedure" (Sec 5.2), so this criticism is not supported; removed.
- **"Delim cosine similarity interpretation"**: the reviewer notes this is a subtlety the paper addresses correctly; moved to nice-to-have for clarity.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report variance for the ASR values** in Table 1, ideally from 3–5 independent attack runs with different random seeds, and include standard deviations or ranges.
2. **Add a brief discussion of adaptive attacks** in a limitations paragraph in Section 7, acknowledging that evaluations against standard attacks may not capture worst-case adversarial scenarios.
3. **Discuss the pattern of diminishing returns** with larger models/DPO training — even a brief hypothesis would strengthen the paper's intellectual completeness.

---

## Calibration Report

**Anchors retrieved:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| sjWG7B8dvt.md (ISE paper) | 6.00 | Round 1 | Yes | Directly comparable prior work. The ISE paper had more severe weaknesses (clarity issues, methodology concerns). The current paper is cleaner, better-motivated, and achieves stronger results against its own baseline. |
| l3bUmPn6u5.md (PFT paper) | 4.25 | Round 1 | CUDA error | Prompt injection defense paper. Lower-scored; this paper is clearly stronger in idea clarity, evaluation breadth, and result quality. |
| 3MDmM0rMPQ.md (IPE paper) | 3.00 | Round 1 | Yes | Task-specific LLM safety. Much lower-scored due to unclear contributions and weak experiments; not directly comparable to this paper. |
| kUH1yPMAn7.md (Safety Layers) | 6.00 | Round 2 | No | About locating safety layers in LLMs. Topically related but different contribution. Similar score range. |
| eC4WlSZc4H.md (Robustness Over Time) | 6.75 | Round 2 | No | Longitudinal study of LLM robustness. Not directly comparable in methodology. |
| sULAwlAWc1.md (ArrAttack) | 7.00 | Round 2 | No | Attack paper on jailbreaking defended LLMs. Different scope (attack vs. defense). |

**Weighted item comparison:** The ISE paper (avg 6.0) had extreme negative weights (a -9.58 clarity/novelty item and -5.67 experiment clarity item) that dragged its score down. This paper's draft shows no such extreme negatives: the largest negative weight is -2.90 (adaptive attacks), while the strengths are strongly positive (+5.23, +4.93, +4.29). The net weighted balance is clearly positive. This paper is cleaner, better-motivated, and better-presented than the ISE anchor at 6.0, while having milder weaknesses. The round-1 bracket was [5.5, 7.5]; within this bracket, the comparison to the 6.0 ISE anchor and the strongly positive weighted-item profile support a score above 6.0. The absence of any fatal flaw and the consistency of the empirical pattern across all evaluated configurations bring it to 6.5.

## Score and Decision

**Score:** 6.5 — The paper makes a clear, well-motivated contribution with solid empirical support. The main weakness is the lack of variance reporting for the central ASR results, but the consistent pattern across all configurations mitigates this concern. The adaptive attacks limitation is notable but not fatal as the paper does not claim worst-case robustness. The paper is clearly above the acceptance threshold but not at the level of an 8 (accept) due to these methodological gaps.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>