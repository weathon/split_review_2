## Summary

The paper proposes ELMUR, a transformer architecture augmented with per-layer external memory embeddings, bidirectional token-memory cross-attention (mem2tok and tok2mem blocks), and a Least Recently Used (LRU) update rule that fills empty slots by full replacement and then refreshes the oldest slot via convex blending. This design is applied to imitation learning policies for long-horizon partially observable decision-making tasks. Experiments on the synthetic T-Maze, the MIKASA-Robo robotic manipulation suite (visual observations, sparse rewards), and the 48-task POPGym benchmark show that ELMUR achieves a 100% success rate on T-Maze corridors up to one million steps, outperforms strong baselines on the majority of tasks, and yields an aggregate improvement of about 70% over prior best methods on the robotic tasks.

## Strengths

- **Clear architectural contribution.** The idea of giving each transformer layer its own persistent, bounded external memory with explicit read/write cross-attention and an LRU-based update policy is well-motivated and elegantly simple. The separation of token track and memory track with bidirectional interaction is a neat design.
- **Strong empirical results across diverse benchmarks.** ELMUR demonstrates near-perfect retention on the extremely long T-Maze (100% up to 1e6 steps), consistently best aggregated scores on POPGym (10.4 vs 9.5 for the next best), and first-place performance on 21 of 23 MIKASA-Robo tasks. The generalization heatmap (Figure 4) shows robust transfer across unseen sequence lengths.
- **Ablation study provides solid evidence for design choices.** The experiments in Figure 6 and Table 3 clearly isolate the importance of per-layer memory, the LRU mechanism, and sufficient memory capacity (M ≥ N). The ablation of λ, σ, and segmentation parameters is thorough and informative.
- **Efficiency considerations are addressed.** The paper reports per-step runtimes and parameter counts, noting that ELMUR is competitive or faster than some baselines despite having more parameters, thanks to MoE feed-forward layers and the short attention window that defers long-term storage to the external memory.
- **Theoretical retention analysis.** Although elementary (exponential decay from convex updates), Propositions 1 and 2, the corollary on half-life, and the effective horizon formula provide formal lower bounds on memory retention and boundedness, which support the empirical findings.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Exaggerated claim about retention factor.** The paper states “ELMUR extends effective horizons up to 100,000 times beyond the attention window”. However, the T-Maze experiment uses L=10 and S=3, yielding a context of 30 tokens. A corridor of 1,000,000 steps gives a factor of ~33,333, not 100,000. While still impressive, the claim should be corrected to avoid misrepresentation.
- **Limited baseline set for memory architectures.** The comparison includes RATE, DT, BC-LSTM, DMamba, and offline RL methods, but does not include other external-memory transformers (e.g., Memformer, Block-Recurrent Transformer, RETRO-style retrieval) that would better isolate the value of ELMUR’s specific memory design. The current baselines make ELMUR look strong, but a more comprehensive comparison would strengthen the claims.
- **Dependence on sufficient memory capacity.** The ablation (Figure 6) shows that ELMUR’s success collapses when the number of memory embeddings M is smaller than the number of segments N. In practice, N is unknown at design time; the paper does not discuss how to choose M robustly or whether the model can adapt to varying horizons.
- **Theoretical analysis is basic.** The exponential forgetting and boundedness results are direct consequences of convex combination updates under bounded inputs. While helpful, they do not go beyond textbook properties and do not offer novel insight into, e.g., the dynamics of the memory selection mechanism.

### Trivial
- The integer score scale in Table 1 could be more clearly explained; the meaning of “Score” in Table 3 is not defined upfront.

## Nice-to-Haves
- Compare against a retrieval-augmented transformer (e.g., using a differentiable key-value store or a slot-attention model) to further disentangle the contributions of the LRU policy versus the cross-attention interface.
- Provide a discussion or heuristic for setting M in practice when the trajectory length is unknown.
- Include confidence intervals or error bars for the aggregated POPGym scores in Table 2.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions
- Correct the “100,000×” factor to reflect the actual ratio (≈33,000×) or rephrase to “up to 100,000×” if a different configuration justifies that number.
- Add a comparison to at least one additional external memory architecture (e.g., Memformer or a Slot Attention baseline) to better contextualize the advantages of the ELMUR design.
- Discuss strategies for selecting the memory size M, especially for open-ended tasks where the required number of segments is not known a priori.

## Score and Decision

**Score:** 8  
**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>