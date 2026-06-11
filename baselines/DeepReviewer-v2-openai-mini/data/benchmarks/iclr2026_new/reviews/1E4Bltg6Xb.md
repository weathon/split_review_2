## Summary
This paper proposes a **Dynamics Feature Representation (DFR)** framework for reinforcement learning-based dynamic path planning in urban road networks. The core idea is a hierarchical two-stage refinement: (1) a policy attention mechanism that extracts a task-relevant subgraph using distance-based shortest paths, and (2) an n-hop neighborhood method that further prunes this subgraph to agent-centric local features. The resulting low-dimensional state vector aims to preserve Markovian sufficiency while drastically reducing computational cost. Experiments on three Chinese urban road networks (Nanjing, Chaoyang Beijing, Pudong Shanghai) with DQN, PPO, and GCN+DQN baselines show that DFR improves mean GAP from 0.170 to 0.095, increases success rate from 0.884 to 0.905, reduces feature dimensionality to under 5.7% of the original, and cuts planning time by 46–86%.

**Overall assessment:** The paper addresses a relevant and practically important problem — state representation for RL-based dynamic path planning. The DFR framework is intuitive and the empirical results suggest meaningful improvements. However, the paper has several significant weaknesses that limit its current contribution. The theoretical grounding (PSR-based) is asserted but not formally connected to the specific DFR design. The MDP formulation has a temporal modeling gap (agent-step time vs. wall-clock time). The experiments lack multi-seed statistical significance tests, the congestion dynamics are not described, and the AD (all dynamics) baseline may be at an unfair capacity disadvantage. The distance-based policy attention assumption that optimal dynamic paths overlap with static shortest paths is critical but untested. Novelty assessment cannot be completed due to external literature search being unavailable in this run.

**Central tension:** The paper makes strong claims about Markov property restoration and PSR-grounded theoretical guarantees, but the actual mechanism is a heuristic graph sparsification pipeline whose effectiveness is demonstrated empirically rather than theoretically. The paper would benefit from repositioning as an empirical engineering contribution with honest scope boundaries, rather than claiming theoretical grounding that is not formally justified.

## Strengths
1. **Well-motivated and practical problem.** The completeness-efficiency trade-off in state representation for RL-based DPP is a genuine challenge with direct practical implications for urban logistics, intelligent transportation, and on-demand delivery. The paper clearly articulates this trade-off and positions DFR as a targeted solution.

2. **Simple, intuitive, and computationally efficient design.** The two-stage refinement (policy attention → n-hop neighborhoods) is conceptually clean and easy to understand. The use of a one-time offline pretrained distance-based policy for subgraph extraction is computationally efficient and exploits the static road network topology, which does not change over time. The computational overhead reduction (46-86% planning time reduction, CR below 5.7%) is substantial and practically relevant.

3. **Consistent empirical improvement across multiple RL algorithms.** The experimental results show that DFR improves GAP, SR, and planning time consistently across DQN, PPO, and GCN+DQN, and across three different urban networks (Nanjing, Beijing Chaoyang, Shanghai Pudong). This multi-algorithm, multi-city evaluation provides reasonable evidence that the benefit of DFR is not algorithm-specific or city-specific.

4. **Comprehensive ablation study.** The paper provides a thorough ablation over both key hyperparameters k (policy attention strength) and n (neighborhood size), including heatmaps and training curves. This allows readers to understand the sensitivity of DFR to its two parameters and provides practical guidance for deployment (moderate k, smaller n preferred).

5. **Publicly available code.** The authors provide an anonymous code repository, which supports reproducibility and allows other researchers to build on this work.

## Weaknesses
### W1 (Critical): Missing statistical significance and multi-seed variance reporting

**Evidence:** Page 1 - Section 5.1-5.2 (Experiment Settings and Main Results). The paper reports GAP and SR as point estimates without confidence intervals, standard deviations, or significance tests. The planning time is the only metric reported with mean±std (8.18±1.74 ms). The paper does not state how many independent training runs were conducted.

**Impact:** Without multi-seed variance, the claimed improvements (GAP from 0.170 to 0.095, SR from 0.884 to 0.905) could be within the noise range of a single seed. RL algorithms are notoriously seed-sensitive, and single-run comparisons are not statistically reliable. This undermines the central empirical claim of the paper.

**Required fix:** Report all primary metrics (GAP, SR) as mean±std over at least 5 independent seeds. Add statistical significance tests (paired bootstrap or Wilcoxon) comparing DFR against AD baselines for each algorithm-graph pair. This is a **Must**-fix — without it, the empirical contribution is not verifiable.

---

### W2 (Major): MDP formulation does not properly handle time-dependent dynamics

**Evidence:** Page 1 - Section 3.2 (Markov Decision Process). The state is defined as s_t = {v^t, v_g, f_t} without a time index. The MDP transition and reward functions are written as time-homogeneous (no explicit dependence on wall-clock time). Footnote 2 acknowledges the dual use of t but does not resolve the modeling issue.

**Impact:** Traffic dynamics W_t evolve with wall-clock time, not agent decision steps. If the agent takes different path lengths (different number of steps), it experiences different calendar times. A state without a time index cannot be Markovian with respect to time-varying edge weights. This means the MDP formulation is incomplete, and the paper's claim that DFR "approximates the Markov property" is addressing a problem that is not properly defined in the first place.

**Required fix:** Augment the state with the current time index t, i.e., s_t = (v^t, v_g, t, f_t). Rewrite the Bellman equation to include time-dependent transitions. Alternatively, explicitly state that the paper assumes stationarity within each episode and relaxes this assumption empirically. This is a **Must**-fix for theoretical correctness.

---

### W3 (Major): PSR-based theoretical grounding is asserted without formal connection to DFR design

**Evidence:** Page 1 - Section 4.2 (Theoretical Basis). The paper invokes Predictive State Representations (PSR) and claims that "grounding DFR in PSR principles guarantees compact, temporally predictive, and theoretically sufficient" representations. However, the paper provides no formal proof or argument that the specific two-stage refinement (distance-based subgraph → n-hop pruning) preserves PSR-sufficiency. The approximation symbol "≈" in Equations (6-8) is undefined — no error metric, no bound, no characterization.

**Impact:** The theoretical claims are substantially overstated. What the paper actually has is an intuitive design hypothesis that is evaluated empirically. Presenting this as a "guarantee" is misleading and will be identified by reviewers as an overclaim.

**Required fix:** Either (a) provide a formal analysis showing that the DFR refinement preserves sufficient statistics for optimal control (unlikely without strong assumptions), or (b) remove the PSR grounding and reposition DFR as a heuristic architecture motivated by the intuition that task-relevant dynamics are sparse. Option (b) is more realistic and honest. This is a **Must**-fix.

---

### W4 (Major): Congestion dynamics generation is unspecified

**Evidence:** Page 1 - Section 5.1 (Scenarios). The paper defines β ∈ [0.1, 1.5] as a congestion factor but does not describe how β evolves over time. Is it a stochastic process? A pre-recorded trace? An adversarial sequence? The correlation structure (or lack thereof) directly affects whether DFR's assumption of "local congestion propagation" is valid.

**Impact:** Without this information, the experiments are not reproducible, and the reader cannot assess whether the tested scenarios are realistic or favorable to DFR. If β varies randomly at each time step, there is no temporal correlation to exploit, and the PSR-based justification collapses entirely.

**Required fix:** Provide the complete dynamics generation process: functional form, parameters, and random seed(s). If using real traffic data, specify the source and preprocessing. This is a **Must**-fix for reproducibility.

---

### W5 (Major): AD baseline may have an unfair capacity disadvantage

**Evidence:** Page 1 - Section 5.1 (Model Training). Both DFR and AD baselines use the same MLP architecture (64-unit embedding + two 64-unit hidden layers). Since AD receives the full graph dynamics (|E|-dimensional input) while DFR receives a compressed representation (≤5.7% of |E|), the AD network has much higher input dimensionality but the same capacity.

**Impact:** Poor AD performance could be due to insufficient network capacity for the larger input, rather than the inherent quality of the state representation. This confounds the comparison and weakens the claim that DFR "improves performance."

**Required fix:** Add a capacity-matched control — either scale the AD network (wider/deeper) to handle its larger input, or add a baseline that uses dimensionality reduction (PCA or random projection) on the full dynamics to match DFR's input size. Also report the number of parameters for each model variant. This is a **Nice-to-have** but recommended as **Must** for a clean empirical comparison.

---

### W6 (Major): Distance-based policy attention assumption is critical and untested

**Evidence:** Page 1 - Section 4.3 (Policy Attention Method). The policy attention extracts the top-k shortest paths using static distance. The paper argues that "distance naturally serves as one of the most fundamental constraints," but does not test the overlap between optimal dynamic paths and static shortest paths.

**Impact:** If the optimal dynamic path (under time-varying congestion) deviates substantially from the static shortest paths, DFR permanently excludes it. This is a structural limitation — even with optimal k and n, the correct path may be unreachable. Without quantifying this overlap, the practical scope of DFR is unknown.

**Required fix:** Compute and report the overlap ratio between optimal dynamic paths and the static shortest path set for the tested scenarios. Add a discussion of conditions under which the distance-based proxy may fail (e.g., severe local congestion, road closures). This is a **Must**-fix for honest scope disclosure.

---

### W7 (Major): Introduction has grammatical issues and redundancy

**Evidence:** Page 1 - Introduction (lines 12-14). Sentence fragment: "Global methods that encode the entire graph dynamics to ensure information completeness but are computationally prohibitive Liu et al. (2024)." Redundancy: "effectively represent traffic dynamics effectively." Overclaim: "remarkable acceleration in convergence."

**Impact:** While not fatal, these writing issues reduce professionalism and may raise reviewer concerns about the overall carefulness of the work.

**Required fix:** Correct the sentence fragment and remove the redundancy. Replace "remarkable" with the actual measured convergence speedup (e.g., "DFR achieves convergence in X episodes vs Y episodes for the baseline"). This is a **Nice-to-have** but recommended.

---

### W8 (Minor): Radar chart combines incomparable quantities

**Evidence:** Page 1 - Section 5.2 (Figure 5). The radar chart and triangle area metric combine 1-CR (Compactness Rate, a property of the state representation) with SR and GAP (planning performance metrics).

**Impact:** Mixing a design choice metric (how much the state is compressed) with task performance metrics gives a misleading overall assessment. An algorithm with excellent GAP/SR but a larger CR (less compression) would appear worse, even though compression is a means to an end, not an end in itself.

**Required fix:** Report GAP, SR, and CR separately in a table alongside the radar charts. The triangle area should not be used as a composite quality metric without justification.

---

### W9 (Minor): Conclusion is generic and lacks specificity

**Evidence:** Page 1 - Conclusion (line 144). The conclusion uses vague language ("significantly affects the performance," "provides insights") rather than summarizing what was specifically found. The limitation section only mentions manual k/n selection and does not discuss the distance-based attention limitation or the synthetic dynamics limitation.

**Required fix:** Restructure the conclusion to: (1) state 2-3 specific validated findings with numbers, (2) list bounded limitations with concrete conditions, and (3) propose specific next steps.

---

### W10 (Deferred): Novelty and literature positioning cannot be assessed

**Evidence:** External literature search is unavailable in this run (Retrieval-Disabled Mode). The paper claims novelty for the DFR framework, policy attention mechanism, and n-hop neighborhood method, but without access to related work, I cannot verify whether similar hierarchical sparsification approaches have been proposed for RL-based path planning or related graph decision-making tasks.

**Status:** Deferred to manual verification. The authors should ensure comprehensive comparison against existing hierarchical state representation methods and attention-based graph sparsification techniques in the revision.

## Score
**Final Score: 5.5/10**

**Scoring rationale:**

This score prioritizes research value, novelty, and validity as primary dimensions, consistent with the scoring policy.

- **Research value (6/10):** The problem of state representation for RL-based dynamic path planning is practically relevant, and the DFR framework offers an intuitive and computationally efficient approach. The 46-86% planning time reduction with maintained or improved path quality is practically significant. However, the value is limited by incomplete empirical validation (no multi-seed statistics, unspecified dynamics generation) and unverified assumptions (distance-based path overlap with optimal dynamic paths).

- **Novelty (5/10):** The two-stage refinement (policy attention + n-hop neighborhoods) appears to be a reasonable engineering contribution. However, the paper's claim of "novel hierarchical approach" is self-proclaimed without literature comparison to establish what is genuinely new. Novelty assessment is partially deferred due to external literature search being unavailable in this run. The individual components (shortest-path-based subgraph extraction, n-hop neighborhood pruning) are known techniques individually — the novelty lies in their specific combination for DPP state representation.

- **Validity/soundness (5/10):** The paper has significant gaps in theoretical and empirical validity. The MDP formulation is incomplete (missing time index in state), the PSR-based theoretical guarantees are overstated, the experiments lack statistical rigor, and key experimental details (congestion dynamics generation) are omitted. These issues reduce confidence in the reported results.

- **Reproducibility (6/10):** Code is provided, which is positive. However, the missing dynamics generation details significantly hinder full reproducibility. The network architectures and hyperparameters are well-specified.

**Post-revision potential:** With the following must-fix revisions, the score could rise to 7-7.5/10: (1) add multi-seed experiments with statistical tests, (2) fix the MDP time-index issue, (3) remove or substantially revise the PSR theoretical claims, (4) specify the dynamics generation process, (5) add capacity-controlled baselines, and (6) quantify the overlap between static shortest paths and optimal dynamic paths.

**Summary:** The paper presents a practically motivated idea with promising initial results, but the current level of empirical rigor and theoretical precision is insufficient for a strong venue. The core weaknesses are fixable with additional experiments and more honest positioning of the contribution.