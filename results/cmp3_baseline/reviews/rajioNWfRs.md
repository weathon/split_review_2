## Summary

The paper introduces TNT, a two-stage training framework for deep memory modules (e.g., Titans, TTT) that aims to decouple training efficiency from inference performance. Stage 1 pre-trains with a hierarchical memory: a sequential global memory using large chunks for long-range context and multiple parallel local memories with periodic state resets that enable context parallelism. Stage 2 fine-tunes the local modules with smaller chunk sizes to improve inference accuracy. The paper also proposes a Q-K Projection to mitigate a domain mismatch between memory compression and retrieval. Experiments on 150M-parameter Titans models show up to 17× speedups and modest perplexity improvements over the baseline.

## Strengths

- **Addresses a real and important bottleneck**: Deep memory modules have compelling theoretical properties but suffer from severe training inefficiency. The paper clearly articulates this problem and proposes a structured approach to tackle it.
- **Novel combination of ideas**: The hierarchical memory with periodic local resets for context parallelism is a clever mechanism to parallelize non-linear recurrences. The two-stage training (efficiency pre-training, performance fine-tuning) is well-motivated by the observed chunk-size sensitivity.
- **Strong empirical speedups**: The reported 17× time-to-quality improvement over the most accurate baseline configuration is substantial and practically meaningful for scaling these models.
- **Ablation studies are informative**: The ablation confirms the contributions of hierarchical memory, global memory, Q-K Projection, and Stage 2 fine-tuning, giving confidence that each component matters.

## Weaknesses

### Fatal
None.

### Major

1. **Architectural limitation from local memory resets**: The periodic reset mechanism restricts the fine-grained local memory to a fixed window size \(S_L\) (e.g., 2048 or 4096 tokens). While the global memory captures long-range context, it operates at a coarse resolution (chunk size 2048+). This means the model cannot learn fine-grained dependencies beyond the local window—it essentially becomes a local-in-time model for high-resolution processing. The paper does not discuss this trade-off or evaluate on tasks that require long-range fine-grained patterns (e.g., passkey retrieval, multi-step reasoning over long contexts). The claim of “decoupling training efficiency from inference performance” is not fully satisfied; a hard architectural constraint on local memory range is introduced.

2. **Experiments are limited to 150M parameters**: All evaluations are on 150M models. It is unclear whether the benefits of TNT (especially the hierarchical memory and Q-K projection) scale to larger, more practical model sizes where memory modules might behave differently. The time-to-quality comparison uses a single target loss (3.20) on a single dataset; more comprehensive convergence analysis (e.g., training to full convergence with equal FLOPs) is needed.

3. **Q-K Projection is under-justified**: The paper claims a fundamental “domain mismatch” between compression and retrieval, but the proposed projection (onto the subspace of keys in the current chunk) is introduced without theoretical or empirical justification for why this specific form is optimal. The approach is applied only to local memory, but the same mismatch could affect the global memory as well. The ablation shows a clear benefit, but the mechanism feels ad-hoc and not deeply analyzed.

4. **Generality claim is not substantiated**: TNT is described as a general training paradigm for any deep memory module, but the Q-K projection relies on an explicit key/query/value structure. Some deep memory modules (e.g., certain Hopfield-based memories) may not have such a decomposition. Only Titans is tested; TTT (also mentioned in the abstract) is not evaluated under TNT.

### Minor

- The perplexity improvements over the strongest baseline (Titans with C=8) are modest (e.g., 23.13 vs 25.07 for Stage 1, 23.09 vs 25.07 after Stage 2). The gated Transformer still achieves better perplexity (22.39). The claim “improving model accuracy” is supported but the absolute gains are small given the 10B token training budget.
- Runtime comparisons against FlashAttention use a JAX implementation of TNT without custom kernels. The paper acknowledges this, but the claim that TNT “outperforms even the highly optimized FlashAttention kernel” is based on a single configuration (C_L={128}) and a JAX vs. JAX comparison; this is not a fair comparison with the same level of kernel optimization.
- The paper does not analyze the memory overhead of the hierarchical design (global + multiple local memories) compared to baselines, nor the effect of the number of local modules on total parameters and FLOPs.
- The chunk-size sensitivity experiment (Figure 2) is interesting but not fully explained. The paper attributes it to “train-test mismatch,” but alternative explanations (e.g., the optimal chunk size being a property of the data) are not discussed.

### Trivial

- None.

## Nice-to-Haves

- Evaluate TNT on a broader set of deep memory modules (e.g., TTT, Atlas) to demonstrate generality.
- Include experiments on longer sequences (e.g., 64K–128K) to showcase the scaling advantage and the effectiveness of the global memory for truly long-range tasks.
- Provide an analysis of the trade-off between local window size \(S_L\) and model quality, to help practitioners choose this hyperparameter.
- Add a comparison against other parallelization techniques for non-linear RNNs (e.g., the monotonic parallel scan of Gonzalez et al., 2024).

## Novel Insights

The key insight—that the chunk-size trade-off in deep memory modules can be decomposed into two stages by using periodic resets for local modules plus a coarse global memory—is novel and practically useful. The observation that inference performance is maximized only when chunk size matches training (Figure 2) is also insightful, though the paper could delve deeper into why this occurs (e.g., does the memory function learn a specific time-scale?).

## Suggestions

- Discuss the local window size \(S_L\) as a new hyperparameter that controls the capacity for fine-grained long-range memory, and provide guidance on how to set it relative to sequence length.
- Include a task that explicitly requires long-range fine-grained reasoning (e.g., a version of the Selective Copying task with long distractors) to show what the local memory reset sacrifices.
- Run the Stage 2 fine-tuning for more steps to see if the small improvement versus Stage 1 (23.13 → 23.09) is statistically significant, and evaluate whether fine-tuning with larger chunks also helps.

## Score and Decision

The paper presents a well-motivated and novel training framework that achieves impressive speedups. However, the core architectural change introduces a hard limit on fine-grained memory range, and the claims of “decoupling” and “generality” are somewhat overstated given the experiments are limited to a small model size and a single architecture. The modest perplexity gains and the lack of analysis on scaling to larger models or longer sequences prevent this work from being a clear accept. I believe the paper is solid but has significant limitations that need to be addressed before it can be accepted at a top venue.

Score: 3

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>