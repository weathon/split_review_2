The per-item favorabilities confirm that the two core weaknesses (zero-shot framing, missing variance) are the only ones that carry real weight (both ~-7), while all other weaknesses are near-zero impact. The strengths are uniformly very strong (four at 8.0–9.9). 

Now let me produce the final consolidated review.

## Summary

This paper introduces the Temporal Deaggregation Diffusion Model (TDDM), a trajectory generation framework that factorizes the problem into spatial occupancy priors (marginal distributions over geographic regions) and temporal dynamics. By conditioning generation on aggregate spatial priors rather than individual trajectory statistics, TDDM achieves strong results on large-scale trajectory generation across three cities (Beijing, Porto, San Francisco), with 4× improvements in symmetric KL divergence and 3× in Jensen-Shannon divergence over leading baselines. The paper also demonstrates intra-city and cross-city generalization without retraining.

## Strengths

- **A clean and well-motivated factorization.** The core idea — separating spatial occupancy from temporal dynamics — directly addresses a real limitation of existing trajectory generation models. TDDM's use of region-level spatial priors as conditioning signals is a genuine alternative to sample-specific conditioning (used by DiffTraj, ControlTraj), which ties generation to training instances and prevents cross-region transfer. This is not an incremental tweak.

- **Substantial and consistent empirical improvements.** Table 1 shows TDDM beating all baselines by wide margins: symmetric KL of 0.277 vs. next-best (Diffusion-TS at 1.153) — roughly 4× improvement — and JS of 0.059 vs. 0.198 — roughly 3×. These hold across three datasets spanning different continents and mobility patterns. The ablation (Table 2) convincingly attributes the gains to the spatial prior: removing it causes KL metrics to degrade by 3–5× while TSTR is unchanged, confirming the prior is doing the work on distributional coverage.

- **Meaningful generalization experiments.** The intra-city and cross-city transfer experiments (Table 3) go beyond what is standard for this area. The finding that a Porto-trained model often outperforms a model trained on 25% of the target city is non-obvious and practically useful. The paper is also honest about where generalization degrades (Length error in cross-city transfer).

- **Thoughtful evaluation framework.** The paper defines five distinct qualities of synthetic trajectory data (fidelity, diversity, proportionality, usefulness, generalization) and selects metrics that map onto each — a more principled approach than relying on a single metric.

## Weaknesses

### Fatal
None.

### Major
- **The "zero-shot" claim is overstated relative to what is demonstrated.** Algorithm 2 (lines 2–3) computes the spatial prior *H* from **\\( \mathbb{X}_{\text{target}} \\)** trajectories — aggregate occupancy data from the target region. The model never sees individual target trajectories, but it does require per-region occupancy statistics from the target to generate trajectories. The paper mentions (line 145) that *H* could be estimated from non-trajectory sources (census data, satellite imagery), but this is never tested or demonstrated. All experiments compute *H* from the target city's trajectory data. The practical result — *given aggregate spatial statistics from a new city, the model generates realistic trajectories without seeing individual trajectories or retraining* — is still useful (it protects privacy at the trajectory level), but the abstract's "supporting transfer to new regions" and the contributions' "strong out-of-distribution zero-shot performance" imply a less data-dependent capability than is actually shown. The claims should be recalibrated to match the evidence.

### Minor
- **Most metrics are reported as point estimates from a single evaluation run.** Across Tables 1, 2, and 3, only TSTR reports ± values. All KL divergences, JS, Density, Trip, Length, and Pattern scores are point estimates. The paper states (line 267) "Models are trained, sampled and evaluated once per dataset." While the margins in Table 1 are large enough that variance is unlikely to reverse the qualitative picture, the absence of any variance reporting for the majority of metrics weakens the evidential basis for comparative claims. Reporting results across multiple seeds with standard deviations would substantially strengthen the paper.

- **The "w/o spatial prior + rejection" ablation (Table 2) is not described.** What rejection criterion is used? What is the acceptance rate? Without this information, the ablation — which shows this variant often performs *worse* than "w/o spatial prior" alone — is difficult to interpret.

- **The paper does not describe whether baseline hyperparameters were tuned per dataset or kept at defaults.** The paper confirms all models use the same preprocessed data (line 243), which is good, but tuning practices could affect relative comparisons.

### Trivial
- **Inconsistency between normalization ranges.** Line 121 states the similarity transform maps to \\([-1, 1]^D\\), but Algorithm 1 (line 6) and Algorithm 2 (line 11) use \\([0, 1]^D\\), and the caption at line 169 refers to "normalized coordinates \\([0, 1]^D\\)." This should be reconciled.

- **The metric "KL_speed"** (corrupted by the parser in Table 1, intact in Table 3) appears among the evaluation measures but is not defined in the main evaluation section — it is only referenced via "See Appendix E for details on all six measures" (line 241). The main text should briefly define it.

## Nice-to-Haves
- Evaluate the model with spatial priors estimated from genuinely independent sources (e.g., OpenStreetMap road density, census population grids, satellite imagery) rather than from the target city's trajectory data. This would directly validate the claim that *H* can be obtained "even in unseen cities."
- Report the number of tokens consumed by the 64×64 spatial prior grid and discuss the transformer's quadratic attention cost, as the paper acknowledges this tradeoff (line 139).

## Removed Points
These points from the input review are flagged to be removed; treat them with caution.
- Criticisms about filtering thresholds, token counts, and token cost being "in the appendix" are removed because the appendix exists in the original submission. These are presentation choices, not evidential gaps.
- The separate point "Single evaluation run per dataset" is merged into the variance reporting weakness above.
- "Intra-city setting also uses target data for *H*" is subsumed by the zero-shot claim weakness.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Recalibrate the "zero-shot" framing in the abstract and contributions to accurately describe what is demonstrated: the model generalizes across cities using only aggregate spatial statistics (marginal distributions) from the target, without seeing individual target trajectories or requiring retraining.
2. Report all metrics with standard deviations across multiple seeds (at least 3) to establish statistical reliability.
3. Reconcile the \\([-1, 1]\\) vs. \\([0, 1]\\) normalization inconsistency.
4. Describe the rejection sampling scheme used in the "w/o spatial prior + rejection" ablation.

## Score and Decision

The paper's core contribution — spatial-temporal factorization for trajectory generation — is clean, well-motivated, and backed by large and consistent empirical gains. The two significant weaknesses (overclaimed "zero-shot" framing and lack of variance reporting) are real but not structural: they concern framing precision and reporting standards, not the validity of the method or the results. The remaining issues are minor or trivial.

**Score: 8**

**Decision: Accept**

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>