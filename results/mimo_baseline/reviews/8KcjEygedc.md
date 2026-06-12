## Summary

This paper develops a theoretical framework using random matrix theory to analyze when and why data curation (pruning) can outperform training on the full dataset. By modeling an imperfect oracle that selects training examples based on difficulty and correctness, the authors derive exact scaling laws for test error under both label-agnostic and label-aware curation, revealing phase transitions governed by generator quality, oracle quality, and data scale. The framework is validated on synthetic data and ImageNet, and used to provide a principled explanation for the seemingly contradictory success of "less is more" methods (LIMO, s1) versus traditional scaling laws in LLM mathematical reasoning.

## Strengths

- **Clean theoretical contribution with interpretable conditions.** Theorem 2 provides a sharp characterization: "keep hard" is optimal for strong generators with abundant data, while "keep easy" is optimal for weak generators. This resolves the apparent tension between LIMO-style curation and classical scaling laws with a principled condition (ρ, ρ*, data scale). The four-regime analysis (Figure 1) clearly demonstrates when "less is more" applies.

- **Novel extension of prior RMT-based analyses.** The framework generalizes the label-only curation settings of Feng et al. (2025) and Firdoussi et al. (2024) to incorporate difficulty-based pruning, which is the mode used in practice (Sorscher et al., 2022; LIMO; s1). The constants p, γ, β, β̃ from Eq. (8) cleanly capture the pruning strategy's effect on learning dynamics.

- **Dual practical relevance: efficiency and stability.** Beyond the efficiency story (curating less data to get better performance), the paper demonstrates that strategic pruning can prevent model collapse under iterative pseudo-labeling (Figure 3). This adds a practically important dimension—curation as a stabilizing mechanism for self-improvement loops.

- **Coherent unification of contradictory empirical findings.** The interpretation of Tables 1 and 2—showing that the same LLM is a strong generator for average AIME performance but a weak generator for the hardest questions—provides a satisfying explanation that directly follows from the theory rather than being ad hoc.

## Weaknesses

### Fatal
None.

### Major

- **Gap between theoretical assumptions and empirical validation.** The core theory assumes isotropic Gaussian features, linear models with squared loss, and independent generator/pruner/ground-truth vectors. The ImageNet experiments use a single pretrained model as both generator and pruner with pseudo-labels—this confounds several factors not in the theory (the pruner is not independent of the generator, features are not Gaussian, the model is nonlinear). While the qualitative trends match, the quantitative correspondence is not established, making it unclear how predictive the theory actually is for practical settings.

- **The LLM math reasoning analysis is purely interpretive, not experimental.** Section 4.2 reinterprets tables from other papers (Muennighoff et al., 2025; Ye et al., 2025; Sun et al., 2025) rather than presenting controlled experiments. The claim that "the base LLM is a strong generator for average problems but a weak generator for hard problems" is an assumption that maps onto the theory, not a measured quantity. This risks circular reasoning: the theory's flexibility (any observation can be explained post-hoc by tuning ρ) reduces its explanatory power.

- **Theorem 2 requires ρ* → 1 (excellent pruner).** The most practically relevant case is when the pruner is imperfect (ρ* < 1), which is not characterized in the main text. If the pruner has moderate quality, it's unclear whether the "keep hard" vs. "keep easy" dichotomy still holds or whether intermediate strategies dominate. This limits the practical guidance the theory provides.

### Minor

- **The pruning ratio p is treated as given, not optimized jointly.** In Theorem 2, the analysis fixes p and asks which q is optimal over Q_p. The more practical question—what is the jointly optimal (p*, q*)—would require additional analysis and is left implicit in the phase diagrams of Figure 1.

- **The squared loss + sign classifier pipeline is non-standard.** Using squared regression loss for binary classification is analytically convenient but uncommon in practice. The paper does not discuss how results might change under logistic loss or hinge loss, which would better match practical classification setups.

- **Model collapse experiment is suggestive but limited.** Figure 3 shows 6 rounds of pseudo-labeling on a single task. The paper claims to "prevent model collapse," but the experiment doesn't show the long-run dynamics or the conditions under which pruning eventually fails, which would strengthen the claim.

### Trivial
None.

## Nice-to-Haves

- A sensitivity analysis showing how the optimal strategy changes as ρ* decreases from 1 (i.e., imperfect oracle) would significantly strengthen the practical guidance.
- Quantifying ρ empirically for the LLM experiments (e.g., measuring the generator's error rate on different difficulty slices of AIME) would make the interpretation in Section 4.2 more than post-hoc.
- A brief discussion of how the theory changes under non-isotropic covariate shift (C_g ≠ Σ ≠ I) would address a more realistic setting, even if only qualitatively.

## Novel Insights

The paper's genuinely novel insight is the identification of generator quality ρ as the key variable governing when to prune and in which direction. While "keep hard" strategies have been explored empirically, the theoretical result that the optimal strategy flips depending on the generator's proficiency—and that this flip interacts with data scale to create a four-regime taxonomy—is new. The observation that model collapse can be understood through this lens (a collapsed model is a weak generator, so one should keep easy examples) provides a principled alternative to the ad hoc correction methods in the model collapse literature. Additionally, the resolution of the LIMO-vs-scaling-laws paradox through the strong-vs-weak generator distinction is a clean conceptual contribution.

## Suggestions

- Add controlled experiments where generator quality (ρ) is explicitly varied (e.g., by training generators on different amounts of clean data) and the predicted regime transitions are measured quantitatively, not just qualitatively.
- Characterize the optimal strategy for imperfect pruners (ρ* < 1) in the main text, as this is the realistic setting for LIMO/s1 where the "verifier" is a capable but fallible LLM.
- Validate the LLM interpretation by computing ρ on actual difficulty-sliced subsets of AIME, making the theory's predictions falsifiable rather than purely explanatory.

## Score and Decision

The paper makes a genuine theoretical contribution with clean results that address a timely and important question. The framework is well-motivated, the mathematical analysis appears sound, and the connections to practical methods and model collapse add value. However, the gap between theory and practice is significant, the most practically relevant case (imperfect oracle) is underexplored, and the LLM analysis risks being unfalsifiable post-hoc interpretation. The paper sits at the boundary: the theoretical insights are valuable, but the empirical validation doesn't fully close the loop.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>