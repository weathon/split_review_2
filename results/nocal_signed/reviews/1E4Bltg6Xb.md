Now let me write the final review incorporating all the analysis.

## Summary

This paper proposes the Dynamics Feature Representation (DFR) framework for RL-based Dynamic Path Planning in road networks. DFR refines global graph dynamics through a two-stage pipeline: (1) a "policy attention" mechanism that extracts a subgraph from top-k shortest paths (guided by a pre-trained distance policy), and (2) an n-hop neighborhood method that further decouples this into node-local feature vectors. The goal is to produce a compact yet sufficient state representation that preserves the Markov property while reducing computational cost.

## Strengths

- **Well-motivated problem.** The trade-off between global completeness and local efficiency in RL state design for path planning is clearly articulated (Sections 1 and 4.1). The paper correctly identifies that naive state representations undermine the Markov property, leading to unstable training.

- **Clean conceptual hierarchy.** The three-level formalization (global W → task-relevant W' → node-local W'') in Equation 5, with corresponding sufficiency conditions (Equations 6–8), provides a principled logical structure that is more rigorous than most ad-hoc state designs in the applied RL literature. This framing is the paper's strongest conceptual contribution.

- **Systematic ablation.** The heatmap study of k and n (Figure 6) explores the interaction between the two hyperparameters with concrete numerical values, yielding the practical insight that moderate n (2–3) saturates performance gains.

## Weaknesses

### Major

- **Missing comparison against existing state representation methods.** The evaluation compares DFR against AD (All Dynamics — the full edge-weight vector fed as a flat input) and a standard GCN+DQN. These baselines demonstrate that compression helps, but they do not establish that DFR's specific form of compression is advantageous. The paper explicitly cites a body of work on state representations for graph-based RL — Francis et al. (2025), Zhao et al. (2025), Lin et al. (2025), Zang et al. (2023), Sun et al. (2025) — and does not compare against a single one of these. Without comparisons to existing state compression strategies (GCN-based graph embeddings with learned pooling, attention-based node selection, or local-observation methods), the central claim that DFR provides a better state representation cannot be evaluated.

- **No statistical rigor.** The paper reports means and standard deviations (e.g., "8.18 ± 1.74 ms") and percentage improvements, but never states the number of independent runs or random seeds. DQN and PPO are high-variance algorithms. The radar charts (Figure 5) show single points with no error bars; the training curves (Figure 6) appear to be single trajectories. Without multiple seeds and significance testing, the reported improvements cannot be assessed for reliability.

### Minor

- **Unsupported temporal dependency claim.** Section 4.2 claims DFR "implicitly captures short-term temporal correlations—such as local congestion propagation and flow continuity." However, DFR's refinement at each timestep operates on a single W_t (dynamics at that timestep) filtered spatially via the subgraph and n-hop neighborhood. There is no temporal aggregation, recurrence, sequence model, or sliding window. The claim is asserted but not implemented.

- **Decorative PSR theory.** Section 4.2 invokes Predictive State Representations as a theoretical foundation, but the connection is analogical. No formal objects are defined (what are the "tests"? what are the "core tests"?), no sufficiency proof is given, and no information-loss bound is established. The statement that "Grounding DFR in PSR principles thus guarantees..." is not supported by any actual grounding in the paper. Removing or substantially rewriting this section would not affect the method's technical content.

- **CR definitional ambiguity.** The Compactness Rate for the no-compression baseline (k=-1, n=-1) is reported as 121.042%. Since CR is defined as "the proportion of the reduced feature dimension after DFR to the original dimension," the no-compression case should yield 100%. The value of 121% suggests either that the "reduced feature dimension" includes state components beyond raw edge weights (making the definition ambiguous), or there is an implementation issue. The discontinuous jump between k=0.4,n=-1 (0.678%) and k=0.6,n=-1 (11.643%) also lacks explanation. These need clarification before the ablation numbers can be fully trusted.

- **Unreported pre-training cost.** The "policy attention" module pre-trains a distance-based RL policy π_d*. The paper claims this incurs "negligible additional computational overhead" (Section 4.3) because it is one-time and offline, but does not report the number of episodes, architecture, or convergence criteria used for this pre-training.

### Trivial

None.

## Nice-to-Haves

- The "policy attention" naming is non-standard (it performs subgraph extraction via shortest-path ranking, not learned weighting). While the paper frames it as "hard, pre-computed attention," a more descriptive name such as "shortest-path subgraph extraction" would avoid confusion.
- Reporting the graph sizes (number of nodes/edges) for each subgraph in the text would improve interpretability.

## Removed Points

These points were raised in the input review but removed after verification against the paper:
- *"Policy attention is not attention and this is a methodological gap"* — The paper explicitly frames this as "hard, pre-computed attention" (Related Work section). This is a defensible if non-standard usage; the underlying operation is valid regardless of naming.
- *"Pre-trained distance policy filters out relevant congestion dynamics"* — The paper addresses this in Section 4.3, arguing that distance is the most fundamental constraint. The ablation's varying k tests whether the subgraph is overly restrictive.
- *"Graph sizes not reported"* — The figure legend indicates nodes/edges counts are present in Figure 4 (in the image), and the extraction method (center + radius) is described.
- *"Planning times not interpretable without hardware"* — Reported as relative comparisons (DFR vs AD), which is standard.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add baselines from the literature.** Include at least one existing state representation method (e.g., GCN-based embeddings with learned pooling from Zang et al. / Sun et al., or a local-observation method like Zhao et al.) to contextualize DFR's performance.
2. **Report multiple seeds.** Run all experiments with at least 5 random seeds and report means with standard deviations. Use statistical significance tests where appropriate.
3. **Clarify the CR definition.** Specify what constitutes the "original dimension" and what is included in the "reduced feature dimension." Explain the 121% value for the baseline configuration.
4. **Remove or substantiate the temporal claim.** Since DFR performs only spatial filtering at each timestep, the claim about capturing temporal correlations should either be removed or supported by a temporal aggregation mechanism.
5. **Remove or formalize the PSR framing.** Either drop the PSR reference or provide a concrete formal argument (define tests/core tests, provide sufficiency proof or information-loss bound).
6. **Report pre-training cost.** Provide the number of episodes, architecture details, and convergence criteria used to train the distance-based policy π_d*.

## Score and Decision

The paper identifies a genuine problem and proposes a clean, well-structured hierarchical approach to state representation for RL-based dynamic path planning. The conceptual framework (three-level formalization with sufficiency conditions) is a genuine strength. However, the empirical evaluation has two major gaps: (1) the comparison set does not include any existing state representation method from the literature the paper itself cites, so DFR's relative advantage is unsubstantiated; and (2) the absence of multi-seed experimental protocols means the reported numbers cannot be assessed for reliability. These gaps prevent the paper from supporting its central claims, but they are addressable with additional experiments rather than being fundamental to the approach.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>