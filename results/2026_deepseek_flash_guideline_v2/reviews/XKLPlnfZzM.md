Now I have enough to write the final consolidated review.

## Summary
TDDM (Temporal Deaggregation Diffusion Model) is a hierarchical trajectory generation framework that factorizes generation into spatial occupancy priors and temporal dynamics, using similarity-transform canonicalization to enable cross-region transfer. The model conditions a diffusion transformer on region-level spatial marginals (H) rather than sample-specific statistics, achieving strong distributional alignment and zero-shot generalization to new cities. Evaluation across three cities (Beijing, Porto, San Francisco) shows improvements over unconditional baselines on KL divergences, TSTR, Density, Trip, and Pattern measures.

## Strengths

1. **Clean factorization with causal evidence.** The spatial-temporal factorization is well-motivated and the ablation study (Table 2) causally demonstrates that the spatial prior drives the large distributional alignment gains (KL_sym degrades ~5× when removed, from 0.277→1.334) while TSTR stays flat. This cleanly separates the conditioning mechanism from architecture capacity.

2. **Zero-shot generalization is a genuine capability gap-fill.** Table 3 shows TDDM can generate realistic trajectories in entirely unseen cities without gradient updates on target data, maintaining TSTR of 0.010 and Pattern >0.915. Existing unconditional models and sample-conditioned diffusion models (DiffTraj, ControlTraj) do not offer this property, making this a concrete contribution.

3. **Comprehensive standardized benchmark.** The paper establishes a unified evaluation across three continents with 10 metrics spanning fidelity, diversity, proportionality, usefulness, and generalization — a more thorough setup than prior trajectory generation work which typically evaluates on a single city.

4. **Non-obvious empirical finding.** The Porto-trained model generalizing better than 25%-local-data models (KL_sym 0.335 vs. 0.545) surfaces a practical insight: certain cities serve as richer source distributions for cross-city transfer.

## Weaknesses

### Major

- **Asymmetric comparison on spatial KL metrics.** The KL divergences evaluate support coverage and proportionality of the spatial distribution (i.e., how well generated trajectories occupy the right 2D areas in the right proportions). TDDM is explicitly conditioned on this exact quantity — the spatial prior H is a discretized marginal distribution over geographic occupancy. Unconditional baselines receive no such information. This is evident from the ablation: removing the spatial prior collapses the KL improvement (0.277→1.334). The paper frames the 4× KL improvement as a general fidelity win over baselines, but it primarily reflects the value of giving the model the spatial marginal as conditioning. The claim is valid as framed (TDDM does achieve lower KL), but the comparison is not apples-to-apples on this metric family. Conditioning the strongest baseline (e.g., Diffusion-TS) on the same spatial prior would isolate whether TDDM's architecture provides additional benefit beyond the conditioning signal itself.

- **Variance unreported for most metrics.** Only TSTR includes standard deviations in Table 1. All KL divergences, Density, Trip, Length, and Pattern are single-run point estimates. The paper states models are "trained, sampled and evaluated once per dataset." For several metrics where gaps are modest (Pattern: 0.917 vs. 0.907; Density: 0.019 vs. 0.029; Trip: 0.031 vs. 0.041), per-seed variance could affect the apparent ranking. Without variance estimates, the reader cannot assess statistical significance of these advantages.

### Minor

- **Cross-boundary trajectory truncation.** Algorithm 1 (line 4) extracts "contiguous subsequences of trajectories that lie within r_c," meaning trajectories crossing region boundaries are truncated. The model never observes full multi-region trajectories during training. This design choice affects long-range trajectory coherence and the method's ability to generate plausible cross-region movement — it merits explicit discussion, which the paper does not provide.

- **"Zero-shot" terminology could be more precise.** Algorithm 2 requires computing the spatial prior H from target-city trajectories (X_target). The model does not perform gradient updates on target data (a meaningful distinction), but it does require aggregate observations from the target city. A reader could misinterpret "zero-shot" as requiring no target data at all. The paper describes this clearly in Section 4.3 but the abstract and conclusion use "zero-shot" without the same qualification.

- **Spatial prior data source ambiguity.** In the unconditional generation setting (Section 4.1), the paper states that spatial priors are "learned during training" but does not explicitly confirm they are computed from only the training split. If H were derived from the full dataset (including test data), this would constitute leakage. The paper should clarify this.

### Trivial

- Table 1 has a minor rendering artifact in the "KL_speed" row (rendered as "KL_apeed" / "KL_peeed" in the PDF-extracted text).

## Nice-to-Haves

- Conditioning DiffTraj or Diffusion-TS on the same spatial prior H to isolate TDDM's architectural contribution from the conditioning advantage.
- Variance estimates (3–5 seeds) on the key metrics in Table 1, especially Pattern and Density where gaps are small.

## Removed Points

These points were considered but removed from the main weakness list — treat with caution if referenced:

- **"Similarity transform is the inductive bias" (Harsh Critic).** The paper says "without *additional* inductive bias" — accurately acknowledging the similarity transform as the chosen mechanism. This is a semantic nitpick, not a substantive flaw.

- **"KL_speed variation suggests baseline failure" (Harsh Critic).** The huge variation (COSCI-GAN gets 6.463) is noted in the paper and is a parser artifact. The critic's speculation about binning is unverifiable without the appendix.

- **"Map-matching ablation conclusion doesn't follow" (Harsh Critic).** The paper claims the map-matching ablation shows the *relative ordering* of models is consistent, supporting the deaggregation framework as the source of TDDM's advantage. This is logically valid — if results pattern holds with and without map-matching, the relative advantage is not driven by map-matching.

- **"No analysis of individual sample realism" (Harsh Critic).** TSTR evaluates downstream predictive usefulness on individual trajectories, and visual inspection (Figure 2) is provided. While more analysis is always possible, the paper does assess sample-level quality through TSTR.

- **Strongth Finder's "ablation study isolates conditioning mechanism" as a strength.** The ablation does cleanly show the spatial prior drives KL gains, but this same evidence is also what raises the fairness concern about the KL metrics. It's retained as a strength because it *does* validate the paper's core claim about the factorization's importance, but paired with the caveat about the metric.

## Novel Insights

The integration of the two reviews surfaces a tension that neither individually fully resolves: the ablation study (Table 2) simultaneously provides the strongest evidence *for* the paper's contribution (the spatial prior causally drives performance) and the strongest evidence *against* the fairness of the headline KL comparison (removing the prior collapses the KL advantage). This means the paper's central empirical claim is both supported and contextualized: TDDM works as designed, but the 4× KL improvement is a statement about the value of conditioning on spatial priors, not about the superiority of the TDDM architecture over all alternatives. The generalization experiments provide orthogonal evidence that partially sidesteps this concern — the zero-shot capability is independent of whether the unconditional baseline comparison is fair — and the Porto-as-universal-source finding is genuinely novel. The paper would be strengthened by acknowledging this more directly and reframing the main comparison as "conditional vs. unconditional" rather than "TDDM vs. baselines" on the spatial KL metrics.

## Suggestions

1. Reframe the main quantitative comparison: explicitly separate the claim "TDDM with spatial prior conditioning outperforms unconditional models on spatial KL metrics" from "the TDDM architecture provides additional benefit beyond the conditioning signal." The former is well-supported; the latter requires a controlled experiment.

2. Add a controlled comparison where the strongest baseline (Diffusion-TS) is conditioned on the same spatial prior H. This establishes whether TDDM's architecture adds value beyond the conditioning advantage.

3. Report variance (standard deviations or confidence intervals) on all metrics in Table 1 using at least 3 random seeds.

4. Clarify that the spatial prior H in the unconditional setting (Section 4.1) is derived from training data only, and more precisely qualify the "zero-shot" terminology.

5. Add a brief discussion of the implications of truncating cross-boundary trajectories during training and how the method handles multi-region coherence in practice.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>