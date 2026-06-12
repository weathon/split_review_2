## Summary

This paper proposes a novel batch multi-objective Bayesian optimization (MOBO) acquisition strategy called Probability of Matching, which aims to balance candidate quality and diversity by explicitly modeling the likelihood that a batch matches the true Pareto set. The authors factorize this probability into two components: the probability that batch points are Pareto optimal (approximated via qEHVI) and the probability that they collectively cover the full Pareto set (approximated via space-filling design principles). The resulting method, qEHVI-SF, is evaluated on synthetic benchmarks and a real-world alloy design task, showing improvements over qEHVI and QSVGD baselines in terms of hypervolume, a new design-space coverage metric (EMD), and rediscovery ratio.

## Strengths

- **Novel probabilistic framing**: The decomposition of the matching probability into quality and coverage components provides a principled and interpretable framework for batch MOBO that goes beyond simple additive regularization approaches.
- **Strong empirical results**: The method consistently outperforms baselines across multiple benchmarks (GM, RE4-7-1) and a real-world alloy design task with up to six objectives, with improvements in both hypervolume and the proposed EMD coverage metric.
- **Computational efficiency**: The space-filling term adds only modest computational overhead (Θ(q(n+q)d)) compared to qEHVI, and the runtime analysis in Table 1 confirms practical feasibility.
- **Well-motivated design-space diversity**: The paper makes a compelling argument for promoting diversity in the design space rather than the objective space, addressing validity, bias, and alignment issues that plague objective-space diversity methods.

## Weaknesses

### Major

- **Theoretical gap between distance-based heuristic and coverage probability**: The paper acknowledges this limitation (Section 5) but the core claim of "explicitly capturing the likelihood that a batch matches the true Pareto set" is not fully supported. The coverage component is approximated by maximizing minimum pairwise distance, which is a heuristic with no proven relationship to the true coverage probability P(𝒳* ⊆ 𝐗 | 𝐗 ⊆ 𝒳*). The paper would benefit from either a theoretical justification or a more direct estimator.
- **Limited baseline comparison**: The paper only compares against qEHVI and a modified QSVGD. Several relevant batch MOBO methods are missing, including: (1) methods that explicitly optimize for diversity in the design space (e.g., Thompson sampling-based approaches, Pareto frontier entropy search), (2) recent diversity-aware acquisition functions like USeMO or other information-theoretic approaches, and (3) methods that handle batch diversity through determinantal point processes (DPPs). The absence of these baselines weakens the claim of state-of-the-art performance.
- **The QSVGD baseline implementation is questionable**: The paper modifies QSVGD (originally for single-objective BO) by adding an entropy term to qEHVI, but this is not the standard QSVGD formulation. The authors note that finding the optimal exploration-exploitation balance is challenging and that the diversity term can dominate, leading to poor performance. This raises concerns about whether QSVGD is implemented fairly as a baseline, especially given the sensitivity to the η hyperparameter and the decaying schedule.

### Minor

- **The EMD metric requires the true Pareto set**: The proposed Expected Minimum Distance metric (Equation 9) requires knowledge of the true Pareto optimal set 𝒳*, which is unknown in real-world applications. While useful for benchmarking, its practical utility is limited.
- **Figure 1 caption is garbled**: The caption describes "BOILS", "BOILS+LBO", and "BOILS+LBO+LBO" methods that do not appear in the paper, suggesting a figure-caption mismatch from the PDF extraction. This makes the figure difficult to interpret.
- **The complexity analysis (Section 3.3) is somewhat opaque**: The derivation of the per-evaluation complexity includes combinatorial terms (|𝒳| choose q) that are not clearly defined, and the practical implications of the super-polynomial K term are not discussed.

### Trivial

- The paper uses "tnnv", "qnvcd", and "tnnv-sf" in Figure 2's caption instead of the actual method names (qEHVI, QSVGD, qEHVI-SF), which is confusing.

## Nice-to-Haves

- A theoretical analysis connecting the minimum-distance heuristic to coverage probability would significantly strengthen the paper.
- Ablation studies isolating the contribution of the space-filling term versus the qEHVI term would help understand the method's behavior.
- Experiments on higher-dimensional design spaces (d > 7) would test the scalability of the distance-based diversity approach.

## Novel Insights

The key insight is that batch MOBO can be reframed as a probabilistic matching problem, where the goal is to maximize the joint probability that batch points are both Pareto optimal and collectively cover the entire Pareto set. This decomposition naturally leads to a principled trade-off between quality and diversity without requiring sensitive hyperparameter tuning. The paper's argument for promoting diversity in the design space rather than the objective space is well-reasoned and addresses fundamental limitations of existing approaches.

## Suggestions

- Add more diverse baselines, particularly methods that explicitly handle batch diversity (e.g., DPP-based acquisition, Thompson sampling with repulsion, or other design-space diversity methods).
- Provide a theoretical or empirical analysis of the relationship between minimum distance and coverage probability, or consider alternative coverage estimators.
- Fix the figure caption issues and ensure consistency between figure labels and method names.
- Discuss the practical limitations of the EMD metric and consider alternative evaluation protocols for real-world settings where the true Pareto set is unknown.

## Score and Decision

The paper presents a novel and well-motivated approach to batch MOBO with strong empirical results. However, the theoretical gap between the claimed "Probability of Matching" and the actual distance-based heuristic, combined with limited baseline comparisons, prevents the paper from being a strong accept. The contribution is solid but not transformative.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>