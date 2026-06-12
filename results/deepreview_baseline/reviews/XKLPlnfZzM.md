## Summary

This paper introduces the Temporal Deaggregation Diffusion Model (TDDM), a hierarchical framework that factorizes trajectory generation into spatial occupancy priors (marginal distributions over geographical occupancy) and temporal dynamics. By conditioning a diffusion model on aggregate spatial distributions rather than trajectory-level statistics, TDDM achieves controllability without sample-specific conditioning, enabling zero-shot generalization to unseen regions and cities. The authors establish a standardized benchmark across three cities (Beijing, Porto, San Francisco) and demonstrate that TDDM consistently outperforms existing GAN-, VAE-, and diffusion-based baselines on distributional alignment metrics while maintaining competitive fidelity.

## Strengths

- **Novel problem formulation**: The factorization of trajectory generation into spatial priors and temporal dynamics is a conceptually clean and well-motivated contribution. The idea that "where" people move can be decoupled from "how" they move in time is both intuitive and practically useful, enabling controllability without strong sample-specific conditioning that limits generalization.

- **Strong empirical results across multiple dimensions**: TDDM achieves substantial improvements over baselines, particularly on KL-based distributional measures (KL_sym: 0.277 vs. 1.153 for next-best Diffusion-TS) and JS divergence (0.059 vs. 0.198). The improvements span multiple evaluation axes—fidelity, coverage, proportionality—rather than optimizing a single metric.

- **Convincing generalization demonstration**: The zero-shot intra-city and city-to-city transfer experiments are compelling. The finding that models trained on Porto generalize better to other cities than partial local training data is non-trivial and provides practical insights for deployment scenarios where data availability varies.

- **Comprehensive and standardized evaluation framework**: The paper harmonizes multiple evaluation perspectives (fidelity, diversity, proportionality, usefulness, generalization) across three diverse cities on different continents, establishing a benchmark that will be useful for future work in this area.

## Weaknesses

### Major

- **Limited architectural novelty**: The core technical contribution is the conditioning mechanism (spatial priors as input tokens to a transformer encoder), while the underlying denoising diffusion framework is standard. The paper would benefit from clearer articulation of what specific technical challenges were overcome beyond the conceptual factorization. The transformer encoder architecture with trajectory tokens, marginal distribution tokens, and denoising step tokens is a straightforward application of existing techniques.

- **Incomplete baseline comparisons**: The paper omits several relevant recent methods for trajectory generation, particularly those based on score matching or flow matching (e.g., Trajectory Flow Matching, recent implicit models). While the authors acknowledge that some methods lack reproducible code, the comparison set feels somewhat dated and does not represent the full frontier of trajectory generation research at ICLR 2026.

- **Limited analysis of failure modes**: The generalization results show increased Length error (0.06–0.11) across city transfers, which the paper acknowledges but does not deeply analyze. Understanding when and why the spatial-temporal factorization breaks down (e.g., left-hand vs. right-hand traffic, different road network topologies) would strengthen the contribution. The paper mentions this as future work but the current analysis remains surface-level.

### Minor

- **The spatial prior resolution (64×64 for 3×3 km) and region size (3×3 km) seem somewhat arbitrary**: The ablation shows that 1×1 km regions yield different trade-offs, but there is no systematic investigation of how region size interacts with city characteristics (e.g., road network density, typical trajectory length). A sensitivity analysis would help practitioners choose appropriate parameters.

- **TSTR metric limitations**: The TSTR evaluation uses a transformer decoder trained on synthetic data to predict future states. While this captures usefulness, it may favor models that produce smoother trajectories rather than more realistic ones, and the single "mean absolute value" metric may obscure important differences in prediction quality across different spatiotemporal regimes.

- **Map matching confound**: The paper uses map-matched data for all experiments and then verifies that TDDM still outperforms baselines without map matching. However, the map matching step itself could be introducing artifacts or biases that advantage the proposed model's factorization. The relationship between map matching quality and model performance is not explored.

## Nice-to-Haves

- Including explicit comparison of computational cost (training time, inference time, parameter count) between TDDM and baselines would help practitioners assess practical trade-offs.
- Visualization of spatial priors themselves (not just the resulting trajectories) would provide more intuition about what information the model conditions on.
- Analysis of privacy guarantees: since TDDM conditions only on aggregate distributions rather than trajectory instances, it may offer inherent privacy advantages. This could be a selling point worth exploring.

## Novel Insights

Beyond the paper's own contributions, the observation that training on Porto yields better cross-city generalization than partial local data is genuinely interesting and somewhat counterintuitive. It suggests that certain urban mobility datasets may serve as "universal" priors that capture dynamics common across cities, while others may be more idiosyncratic. This raises a deeper question about what properties of a source dataset enable strong transferability—trajectory length distribution? Road network structure? Diversity of movement patterns? The paper does not fully explore this, but it points toward an important direction for understanding when spatial-temporal factorization is most beneficial.

## Suggestions

- Provide a more systematic analysis of when the spatial-temporal factorization breaks down, including controlled experiments with synthetic data where the true spatial prior is known and can be manipulated.
- Include computational efficiency comparisons (FLOPs, training time, inference speed) alongside quality metrics to help practitioners understand the practical cost of the improved performance.
- Consider adding a simple baseline that uses the spatial prior but with a non-diffusion generative model (e.g., a simple sequential VAE conditioned on H) to isolate the benefit of the diffusion framework from the benefit of conditioning on spatial priors.

## Score and Decision

The paper presents a clean and well-motivated approach with strong empirical support across multiple datasets and evaluation metrics. The conceptual contribution (factorizing trajectory generation into spatial priors and temporal dynamics) is genuinely useful, and the zero-shot generalization results are compelling. However, the architectural contribution is incremental, and the lack of comparison with the most recent trajectory generation methods limits the assessment of where this work stands in the current landscape. The paper is a solid contribution that advances the state of the art in trajectory generation, but it does not represent a breakthrough that would merit the highest scores.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>