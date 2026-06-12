## Summary

This paper proposes "Probability of Matching," a new batch acquisition strategy for multi-objective Bayesian optimization (MOBO) that jointly considers candidate quality and Pareto front coverage. The key idea is to factorize the probability that a batch exactly matches the true Pareto set into (1) the probability all batch points are Pareto optimal and (2) the probability they collectively cover the full Pareto set. This yields qEHVI-SF, which multiplies qEHVI by a minimum-distance diversity term. Experiments on synthetic benchmarks and a real-world alloy design task demonstrate consistent improvements over qEHVI and QSVGD across hypervolume, EMD, and rediscovery metrics.

## Strengths

- **Principled probabilistic framework**: The factorization in Eq. 7 provides an interpretable decomposition of the batch MOBO objective into quality and coverage components, offering conceptual clarity about why qEHVI underperforms on coverage and how to address it. This framing is genuinely useful for thinking about the problem.

- **Thorough and realistic evaluation**: The real-world alloy inverse design case study is comprehensive, spanning bi-objective, tri-objective, and six-objective tasks with physically meaningful property tradeoffs. The rediscovery ratio metric is practical and well-motivated for materials discovery. Combined with synthetic benchmarks (GM, RE4-7-1) and multiple batch sizes, the experimental scope is strong.

- **Negligible computational overhead**: The complexity analysis (Section 3.3) and runtime experiments (Table 1) convincingly show that the space-filling component adds minimal cost, as the O(q(n+q)d) term is dominated by the O(NmK(2^q-1)) hypervolume computation for moderate batch sizes and objectives.

- **Useful new metric**: The EMD metric, operating in design space rather than objective space, provides a stricter evaluation of Pareto set recovery than IGD and addresses a genuine gap in MOBO evaluation.

## Weaknesses

### Fatal

None.

### Major

- **Gap between the probabilistic framework and the actual implementation**: The paper motivates the approach through the elegant Probability of Matching factorization (Eq. 7), but the actual acquisition function (Eq. 8) is simply qEHVI multiplied by a minimum-distance term. The approximation of P(X ⊆ X*) by "normalized qEHVI" is loose—qEHVI measures expected hypervolume improvement, not the probability of Pareto optimality. The approximation of P(X* ⊆ X | X ⊆ X*) by maximizing minimum pairwise distance is a heuristic proxy for coverage whose theoretical relationship to true coverage probability is not established. The paper acknowledges this gap in the conclusion, but it significantly weakens the claim that this is a principled probabilistic approach rather than an ad hoc composite acquisition function.

- **Limited baselines**: Only qEHVI and QSVGD are compared. QSVGD was originally designed for single-objective BO and requires adaptation with a decay schedule for the hyperparameter η, which the authors themselves note is challenging to tune optimally. Other MOBO methods such as EMMI (mentioned in Section 2.2), PESMO, or Thompson sampling variants for MOBO would strengthen the comparison. Without these, it is difficult to gauge the true advantage of the proposed method over the broader landscape of diversity-aware MOBO strategies.

### Minor

- **Implicit hyperparameters in qEHVI-SF**: The paper claims the method "removes the need for sensitive hyperparameter tuning" compared to QSVGD. However, qEHVI-SF involves implicit design choices—the normalization procedure for qEHVI, the form of the distance metric (L2 vs. others), and the relative weighting between qEHVI and the distance term are all effectively hyperparameters. The formulation in Eq. 8 uses multiplication rather than addition, which implicitly controls the tradeoff, but the choice of multiplicative vs. additive combination is itself a design decision.

- **Inconsistency in robustness claims**: The paper states qEHVI-SF has "stable performance across different batch sizes," but Figure 2 shows meaningful variation (e.g., in the six-objective task of Fig 2f, performance differs between batch sizes). The improvement is more robust than baselines, but the stability claim is overstated.

### Trivial

- Figure 1 caption references "BOILS" methods that appear to be OCR artifacts from replaced figures.

## Nice-to-Haves

- An ablation study separating the effect of the multiplicative combination from an additive one (analogous to QSVGD's formulation) would help isolate whether the probabilistic framing's multiplicative structure provides actual benefit.
- Comparing against additional baselines, particularly EMMI or methods that combine hypervolume with other diversity mechanisms.

## Novel Insights

The key novel insight is that the batch MOBO objective can be decomposed into a quality component (probability all points are Pareto optimal) and a coverage component (probability of covering the full Pareto set), and that these should be estimated jointly rather than via additive regularization with a tunable tradeoff parameter. The argument that diversity should be promoted in the design space rather than the objective space (due to validity, bias, misalignment, and noise-robustness concerns) is well-reasoned, though not entirely new. The multiplicative combination naturally balances quality and coverage without a weight hyperparameter, which is conceptually cleaner than additive approaches.

## Suggestions

- Provide tighter justification for why normalized qEHVI approximates P(X ⊆ X*), or alternatively, frame the method more honestly as a heuristically motivated composite acquisition function with a probabilistic intuition.
- Expand baseline comparisons to include at least one additional diversity-aware MOBO method to strengthen the empirical contribution.
- Include an ablation on the multiplicative vs. additive combination structure to validate the claim that the unified probabilistic framework provides benefit beyond its individual components.

## Score and Decision

The paper presents a clear conceptual framework for batch MOBO with solid empirical evaluation across synthetic and real-world tasks, a practical new metric, and minimal computational overhead. However, the connection between the elegant probabilistic framework and the actual implementation is loose, the baseline comparisons are limited to two methods (one of which was adapted from single-objective BO), and the claimed advantages of hyperparameter-free design are overstated. The contribution is incremental but useful, with the real-world alloy study being a genuine highlight.

MY FINAL SCORE: 5.0
MY FINAL DECISION: Accept