## Summary

This paper presents WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-resource compatibility. The framework uses a weighted cross-attention network to encode compatibility coefficients and a longest-directed-distance GNN for task dependencies, enabling single-pass inference. It introduces skip actions within this single-pass setting to close the optimality gap inherent in list-scheduling-based methods. Experiments on TPC-H and Computation Graphs datasets show consistent improvements over heuristics and prior neural approaches, with up to 18.1% makespan reduction over the best heuristic.

## Strengths

- **Practical and well-motivated problem:** Heterogeneous DAG scheduling with compatibility coefficients is a real challenge in cloud computing, data centers, and ML compilers; the paper targets a clear gap in existing neural schedulers.
- **Novel weighted cross-attention design:** Integrating compatibility coefficients as an additive bias outside the softmax normalization is a simple but effective idea that preserves distinguishability across tasks with different compatibility profiles while maintaining adaptability to varying numbers of pools and task types.
- **Theoretical analysis of the optimality gap:** The paper provides a clean analysis showing that list scheduling can fail to represent optimal solutions and formally shows that the proposed skip-action mechanism (Theorem 1) restores surjectivity and can cover optimal schedules without multi-round network processing.
- **Strong empirical results:** WeCAN outperforms all listed baselines (including Tetris, HEFT, PPO-BiHyb, One-Shot) on both real-world TPC-H and synthetic Computation Graphs datasets, with significant makespan improvements and inference times comparable to heuristics. Ablation studies convincingly validate the contributions of each component, and the heavy-task experiments illustrate the practical benefit of skip actions.

## Weaknesses

### Fatal  
None.

### Major  
1. **Limited theoretical guarantee on learning:** Theorem 1 shows that *there exist* scores that enable an optimal schedule by greedy selection, but does not guarantee that the REINFORCE-based training will find these scores. The paper does not discuss convergence properties or whether the learned policy actually achieves optimality, only that the representation capacity is sufficient. This is a common but important limitation that should be acknowledged and addressed (e.g., with additional empirical analysis of learned policies).  
2. **Skip action score design is ad hoc and unvalidated:** The specific form \( u_{\pi_{skip}} = u_a(1 - \frac{k}{2n})^{u_b} + u_c \) is introduced without strong motivation or ablation. The claim that this design “clusters most poor solutions in the high-\(u_a\), high-\(u_c\) region” is not empirically demonstrated (e.g., by visualizing learned scores or analyzing skip usage patterns).  
3. **Incomplete description of key network components in the main text:** The Longest Directed Distance GNN (LDDGNN) attention masks \( M_{v,w}^j \) and bias embeddings \( b_{d_c(v,w)} \) are mentioned but not fully specified; the paper relies on the appendix for details. For a self-contained evaluation, the main paper should include at least a brief description of how these are computed.  
4. **Potential unfairness in baseline comparison:** One-Shot (Jeon et al., 2023) was not designed to handle compatibility coefficients; the paper adds these to the TPC-H dataset but does not explain whether or how One-Shot was adapted. If One-Shot treats compatibility coefficients as part of the environment without dedicated architecture, the comparison may favor WeCAN. The paper should either adapt One-Shot appropriately or explicitly note this limitation.

### Minor  
- The claim that HEFT is a “non-list scheduling algorithm” is inaccurate; HEFT is a list scheduling heuristic (it uses upward rank ordering and insertion-based assignment).  
- Standard deviations are reported only for neural methods; providing variances for heuristic baselines across multiple random seeds (where applicable) would improve completeness.  
- The paper refers to “Appendix C” and “Appendix D” for supporting analysis and dataset details, but these are not available in the parsed text. The claims about heavy-task performance and scalability should be judged on the content actually presented.

### Trivial  
- Minor phrasing issues (e.g., “the skip benefits more when the percentage of heavy tasks increases” could be clearer).  
- Figure captions are provided but the figures themselves are not rendered in the text; this is a parser issue.

## Nice-to-Haves  
- A visualization or quantitative analysis of when the skip action is invoked during scheduling and how the learned scores \( u_a, u_b, u_c \) vary with heavy-task proportion.  
- An ablation study comparing the proposed skip score formula with simpler alternatives (e.g., fixed skip score or learnable per-step skip score) to justify the design.  
- A discussion of the REINFORCE variance in the presence of skip actions and any techniques used to stabilize training.

## Novel Insights  
Beyond the paper’s own contributions, the observation that list scheduling fails to cover optimal solutions because \( T \circ S_{list} \) is not surjective, and that skip actions can bridge this gap without requiring multi-round network processing, is a conceptually clean insight that could influence future work on scheduling generation maps. The placement of compatibility coefficients outside softmax to preserve distinguishability is a simple but non-obvious architectural insight with potential value beyond scheduling.

## Suggestions  
- Clarify that the network is evaluated once (single-pass), while the schedule construction (Algorithm 1) still involves iterative steps of masking and selection. The term “single-pass” should be defined precisely.  
- Add a brief description of the LDDGNN attention mask and bias definition in the main text, or point to an accessible appendix if space permits.  
- Discuss how baselines (especially One-Shot) were adapted to handle compatibility coefficients, or note that they were not designed for this and the comparison should be interpreted accordingly.  
- Consider including an analysis of the learned skip action usage (e.g., frequency, correlation with heavy tasks) to support the theoretical claims about optimality gap closure.

## Score and Decision  
The paper addresses a significant problem, presents a well-motivated architecture, provides useful theoretical analysis, and demonstrates empirical improvements. However, the limited theoretical guarantee on learning, the ad hoc skip score design, and potential baseline fairness issues reduce confidence. Overall, the work is solid and contributes new knowledge, but the weaknesses warrant a borderline acceptance.

**Score:** 6.0  
**Decision:** Accept  

MY FINAL SCORE: <score>6.0</score>  
MY FINAL DECISION: <decision>Accept</decision>