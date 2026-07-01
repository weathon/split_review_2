## Summary
The paper proposes a Dynamics Feature Representation (DFR) framework for reinforcement-learning-based dynamic path planning in urban road networks. DFR hierarchically refines global traffic dynamics into compact, decision-relevant features using a policy attention mechanism (extracting a subgraph based on top-\(k\) shortest distance paths) and an \(n\)-hop neighborhood method (decoupling that subgraph into local features). Experiments on three real-world road networks show that DFR improves the performance of DQN, PPO, and GCN-based agents over the full-dynamics baseline while reducing feature dimensionality and planning time.

## Strengths
- **Practical problem formulation.** The paper tackles a real and timely challenge—efficient routing under time-varying traffic—and clearly motivates why state representation is a bottleneck in RL-based dynamic path planning.
- **Hierarchical design is intuitive.** The two-stage refinement (global task-relevant subgraph followed by agent-centric local features) is a natural way to balance completeness and efficiency, and the ablation study systematically explores how the parameters \(k\) and \(n\) affect performance.
- **Real-world experimental setting.** The evaluation on three distinct urban road networks from OpenStreetMap (Nanjing, Chaoyang, Pudong) lends credibility to the empirical findings beyond synthetic benchmarks.

## Weaknesses
### Fatal
- **Unclear/incorrect definition of the Compactness Rate (CR).** The paper defines CR as “the proportion of the reduced feature dimension after DFR to the original dimension” but reports CR values far exceeding 1.0 (e.g., 121.042 for the AD baseline). This makes the quantitative claims about dimensionality reduction uninterpretable and potentially spurious. The radar charts cannot be properly assessed without a valid metric, undermining one of the paper’s core contributions.

### Major
- **Overclaimed theoretical grounding.** The paper invokes Predictive State Representations (PSR) to argue that the DFR representation is “theoretically sufficient” and Markovian, yet provides no formal proof, constructive mapping, or empirical verification of sufficiency. The connection is superficial and does not substantiate the guarantee claimed.
- **Convergence acceleration claim is not supported.** The abstract and contributions state that DFR “accelerates convergence,” but the only training curves shown (Fig. 6, bottom) compare different \(n\) values at fixed \(k=0.6\)—not DFR versus the AD baseline across episodes. Without that comparison, the claim is unsubstantiated.
- **Limited baselines and missing ablations for key components.** The only baseline is “All Dynamics” (global features). There are no comparisons to other natural compression methods (e.g., random subgraph sampling, simple local-only state, or learned attention-based pooling). The ablation includes \(k=-1\) (no policy attention), which partially addresses this, but a standalone comparison to a simpler local-only baseline (without the pretrained policy attention) would better isolate the benefit of each component. The GNN baseline (GCN+DQN) is also not compared with other state-of-the-art GNN architectures for graph-based RL.

### Minor
- **No statistical significance or variability reported.** The main results (Fig. 5) and ablation tables (Fig. 6) show single point values without error bars, confidence intervals, or number of random seeds. Given the inherent noise in RL training, this weakens the reliability of the reported improvements.
- **Distance-based attention assumption not critically examined.** The policy attention selects paths based on static shortest distance, but the objective in DPP is travel time under dynamic congestion. The paper argues that distance is a “fundamental constraint,” but does not discuss cases where the optimal dynamic path is far from any of the top-\(k\) shortest-distance paths, nor does it analyze the sensitivity of results to this mismatch.

### Trivial
- The notation conflates the time index of the MDP step with the global time axis (footnote partially clarifies, but the text remains confusing in places, e.g., “t” used for both).

## Nice-to-Haves
- A comparative analysis with other non-RL dynamic planning methods (e.g., receding-horizon A*, learning-enhanced Dijkstra) could better contextualize the gains.
- A formal or empirical check of how well the compact state approximates the Markov property (e.g., by measuring prediction error of next-state dynamics) would strengthen the PSR connection.

## Novel Insights
None beyond the paper’s own contributions. The hierarchical refinement idea is sensible but conceptually straightforward.

## Suggestions
- **Clarify the CR metric immediately.** Define whether it is a ratio, a count, or a normalized index, and ensure that all reported values are consistent with that definition. Re-run the compactness analysis with proper normalization and report both original and reduced dimensions clearly.
- **Add training curves comparing DFR-enhanced agents (DQN+DFR, PPO+DFR) against their AD counterparts** to support the convergence acceleration claim.
- **Include a comparison with a “local-only” baseline** that uses \(n\)-hop neighborhoods but no policy attention, to ablate the benefit of the pretrained attention step.
- **Discuss the limitations of the distance-based attention**, especially in scenarios where the optimal dynamic path deviates strongly from the shortest-distance path, and suggest when the approach might fail.
- **Report means and standard deviations over multiple seeds** for all main results (at least 5 seeds) to indicate statistical robustness.

## Score and Decision
The paper addresses an important problem with a reasonable idea, but the unclear and seemingly inconsistent compactness metric is a fatal flaw that invalidates one of its core quantitative claims. Combined with overstated theoretical guarantees and missing evidence for convergence acceleration, the paper in its current form does not meet the bar for acceptance. I recommend rejection.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>