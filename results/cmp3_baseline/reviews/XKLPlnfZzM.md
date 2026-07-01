## Summary
This paper introduces the Temporal Deaggregation Diffusion Model (TDDM), a hierarchical generative framework that separates spatial occupancy priors from temporal dynamics for large-scale trajectory generation. The key insight is to condition a diffusion model on aggregate marginal distributions over geographical regions rather than sample-specific statistics, combined with a canonicalization step that enables parameter sharing across different regions and cities. The method achieves strong improvements over existing GAN-, VAE- and diffusion-based baselines on a newly established three-city benchmark, and demonstrates competitive zero-shot generalization to unseen parts of a city and to entirely new cities.

## Strengths
- **Novel and principled factorization**: Decoupling *where* people move (spatial occupancy priors) from *how* they move (temporal dynamics) is a well-motivated idea that naturally supports controllability and cross-region generalization. The use of similarity transforms for canonicalization is elegant and avoids architectural complexity.
- **Strong empirical results**: TDDM consistently outperforms five strong baselines (including recent diffusion models) across all three cities on most metrics, often by large margins (e.g., KL_sym 0.277 vs. 1.153 for Diffusion-TS). The ablation study clearly demonstrates the critical role of spatial priors.
- **Comprehensive evaluation framework**: The paper constructs a standardized benchmark across three continents with a principled set of metrics covering fidelity, coverage, proportionality, and downstream usefulness. This is a valuable contribution in itself.
- **Demonstrated generalization capability**: Both intra-city (trained on 25% of a city) and city-to-city zero-shot transfer results show that TDDM can generate realistic trajectories in unseen regions using only aggregate spatial statistics, which is a practically important and challenging capability.

## Weaknesses

### Fatal
None.

### Major
- **The zero-shot generalization setting is not fully unsupervised** because computing the spatial prior H (Equation 3) requires trajectory data from the target region (Algorithm 2, line 3). The method assumes access to aggregate occupancy counts in target areas, which may not always be available (e.g., for a completely new city with no trajectory observations). The paper should explicitly discuss how many trajectory observations are needed to estimate reliable spatial priors, especially in low-data regimes.
- **Reliance on map matching in preprocessing** limits the general applicability of the evaluation. The preprocessing pipeline involves map matching to reduce noise, which requires a road network map for each city. This raises questions about how the method would perform on unstructured environments or on raw GPS data without map matching, especially as the ablation shows a significant drop for all models when map matching is omitted. The paper claims TDDM's relative improvements hold, but the absolute numbers degrade, and the necessity of map matching may restrict practical deployment.
- **The KL divergence metric is computed over discretized 2D grids**, which may not capture fine-grained trajectory structure (e.g., sequential patterns, road segment adherence). While other metrics (TSTR, Pattern) partially address this, the heavy reliance on grid-based KL makes the evaluation sensitive to bin resolution. The paper does not analyze the effect of grid resolution on the reported scores.

### Minor
- **Comparison with ControlTraj and TrajGen is omitted** due to lack of reproducible code. This is understandable, but it leaves a gap in the comparison, especially since ControlTraj also uses conditional diffusion. Including a qualitative or conceptual comparison in the main text would strengthen the positioning.
- **The ablation study only varies region size (1×1 km) and removal of spatial priors.** More ablations (e.g., different spatial prior granularity, different canonicalization choices, impact of transformer tokenization strategies) would help understand which components drive performance.
- **TSTR uses a transformer decoder** to measure downstream usefulness. While reasonable, it would be helpful to justify why this particular architecture was chosen over more standard trajectory forecasting baselines (e.g., LSTM, SimpleDecoder).

## Nice-to-Haves
- An analysis of the number of target trajectories needed to estimate spatial priors reliably for zero-shot generalization.
- Qualitative examples of failure modes in cross-city transfer (e.g., where length error increases).
- Ablation on the spatial prior grid resolution (the paper uses 64×64; varying this could reveal the tradeoff more fully).

## Novel Insights
The paper's central insight—that generative trajectory modeling can be effectively factorized by conditioning on aggregate spatial statistics rather than sample-specific features—is genuinely novel and well-executed. The finding that a model trained on Porto generalizes better to other cities than partial local training data is a counterintuitive and practically useful observation. More broadly, the work shows that spatial-temporal factorization combined with input-output canonicalization can achieve location-invariant temporal dynamics learning, which is a concrete step toward scalable and transferable mobility modeling.

## Suggestions
- Explicitly discuss the minimum amount of trajectory data needed to estimate spatial priors for zero-shot transfer, and consider providing a sensitivity analysis for different levels of data availability.
- If possible, include a comparison with a version of TDDM that uses a smaller spatial prior grid (e.g., 32×32) to show robustness to prior resolution.
- Clarify in the main text that “zero-shot” still requires aggregate information from the target region, and discuss the practical implications (e.g., this can come from census data, other open datasets, or short-term observations).

## Score and Decision
Based on its novel factorization, strong and consistent empirical results, careful benchmarking, and demonstrated generalization capabilities, this paper makes a significant contribution to the trajectory generation literature. Despite some minor concerns about the evaluation setup and the definition of zero-shot generalization, the work is sound, well-written, and provides both methodological and practical advances. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>