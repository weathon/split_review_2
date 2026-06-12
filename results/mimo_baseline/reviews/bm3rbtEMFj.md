## Summary

The paper proposes ELMUR, a transformer architecture augmented with structured layer-local external memory for long-horizon, partially observable decision-making tasks. Each transformer layer maintains persistent memory embeddings that interact with tokens via bidirectional cross-attention and are updated through a Least Recently Used (LRU) block employing either full replacement or convex blending. The paper provides theoretical analysis of retention and boundedness properties under the LRU rule, and demonstrates strong empirical results on T-Maze (100% success up to 1M steps), POPGym (best aggregate score across 48 tasks), and MIKASA-Robo (best on 21/23 sparse-reward manipulation tasks).

## Strengths

- **Impressive retention results**: ELMUR achieves 100% success on T-Maze with corridors up to one million steps while using a context window of only L=10 with S=3 segments, demonstrating a 100,000× extension beyond the attention window. This is a striking and well-controlled result (Figure 3).

- **Consistent gains across diverse benchmarks**: ELMUR outperforms strong baselines across three qualitatively different benchmark families — synthetic T-Maze, 48 POPGym puzzle/control tasks (10.4 aggregate vs. 9.5 for RATE), and MIKASA-Robo manipulation (best on 21/23 tasks, ~70% aggregate improvement). This cross-domain consistency strengthens the evidence for the architecture's generality.

- **Clean, well-motivated architecture with thorough ablations**: The combination of layer-local memory, bidirectional cross-attention, and LRU management is principled. The ablation study (Table 3, Figure 6) provides clear evidence that per-layer memory, LRU, and sufficient capacity (M ≥ N) are all critical, while MoE→MLP replacement does not hurt accuracy. This gives actionable design guidance.

- **Efficient segment-level recurrence**: The design processes long trajectories in fixed-length segments with detached memory, keeping computational cost dependent on memory size rather than sequence length. ELMUR has comparable parameter counts and faster per-step inference than baselines.

## Weaknesses

### Fatal
None.

### Major

- **Modest aggregate POPGym improvement**: While ELMUR ranks first on 24/48 tasks, the aggregate improvement over RATE is only ~10% (10.4 vs. 9.5), and on reactive (non-memory) tasks, ELMUR is not the best (9.2 vs. 9.3 for DT, 9.1 for RATE/BC-LSTM). This suggests the architecture's advantage is primarily on memory-intensive tasks, which is expected but limits claims of broad superiority.

- **Theoretical analysis is correct but shallow**: Proposition 1 (exponential forgetting under convex blending) and Proposition 2 (boundedness of convex combinations) are mathematically straightforward consequences of the update rule. The half-life and effective horizon formulas are useful but constitute standard analysis of geometric decay. A deeper theoretical contribution — e.g., characterizing what information is retained optimally, or connecting to information-theoretic bounds — would significantly strengthen the paper.

### Minor

- **Hyperparameter sensitivity**: The ablation reveals that intermediate λ values (0.4–0.6) are unstable (Figure 6a), and performance drops sharply when M < N. While the paper documents this clearly, practitioners must carefully tune M relative to task structure, which limits plug-and-play applicability.

- **MIKASA-Robo baseline strength varies**: While ELMUR achieves best results on 21/23 tasks, some individual improvements are modest (RememberColor5-v0: 0.19 vs. 0.13 for RATE, with substantial variance). DT performs poorly on most tasks, which inflates relative gains. Comparison against more recent memory-augmented baselines would strengthen the claims.

- **RMT not consistently evaluated**: RMT appears as a baseline in Figure 3 (T-Maze) where it fails dramatically at long horizons, but is absent from POPGym and MIKASA-Robo comparisons. If RMT is a relevant memory-augmented baseline, it should be included consistently.

### Trivial
- Minor references to "Figure 2, Figure 2" appear to be parser artifacts.

## Nice-to-Haves

- A comparison of wall-clock training time and sample efficiency across methods would help practitioners assess the practical overhead of ELMUR's memory mechanism.
- Analysis of what the learned memory embeddings encode (e.g., visualization or probing experiments) would provide insight into *what* the model stores, complementing the analysis of *how long* it stores.
- Evaluation on at least one real-robot task, even a simple one, would substantially increase the impact claims for robotics.

## Novel Insights

The paper's most novel observation is that layer-local external memory with LRU-based slot management can extend effective memory horizons by orders of magnitude beyond the attention window while keeping computational cost bounded. The finding that per-layer memory significantly outperforms shared memory (Table 3) is a concrete architectural insight: each layer processes different levels of abstraction and benefits from independent memory. Additionally, the demonstration that memory capacity (M ≥ N) is the dominant factor over other hyperparameters provides clear design guidance for practitioners.

## Suggestions

- Deepen the theoretical analysis: derive bounds on task-relevant information retention (e.g., mutual information between stored memory and the initial cue as a function of λ and k), or analyze what types of POMDP structure the LRU policy handles optimally.
- Include RMT as a baseline across all benchmarks for consistent comparison, or explain its exclusion.
- Add a "scaling" experiment varying M and N together on a harder task to show whether the M ≥ N rule generalizes beyond RememberColor3-v0.
- Consider reporting per-task POPGym results in the main paper (currently in appendix) since they are central to the RQ4 claims.

## Score and Decision

ELMUR presents a well-designed memory-augmented transformer architecture with compelling empirical results, particularly the 100% T-Maze success at 1M steps and consistent MIKASA-Robo improvements. The architecture is clean and the ablations are informative. However, the theoretical contribution is shallow (standard convex-combination analysis), the POPGym aggregate gains are modest, and the baseline set could be more comprehensive. The paper is a solid contribution to memory-augmented RL but falls short of the theoretical or empirical depth needed for a strong accept.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>