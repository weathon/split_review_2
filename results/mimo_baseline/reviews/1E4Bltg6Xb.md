## Summary
This paper proposes a Dynamics Feature Representation (DFR) framework for Reinforcement Learning-based Dynamic Path Planning in urban road networks. DFR progressively refines high-dimensional global traffic dynamics into compact state representations through two stages: (1) a policy attention mechanism that pre-trains a distance-based shortest-path policy to extract a task-relevant subgraph, and (2) an n-hop neighborhood method that further localizes features around the agent's current node. Experiments on three synthetic urban road networks with DQN, PPO, and GCN+DQN show improved success rate, reduced optimality gap, faster convergence, and substantially lower planning time compared to using all dynamics.

## Strengths
- **Clear problem framing and motivation.** The paper articulates the completeness-efficiency tradeoff in state representation for RL-based DPP well. The hierarchical refinement from global → task-related → node-related features is an intuitive decomposition of the problem, and the formalization in Equations 5–7 provides a clean conceptual structure.
- **Practical efficiency with offline precomputation.** The policy attention subgraph depends only on static network topology and can be precomputed once, while n-hop neighborhoods are inexpensive to extract. The reported planning time reductions (85%, 46%, 79% for the three baselines) demonstrate meaningful computational savings, which is important for real-time deployment.
- **Consistent improvements across diverse RL algorithms.** The DFR framework improves DQN, PPO, and GCN+DQN across all three graph instances, suggesting the approach is model-agnostic and the benefit stems from better state representation rather than a specific algorithmic synergy. The ablation over k and n is thorough and provides actionable guidance for parameter selection.

## Weaknesses
### Fatal
None.

### Major
- **Theoretical claims are asserted but not established.** Equations 6, 7, and 8 claim that optimal policies under reduced features approximate optimal policies under full dynamics, but no formal bounds, conditions, or proofs are provided. The invocation of Predictive State Representations (PSR) is brief and does not connect to the specific extraction method—there is no argument that top-k shortest paths from a static distance policy provably preserve decision-relevant dynamics information. This is the paper's central theoretical claim and it remains unsubstantiated.
- **Weak and narrow experimental evaluation.** Only three small graphs (~300 nodes) with purely synthetic dynamics (random congestion factors drawn uniformly) are tested. There are no comparisons with (a) other state representation or graph sparsification methods from the graph RL literature, (b) more sophisticated RL baselines (e.g., graph attention networks, hierarchical RL), or (c) classical replanning baselines (D*-Lite, A* with replanning). The dismissal of classical methods in Section 2 and footnote 3 without any empirical comparison weakens the experimental contribution. The paper claims its work is validated on "realistic urban graphs" but uses entirely synthetic traffic dynamics.
- **Questionable naming and conceptualization of "policy attention."** What is called "policy attention" is simply extracting the union of edges from the top-k shortest paths under static distance. This is a straightforward structural filtering operation, not a learned attention mechanism. While the term "attention" has some precedent for feature selection, calling pre-computed shortest-path extraction "policy attention" overstates the novelty and could mislead readers about the mechanism involved.

### Minor
- **Deterministic MDP formulation vs. stochastic dynamics.** Section 3.2 states the MDP is "deterministic," yet the entire motivation revolves around stochastic, time-varying traffic dynamics. This inconsistency in the formal model should be reconciled.
- **Limited ablation on dynamics complexity.** The synthetic dynamics use a single congestion factor β ∈ [0.1, 1.5] uniformly sampled per edge per timestep. There is no evaluation of DFR's robustness to more realistic dynamics patterns (e.g., correlated congestion, rush-hour patterns, abrupt disruptions like accidents).
- **No analysis of failure modes.** When does DFR fail? The paper reports aggregate metrics but provides no case analysis of scenarios where DFR produces worse routes than the AD baseline, which would be important for understanding the method's limitations.

### Trivial
- Notation overload with multiple meanings of t across graph-theoretic and MDP formulations (acknowledged in footnote 2 but still confusing).

## Nice-to-Haves
- A comparison showing how DFR performs when the underlying dynamics deviate significantly from the static topology (e.g., road closures, one-way changes) would demonstrate robustness.
- Visualization of the extracted subgraphs for representative tasks to build intuition about what policy attention captures.

## Novel Insights
The paper's core insight is that a two-stage hierarchical refinement—first filtering by task relevance using static structural priors, then localizing by spatial proximity—can effectively bridge the global-vs-local state representation tradeoff in graph-based RL. While each individual component (shortest-path extraction, k-hop neighborhoods) is not new, the specific combination and the argument that static distance serves as a reliable prior for dynamic planning is a reasonable observation. However, beyond the paper's own contributions, no deeper novel insight emerges about the nature of state representation in RL or graph-based planning.

## Suggestions
- Strengthen the theoretical section by providing formal conditions (even loose sufficient conditions) under which the subgraph extraction preserves near-optimality, possibly via bounds on the value function error as a function of k.
- Expand experiments to include real traffic datasets (e.g., METR-LA, PEMS-BAY) and additional RL baselines that use graph-structured state representations.
- Rename "policy attention" to something more descriptive, such as "task-aware subgraph extraction" or "shortest-path attention," to avoid confusion with learned attention mechanisms.
- Address the deterministic MDP inconsistency and evaluate on more complex, correlated dynamics.

## Score and Decision
The paper addresses a relevant problem with a clear framework and shows consistent empirical improvements. However, the theoretical analysis is insufficiently rigorous, the experimental evaluation is limited in scale and baseline coverage, and the claimed novelty is modest given that the core operations (shortest-path extraction and k-hop neighborhoods) are well-established techniques. The work reads more as a solid application paper than a contribution that advances fundamental understanding of state representation in RL.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>