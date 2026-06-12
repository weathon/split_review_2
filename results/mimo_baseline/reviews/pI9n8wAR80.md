## Summary

This paper proposes CoLA (Co-Calibrated Logit Adjustment), a framework for Long-Tailed Semi-Supervised Learning that addresses two limitations of existing Logit Adjustment (LA) methods: (1) overestimation of head-class prevalence due to sample redundancy in frequency counting, and (2) failure to adapt the overall adjustment strength to the estimated distribution. CoLA introduces DDDE, which uses effective rank of class representations to produce redundancy-aware distribution estimates, and LMC, a meta-learning procedure that learns the optimal overall adjustment strength on a distribution-matched proxy validation set. Extensive experiments across 4 benchmarks and multiple distribution types demonstrate consistent improvements over existing methods.

## Strengths

- **Clear problem decomposition and motivation**: The paper identifies two specific, concrete weaknesses of existing LA-based LTSSL methods and motivates them well with Figure 1. The observation that optimal τ is highly sensitive to the estimated distribution and number of classes (Figure 1b) is a genuinely useful insight that is empirically well-supported.
- **Principled co-design framework**: The key contribution—co-designing class-wise and overall adjustment—addresses a real gap. The ablation in Table 4 convincingly shows the bidirectional interaction: DDDE without LMC (w/o D-1/2/4) shows inconsistent optimal τ across datasets, and LMC without DDDE (w/o D-L) produces misguided τ due to unreliable distribution estimates.
- **Comprehensive experimental evaluation**: Experiments span 4 datasets (CIFAR-10-LT, CIFAR-100-LT, STL-10-LT, SIN-127) across 6 distribution types with 18+ baseline methods. CoLA achieves the best or near-best performance across virtually all settings, with particularly strong gains on CIFAR-100-LT where it surpasses the runner-up by over 1 percentage point in most cases.
- **Theoretical grounding**: The generalization bound (Proposition 1) meaningfully connects the quality of distribution estimation (DDDE) to the meta-learning procedure (LMC) through the discrepancy term, providing principled justification for the co-design philosophy.
- **Effective rank for distribution estimation**: Using erank to quantify sample redundancy is a creative approach that leverages the geometry of learned representations rather than relying on naive counting. Table 5 demonstrates consistently lower L₂ distances to the true distribution compared to MCA and NWGMA baselines.

## Weaknesses

### Fatal
None.

### Major

- **Modest margins with overlapping confidence intervals**: On CIFAR-10-LT, the improvements over the best existing methods (e.g., Meta-Expert, ACR) are often 0.5–2 percentage points, and several improvements fall within one standard deviation of the second-best method. For example, on CIFAR-10-LT consistent distribution, CoLA achieves 81.87±2.70 vs. ACR's 80.85±2.92—a gap of 1.02 but with overlapping intervals. While consistency across distributions is valuable, the practical significance of gains within noise bounds is uncertain. Reporting significance tests or confidence-level comparisons would strengthen the claims.

- **Assumption 3 (shared class-conditional distribution) is strong in real-world settings**: The theoretical analysis and the proxy validation set construction both rely on labeled and unlabeled data sharing class-conditional distributions. On STL-10, the unlabeled data may contain OOD samples, violating this assumption. The paper does not discuss how violations of this assumption affect the meta-learning procedure or the quality of the learned τ, which is important given that one of the paper's motivations is handling realistic scenarios.

### Minor

- **Computational overhead of DDDE**: Computing the effective rank requires forming d × m_y feature matrices and performing SVD for each class at every update. For large feature dimensions d and large unlabeled datasets, this could be nontrivial. While mentioned to be in Appendix H, a brief in-paper discussion of practical overhead would help readers assess scalability.

- **Two-stage training procedure**: The method requires a warm-up phase using ACR's τ before switching to LMC-learned τ. This introduces sensitivity to the warm-up duration and the transition point (epoch 200 in experiments). The paper does not ablate the warm-up length or discuss sensitivity to this hyperparameter.

- **Linear vs. logarithmic LA term**: The choice to use -τ·p instead of -τ·log(p) in the meta-learning objective (Section 4.2) is motivated by numerical stability and a reference to Mor & Carmon (2025), but the paper does not empirically compare these two formulations. Given that the standard post-hoc LA uses the log term, this design choice warrants empirical validation.

### Trivial
None.

## Nice-to-Haves

- Empirical comparison of linear vs. logarithmic adjustment terms in the meta-learning objective to validate the design choice.
- Sensitivity analysis of the warm-up phase length and the transition epoch.
- Experiments on larger-scale benchmarks (e.g., ImageNet-LT with SSL) to better demonstrate scalability claims.
- Analysis of how the effective rank estimation quality evolves during training—does it become more reliable as the model improves?

## Novel Insights

The paper's most novel insight is that the two components of Logit Adjustment—class-wise and overall—are not independent but mutually dependent: the optimal overall adjustment strength is a function of the estimated class distribution, and vice versa. This bidirectional interplay, empirically demonstrated in Figure 1b and the ablation studies, suggests that treating these components independently (as all prior work does) leaves significant performance on the table. The effective rank approach for capturing representation-level redundancy in class frequency estimation is also a novel contribution that could have applications beyond LTSSL.

## Suggestions

- Add statistical significance tests (e.g., paired t-tests or bootstrap confidence intervals) to the main results tables, especially for cases where margins are within one standard deviation.
- Include a brief ablation comparing -τ·p vs. -τ·log(p) in the LMC objective.
- Discuss the sensitivity of CoLA to the warm-up phase length and provide guidance on selecting it.
- Acknowledge and analyze the impact of Assumption 3 violations on the proxy set construction and τ optimization, particularly for STL-10 settings.

## Score and Decision

The paper presents a well-motivated and technically sound framework that makes meaningful contributions to the LTSSL problem. The co-design principle is insightful, the components are well-justified both theoretically and empirically, and the experimental evaluation is comprehensive. However, the gains, while consistent, are sometimes modest and within statistical noise margins. The method's reliance on the shared class-conditional distribution assumption is a limitation that deserves more discussion. Overall, this is a solid paper that advances the state of the art in a principled way, though the incremental nature of improvements over strong baselines warrants a cautious recommendation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept