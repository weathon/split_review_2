## Summary

This paper proposes methods for learning the Minimum Action Distance (MAD) — the minimum number of actions needed to transition between states in an MDP — from state trajectories alone, without requiring reward signals or action labels. The authors introduce two learning algorithms (MadDist and TDMadDist), a novel simple quasimetric function for asymmetric distance estimation, and a benchmark suite of environments with known ground-truth MAD for evaluation. Empirical results demonstrate that MadDist outperforms existing baselines on both representation quality metrics and a downstream planning task.

## Strengths

- **Well-motivated problem formulation**: Learning MAD from trajectories without actions or rewards is a clean, well-defined problem with clear downstream applications. The paper clearly articulates why MAD is a useful quantity (robust to transition probability changes, serves as a heuristic for planning, enables reward shaping) and positions it relative to stochastic shortest path and temporal distance.

- **Elegant scale-invariant loss design**: The MadDist loss (Eq. 5) divides by the trajectory distance `j-i`, preventing distant state pairs from dominating the loss simply due to larger error magnitudes. This is a simple but effective improvement over prior work (Eq. 2), and the empirical results confirm its impact.

- **Comprehensive benchmark suite**: The environments span discrete/continuous state spaces, deterministic/stochastic dynamics, symmetric/asymmetric transitions, and noisy observations — all with computable ground-truth MAD. This is a valuable contribution for controlled evaluation and will be useful to the community.

- **Strong empirical results in downstream planning**: Table 1 shows MadDist achieves near-perfect success rates (1.00 ± 0.00) across multiple PointMaze environments, including challenging "Stitch" variants requiring composition from disconnected trajectories and large-scale "Giant" environments. These results convincingly demonstrate practical value.

- **Clear exposition and honest framing**: The paper is well-written, with the motivation, methods, and experiments presented in logical order. The distinction between MAD and SSP is articulated clearly (Section 4), and the limitations of the approach (e.g., MAD being a lower bound in stochastic settings) are acknowledged.

## Weaknesses

### Fatal
None.

### Major

- **TDMadDist consistently underperforms MadDist**: Across all environments in Figure 3, TDMadDist achieves lower correlation and higher CV than MadDist. In Table 1, TDMadDist has high variance (e.g., 0.99 ± 0.05 vs 0.93 ± 0.17 in Giant Navigate, but 0.74 ± 0.26 vs 0.99 ± 0.07 in Giant Stitch). The paper does not adequately explain why the TD-based approach fails to improve over the direct method, which weakens the paper's second algorithmic contribution. The authors should either explain when/why TDMadDist would be preferred, or acknowledge it as a less successful variant.

- **Limited baseline comparison**: The paper compares against only two baselines (QRL and Hilbert). Many other representation learning approaches exist that could serve as baselines, including bisimulation-based methods, successor features, contrastive learning methods, and time-contrastive representations — all of which are discussed in Section 2 but not compared empirically. This makes it difficult to fully assess the relative contribution of the quasimetric versus the learning objective.

- **No demonstration on actual RL tasks**: The downstream task is a planning task using the learned distances directly (Table 1). Showing integration into a full goal-conditioned RL pipeline would substantially strengthen the practical impact argument, particularly given that goal-conditioned RL and reward shaping are cited as key motivating applications throughout the paper.

### Minor

- **Leveraging path distances as supervision is not entirely novel**: The core idea of using trajectory indices to derive upper bounds on distances (L_c term) is inherited from Steccanella & Jonsson (2022). The contribution is the combination with quasimetrics and scale-invariant losses, which is useful but somewhat incremental.

- **Quasimetric ablation deferred to appendix**: The choice of quasimetric (d_simple, d_WN, d_IQE) is a central design decision, but the ablation study is relegated to Appendix E. Presenting key ablation results in the main text would strengthen the argument that d_simple is competitive with more complex alternatives.

- **The contrastive term L_r (Eq. 6) is somewhat ad hoc**: Random state pair separation with a hyperparameter d_max is introduced without strong theoretical motivation. The sensitivity to d_max is not discussed in the main text.

### Trivial

- The paper notes "see Appendix A" for a proof that d_MAD is the unique solution to Eq. 1, but this is essentially a standard result from shortest path theory. The claim could be stated more concisely.

## Nice-to-Haves

- A discussion of computational costs comparing MadDist, TDMadDist, QRL, and Hilbert would be informative, especially given the differing quasimetric complexities.
- Sensitivity analysis for key hyperparameters (w_r, w_c, H_c, d_max, α) presented in the main paper.
- Experiments on environments with visual observations (e.g., image-based states) to test scalability beyond tabular or low-dimensional state spaces.

## Novel Insights

The paper makes a useful conceptual contribution by framing MAD learning as a self-supervised problem decoupled from actions and rewards, and by rigorously establishing that asymmetric distance metrics are essential for environments with irreversible dynamics. The empirical finding that a simple quasimetric (d_simple) outperforms more elaborate alternatives like IQE on this specific task is a practical insight worth noting — it suggests that for MAD learning, the learning objective (scale-invariant loss with trajectory-derived constraints) matters more than the quasimetric architecture.

## Suggestions

- Add at least 2-3 more baselines from the related work (e.g., successor features, bisimulation-based embeddings, contrastive methods) to provide a more complete comparison landscape.
- Integrate MadDist into a goal-conditioned RL agent to demonstrate end-to-end value beyond planning.
- Provide a clearer narrative about when TDMadDist should be preferred over MadDist, or frame it as an ablation/exploration rather than a primary contribution.
- Move key ablation results (quasimetric choice, dataset size sensitivity) into the main text to support design decisions.

## Score and Decision

The paper addresses a well-defined problem with a clean formulation, proposes practical improvements over prior work, introduces a useful benchmark suite, and demonstrates strong empirical results particularly in downstream planning. The main limitations are that the second algorithm (TDMadDist) doesn't clearly outperform the first, baseline comparisons are narrow, and the overall contribution is somewhat incremental beyond the scale-invariant loss and quasimetric combination. However, the benchmark suite, the clarity of exposition, and the convincing planning results provide meaningful value to the community.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>