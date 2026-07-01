Now let me write the final consolidated review.

## Summary

This paper introduces Dynamic Nested Depth (DND), a post-training method that enhances LLMs by selectively routing ~20% of tokens through an additional transformer layer pass. DND uses a learned linear router with a training strategy combining score dispersion loss, distribution preservation loss, and EMA-synchronized adaptive threshold control. The method is evaluated on three 1B-class dense models (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and one 30B MoE model (Qwen3-30B-A3B), showing consistent average improvements of +1.88%, +2.61%, +2.50%, and +0.87% respectively with ~6% extra FLOPs and 91.6-93.1% of vanilla throughput.

## Strengths

1. **Well-motivated architecture design.** The paper makes a clear case for why selective *deepening* (allocating extra computation to hard tokens) is the natural extension of token-level adaptive computation beyond pruning or uniform processing (Sec. 1, Fig. 1). The distinction from prior work (which either discards tokens or applies computation uniformly) is well articulated.

2. **Comprehensive ablation study.** Table 4 systematically ablates the router controlling loss, threshold control (BPC + EMA), selection ratio (10/20/30%), and layer ranges. The ablations convincingly show that both the router loss and threshold control contribute meaningfully, with the combination yielding the best results. This provides strong empirical support for the design choices.

3. **Token selection analysis provides genuine insight.** Figures 4a and 4b demonstrate that the router preferentially selects tokens with higher logit entropy (greater model uncertainty), and that after nested processing, entropy decreases. This directly validates the paper's stated motivation and shows the method is doing what it claims. Figures 5 and 6 further demonstrate that the threshold control mechanism stabilizes selection during training.

4. **Cross-model validation on diverse architectures.** The method is evaluated on three dense 1B-class models (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and one 30B MoE model (Qwen3-30B-A3B), showing consistent improvements across all without any performance degradation on individual benchmarks. This demonstrates generalizability across model families and scales.

## Weaknesses

### Fatal
None.

### Major

1. **Limited experimental baselines.** The paper compares experimentally against only one method — ITT (Chen et al., 2025) — on a single model (Qwen3-1.7B), where ITT shows a negligible +0.05 improvement. The most closely related work, MOR (Bae et al., 2025), shares the goal of "dynamically increased computational depth" and is discussed at length in Sec. 2.2, but receives no experimental comparison. While the paper correctly notes that MOR requires pre-training from scratch, the central claim that DND's routing control is superior would be strengthened by: (a) adapting MOR's z-loss mechanism as a post-training control, (b) comparing against a simple uniform-depth baseline (e.g., adding an extra layer to all tokens at comparable FLOPs), or (c) comparing against token-pruning methods (the natural alternative of removing easy tokens and reallocating compute). The paper's empirical evidence for the superiority of DND's selection strategy rests on a single weak baseline.

2. **No variance or statistical significance reported.** Every result in Tables 1, 2, and 4 is reported as a single point estimate with no variance, confidence intervals, or significance tests. For the MoE model (Table 2), many individual benchmark gains are small: MMLU (+0.50), CMMLU (+0.37), BBH (+0.13), DROP (+0.27), MATH (+0.15), MATH-500 (+0.20). The overall average claim of +0.87% aggregates these small-to-moderate improvements. Without variance information, the reader cannot assess whether these individual gains reflect genuine improvement or evaluation noise — especially for benchmarks like BBH and GPQA known to have non-trivial variance under few-shot settings. This weakens the support for the paper's quantitative claims.

### Minor

1. **Unanalyzed nested attention mechanism.** The paper adopts token-choice routing to avoid information leakage in the *routing decision* (Sec. 3.1.1), but does not clarify the attention mechanism inside the nested pass. Selected tokens are packed into a compact subsequence with "new positional embeddings" (Eq. 3, line 98), but the paper does not specify: (a) what these positional embeddings are (original absolute positions vs. sequential 0,1,2...), (b) whether causal masking is applied to the compact sequence, or (c) how this interacts with auto-regressive decoding. If the packed sequence uses sequential positions and standard causal attention, a token from original position i could attend to a token from original position j > i within the nested pass — a form of information flow not possible in standard auto-regressive decoding. The method clearly works empirically, but this aspect of the architecture is underspecified.

2. **Router loss components not ablated individually.** Table 4 combines the Score Dispersion Loss (L_sd) and Distribution Preservation Loss (L_dp) into a single "RC" (Router Control) condition without testing them individually. Since these two losses have competing objectives (pushing scores apart vs. pulling them toward 0.5), their independent contributions and the sensitivity to the weighting hyperparameters (λ_sd / λ_dp) are not assessed.

3. **Training data description is vague.** The SFT dataset is described as "1-2 million instances curated from human annotations and open-source materials" with "a significant volume of synthetic material" (Sec. 4.2). The synthetic-to-real ratio, specific open-source datasets used, and filtering criteria are not specified, which limits reproducibility.

4. **Framing of some results is slightly overstated.** The +0.87% average gain on the MoE model is described as "substantial" in the conclusion — this is not consistent with typical usage for LLM improvements at this scale where sub-1% gains are generally considered modest. The entropy correlation (r=0.3359, Fig. 4a) is interpreted as showing tokens with higher entropy "are frequently selected," but r² ≈ 0.11 indicates that uncertainty explains only about 11% of the variance in selection frequency.

### Trivial
None.

## Nice-to-Haves

- A compute-matched baseline: what would the same ~6% FLOPs increase buy if allocated to uniform model deepening or slightly larger hidden dimensions? This would directly contextualize whether DND's targeted allocation is more efficient than uniform alternatives.
- Clarify whether the "same computation cost" claim for the ITT comparison (Sec. 4.3) refers to same number of selected tokens, same FLOPs budget, or same throughput.
- Individual ablation of λ_sd and λ_dp sensitivity.

## Removed Points

These points were raised in the input review but are removed under the filtering guidelines:

- **Criticism about missing appendix content:** The paper states hyperparameters and training details are in Appendix Sec. B. Appendix sections are stripped by the PDF parser; cannot verify they are missing from the submission.
- **Criticism about code/model release:** Not a requirement for ICLR review; irreproducibility via missing code release is not evaluated as a paper weakness.
- **Speculative throughput concerns at larger batch sizes:** The paper already reports throughput using vLLM kernels. The claim that packing/unpacking causes irregular memory access that would degrade at scale is speculation without evidence.
- **"Performance predictably increases" phrasing (line 13):** Minor framing nitpick about a single sentence in the introduction that does not affect the paper's contribution.
- **MOR "limited to 1B-parameter" characterization:** The paper refers to the scale MOR was demonstrated at (1B), which is factually correct; the critic's interpretation as an "architectural limitation" reads into the text more than it says.
- **The +1.01 gain from the simple z-loss-like method is "actually quite reasonable":** A difference in framing emphasis, not a factual error in the paper's reporting.
- **"Scales" is overstated when only tested on one 30B model:** The paper evaluates on one 30B model, but "scales" is commonly used in the field to mean "works at this size"; this is a minor word choice preference.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add at least 2-3 baselines: (a) a uniform-depth extension baseline (add an extra layer to all tokens at comparable FLOPs), (b) a post-training adaptation of MOR's z-loss-based routing control, and (c) a token-pruning baseline that removes easy tokens.
2. Report variance across multiple evaluation seeds or provide confidence intervals, especially for the MoE results where many gains are under 0.5 points.
3. Clarify the nested pass attention mechanism: specify whether causal masking is applied to the compact subsequence and what positional embeddings are used.
4. Ablate the two router loss components (L_sd and L_dp) individually and report sensitivity to λ_sd / λ_dp.
5. Provide more specific details about training data composition in the main text.

## Score and Decision

**Anchors used for calibration:**

| Path | Score | Round | Comparison |
|---|---|---|---|
| Stutter makes LLMs smarter (UvYrFbKj8j) | 4.50 | R1 | Very similar topic (selective additional layers for challenging tokens) but weaker evaluation — only Pythia models, inconsistent gains, no efficiency analysis. DND is stronger on all dimensions. |
| LazyLLM Dynamic Token Pruning (am5Z8dXoaV) | 5.00 | R1/R2 | Token pruning for efficiency; different goal (speed vs quality), comparable evaluation breadth. |
| Learning How Hard to Think (6qUUgw9bAZ) | 6.50 | R1/R2 | Adaptive compute allocation. Stronger theoretical framing and baselines, but narrower scope (decoding-level rather than architecture-level). |
| CoTFormer (7igPXQFupX) | 5.75 | R2 | Adaptive computation via chain-of-thought driven architecture. Comparable contribution level but different methodology. |
| γ-MoD (q44uq3tc2D) | 6.67 | R2 | MoD adaptation for MLLMs with cleaner efficiency-accuracy tradeoff analysis. |
| FiRST Router-Selective Transformers (ulGwcj1egv) | 3.00 | R2 | Layer skipping for latency reduction; less relevant topic, weaker paper. |
| FlexPrefill (OfjIlbelrT) | 8.00 | R2 | Sparse attention for efficiency; stronger baselines and cleaner evaluation. Above DND in overall quality. |

**Initial bracket:** 5.5 – 7.0. DND is clearly stronger than Stutter (4.50) and comparable to the 5.75–6.67 range. The main gap relative to higher-scoring papers is the limited baseline comparison.

**Final score:** 6.0. The paper has a well-motivated idea, consistent empirical support across multiple architectures, thorough ablations, and insightful analysis of token selection behavior. The main weakness is the limited experimental baselines — only ITT is compared — which prevents stronger conclusions about DND's superiority over alternative approaches. The lack of variance reporting for the MoE model's small individual gains further tempers the quantitative claims. These are addressable weaknesses that do not invalidate the core contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>