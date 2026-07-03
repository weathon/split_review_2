## Summary

The paper proposes a Dynamics Feature Representation (DFR) framework for RL-based Dynamic Path Planning (DPP) in urban road networks. DFR progressively refines global traffic dynamics into compact, decision-relevant features through a two-stage process: (1) a pre-trained distance-based policy attention mechanism that selects top-k shortest paths to form a task-relevant subgraph, and (2) an n-hop neighborhood method that extracts local dynamics features from this subgraph relative to the agent's current node. Experiments on three real urban road networks with DQN, PPO, and GCN+DQN base algorithms show that DFR reduces planning time by 46-86% while maintaining or improving solution quality relative to "All Dynamics" baselines.

## Strengths

1. **Clear hierarchical refinement framing with formal sufficiency conditions** (Section 4.2, Equations 5–8): The paper formalizes the compression problem as a progressive chain W → W′ → W′′ with explicit optimality-preservation conditions at each stage (π* conditioned on W′ ≈ π* conditioned on W, etc.). This goes beyond prior ad hoc state designs by making explicit what information each stage is intended to preserve.

2. **Offline-precomputable policy attention for practical efficiency** (Section 4.3, line 149): The distance-based policy attention is pre-trained on static distances only, which are time-invariant. The resulting subgraphs are "pre-computable" (line 153), meaning the planning-time reduction (85.59% for DQN, 46.08% for GCN+DQN, 79.32% for PPO) does not trade off runtime for representation quality at inference time — a practical advantage over methods that must recompute attention weights from dynamic data at each step.

3. **Consistent empirical gains across three cities and three RL algorithms** (Section 5.2, Figure 5): DFR-enhanced models consistently show improved (1-GAP, SR, 1-CR) trade-offs across Nanjing, Beijing Chaoyang, and Shanghai Pudong. Planning time drops to 8.18±1.74 ms for DQN/PPO and 27.26±6.8 ms for GCN+DQN (vs. substantially higher AD variants), while solution quality is maintained or improved.

4. **Systematic ablation study with actionable parameter guidance** (Section 5.3, Figure 6): The heatmap exploration over 6×5=30 (k, n) configurations provides concrete tuning recommendations (e.g., "configurations with moderate k and smaller n should be preferred," line 253). The analysis documents that n-hop widening quickly reaches diminishing returns and that policy attention (k) has a more complex, less predictable effect — providing useful guidance for practitioners.

## Weaknesses

### Fatal

None.

### Major

1. **Distance-based filtering creates a structural mismatch with the time-minimization objective** (Section 4.3, line 149): The policy attention subgraph is built from top-k *shortest-distance* paths, but the DPP objective is *travel time* (Equation 2), which depends on both distance and congestion (β as in Equation 9). A longer-distance but congestion-free path could be time-optimal, yet DFR's first filtering step would discard it by construction. The paper acknowledges this design choice ("distance naturally serves as one of the most fundamental constraints") but provides no experiment or argument showing that the set of near-optimal time-minimizing paths is a subset of top-k shortest-distance paths under realistic traffic variation. This is a core limitation of the approach — not necessarily fatal, since the empirical results suggest the retained subgraph is often sufficient, but the paper should address it directly rather than relying on plausibility reasoning.

2. **No statistical significance or multi-seed reporting for the core quality metrics** (Section 5): The paper reports single GAP and SR values per configuration with no indication of variance across random seeds. Planning time has standard deviations, but the primary quality metrics do not. Given stochastic dynamics and randomized source-goal sampling, single-run results could be dominated by noise. This significantly weakens the reliability of the reported improvements.

3. **Convergence acceleration is claimed but not substantiated** (Abstract, line 9; Section 5.2): The abstract claims "remarkable acceleration in convergence," but the only training curves shown are in Figure 6 (bottom), which cover DQN-based models on a single subgraph. No quantitative convergence-speed metric (e.g., episodes to reach a performance threshold) is reported, and no convergence curves are provided for the main results or for PPO/GCN+DQN variants.

4. **Synthetic dynamics lack spatiotemporal structure** (Section 5.1): The congestion factor β is sampled from a uniform range [0.1, 1.5], but the paper does not specify whether it evolves with temporal or spatial correlation. If β is i.i.d. at each time step per edge, the setting lacks real-world congestion patterns (rush-hour propagation, accident spillover, etc.), which are the very phenomena where non-local dynamics matter most. The experimental design may inadvertently favor DFR by making local information largely sufficient.

### Minor

5. **Graph sizes are never reported** (Section 5.1): The paper uses subgraphs extracted "by radius around a center node" but never reports the number of nodes or edges in each subgraph. This makes the compression (CR) numbers and scalability claims hard to interpret — a CR below 5.7% means very different things if the original graph has 50 nodes vs. 5000.

6. **PSR grounding is asserted without demonstration** (Section 4.2, lines 129–135): The connection to Predictive State Representations is mentioned as a theoretical basis, claiming W″_t "preserves all decision-relevant information" and is "theoretically sufficient." No formal proof, bound, or empirical validation of PSR properties is provided. This reduces the PSR reference to a conceptual analogy rather than a substantive theoretical foundation.

7. **Radar charts hide absolute values** (Figure 5, Section 5.2): The main results are presented as radar charts of scaled metrics (1−GAP, SR, 1−CR), which show relative shapes but obscure the actual GAP and SR numbers. The paper describes trends ("larger triangle areas") without reporting the underlying numerical values that would let a reader verify the magnitude of improvement. The ablation study provides numerical values, but only for one subgraph.

8. **DFR can substantially degrade performance with poorly chosen parameters** (Section 5.3, heatmaps): Configurations like k=0.2,n=1 (SR=0.764 vs baseline 0.884) and k=1.0,n=1 (SR=0.672, GAP=0.174 vs baseline 0.884, 0.170) are strictly worse than the AD baseline. The paper acknowledges this in Section 6 but frames parameter sensitivity as a minor "manual" inconvenience rather than a deeper concern that the distance-based filter can systematically exclude task-relevant information when parameters are poorly chosen.

### Trivial

9. Some figure references in the extracted text appear duplicated or contain placeholder descriptions. (Parser artifact, but the original submission should verify these render cleanly.)

## Nice-to-Haves
- Design a controlled experiment where the shortest-distance path is deliberately time-suboptimal due to congestion on key edges, to empirically test whether DFR's distance filter causes the agent to systematically miss better routes.
- Report the temporal dynamics generation process precisely: is β sampled independently per time step? Does it follow a Markov process or random walk? What spatial correlation (if any) exists between adjacent edges?
- Provide convergence curves (GAP/SR vs. episodes) for all algorithm variants (PPO, GCN+DQN), not just the DQN ablation.

## Removed Points

The following points from the inputs were removed with justification:

1. **"AD baseline is a strawman" (Harsh Critic Issue 2):** Partially removed. The AD baseline feeds *all* available information — it is information-rich, not deliberately weak. The ablation study (k=-1.0 configurations) provides the n-hop-only baseline the critic asks for, and GCN+DQN+AD processes the full graph with GCN, which is what the critic requests as a "proper graph encoder." The architectural simplicity of the AD MLP does not make it a strawman; compressing global dynamics into a local representation and measuring the information loss is exactly the right comparison. The critic's sub-point about missing "local dynamics only" baselines is addressed by the k=-1.0 ablation rows. Moved to Nice-to-Haves for the reader's consideration.

2. **"Single source-destination pair per subgraph" (Harsh Critic Issue 3b):** Factually inaccurate. The paper states source and goal nodes are "randomly sampled from a subgraph" and each of the 75,600 training episodes corresponds to "a new scenario" (line 177). Multiple (source, goal) pairs are evaluated.

3. **"No comparison to other DPP methods" (Harsh Critic):** The paper explicitly scopes itself (footnote 3) to investigating DFR *within the RL paradigm*, and the RL advantages over non-RL methods are cited as established. This is a legitimate scoping choice.

4. **"DFR does not reduce cost of monitoring" (Harsh Critic Section notes):** The paper's claim is about *representation* compression, not sensor cost. Lines 153 state that DFR "reduces the scope of dynamics feature collection," which is a monitoring claim. However, this is a minor imprecision, not a critical flaw.

5. **PSR theoretical grounding (Strength Finder point 4):** Removed because it conflicts with verified Weakness #6 — the PSR connection is asserted without proof, so claiming it as a strength would be inconsistent.

6. **Generic/superficial strengths from Strength Finder:** Removed generic statements about "addressing an important problem" that lack specific evidence from the paper. Only concrete, evidence-backed strengths are retained.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any observation about the method that the paper itself fails to identify.

## Suggestions

1. Report all main results numerically in a table (GAP, SR, PT) with means and standard deviations over at least 5 random seeds, replacing or supplementing the radar charts.
2. Clarify the temporal dynamics generation process — is β temporally correlated? If not, add experiments with structured congestion patterns (e.g., rush-hour waves, accident propagation).
3. Add a dedicated experiment to test the distance-vs-time mismatch: construct a scenario where the shortest-distance path is heavily congested and a longer alternative is time-optimal, then measure whether DFR (with optimally tuned k,n) can discover the better route.
4. Report the node/edge counts for each subgraph used in the experiments.
5. Provide convergence curves (GAP/SR vs. episodes) for all algorithm variants, and report a quantitative convergence speed metric (e.g., episodes to 90% of final performance).
6. Discuss the structural limitation of distance-based filtering more prominently, and consider adding a "soft" policy attention variant that uses distance-weighted sampling rather than hard thresholding.

## Score and Decision

I was unable to use the calibration tool (an indexing error prevented retrieval). However, based on direct assessment against the ICLR scoring guidelines:

The paper makes a concrete, well-formulated contribution — a hierarchical state representation framework that is novel, clearly described, and has a practical offline-computation advantage. The empirical evidence is consistent across diverse settings (3 cities, 3 RL algorithms), and the ablation study is unusually thorough.

However, the evaluation has important gaps that prevent the paper from reaching the level of rigor expected for acceptance: (1) no multi-seed statistical testing for core metrics, (2) a structural concern about distance-based filtering vs. time-minimization that is reasoned about but never empirically tested, (3) convergence claims made but not substantiated with evidence, and (4) missing basic reporting details (graph sizes, dynamics generation process). These are addressable in revision but weaken the current submission.

The paper is not fatally flawed — the core idea has merit, and the evidence is directionally positive — but it is not strong enough for acceptance in its present form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>