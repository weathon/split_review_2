Now I have all the information I need. Let me produce the final review.

## Summary

DND proposes a post-training method that retrofits existing transformer LLMs with lightweight linear routers at each layer. During a forward pass, the router identifies "critical" tokens (those the model is uncertain about) and routes them through an additional nested pass of the same transformer layer, selectively deepening computation for difficult tokens while leaving easy tokens unchanged. The paper introduces two training strategies—a dual-objective router loss for score discriminability and an adaptive threshold control scheme—to stabilize the token selection mechanism. Experiments on three small dense models (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and one large MoE model (Qwen3-30B-A3B) show consistent gains across 11–17 benchmarks each, with a minimal parameter increase (<0.1M) and throughput retention of 91.6–93.1%.

## Strengths

- **Consistent improvements across all tested models with no degradation on any benchmark.** Tables 1 and 2 show DND improves average scores on Qwen3-1.7B (+1.88%), Llama3.2-1B (+2.61%), Gemma3-1B (+2.50%), and Qwen3-30B-A3B (+0.87%) across 28 total benchmarks. Every single individual metric improves or stays flat — no regressions — which is an unusually clean result for a post-training method.

- **Mechanistic validation that the router targets genuinely uncertain tokens and reduces that uncertainty.** Section 4.5 (Figs. 4a and 4b) provides correlational evidence: (a) token selection frequency positively correlates with vanilla logit entropy (Pearson r = 0.336), confirming the router preferentially selects tokens the model is uncertain about; (b) after DND reprocessing, logit entropy drops, with higher-selection-frequency tokens showing larger reductions (r = −0.581). This validates the causal chain — select uncertain tokens → reduce uncertainty — rather than reporting only aggregate accuracy numbers.

- **Controlled comparison against the most related prior method (ITT) under the same compute budget.** In Table 1, DND (+1.88% average) substantially outperforms ITT (+0.05% average) on Qwen3-1.7B. The paper identifies the likely reason (Top-P selection causes training-inference mismatch for auto-regressive models), strengthening the claim that DND's token-choice routing design is a genuine advance, not just a generic benefit of adding compute.

- **Thorough ablation study isolating each design component.** Table 4 ablates the router controlling loss, threshold control, selection ratio (10%/20%/30%), and layer range. Both router control and threshold control are individually modest (~+1.0% each), but their combination yields +1.88%, providing clean evidence that both are necessary.

- **Practical throughput measurements under realistic inference conditions.** Table 3 reports tokens/sec on a single H100 GPU (vLLM, BF16) across four input/decode length combinations, showing DND maintains 91.6–93.1% of vanilla speed — a concrete efficiency claim for practitioners.

- **Qualitative analysis revealing a hierarchical selection pattern.** Fig. 7b shows shallower layers primarily select nouns (key entities), while deeper layers select mathematical expressions and verbs (relational/logical operations), providing interpretable evidence of multi-level processing.

- **Parameter efficiency is demonstrated convincingly.** Only ~0.03M parameters added for the 30B MoE model, and the method requires no pretraining from scratch — it works via post-training on existing models.

## Weaknesses

### Fatal
None.

### Major

- **Training compute is not controlled between DND and the SFT baseline.** DND's nested pass adds extra forward (and backward) compute during training: for each selected token at each DND layer (~20% of tokens across ~20 layers), there is an additional full layer-pass. The paper states both DND and the baseline undergo "standard full-scale supervised fine-tuning" with "all parameters set as trainable and the same learning rate applied" (Sec. 4.2), but does not specify whether the same number of training steps was used. If steps are matched, DND receives substantially more training FLOPs (roughly 4 extra layer-passes per token), meaning the observed gains could partly reflect additional training budget rather than the architectural innovation. The ITT comparison is noted as "under the same computation cost," but the primary SFT baseline is not similarly qualified. This issue is addressable (a clarification or a compute-matched ablation), but as presented it undermines clean interpretation of the reported improvements.

### Minor

- **The ITT comparison lacks diagnostic evidence for why it underperforms.** The paper attributes ITT's near-zero improvement (+0.05) to "Top-P-based selection causing training-inference mismatch" but provides no direct analysis to support this claim (e.g., actual selection ratios during ITT training vs. inference, attention pattern analysis, or oracle studies). While the comparison is useful, the explanation is asserted without experimental backing.

- **The paper does not address the edge case of zero tokens exceeding the threshold at a DND layer.** Since selection is per-token via threshold comparison (Eq. 2), it is theoretically possible for all tokens to have p^i ≤ τ at some layer. The paper does not specify how this case is handled during training or inference (is the nested pass simply skipped?).

- **No discussion of positional embedding reassignment effects in the nested pass.** Eq. (3) shows selected tokens receive new positional embeddings when packed into the compact sequence. This means the attention pattern in the nested pass differs substantially from the vanilla pass. The paper does not analyze whether this effect is intentional, how it influences attention, or whether alternatives were considered.

- **The "no degradation on any benchmark" pattern across ~28 benchmarks is unusual.** Even well-motivated methods typically hurt somewhere. The paper offers a post-hoc hypothesis ("DND filters extraneous noise") but does not empirically test this claim.

- **The correlation between selection frequency and vanilla logit entropy is weak (r = 0.336, ~11% variance explained).** The paper describes this as validating the router's behavior, which overstates the strength of the evidence. The negative correlation with entropy reduction (r = −0.581) is more convincing.

- **Router parameter count is asserted as <0.1M without showing the calculation.** The paper could make this concrete by providing per-model arithmetic (e.g., for Qwen3-30B-A3B with d_model ≈ 7168 and ~20 layers, the router adds ~20 × 7168 ≈ 143K parameters).

### Trivial
None.

## Nice-to-Haves

- A compute-matched experiment (vanilla SFT trained for proportionally more steps to equalize total FLOPs) would directly address the major concern and would substantially strengthen the paper's central claim.
- Reporting evaluation variance across seeds or multiple evaluation runs would strengthen confidence, particularly for the smallest gains (e.g., +0.13 on BBH, +0.15 on MATH).
- A brief discussion of how selection rates vary across layers during inference and what happens at extreme selection ratios would aid practical reproducibility.

## Removed Points

These points were raised by one or both reviewers but are removed after verification against the paper:

1. **Gradient flow through the binary selection mask (Harsh Critic, "structural" issue):** REMOVED. The critic claimed the paper does not explain how gradients flow through the binary mask. This is incorrect. The fusion design (Eq. 4) uses the *continuous* routing score p^i as a mixing weight: x^i = (β·p^i)·x_d^i + (1−β·p^i)·x_v^i for selected tokens. Gradients flow to the router R through p^i in this fusion weight, and to the transformer weights through x_d^i (the nested pass output). The binary mask is used only for Pack/Unpack indexing, which is differentiable with respect to the source tensor in standard frameworks. The paper's architecture is sound on this point.

2. **Table 4 formatting ambiguity (Harsh Critic):** REMOVED. The claimed ambiguity (TC column apparently marked "–") is a parser/formatting artifact; the table is interpretable as-is.

3. **Statistical significance / confidence intervals (Harsh Critic):** MOVED to Nice-to-Have. Single-run evaluation on large-scale benchmarks is standard in this community; requesting confidence intervals across runs is not a standard expectation for this type of work.

4. **"Could the metric be measuring a proxy?" / area-of-concern speculation (Harsh Critic general sweep):** REMOVED. The critic's sweeping area-based concerns (confounders, metric validity) lack specific anchors in the paper and are not supported by the evidence presented.

5. **Generic strengths (Strength Finder):** REMOVED. Strengths like "addresses an important problem" or "targets an interesting question" are removed as generic/superficial.

6. **Missing appendix / references (both reviewers):** REMOVED per hard rules — the parser strips these sections from all papers; they exist in the original submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify the training-step setup: state whether DND and the SFT baseline used the same number of training steps. If so, provide a compute-matched ablation experiment where the baseline is trained for proportionally more steps to match total FLOPs. At minimum, explicitly acknowledge and bound the FLOPs gap.

2. Provide a brief diagnostic for the ITT comparison (e.g., report actual selection ratios during ITT training vs. inference, or show an entropy/attention analysis for ITT similar to Fig. 4 for DND) to substantiate the claimed training-inference mismatch.

3. Explicitly state how the case of zero selected tokens at a layer is handled during training and inference.

4. Discuss the positional embedding reassignment in the nested pass — is the effect on attention patterns intentional, and was it studied empirically?

5. Show the router parameter count calculation for each model size to make the "<0.1M" claim concrete.

**Calibration rationale:** The calibration_search tool was unavailable due to infrastructure issues. Based on my analysis of the paper and knowledge of typical ICLR score distributions, this paper sits between Accept (6) and Accept (8). It has a clear, well-motivated contribution, unusually consistent empirical results with mechanistic validation, and practical efficiency measurements. The main weakness is the unresolved training-compute control issue, which is significant but addressable (a clarification could resolve it). At ICLR, papers with this level of contribution, breadth of evaluation, and mechanistic depth typically score in the 6–8 range. I assign a score of 7.0.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>