## Summary

This paper introduces R2PS, the first approach to worst-case robust real-time pursuit strategies in graph-based pursuit-evasion games under partial observability. The authors prove that a dynamic programming algorithm for Markov PEGs maintains optimality under asynchronous evader moves, propose a belief preservation mechanism for partially observable settings, and embed this into the EPG reinforcement learning framework to train a GNN-based pursuer policy that achieves zero-shot generalization to unseen real-world graph structures with O(n²m) inference complexity.

## Strengths

- **Genuine theoretical contribution on asynchronous-move optimality.** The paper provides a clean proof (Theorem 2, Corollary 1) that the DP-induced strategies remain strictly optimal when the evader can observe/predict pursuer actions before moving, which is a practically important adversarial model. The recursive structure revealed by Lemma 1 connects the DP algorithm's properties to the asynchronous setting in a satisfying way.

- **Practical significance of real-time inference.** The complexity analysis clearly demonstrates the gap between O(n²m) for the GNN policy and O(n^(m+1)) for recomputing DP, with concrete timing comparisons (e.g., <0.01s vs. >100s on large graphs). This addresses a genuine real-world need for dynamically changing environments.

- **Strong zero-shot generalization results.** The cross-graph RL policy trained on 300 graphs consistently outperforms PSRO directly trained on the 10 test graphs, across multiple evader policies and diverse real-world map structures (Times Square, Eiffel Tower, etc.). This is a compelling demonstration of the approach's generalization capability.

- **Well-designed belief preservation mechanism.** The transition from position set (5) to belief-averaged policy (6) with the update rule (7) is well-motivated and empirically validated—belief consistently outperforms the position-only approach (Table 1), and reducing update frequency significantly degrades performance (Table 4).

- **Transparent evaluation under strong adversarial conditions.** The paper tests against multiple evader policies including the provably optimal asynchronous DP evader and a best-responding evader trained against the pursuer, providing a thorough worst-case assessment.

## Weaknesses

### Fatal
None.

### Major

- **Limited comparison baselines for partial observability.** The paper does not compare against other approaches that handle partial observability in pursuit-evasion or adversarial settings (e.g., POMDP-based methods, particle filter approaches, or other heuristic PO pursuit strategies). This makes it difficult to assess how much the belief preservation mechanism specifically contributes versus alternative PO handling techniques.

- **Low success rates against best-responding evaders on complex maps.** Against BR_async, several maps show success rates below 30% (Hollywood Walk of Fame: 0.10, Sagrada Familia: 0.20, The Bund: 0.23). While the paper is transparent about this being the worst case, it raises questions about the practical utility for security applications on topologically challenging graphs, which is the paper's primary motivation.

### Minor

- **Comparison with PSRO has asymmetric training conditions.** PSRO uses 10 iterations × 10,000 episodes on 10 graphs, while R2PS uses 100,000 episodes across 300 graphs. While the point is zero-shot generalization, a controlled comparison matching total training compute would strengthen the claim. A PSRO variant trained on 300 graphs for equivalent compute would be informative.

- **Fixed m=2 pursuers throughout.** Although justified by the planar graph result (3 pursuers suffice for capture), the paper provides no experiments with varying pursuer numbers. For real-world scalability to larger teams, this would be valuable.

- **Uniform prior in belief update.** The default assumption of uniform evader policy for belief propagation (Section 3.2) is acknowledged, but the gap between "Known Opponent" and "Original" conditions (Table 4, e.g., Scotland-Yard: 0.99 vs 0.73) suggests this is a significant limitation. More discussion on how to learn or estimate a better prior would strengthen the work.

### Trivial
None.

## Nice-to-Haves

- A visualization of how the belief distribution evolves during actual pursuit trajectories on a sample graph would make the mechanism more intuitive.
- Analysis of how the approach performs with varying numbers of pursuers (m > 2).
- Discussion of robustness to noise in observations (e.g., probabilistic detection rather than deterministic range-based).

## Novel Insights

The paper's core novel insight is that the DP algorithm's distance table D simultaneously encodes optimal strategies for both synchronous and asynchronous-move settings (Theorem 2/Corollary 1), which means a single preprocessing can support adversarial training against the strongest evader model. Combined with the observation that belief averaging over possible evader positions outperforms minimax over positions under continual partial observability (presumably because the minimax policy becomes overly pessimistic with large Pos sets), this provides a practical bridge between the computationally expensive perfect-information solutions and real-time partially observable deployment. The exponential improvement argument through cross-graph policy-space divisions (Section 4.1) is also an interesting framing of why training across diverse graph structures yields robust generalization.

## Suggestions

- Include a comparison baseline against at least one alternative partial-observability method (e.g., a particle-filter-based PEG solver or a POMDP approximation) to contextualize the contribution of belief preservation.
- Provide a controlled experiment where PSRO is trained on the same 300-graph training set for the same total compute budget, to isolate the benefit of EPG-style guidance versus simply more diverse training.
- Analyze the relationship between graph topology properties (diameter, degree distribution) and success rates more systematically, as the current results suggest strong topology dependence.

## Score and Decision

The paper makes a solid contribution by extending pursuit-evasion game solutions to the practically important setting of partial observability with worst-case adversarial evaders. The theoretical results are clean and correct, the belief preservation mechanism is well-motivated and empirically effective, and the zero-shot generalization results are convincing. The main weaknesses are limited PO baselines and some moderate success rate gaps, but these do not invalidate the core claims. This is a well-executed paper that advances the state of the art in an important direction.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>