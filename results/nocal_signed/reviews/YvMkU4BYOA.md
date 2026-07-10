Now I have all the verification I need. Let me compose the final review.

## Summary

This paper proposes XBIC, a score-based causal discovery method for discrete data that soft-weights BIC's complexity penalty using Shapley values from per-node predictive classifiers. The core idea is that asymmetry in mean Shapley values between two variables provides directional evidence for causal orientation. XBIC is evaluated on 10 benchmark Bayesian networks (6–76 nodes) across 7 sample-size regimes (700 runs), reporting consistent F₁ improvements over BIC-HC (+5.6% relative, +0.04 absolute), GES (+9.6%), and PC (+20.9%).

## Strengths

- **Creative integration of ideas:** Using Shapley values from per-node predictive classifiers to inform structure learning is novel and clearly described. The pipeline (Algorithm 1, Figure 1) is well-structured, and the design choice that XBIC defaults to BIC when directional evidence is absent (w=0 or SHAP(G)=0) properly bounds the downside risk.
- **Systematic evaluation across diverse benchmarks:** The evaluation spans 10 networks from multiple domains (medical, insurance, weather, software) with 6–76 nodes and 7 sample-size regimes, totaling 700 runs. This breadth is commendable and supports the claim of consistent gains.
- **Clear problem identification:** The paper correctly identifies that BIC-based discrete causal discovery struggles to orient edges within Markov-equivalence classes (Section 1, end of Section 2.1), a genuine and well-recognized limitation.

## Weaknesses

### Major

1. **Missing validation of the core premise and critical ablations.** The entire method rests on the claim that mean Shapley-value asymmetry from predictive classifiers tracks causal direction — stated in Section 3.2 as "if $|\bar{\phi}_{1 \rightarrow 2}| \gg |\bar{\phi}_{2 \rightarrow 1}|$, the edge $X_1 \rightarrow X_2$ has stronger directional support than $X_2 \rightarrow X_1$" — but the paper provides no theoretical justification or controlled experiment validating this link. More critically, no ablation rules out the simpler hypothesis that XBIC's gains come from its uniformly softer penalty rather than directional signal. The evaluation does not compare against (a) BIC with a uniformly reduced penalty (e.g., $\lambda \cdot \frac{\log N}{2} \dim(G)$ with $\lambda < 1$) or (b) XBIC with permuted Shapley assignments. Without such controls, the claimed mechanism driving the improvements — directional signal vs. penalty softening — is not established.

2. **Unfair PC comparison inflates the headline result.** Section 4.1 states: "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." PC deliberately leaves edges undirected when CI tests provide no grounds for orientation. Randomly orienting them systematically penalizes PC (correct orientations occur only by chance). This makes the reported 20.9% improvement over PC unreliable. A proper comparison would use CPDAG-level structural metrics (e.g., skeleton F₁, orientation F₁ on orientable edges) or a principled orientation completion (e.g., BIC-based orientation).

### Minor

3. **Modest absolute gains at high computational cost.** The absolute F₁ improvement over BIC is +0.04 (Table 4), yet runtime increases by 100–1000× (Table 5: e.g., 75s → 2139s on Win95pts). Describing XBIC as a "drop-in upgrade" (abstract, conclusion) overstates this: a method that takes 35 minutes on a 76-node network is not practically interchangeable with a 75-second BIC run.

4. **Missing default value for confidence threshold $\tau$.** Section 4.1 reports sensitivity analysis varying $\tau$ between 0.7 and 0.95 but does not specify which value was used as the default in the main experiments. This is a reproducibility gap.

5. **Table 2 lacks uncertainty estimates.** With only 10 repetitions per setting, reporting F₁ deltas without standard deviations or confidence intervals (unlike Figure 2, which does include confidence shading) makes it impossible to assess whether reported deltas are within noise range.

6. **No validation split for hyperparameter $w$.** The paper sweeps $w \in \{1,2,3\}$ and reports $w=2$ as best across all settings (Table 4), but the same data appears to be used for both selection and evaluation. A validation split or nested cross-validation would provide a more rigorous assessment.

7. **Consistency claim lacks formal support.** Section 3.3 argues that XBIC preserves BIC's large-sample consistency because the penalty still grows like $\log N$, but this is stated informally without proof or citation to relevant theory. The graph-dependent scaling factor $c(G)$ complicates the standard consistency argument.

### Trivial

- Minor imprecision in the abstract ("when a candidate parent contributes strongly to its child's likelihood") could be read as conflating Shapley importance (contribution to classifier prediction) with BIC likelihood (model fit), though the method section clarifies the distinction.

## Nice-to-Haves

- Validate the core premise in controlled settings: demonstrate in synthetic data with known ground-truth graphs that pairwise Shapley-value asymmetry correlates with causal direction, varying mechanism type (linear, nonlinear, with/without confounding).
- Add control ablations: (a) uniformly scaled BIC penalty and (b) XBIC with permuted Shapley assignments. If either achieves similar gains to XBIC, the directional signal is not the source of improvement.
- Fix PC comparison: use CPDAG-level structural metrics or a principled orientation completion, and correct the 20.9% headline accordingly.

## Removed Points

- *"The hyperparameter w is selected on the test data"* — Retained as Minor (item 6) because it is a genuine methodological concern about evaluation rigor. Not removed.
- *"Equation (2) has concerning scaling properties"* — Removed. This is a speculative concern about the effective penalty varying "arbitrarily across networks and sample sizes." The paper does sweep w over three values, and the empirical results show the method works across diverse networks. Without concrete evidence that the scaling causes a specific problem, this is category-driven speculation.
- *"Unreleased code/reproducibility concerns"* — Removed. The paper states code is released.
- *"GES comparison on favorable subset"* — Removed as a standalone criticism. The paper is transparent about GES completion issues and reports XBIC(w=3) as not showing significant SHD advantage. This honesty does not constitute a weakness of the proposed method.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify whether hyperparameter $w$ was selected using a held-out validation set or directly from test results.
- Report the exact default confidence threshold $\tau$ (or justify why no single default was used and report per-value results).
- Include control experiments with uniformly scaled BIC penalty and permuted Shapley assignments to isolate the effect of directional signal from penalty softening.

## Score and Decision

The paper proposes a genuinely creative approach and provides broad empirical evaluation. However, two major weaknesses prevent acceptance in the current form: (1) the core premise linking Shapley asymmetry to causal direction is not theoretically grounded or controlled-validated, and critical ablations that would isolate the directional signal from a trivial penalty-softening effect are absent; (2) the PC baseline comparison uses a random-orientation completion that systematically penalizes PC, inflating the headline 20.9% improvement. These gaps significantly weaken the paper's central claims about its mechanism and its reported margins over baselines.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>