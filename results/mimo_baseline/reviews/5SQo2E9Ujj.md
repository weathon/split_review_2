## Summary

This paper reframes curriculum learning in goal-conditioned RL as selective data acquisition, arguing that curricula structurally reshape the state–goal visitation distribution rather than serving merely as exploration heuristics. Using UVFAs with potential-based reward shaping in a GridWorld environment, the authors compare uniform goal sampling to hand-designed edge-biased curricula and report modest improvements on harder-to-reach edge goals.

## Strengths

- **Clear conceptual framing.** The paper articulates a coherent perspective: curricula as data distribution reshaping rather than exploration heuristics. This lens connects curriculum design to function approximation quality and to broader open-ended learning goals (Hughes et al., 2024), providing a useful conceptual anchor.
- **Transparent reporting.** The authors report means and standard deviations across three seeds, separate results for edge vs. interior goals, and multiple curriculum variants, which allows the reader to assess the evidence honestly.

## Weaknesses

### Fatal

None.

### Major

- **Extremely weak experimental evidence.** The improvements are tiny (overall +0.02, edge +0.08) with large standard deviations (e.g., edge success 0.183 ± 0.131 vs. 0.217 ± 0.125). With only 3 seeds and no statistical significance tests, these differences are not distinguishable from noise. The weighted curriculum variant shows edge success of 0.05 vs. 0.14 — absolute numbers so low that the practical significance is questionable. The paper's central claim that curricula act as "structural mechanisms for data acquisition" is not convincingly supported by these results.

- **Trivial curriculum instantiation.** The "curriculum" is simply a fixed reweighting toward edge cells — one of the most basic possible forms of non-uniform sampling. There is no comparison to any established automatic curriculum method (e.g., AMIGo, teacher-student frameworks, or even simple self-play curricula), making it impossible to assess whether the proposed framing offers any practical advantage over existing approaches.

- **Toy environment with no scaling evidence.** A deterministic GridWorld with full observability, 1000 episodes per seed, and a 64-hidden-unit MLP is an extremely limited testbed. The paper acknowledges this but does not provide any evidence (even preliminary) that the findings would hold in more complex settings. The gap between the ambition (open-ended learning, persistent agents) and the experimental scope is very large.

### Minor

- **No analysis of approximation error.** The abstract and introduction claim that curricula "reduce approximation error," but the results section reports only success rates, not UVFA value prediction errors. This claim is unsupported by the presented experiments.

- **Confusing figure/table structure.** Figures 1 and 2 appear to present overlapping or duplicate information (both show "Edge vs. Interior Curriculum" at H=16). Table 1 reports different numbers than Figure 1 for what appears to be the same condition, suggesting different horizons or evaluation protocols without clear explanation.

- **Missing comparison to HER or other GCRL baselines.** Hindsight Experience Replay (Andrychowicz et al., 2017) is cited but never compared against, despite being the most natural baseline for addressing sparse rewards in GCRL through data augmentation.

### Trivial

- The placeholder reference "First Wang and Others (2024)" in the bibliography.

## Nice-to-Haves

- A statistical significance analysis (even a simple t-test or bootstrap confidence intervals) would substantially strengthen the empirical claims.
- Comparison to at least one automatic curriculum baseline to contextualize the value of the selective data acquisition framing.
- Reporting of UVFA approximation error (MSE on held-out goals) to directly support the claim about reduced approximation error.

## Novel Insights

The paper's central reframing — that curriculum learning should be understood as selective data acquisition that reshapes the state–goal visitation distribution — is a reasonable conceptual contribution, but it is not as novel as presented. The idea that curricula change what data the learner sees is implicit in virtually all prior curriculum work (Bengio et al., 2009; Florensa et al., 2017; Narvekar et al., 2020). The paper does not sufficiently distinguish this perspective from existing understanding, nor does it demonstrate that the reframing leads to new algorithmic insights or practical improvements beyond what prior curriculum methods already achieve.

## Suggestions

- Strengthen the experiments: use more seeds (≥10), report confidence intervals, and run statistical tests. Even in a toy domain, rigorous statistics are needed to support the claims.
- Add a comparison to an established automatic curriculum method (e.g., teacher-student, adversarial goal generation) to show that the "selective data acquisition" framing yields insights beyond what existing methods provide.
- Actually measure and report UVFA approximation error across the state–goal space to support the claim that curricula reduce approximation error.
- Consider a slightly more complex environment (e.g., stochastic transitions, continuous state spaces, or multi-room GridWorld) to test whether the findings are robust.

## Score and Decision

The paper presents a reasonable conceptual framing but the experimental evidence is too weak to support its claims. The improvements are small, statistically unconvincing, and demonstrated only in a trivially simple environment with a trivially simple curriculum. The gap between the ambitious framing (open-ended learning, persistent agents) and the actual contribution (a fixed reweighting in GridWorld with marginal gains) is too large for a top venue.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: Reject