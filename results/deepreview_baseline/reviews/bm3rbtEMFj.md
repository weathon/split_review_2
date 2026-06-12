## Summary

This paper introduces ELMUR (External Layer Memory with Update/Rewrite), a transformer architecture augmented with structured external memory for long-horizon reinforcement learning under partial observability. Each transformer layer maintains persistent memory embeddings that interact with tokens via bidirectional cross-attention (mem2tok read, tok2mem write), and are updated through a Least Recently Used (LRU) mechanism using replacement or convex blending. The method achieves 100% success on T-Maze corridors up to one million steps, outperforms baselines on 21 of 23 MIKASA-Robo manipulation tasks with visual observations, and achieves the best aggregate score on POPGym benchmarks.

## Strengths

- **Strong empirical results across diverse benchmarks**: ELMUR demonstrates compelling performance on three distinct evaluation suites (synthetic T-Maze, robotic MIKASA-Robo, and POPGym), with particularly impressive results on the T-Maze task where it maintains 100% success rate at corridor lengths up to 10^6 steps—100,000× beyond the attention window. The MIKASA-Robo results show nearly doubling of baseline performance on several tasks.

- **Clean architectural design with principled memory management**: The combination of layer-local external memory, bidirectional cross-attention for read/write, and LRU-based update with convex blending is well-motivated and clearly described. The design addresses the fundamental tension between bounded memory capacity and long-term retention in a theoretically grounded way.

- **Theoretical analysis of memory dynamics**: The paper provides formal bounds on forgetting (exponential decay), half-life, effective retention horizon, and memory boundedness. Proposition 2 (memory boundedness under convex updates) is a nice theoretical guarantee that addresses a practical concern about stability.

- **Comprehensive ablation study**: The ablation experiments systematically investigate the impact of memory size M, blending factor λ, initialization scale σ, segment configuration, and component removal (LRU, relative bias, shared vs. per-layer memory). This provides clear guidance for practitioners.

## Weaknesses

### Major

- **Limited comparison to relevant memory-augmented architectures**: The paper compares against RATE, DT, BC-MLP, CQL-MLP, and DP, but does not include comparisons to other explicit memory architectures such as Memformer, Differentiable Neural Computer (DNC), or Neural Turing Machines (NTM) that also address long-term memory in sequence models. Given that ELMUR's core contribution is a memory architecture, the absence of these comparisons weakens the claim of architectural novelty.

- **Theoretical analysis is relatively shallow**: While Proposition 1 and the half-life analysis are useful, the theoretical contribution is essentially a straightforward analysis of convex combination dynamics. The "formal bounds" claimed in the contributions are basic properties of convex updates. The analysis does not address more interesting questions such as: how does the LRU policy compare to other eviction policies (e.g., LFU, FIFO) in terms of information-theoretic optimality? How does the interaction between layers' memories affect overall retention?

- **Missing analysis of memory content and interpretability**: The paper does not analyze what information is actually stored in the memory embeddings. Are they learning to store task-relevant cues? Do different layers specialize in different types of information? This would significantly strengthen the claim that the memory mechanism is working as intended.

### Minor

- **The POPGym results, while positive, show modest improvements**: The aggregate score of 10.4 vs. 9.5 for RATE represents a relatively small improvement. On reactive tasks, ELMUR is essentially tied with baselines (9.2 vs. 9.1-9.3). The paper would benefit from statistical significance testing to confirm these differences are meaningful.

- **The ablation study uses RememberColor3-v0 with only 20 evaluation episodes per run**: This is a relatively small evaluation budget for drawing conclusions about component importance. The high variance in some ablation conditions (e.g., "No LRU" with 0.43 ± 0.22) suggests the results may not be fully reliable.

- **The paper claims "100% success rate" on T-Maze but only shows results for one training configuration (L=10, S=3)**: It would be informative to see whether this robustness holds across different segment lengths and numbers of segments.

### Trivial

- The paper uses "100,000×" as a headline number, but this is derived from a specific configuration (L=10, S=3, corridor=10^6). The actual multiplier depends on the specific hyperparameter choices.

## Nice-to-Haves

- Analysis of memory content (e.g., via probing or visualization) to understand what information is being stored and retrieved
- Comparison to other memory eviction policies beyond LRU
- Experiments on real-world robotic hardware to validate sim-to-real transfer
- Analysis of computational cost scaling with longer trajectories

## Novel Insights

The key insight is that combining layer-local external memory with LRU-based convex blending creates a surprisingly effective mechanism for long-horizon retention in transformers. The finding that memory capacity M needs to be at least as large as the number of segments N for reliable performance (from the ablation study) provides a practical design principle. The theoretical result that memory norms remain bounded under convex updates, while simple, is important for practical deployment. However, the paper's main contribution is empirical rather than providing fundamentally new theoretical understanding of memory in neural networks.

## Suggestions

1. Add comparisons to other explicit memory architectures (DNC, NTM, Memformer) to better contextualize the architectural contribution.
2. Include analysis of what information is stored in memory embeddings across layers, perhaps via probing tasks or visualization of attention patterns.
3. Add statistical significance tests for the POPGym results to confirm that the improvements over RATE are meaningful.
4. Report results for multiple training configurations on T-Maze to demonstrate robustness of the 100% success rate claim.
5. Consider adding a comparison to a simpler baseline that just concatenates a learned recurrent state with token embeddings, to isolate the benefit of the full bidirectional cross-attention design.

## Score and Decision

The paper presents a well-engineered memory architecture with strong empirical results across multiple benchmarks. The core ideas (layer-local memory, bidirectional cross-attention, LRU with convex blending) are sound and the ablation study provides good insight into design choices. However, the theoretical contribution is relatively modest, the comparison set for memory architectures is incomplete, and the POPGym improvements are modest. The paper represents a solid incremental contribution to memory-augmented transformers for RL, but does not rise to the level of a breakthrough.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>