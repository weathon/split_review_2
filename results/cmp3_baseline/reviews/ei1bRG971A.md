## Summary

The paper introduces Dynamic Nested Depth (DND), a post-training method that improves LLM performance by selecting critical tokens via a learned router and reprocessing them through the same transformer layer (nested depth). A router controlling loss and an adaptive threshold control scheme are designed to ensure stable and discriminative token selection. Experiments on dense models (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and a MoE model (Qwen3-30B-A3B) show average gains of 0.87–2.61% across diverse benchmarks with a small parameter increase (<0.1M) and roughly 6% extra FLOPs.

## Strengths

- **Well-motivated and clearly presented idea.** The paper builds on the observation that token difficulty varies and that additional computation should be allocated to hard tokens. The DND framework (router → nested pass → normalized fusion) is logically structured and easy to follow.
- **Carefully engineered training strategies.** The router controlling loss (score dispersion + distribution preservation) and the threshold control scheme (buffer proportional control + EMA synchronization) are thoughtfully designed to address the challenges of token-choice routing. Ablations confirm that both components contribute to performance and stability.
- **Comprehensive evaluation across multiple models and tasks.** Experiments cover three small dense models and a 30B MoE model, with benchmarks spanning general knowledge, math/STEM, and coding/agent tasks. The scaling evaluation on Qwen3-30B-A3B is particularly valuable.
- **Insightful analysis of token selection behavior.** The correlation between selection frequency and logit entropy (Fig. 4a), the reduction in entropy after DND (Fig. 4b), and the layer-wise selection patterns (Fig. 7a) provide strong evidence that the router is identifying genuinely difficult tokens and that the nested pass reduces uncertainty.

## Weaknesses

### Major

- **Modest performance gains relative to computational overhead.** The average improvements are 0.87% (30B MoE) and 1.88–2.61% (1B dense). While consistent, these gains are small. The paper claims “substantial accuracy improvements,” but a 0.87% average gain on a 30B model is modest. The 6% extra FLOPs and 7–8% throughput reduction (Table 3) represent a non-trivial cost. The paper does not provide a cost-benefit analysis (e.g., whether the same compute budget spent on more SFT data or longer training would yield larger gains).
- **Limited comparison to alternative post-training methods.** The only direct baseline is ITT (Chen et al., 2025), shown on one model. Other relevant approaches—such as early exit with additional layers, adaptive depth methods, or simply fine-tuning with more data—are not compared. The paper also mentions MOR (Bae et al., 2025) but dismisses it as requiring pretraining from scratch, which is fair, but other token-level adaptive computation methods exist (e.g., conditional computation, dynamic depth networks) that could serve as baselines.
- **The “post-training” framing is slightly misleading.** DND is integrated during full-scale SFT with all parameters trainable, not applied after training is complete. This is fine-tuning, not post-training in the strict sense. The paper should clarify that DND requires a fine-tuning stage and is not a plug-and-play inference-only modification.

### Minor

- **The router controlling loss uses a sigmoid activation, but the loss terms are applied to the sigmoid outputs (p^i).** The distribution preservation loss (L_dp) pulls scores toward 0.5, which is reasonable. However, the score dispersion loss (L_sd) normalizes scores to sum to 1 within a sequence, which may interact oddly with the sigmoid—scores are already bounded in (0,1). The paper could discuss why this normalization is needed and whether it causes unintended biases.
- **The threshold control scheme uses a buffer of recent samples, but the buffer size is not specified.** The EMA synchronization period (every 50 steps) is given, but the buffer length N_b is not. This affects reproducibility.
- **The paper states “minimal computing increase” but later reports 6% extra FLOPs and 7–8% slower throughput.** These numbers are not minimal; they are moderate. The phrasing should be adjusted.

### Trivial

- Figure 4a and 4b have duplicated axis labels and redundant text in the captions.
- Some hyperparameters (e.g., λ_sd, λ_dp, α, γ) are not reported in the main text; they are presumably in the appendix, but the paper should at least mention that they are provided.

## Nice-to-Haves

- A comparison to simply training the base model for more steps or with more data (same compute budget) would help isolate the benefit of DND from the benefit of additional SFT.
- An analysis of how the selection ratio varies across different types of tokens (e.g., nouns vs. verbs vs. punctuation) would strengthen the qualitative claims in Fig. 7b.
- A discussion of failure cases or tasks where DND does not improve (if any) would add depth.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that token-level uncertainty (measured by logit entropy) correlates with the need for additional computation, and that a nested pass through the same layer can reduce that uncertainty. The observation that selection frequency is higher in middle layers and that deeper layers focus on more abstract tokens (Fig. 7b) suggests a hierarchical processing strategy that could inspire future work on layer-specific adaptive computation.

## Suggestions

- Provide a clearer cost-benefit analysis: compare the performance gain of DND to the gain from spending the same extra FLOPs on additional SFT steps or a larger model.
- Include at least one more baseline, such as a simple “repeat hard tokens” heuristic or a dynamic depth method that does not require training from scratch.
- Report the buffer size N_b and the hyperparameters λ_sd, λ_dp, α, γ in the main text or a table.

## Score and Decision

The paper presents a well-engineered method with careful training strategies and thorough analysis. However, the performance gains are modest, the computational overhead is non-trivial, and the comparison to alternatives is limited. The contribution is solid but incremental. I lean toward borderline reject.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>