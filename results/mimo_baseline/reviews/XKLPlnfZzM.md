## Summary
This paper introduces the Temporal Deaggregation Diffusion Model (TDDM), a hierarchical diffusion framework that factorizes trajectory generation into spatial occupancy priors (where people move) and temporal dynamics (how people move). By conditioning a transformer-based denoising model on discretized marginal distributions over spatial occupancy and canonicalizing regions via similarity transforms, TDDM achieves both high-fidelity trajectory generation and zero-shot generalization to unseen city regions and entirely new cities. The authors establish a standardized benchmark across three cities on different continents with comprehensive metrics, demonstrating consistent improvements over GAN, VAE, and diffusion baselines.

## Strengths
- **Clear and well-motivated conceptual contribution**: The spatial-temporal factorization—decoupling "where" from "how" people move—is a clean, interpretable decomposition that is both theoretically grounded and practically useful. The canonicalization via similarity transforms is a clever mechanism that keeps the architecture lightweight while achieving invariance, contrasting favorably with heavier equivariant architectures.

- **Rigorous and comprehensive experimental evaluation**: The evaluation spans three cities across different continents (Beijing, Porto, San Francisco), covers five distinct quality dimensions (fidelity, diversity, proportionality, usefulness, generalization), and includes six quantitative metrics plus visual inspection. The ablation studies (Table 2) properly justify design choices by isolating the contribution of spatial priors and region size, confirming that spatial priors are critical for distributional coverage (KL_sym degrades ~5x without them).

- **Meaningful generalization experiments**: The paper goes beyond standard in-distribution evaluation to demonstrate both intra-city (train on 25%, generate for 75%) and cross-city zero-shot transfer. The finding that Porto-trained models generalize better to other cities than models trained on limited local data is a genuinely interesting and practically valuable insight about the existence of "universal source" datasets.

- **Multi-city benchmark with standardized metrics**: The harmonization of evaluation perspectives (fidelity, coverage, proportionality, usefulness, generalization) with specific metrics for each is a useful methodological contribution for the trajectory generation community.

## Weaknesses
### Fatal
None.

### Major
- **Fairness of baseline comparisons**: The baselines include general time-series models (Diffusion-TS, TimeGAN, TimeVAE, COSCI-GAN) that are not designed for spatially-structured trajectory generation and have no mechanism to incorporate spatial structure. The meaningful comparison is primarily with DiffTraj, which uses sample-specific conditioning (OD pairs). While the paper does improve over DiffTraj on most metrics, the headline claim of "consistently surpasses existing GAN-, VAE-, and diffusion-based methods" conflates beating general-purpose baselines (expected) with beating trajectory-specific baselines (meaningful). The fairness concern is partially mitigated by including DiffTraj, but a comparison with ControlTraj (which the paper acknowledges exists but cannot reproduce) would have strengthened the argument.

- **Nuance in zero-shot generalization claims**: The generation process (Algorithm 2, line 3) computes spatial priors from target trajectories (`X_target`). For truly unseen cities, this requires some target data to be available—albeit only aggregate spatial statistics rather than individual trajectories. The paper is transparent about this but could be more explicit about what "zero-shot" means in this context: the *generative model* transfers without retraining, but target data is still needed to estimate spatial priors. This is a reasonable and useful form of transfer, but the framing could overstate the practical generality.

### Minor
- **Length error in cross-city transfer**: Length error increases substantially in cross-city settings (0.06–0.11 vs. 0.003–0.004 in-distribution), indicating that fine-grained temporal dynamics are not as transferable as the spatial-temporal factorization implies. The paper acknowledges this but it somewhat undermines the claim that temporal dynamics are learnable in a transferable manner. This suggests the factorization primarily helps with spatial properties rather than temporal ones.

- **Map-matching preprocessing dependence**: All models benefit significantly from map-matching preprocessing, and the relative improvements of TDDM over baselines may partly reflect differential sensitivity to data quality. While the paper shows consistent trends with and without map matching, the strong dependence on preprocessing is worth noting for practical deployment.

### Trivial
None.

## Nice-to-Haves
- A comparison against a simple baseline that computes spatial priors from training data and generates trajectories by uniformly sampling within high-occupancy cells would help quantify how much the diffusion model adds beyond the spatial prior itself.
- Analysis of computational cost and generation speed relative to baselines would inform practical deployment considerations.

## Novel Insights
The paper's key insight—that trajectory generation can be productively factorized into spatial marginal distributions and temporal dynamics, and that conditioning on aggregate spatial statistics rather than sample-specific features enables cross-region generalization—is genuinely novel and well-supported by experiments. The additional empirical finding that certain cities (Porto) can serve as "universal source" datasets that outperform limited local training data for cross-city transfer is a surprising and practically valuable observation that emerges from the experimental design rather than being the primary contribution.

## Suggestions
- Clarify the distinction between "zero-shot" (no model fine-tuning) and "data-free" (no target data needed) transfer, since the framework requires target spatial priors.
- Consider adding a simple spatial-prior-only baseline to better quantify the marginal contribution of the temporal diffusion model.
- Discuss limitations more explicitly: the Length error increase in cross-city transfer and the requirement for target spatial data represent genuine practical constraints.

## Score and Decision
The paper makes a clear and well-executed methodological contribution with strong experimental evidence. The spatial-temporal factorization is conceptually clean, the canonicalization mechanism is elegant, and the cross-city generalization capability is demonstrated convincingly across multiple settings. The benchmark contribution is valuable. While baseline fairness and zero-shot framing could be sharpened, these are addressable issues rather than fundamental flaws. The contribution advances both methodology and practical capability in trajectory generation.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>