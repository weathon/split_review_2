## Summary

This paper develops a theoretical framework for understanding when data curation (pruning) improves generalization in high-dimensional binary classification. The authors analyze label-agnostic and label-aware curation rules, deriving exact scaling laws for test error that reveal sharp phase transitions based on generator quality, oracle quality, and data size. They show that "less is more" applies when the generator is strong and data is abundant, while "more is more" applies when the generator is weak or data is scarce, and validate their theory on ImageNet and by reconciling contradictory findings in LLM mathematical reasoning.

## Strengths

- **Principled theoretical framework**: The paper provides exact analytical formulas (Theorem 1) for test error under data curation, going beyond heuristic approaches. The derivation using random matrix theory is rigorous and yields interpretable quantities (p, γ, β, β̃) that capture the effect of pruning strategies.

- **Clear, testable predictions**: Theorem 2 provides a crisp, actionable result: keep hard examples when the generator is strong (ρ→1), keep easy examples when the generator is weak (ρ<1). This directly explains the success of LIMO/s1 and resolves the apparent contradiction with classical scaling laws.

- **Empirical validation across domains**: The paper validates theoretical predictions on synthetic data, ImageNet (Figure 2), and provides a compelling explanation for LLM math reasoning results (Tables 1-2). The model collapse mitigation result (Figure 3) is particularly striking and practically relevant.

- **Novel connection to model collapse**: Showing analytically that strategic curation can prevent the catastrophic degradation observed in iterative self-training is a significant contribution that connects two previously separate literatures.

## Weaknesses

### Major

- **Gap between theory and practice in the LLM analysis**: The reconciliation of LIMO/s1 results (Tables 1-2) is post-hoc and qualitative. The paper does not actually compute ρ, ρ_*, or ρ_g for these LLM settings, nor does it verify that the theoretical phase transition curves match the empirical scaling behavior. The argument that "for average performance ρ is high, for hard performance ρ is low" is plausible but not quantitatively validated.

- **Limited empirical scope**: The ImageNet experiments use a pre-trained model as both generator and pruner, which is a specific setup. The paper does not test whether the theoretical predictions hold for other architectures (e.g., ResNets, ViTs with different training recipes) or other datasets (e.g., CIFAR, text classification). The claim that "the same principles apply to large-scale vision tasks" is supported by only one experimental configuration.

- **The "keep easy" vs "keep hard" dichotomy may be oversimplified**: Real-world curation strategies (LIMO, s1) use more nuanced criteria than just margin-based difficulty. The paper acknowledges this but does not analyze whether the theoretical results extend to more complex pruning functions (e.g., diversity-based selection, correctness filtering combined with difficulty).

### Minor

- **The isotropic assumption (Σ = C_g = I_d) limits generality**: While the paper mentions more general results are in the appendix, the main text focuses on the isotropic case. Covariate shift (C_g ≠ Σ) is acknowledged in the setup but not analyzed in the main results, which weakens the claim of a "unifying framework."

- **The model collapse experiment (Figure 3) uses only 6 rounds**: While the trend is clear, longer-term behavior (e.g., 20+ rounds) would strengthen the claim that pruning "prevents" rather than merely delays collapse.

### Trivial

- The notation w_0 and w_o is used inconsistently (Section 2.2 vs Section 3).

## Nice-to-Haves

- Provide quantitative validation of the LLM analysis by estimating ρ, ρ_*, ρ_g from actual model checkpoints and showing that the predicted phase transition matches the empirical scaling.
- Test on at least one additional vision dataset (e.g., CIFAR-100) and one text classification task to demonstrate broader applicability.
- Analyze the effect of the pruning ratio p on the phase transition boundary more explicitly—the current results show the optimal strategy but not the precise p* where "less is more" becomes optimal.

## Novel Insights

The paper's key insight is that the optimal data curation strategy is not universal but depends on a simple geometric quantity: the alignment between the generator (data labeler) and the ground truth (ρ). When ρ is high (strong generator), the model benefits from focusing on hard examples to refine its already good performance. When ρ is low (weak generator), the model needs easy examples to build basic competence. This provides a principled explanation for why LIMO/s1 succeed (strong base LLM) and why "more is more" still holds for hard subsets (weak generator relative to those examples). The connection to model collapse is particularly insightful: strategic pruning acts as a stabilizer by preventing the accumulation of errors from mislabeled or uninformative examples.

## Suggestions

- Add a quantitative analysis of the LLM results: estimate ρ for the base model on average vs hard AIME questions (e.g., using pass rates as a proxy for generator quality) and show that the predicted optimal strategy matches the empirical findings.
- Include experiments with at least one additional architecture/dataset to demonstrate that the theoretical predictions are not artifacts of the specific ImageNet setup.
- Clarify in the main text how the results change under covariate shift (C_g ≠ Σ), even if only through a corollary or remark.

## Score and Decision

The paper makes a significant theoretical contribution by providing exact scaling laws for data curation and resolving a central paradox in modern ML. The theory is rigorous, the predictions are clear and testable, and the empirical validation, while limited in scope, is convincing. The main weaknesses are the post-hoc nature of the LLM analysis and the limited empirical breadth, but these do not invalidate the core contribution. The paper is likely to have high impact by providing a principled foundation for data curation research.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>