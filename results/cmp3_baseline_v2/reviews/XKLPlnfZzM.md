## Summary
This paper introduces the Temporal Deaggregation Diffusion Model (TDDM), a hierarchical generative framework that factorizes trajectory generation into spatial occupancy priors (marginal distributions over geographical regions) and temporal dynamics. By conditioning a diffusion model on these spatial priors and using coordinate canonicalization, TDDM generates high-fidelity trajectories without sample-specific conditioning and demonstrates zero-shot generalization to unseen cities. Extensive experiments across three cities (Beijing, Porto, San Francisco) show consistent improvements over existing GAN-, VAE-, and diffusion-based baselines on distributional metrics.

## Strengths
- **Novel spatial-temporal factorization**: The core idea of conditioning trajectory generation on spatial occupancy priors (marginal distributions) rather than trajectory-level statistics is well-motivated and elegantly enables controllability without sample-specific conditioning. This separation is a genuine conceptual contribution.
- **Strong empirical results**: TDDM achieves substantial improvements over leading baselines, with up to 4× lower symmetric KL divergences (0.277 vs. 1.153 for next-best) and consistent gains across fidelity, proportionality, and coverage metrics (Table 1). Visual results in Figure 2 convincingly support the quantitative findings.
- **Thorough evaluation framework**: The paper establishes a standardized benchmark across three cities on different continents with a harmonized set of metrics covering fidelity, diversity, proportionality, usefulness, and generalization. Ablation studies (Table 2) and both intra-city and city-to-city zero-shot transfer experiments (Table 3) provide comprehensive validation.
- **Effective canonicalization**: The similarity-transform-based canonicalization is simple yet effective, enabling parameter sharing across geographic regions without architectural complexity. The generalization results confirm that this design choice supports transferable temporal dynamics learning.
- **Clear exposition**: The problem motivation is compelling, the method is clearly described with helpful figures, and the algorithms are presented with sufficient detail for reproducibility.

## Weaknesses
### Fatal
None.

### Major
- **Lack of error bars on key metrics**: The paper states that models are trained, sampled, and evaluated once per dataset. Most metrics (KL divergences, JS, Density, Trip, Length, Pattern) are reported as single values without confidence intervals or standard deviations. This makes it impossible to assess the statistical significance of the reported improvements, which is a serious limitation for a benchmarking paper.
- **Misleading "zero-shot" framing**: In the claimed zero-shot generalization (Section 4.3), Algorithm 2 line 3 explicitly computes spatial priors \(H\) from target city trajectory data \(\mathbb{X}_{\text{target}}\). While the model does not undergo gradient updates on target trajectories, it still requires aggregate occupancy statistics from the target distribution. This is a weaker form of generalization than true zero-shot (where no target data of any kind is used). The paper should clarify what minimal information is needed and discuss scenarios where even aggregate data is unavailable.
- **Unfair baseline comparison**: TDDM conditions on spatial priors (strong distributional guidance), while all baselines are purely unconditional. The ablation without spatial priors (Table 2) confirms that conditioning is the primary driver of KL improvement (KL_sym 1.334 vs. 0.277 with priors). A fairer comparison would include conditioned versions of baselines or acknowledge that the added information gives TDDM an advantage that is separate from architectural innovations.

### Minor
- **Fixed grid resolution**: The spatial prior uses a fixed 64×64 grid for 3×3 km regions. The paper does not investigate sensitivity to this resolution or discuss adaptive strategies, leaving questions about applicability at different scales.
- **Cross-city length error degradation**: Length error increases substantially (from 0.004 in-distribution to 0.06–0.11 cross-city), suggesting that trajectory length distributions are not well transferred from spatial priors alone. This is acknowledged but warrants deeper analysis.
- **Single seed/run**: The paper reports results from a single training run per dataset. Multiple runs would strengthen confidence in the conclusions, especially given the stochastic nature of diffusion models.

### Trivial
None.

## Nice-to-Haves
- Explore sources for spatial priors other than target trajectories (e.g., census data, satellite imagery, OpenStreetMap road density) to achieve truly data-free generalization.
- Add confidence intervals via multiple training seeds or bootstrap resampling for all metrics.
- Include conditional versions of baselines (e.g., providing DiffTraj or Diffusion-TS with the same spatial prior) for a more controlled comparison.
- Analyze failure cases: what types of trajectories or regions does TDDM generate poorly?

## Novel Insights
Beyond the paper's own contributions, the observation that training on Porto yields better cross-city generalization than training on partial data from the target city is genuinely interesting. It suggests that some cities may encode more universal or representative mobility patterns, which could inform dataset selection and pre-training strategies for trajectory foundation models. This finding also highlights a trade-off between distributional coverage (better with a universal source city) and fine-grained fidelity measures like trajectory length (better with local data), which has practical implications for deployment.

## Suggestions
1. Add standard deviations or confidence intervals for all reported metrics, ideally from multiple training runs.
2. Clarify the zero-shot framing: rename to "zero-shot adaptation" or explicitly state the need for target-city aggregate statistics, and discuss how spatial priors could be obtained without target trajectories (e.g., from road networks or land-use data).
3. Include an experimental comparison where baselines are also given spatial prior information (e.g., by concatenating the prior as an additional channel in DiffTraj) to isolate the benefit of the factorization from the benefit of conditioning.
4. Analyze the spatial prior sensitivity: vary grid resolution and region size to quantify the trade-off between detail and computational cost.

## Score and Decision
The paper presents a novel and well-motivated factorization approach with strong empirical support. The major weaknesses (lack of error bars, zero-shot framing clarity, and baseline comparison fairness) are addressable and do not invalidate the core contribution. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: Accept