## Summary
The paper proposes Dynamic Nested Depth (DND), a post-training method that improves off-the-shelf LLMs by selecting critical tokens via a token-choice router and reprocessing them through the same transformer layers (“nested depth”). The router is trained with a dual-objective loss (score dispersion and distribution preservation) and the selection threshold is dynamically controlled via buffer proportional feedback and EMA synchronization. DND is applied to Qwen3-1.7B, Llama3.2-1B, Gemma3-1B (dense) and Qwen3-30B-A3B (MoE), yielding average gains of 1.9%–2.6% and 0.87% respectively with negligible parameter (<0.1M) and compute overhead (≈7% speed reduction).

## Strengths
- **Clear and well-motivated idea**: The work extends token-level selection from pruning to extra recurrent computation, and makes it work as a plug-in for existing pre-trained models—a practical and timely contribution.
- **Carefully designed training strategy**: The router controlling loss (𝐿<sub>sd</sub> + 𝐿<sub>dp</sub>) and the threshold control scheme (buffer proportional control + EMA synchronization) are non-trivial components that address the instability of token-choice routing. Ablations confirm each component’s value.
- **Extensive empirical validation**: The method is tested on four different base models (1B–30B) across 17 benchmarks covering general knowledge, math/STEM, and coding/agent tasks. Improvements are consistent and sometimes sizable on reasoning-heavy tasks (e.g., +5.8 on GPQA for Qwen3-1.7B).
- **Low overhead**: The additional parameters are miniscule and the measured throughput (91.6%–93.1% of baseline) demonstrates practical efficiency.
- **Insightful analysis**: The paper correlates token selection frequency with logit entropy (uncertainty), shows that DND reduces entropy for selected tokens, and provides a qualitative visualization that suggests hierarchical processing (concrete nouns in early layers, abstract expressions in deep layers).

## Weaknesses
### Fatal
- None.

### Major
- **Lack of comprehensive baselines**: The only dynamic computation baseline is ITT, which is closely related but not state-of-the-art. Missing comparisons with other adaptive depth methods (e.g., Mixture-of-Depths, early-exit variants, or simply adding a fixed extra layer for a comparable compute budget) weaken the claim that DND’s specific design is uniquely beneficial.
- **Throughput and FLOPs analysis is limited**: The speed measurement uses batch size 1. Real inference serving often uses larger batches, where attention overhead may scale differently. Additionally, FLOPs overhead is reported only for the MoE model; the paper should also report it for dense models to fully support the “minimal computing increase” claim.
- **Training details insufficient for reproduction**: The SFT dataset is described only as “synthetic material built upon a high-quality seed set of 1–2 million instances.” Without a clearer description (or a pointer to an existing dataset), reproducibility is limited. It is also not explicitly stated whether the vanilla baseline receives exactly the same number of training steps and learning-rate schedule as the DND variant.
- **Undiscussed interaction with chain-of-thought / thinking mode**: Modern LLMs often use CoT reasoning, which already allocates more computation to hard tokens. The paper does not discuss whether DND provides additive benefits or becomes redundant in that setting.

### Minor
- **No formal definition of “logit entropy”** – the text uses the term but does not specify whether it is the entropy of the softmax probabilities over the vocabulary or something else.
- **Qualitative visualization is anecdotal**: Figure 7b is interesting but only one example; a broader automated analysis (e.g., part-of-speech tagging of selected tokens) would make the hierarchical claim stronger.
- **No discussion of limitations or failure cases**: The paper does not mention when DND might hurt performance (e.g., very long sequences, very high selection ratios, or models with already deep architectures).

### Trivial
- None.

## Nice-to-Haves
- Compare with a simple “double pass” baseline that applies the same transformer layer to a fixed (non-selective) subset of tokens to isolate the benefit of dynamic selection.
- Evaluate DND on a model that uses chain-of-thought or thinking mode to test compatibility.
- Report FLOPs and throughput for dense models (especially the 1B models) under various batch sizes.

## Novel Insights
Beyond the paper’s own contributions, the most novel observation is that token selection frequency correlates positively with model uncertainty (logit entropy) and that the nested reprocessing systematically reduces that uncertainty. The hierarchical selection pattern—nouns in early layers, mathematical/relational tokens in deeper layers—suggests that the router learns a form of implicit curriculum, which could inspire future studies on layer-wise specialization in LLMs.

## Suggestions
1. Explicitly state that the baseline SFT training used identical data, steps, and hyperparameters as the DND variant, and provide the dataset details (or a public reference) for reproducibility.
2. Report inference throughput under batched settings (e.g., batch size 4, 8, 16) to demonstrate that the advantage generalizes beyond single-sequence inference.
3. Add an ablation on the learnable fusion parameter β to show its sensitivity.

## Score and Decision

MY FINAL SCORE: 6</score>  
MY FINAL DECISION: Accept</decision>