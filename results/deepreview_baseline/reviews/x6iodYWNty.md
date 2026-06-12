## Summary

This paper introduces Neural Predictor-Corrector (NPC), a reinforcement learning framework that unifies diverse homotopy-based problems—including robust optimization, global optimization, polynomial root-finding, and sampling—under a single predictor-corrector structure. NPC replaces hand-crafted heuristics for step sizes and termination criteria with learned neural policies trained via PPO, employing an amortized training regime that enables one-time offline training and zero-shot deployment on unseen instances. Experiments across four problem domains demonstrate that NPC consistently reduces computational cost while maintaining solution quality compared to classical and specialized baselines.

## Strengths

- **Novel unification of diverse problems**: The paper convincingly demonstrates that robust optimization (GNC), global optimization (Gaussian homotopy), polynomial root-finding (homotopy continuation), and sampling (annealed Langevin dynamics) all share a common predictor-corrector structure under the homotopy paradigm. This is a genuinely valuable conceptual contribution that enables cross-pollination of ideas between previously siloed communities.

- **Strong empirical results across multiple domains**: NPC achieves substantial efficiency gains (70-90% reduction in iterations and runtime on GNC tasks, 80-85% reduction on HC tasks, 70-75% reduction on ALD tasks) while maintaining comparable accuracy to classical methods. The experiments cover four distinct problem types with multiple benchmarks each, demonstrating broad applicability.

- **Effective amortized generalization**: The training protocol is carefully designed—training on one dataset (e.g., Aquarius for GNC, Ackley with randomized parameters for GH, 4-view triangulation for HC, 10-mode GMM for ALD) and testing on entirely different instances. The consistent generalization success validates the amortized training approach.

- **Clean RL formulation**: The MDP formulation with state components (homotopy level, corrector statistics, convergence velocity) and actions (step size, corrector tolerance) is well-motivated and the ablation study confirms each component contributes meaningfully.

## Weaknesses

### Fatal
None.

### Major

- **Limited comparison with learning-based baselines**: The paper compares against only one learning-based method per domain (CPL for GH, Simulator HC for HC, iDEM for ALD), and these comparisons are often incomplete. For CPL, the paper reports training time as part of runtime, which is an apples-to-oranges comparison since NPC also requires training. For Simulator HC, runtime is not directly comparable due to implementation differences. The paper would benefit from a fairer comparison where all methods are evaluated on the same hardware with training time either excluded or reported separately for all methods.

- **Missing statistical significance measures**: The paper reports averages over 50 trials but does not provide standard deviations, confidence intervals, or statistical significance tests. Given the stochastic nature of both RL training and the underlying problems, this omission makes it difficult to assess whether the observed improvements are statistically meaningful, especially for metrics where differences are small (e.g., accuracy metrics in Tables 1 and 2).

- **Limited analysis of failure modes**: The paper reports 100% success rates for HC tasks but does not discuss cases where NPC might fail or underperform. For instance, what happens when the test distribution shifts significantly from the training distribution? The paper would benefit from a systematic analysis of when and why NPC might fail, including edge cases with extreme problem parameters.

### Minor

- **Scalability concerns**: All experiments are on relatively small-scale problems (2D optimization, small polynomial systems, low-dimensional sampling). The paper does not discuss how NPC would scale to high-dimensional problems (e.g., 1000+ dimensional optimization or sampling), where the homotopy trajectory might be much more complex and the state representation might need to be richer.

- **Limited architectural exploration**: The neural network uses a simple 2-layer MLP with 16 hidden units. While this works well for the tested problems, there is no discussion of architecture sensitivity or whether more complex architectures would improve performance on harder problems.

### Trivial
None.

## Nice-to-Haves

- A comparison with a simple adaptive heuristic baseline (e.g., adaptive step size based on local curvature estimates) would help isolate the benefit of learning from the benefit of adaptivity.
- Visualizing the learned policy (e.g., how step size varies with homotopy level and convergence velocity) would provide insight into what the agent has learned.
- A discussion of the computational cost of training (not just inference) would help practitioners assess the practical utility of the approach.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the predictor-corrector structure, which appears across diverse scientific computing domains, can be effectively controlled by a single learned policy that generalizes across instances within each domain. This suggests that the sequential decision-making challenges in homotopy methods share common structure that can be exploited by RL, even though the underlying problems (optimization, root-finding, sampling) have fundamentally different mathematical formulations. The success of amortized training further suggests that the "geometry" of homotopy trajectories within a problem class is sufficiently regular for a policy to learn generalizable strategies, which has implications for designing learned solvers for other scientific computing tasks.

## Suggestions

1. Add standard deviations or confidence intervals to all reported metrics, especially for the main results in Tables 1-5.
2. Include a comparison where all learning-based methods are evaluated with training time excluded from runtime, to enable fair comparison.
3. Add a systematic analysis of failure cases or distribution shift scenarios to understand the limits of amortized generalization.
4. Discuss scalability to higher-dimensional problems and potential modifications to the state/action space for such settings.

## Score and Decision

The paper makes a novel and valuable contribution by unifying diverse homotopy problems under a single framework and demonstrating that RL can effectively learn adaptive policies that generalize across instances. The empirical results are strong and consistent across four distinct problem domains. The main limitations are the incomplete comparisons with learning-based baselines and the lack of statistical significance measures, which reduce confidence in the quantitative claims but do not invalidate the core contribution. The paper is clearly written, well-motivated, and the experiments are reproducible in principle.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>