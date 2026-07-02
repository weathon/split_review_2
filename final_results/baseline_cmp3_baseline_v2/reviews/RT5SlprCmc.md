## Summary
The paper introduces two algorithms (MadDist and TDMadDist) for learning the Minimum Action Distance (MAD) between states in an MDP from state-only trajectories, without requiring rewards or action labels. The methods use quasimetric distance functions to capture the natural asymmetry of MAD, and a scale-invariant loss that prevents distant state pairs from dominating training. Empirical evaluations on a diverse suite of environments with known ground-truth MAD show that MadDist consistently outperforms prior quasimetric (QRL) and symmetric (Hilbert) baselines in both representation quality and downstream planning success.

## Strengths
- **Well-motivated problem**: Learning a useful state metric from accessible data (state trajectories) is directly applicable to goal-conditioned RL, reward shaping, and transfer learning. The paper clearly argues why MAD—rather than on-policy temporal distances or Laplacian embeddings—is a desirable target.
- **Principled handling of asymmetry**: By adopting quasimetrics (the proposed simple quasimetric, Wide Norm, IQE) the method can represent directed distances that arise in irreversible environments (e.g., KeyDoor, CliffWalking). This is a clear improvement over prior symmetric approaches.
- **Clean and effective algorithmic design**: The scale-invariant loss (Equation 5) and trajectory-level upper-bound constraints (Equation 7) are simple yet demonstrably superior to prior formulations. MadDist’s strong empirical performance across deterministic/stochastic, discrete/continuous, and noisy settings supports the design choices.
- **Thorough controlled evaluation**: The suite of environments with known ground-truth MAD enables precise quantitative comparison. The paper reports multiple metrics (Spearman, Pearson, CV) and includes a downstream planning task, providing converging evidence that better MAD approximation translates to practical gains.
- **Consistent superiority over baselines**: MadDist achieves higher correlation, lower CV, and near-perfect planning success across all PointMaze variants. QRL is competitive on some metrics but lags in planning; the symmetric Hilbert baseline is clearly inadequate for asymmetric MDPs.

## Weaknesses
### Major
- **TDMadDist underperformance not explained**: TDMadDist (the TD variant) consistently underperforms MadDist, sometimes even falling below QRL. The paper attributes this to “the choice of hyperparameters” and “the use of a TD-based objective” but provides no analysis. Understanding when a TD formulation would be beneficial (e.g., online/streaming settings) is important for practitioners. In its current form, TDMadDist appears to offer no advantage over the simpler MadDist, raising the question of whether it should be presented as a co-equal contribution.
- **Inconsistency in reported runs**: The text (Section 7) states results are averaged over five random seeds, but Figure 3 caption says “three random seeds”. The figure itself shows min/max shading rather than standard deviation, making it difficult to assess variability. This inconsistency weakens confidence in the reported numbers.

### Minor
- **Limited comparison to alternative asymmetric methods**: QRL (Wang et al., 2023b) is the only quasimetric baseline. Given that the proposed simple quasimetric is claimed to be effective, a head-to-head comparison of different quasimetric functions (simple, Wide Norm, IQE) within the same MadDist framework would strengthen the argument that the *learning algorithm*—not just the distance function—is the source of improvement.
- **Missing justification for the simple quasimetric**: Equation 3 defines a convex combination of max and average of relu differences. The paper proves its quasimetric properties in Appendix B (removed) but does not intuitively explain why this particular form works better than, e.g., the Wide Norm. A brief intuition would help readers understand the design principle.

### Trivial
- Equation 9 appears garbled (“$12(9))$”); likely a parser artifact. Not a flaw in the paper.

## Nice-to-Haves
- An ablation study varying the amount of trajectory data, showing performance degradation, is mentioned in Appendix E and would be valuable in the main text to set practical expectations.
- A small-scale study on a stochastic MDP where MAD and SSP differ would clarify the limitations of MAD approximation and the potential benefit of future extensions.

## Novel Insights
Beyond the paper’s own contributions, the key takeaway is that a simple scale-invariant regression loss on trajectory-level state pairs, combined with a quasimetric that respects directedness, suffices to learn a globally coherent distance function that closely mirrors the ground-truth MAD. Prior work relied on either local constraints (QRL) or symmetric approximations (Hilbert); the paper demonstrates that global supervision via trajectory indices is both practical and highly effective, even when trajectories are collected by a random policy. This suggests that the structure of many environments can be captured by counting steps along sampled paths, without needing complex contrastive or spectral objectives.

## Suggestions
- Clearly state the number of seeds used consistently throughout the paper, and consider reporting standard deviation or confidence intervals instead of min/max ranges.
- Add a discussion (even brief) explaining why TDMadDist underperforms—e.g., bootstrapping may propagate errors in the offline setting, or the scale-invariant loss interacts poorly with TD targets.
- Consider including a simple ablation: MadDist with symmetric Euclidean distance vs. with the proposed simple quasimetric, to isolate the benefit of asymmetry.

## Score and Decision
MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>