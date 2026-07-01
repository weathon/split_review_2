## Summary
This paper proposes a Dynamics Feature Representation (DFR) framework for reinforcement learning-based dynamic path planning in urban road networks. DFR uses a two-stage hierarchical refinement process—policy attention to extract task-relevant subgraphs and n-hop neighborhood decoupling for agent-centric local features—to compress global traffic dynamics into compact, decision-relevant state representations. Experiments on three real-world urban road networks show that DFR improves planning performance and convergence speed compared to using full dynamics or other baselines.

## Strengths
- **Clear problem formulation and motivation**: The paper articulates the fundamental trade-off between global dynamics (complete but computationally expensive) and local dynamics (efficient but potentially suboptimal) in RL-based DPP, and positions DFR as a principled solution to this dilemma.
- **Novel hierarchical refinement approach**: The two-stage design (policy attention + n-hop neighborhoods) is well-motivated and provides a natural decomposition of the state representation problem. The use of a pre-trained distance-based policy for attention is a practical and interpretable design choice.
- **Comprehensive experimental validation**: The paper evaluates DFR across three distinct urban road networks (Nanjing, Beijing Chaoyang, Shanghai Pudong) with three different RL algorithms (DQN, PPO, GCN+DQN), and reports multiple metrics (Mean GAP, Success Rate, Compactness Rate, Planning Time). The ablation study on k and n parameters is thorough and provides actionable insights.

## Weaknesses
### Major
- **Limited novelty relative to existing work**: The core idea of using shortest-path-based subgraph extraction and local neighborhood features for state representation in graph-based RL is not fundamentally new. The "policy attention" mechanism is essentially a pre-computed shortest-path subgraph selection, and the n-hop neighborhood method is a standard graph operation. The paper does not adequately differentiate its contributions from existing graph sparsification or attention-based methods in the RL literature.
- **Theoretical grounding is overstated**: The paper invokes Predictive State Representations (PSR) to claim theoretical sufficiency of the compressed features (Equation 8), but this connection is superficial. The paper does not provide any formal proof or rigorous argument that the proposed DFR features actually constitute a sufficient statistic for the optimal policy. The PSR discussion appears as a post-hoc justification rather than a guiding design principle.
- **Baseline comparison is incomplete and potentially unfair**: The paper compares DFR-enhanced models against "All Dynamics" (AD) baselines, but AD is an unrealistic and straw-man baseline—no practical system would feed the entire graph's edge weights as state. Missing comparisons against more realistic baselines such as: (a) simple local k-hop features without policy attention, (b) random subgraph sampling, (c) GNN-based encoders that naturally aggregate neighborhood information, or (d) traditional feature selection methods. Without these, it is unclear whether DFR's benefits come from the specific hierarchical design or simply from dimensionality reduction.

### Minor
- **Limited analysis of computational overhead**: The paper claims "negligible additional computational overhead" but does not report the pre-training cost of the distance-based policy or the subgraph extraction time. The planning time comparison (Section 5.2) only reports inference time, not total system cost.
- **Parameter sensitivity is not fully resolved**: The ablation study shows that k and n have complex interactions and that k's impact is "more complex and less predictable." The paper's recommendation to use moderate k and smaller n is vague and does not provide a principled selection criterion.

### Trivial
- The paper uses "dynamics" and "dynamic" in a potentially confusing way (footnote 1), though this is clarified.

## Nice-to-Haves
- A comparison against a learned attention mechanism (e.g., soft attention over graph nodes) rather than the hard, pre-computed policy attention would strengthen the claim that the proposed hard attention is superior.
- An analysis of how the DFR features affect the Markov property (e.g., measuring state aliasing or temporal correlation in the compressed features) would substantiate the theoretical claims.

## Novel Insights
None beyond the paper's own contributions. The paper's main insight—that hierarchical refinement from global to task-relevant to local features improves RL-based DPP—is sensible but not surprising given the existing literature on state abstraction and graph sparsification.

## Suggestions
- Add comparisons against more realistic baselines: (1) local n-hop features without policy attention, (2) random subgraph of similar size, (3) a learned GNN-based state encoder that processes the full graph but outputs a fixed-size embedding.
- Provide a more rigorous theoretical justification for why the proposed features are sufficient for near-optimal decision-making, or temper the theoretical claims.
- Report the pre-training cost and subgraph extraction time to give a complete picture of computational overhead.

## Score and Decision
The paper addresses a relevant problem and presents a clean, well-motivated framework with solid experimental results. However, the novelty is limited—the individual components (shortest-path subgraph extraction, n-hop neighborhoods) are standard techniques, and the paper does not adequately differentiate itself from existing work or provide sufficiently strong baselines. The theoretical claims are overstated relative to the actual contribution. The paper is technically sound and clearly written, but the incremental nature of the contribution places it below the acceptance threshold for ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>