## Summary

The paper proposes ELMUR (External Layer Memory with Update/Rewrite), a transformer architecture that augments each layer with a structured external memory track. Memory embeddings persist across segments, interact with tokens via bidirectional cross-attention (mem2tok read, tok2mem write), and are updated with a Least Recently Used (LRU) rule that fills empty slots by full replacement and refreshes filled slots via convex blending. The method is evaluated on synthetic T-Maze, POPGym puzzles/control, and the MIKASA-Robo robotic manipulation suite, where it achieves 100% success on T-Maze up to one million steps, outperforms baselines on most tasks, and obtains a 70% relative improvement over prior methods on MIKASA-Robo.

## Strengths

- **Addresses a well-motivated and important problem:** Long-horizon partial observability under sparse rewards is a fundamental challenge for real-world robotics, and the paper cleanly identifies the limitations of fixed-context-window transformers.
- **Clear and well-structured architecture description:** The use of per-layer external memory with separate read/write cross-attention pathways, relative bias for temporal grounding, and an explicit LRU update rule is presented with algorithms (Algorithm 1, 2) and diagrams (Figures 1, 2) that make the method easy to understand and reproduce.
- **Strong empirical results across diverse benchmarks:** ELMUR demonstrates near-perfect retention on synthetic T-Maze even when corridors are orders of magnitude longer than the training context, achieves the best aggregate success rate on 21 out of 23 MIKASA-Robo tasks, and scores highest overall on 24 of 48 POPGym tasks. These results are supported by standard error bars and three independent runs.
- **Theoretical analysis provides formal guarantees:** The paper derives exponential forgetting bounds, half-life formulas, and a boundedness proof for memory embeddings under convex update, which give a principled understanding of the model’s retention properties and complement the empirical findings.
- **Ablation study dissects the contribution of components:** Removing LRU, relative bias, or per-layer memory all degrade performance significantly, while replacing MoE with simple MLP does not hurt (Figure 6, Table 3), confirming that the memory mechanism itself is responsible for the gains.

## Weaknesses

### Fatal
None.

### Major

- **Selective baseline comparison on the key benchmarks:** On MIKASA-Robo and POPGym (Tables 1, 2), the paper compares against DT, RATE, BC, CQL, and Diffusion Policy, but omits other recurrent or memory-augmented architectures that are directly relevant, such as Transformer-XL, Compressive Transformer, RMT (shown only in Figure 3 for T-Maze), or state-of-the-art memory models. This makes it difficult to judge whether the gains are due to ELMUR’s specific design or simply to having *any* external memory. The POPGym aggregated returns show only a modest margin over RATE (10.4 vs. 9.5), and on reactive tasks RATE and DT match ELMUR, suggesting the advantage is not universal.
- **Training is done purely via imitation learning (Behavior Cloning):** The paper evaluates only on offline demonstration data and does not test ELMUR in an online RL setting with exploration. Since long-horizon RL often involves sparse rewards and credit assignment over many steps, it remains unclear whether the memory architecture would offer the same benefits when the agent must explore and learn from its own experience. The authors acknowledge this (no online RL comparison), but it limits the scope of the contribution relative to the title “Long-Horizon RL Problems.”
- **Potential inconsistency in task counts:** The abstract claims “best success rate on 21 out of 23 tasks” and “72 tasks” across all benchmarks. Table 1’s caption says “all 32 MIKASA-Robo tasks,” while the text references 23 tasks. The relation between these numbers is unclear, and without the appendix the reader cannot resolve this. This should be clarified to avoid confusion.
- **The effective horizon claim (100,000×) is shown only on one synthetic task:** While T-Maze is designed to test memory, the extreme extrapolation result (100% success at 1M steps) relies on a very simple cue structure. It is not replicated on the more complex MIKASA-Robo or POPGym tasks, where the maximum horizon is much shorter. The paper would be stronger if it demonstrated similar relative extrapolation ratios on a second benchmark.

### Minor

- **Theoretical analysis is straightforward:** The exponential forgetting under convex blending and the boundedness proof are elementary consequences of the update rule. While they provide reassurance, they do not offer deep insight beyond what the algorithm already suggests.
- **Ablation study is limited to one task (RememberColor3-v0):** Ablations on additional tasks (e.g., a POPGym puzzle) would strengthen confidence that the component contributions are general.
- **Hyperparameter sensitivity for λ:** Figure 6(a) shows that intermediate λ values (0.4–0.6) cause instability when memory is under-provisioned. This suggests that tuning λ may be crucial, yet the paper does not provide guidance on how to set λ in practice across different tasks.

### Trivial
- None.

## Nice-to-Haves

- An online RL evaluation (e.g., on a partially observable MuJoCo task or Minigrid) would significantly broaden the impact.
- Comparison to additional memory-augmented baselines (Transformer-XL, Compressive Transformer, Memformer) on MIKASA-Robo and POPGym would strengthen the empirical case.
- A discussion of failure cases or limitations (e.g., tasks where ELMUR underperforms) would improve the completeness of the paper.

## Novel Insights

Beyond the paper’s contributions, the key insight is that *per-layer external memory with dedicated read/write cross-attention and an LRU management scheme* effectively decouples the memory capacity from the attention window size, enabling bounded yet persistent storage. The finding that the number of memory slots \(M\) must at least equal the number of segments \(N\) for reliable retention (and that performance collapses abruptly when \(M < N\)) highlights a simple but important capacity constraint that designers of memory-augmented transformers should consider.

## Suggestions

- Add a sentence clarifying the relationship between the “21 out of 23” and “32 MIKASA-Robo tasks” numbers in Section 5.2.
- Include the key hyperparameters (\(M, \lambda, L, S\)) used in each benchmark table, either in the main text or in a dedicated table, so that readers can directly verify the effective horizon formula.
- Consider adding a small experiment on a fully observable MDP (CartPole is already done) and confirming that memory does not degrade performance, which is already reported – but this could be mentioned earlier.

## Score and Decision

The paper presents a clean, well-motivated, and empirically strong architecture for long-horizon partial observability. The weaknesses (selective baselines, IL-only training, minor inconsistencies) are significant but not fatal; they can be addressed in revision or discussion. The empirical gains on T-Maze and MIKASA-Robo are impressive, and the ablation study convincingly attributes the improvements to the memory components. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>