## Summary

This paper introduces Generative Trajectory Policies (GTP), a new policy class for offline RL that learns the full solution map of a continuous-time ODE governing the generative process. The authors first present a unified perspective showing that diffusion models, flow matching, consistency models, and consistency trajectory models are all instances of learning this ODE flow map. They then propose two theoretically-grounded adaptations—score approximation for efficient/stable training and an advantage-weighted objective for value-driven policy improvement—to make this framework practical for offline RL. Empirical results on D4RL benchmarks achieve state-of-the-art performance, including perfect scores on several AntMaze tasks.

## Strengths

- **Clear unified perspective**: The paper provides an elegant and well-structured framework that connects a family of modern generative models (diffusion, flow matching, consistency models, consistency trajectory models, shortcut models, mean flows) through the lens of a continuous-time ODE solution map. This offers valuable clarity for the design space of generative policies in RL.
- **Strong empirical results**: GTP achieves state-of-the-art performance on D4RL, outperforming prior generative policies (Diffusion-QL, Consistency-AC, QGPO, BDM) on both Gym and AntMaze suites. The gains on AntMaze are particularly striking (80.6 average vs 78.3 for QGPO, with perfect 100.0 on antmaze-umaze).
- **Principled adaptations to offline RL**: The paper identifies three concrete practical challenges (computational cost, training instability, objective misalignment) and provides theoretically-motivated solutions. Theorem 1 justifies the score approximation with an \(O(h^p)\) error bound, and Theorem 2 provides a formal derivation for advantage-weighted generative training.
- **Well-designed ablation study**: Table 3 convincingly demonstrates that both key components are essential. The score approximation reduces training time and improves stability, while the variational guidance avoids the divergence issues of linearly combining generative loss with a Q-learning term.

## Weaknesses

### Major
- **Theoretical support for score approximation is incomplete**: Theorem 1 addresses only the bias of replacing the true score with the surrogate (difference in expected objectives is \(O(h^p)\)), but does not discuss variance. The practical objective uses a single noisy sample per data point, and the variance of this estimator may be large, especially at small \(h\). The paper claims stability benefits but does not provide any theoretical or empirical analysis of the variance. This gap weakens the theoretical grounding of the core adaptation.
- **Overclaimed "perfect scores"**: The abstract and introduction claim "perfect scores on several notoriously hard AntMaze tasks," but Table 2 shows only one perfect score (antmaze-umaze at 100.0). antmaze-medium-diverse (94.2) and the large tasks (53.5, 71.0) are not perfect. The claim is misleading and should be revised.
- **Moderate novelty of the unified framework**: The paper presents the ODE trajectory perspective as a key contribution, but this view is already present in Consistency Trajectory Models (Kim et al., 2024) and Mean Flows (Geng et al., 2025). The paper's main technical novelty lies in adapting this framework to offline RL, not in the framework itself. The derivation of the advantage-weighted objective (Theorem 2) is also a straightforward application of standard KL-regularized RL results.

### Minor
- **Missing direct comparison to CTM or Mean Flows**: Given that the paper frames these methods as special cases of the same framework, it would strengthen the contribution to compare GTP against a direct application of CTM or Mean Flows to offline RL. The current baselines do not include these methods.
- **Some missing values in Table 2**: Consistency-AC (C-AC) does not report scores for antmaze-medium-diverse, antmaze-large-play, or antmaze-large-diverse. No explanation is provided.
- **Limited domain coverage**: Experiments are restricted to D4RL locomotion and AntMaze. While standard, the claims of resolving the expressiveness–efficiency trade-off would benefit from validation on domains requiring high-dimensional or multi-modal action distributions (e.g., robot manipulation).

### Trivial
- The notation in Eq. (17) could be clarified: \(\tilde{a}_u = a + u \cdot z\) is a closed-form generation without ODE solving, but this relies on the linear forward process defined earlier. The paper could make this connection more explicit.

## Nice-to-Haves

- An empirical analysis of the variance of the score approximation estimator, showing how it behaves across different \(h\) and time horizons, would strengthen the theoretical claims.
- A sensitivity study on the number of sampling steps \(K\) for GTP versus diffusion and consistency policies would better demonstrate the claimed trade-off resolution.
- Comparison against CTM or Mean Flows adapted for offline RL would help isolate the contribution of the specific training techniques.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Revise the claim about "perfect scores on several notoriously hard AntMaze tasks" to reflect the actual results (only one perfect score).
- Add a variance analysis (either theoretical or empirical) for the score approximation to support the stability claim.
- Include a comparison to CTM or Mean Flows as baselines if those methods can be adapted to offline RL within reasonable effort.
- Provide a table or figure showing performance vs. number of sampling steps for GTP, diffusion, and consistency policies to directly quantify the expressiveness–efficiency trade-off.

## Score and Decision

Score: 8

Decision: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>