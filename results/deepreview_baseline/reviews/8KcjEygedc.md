## Summary

This paper develops a theoretical framework for data curation in high-dimensional binary classification, deriving exact scaling laws for test error under two types of pruning oracles: label-agnostic (difficulty-based) and label-aware (correctness + difficulty). The theory reveals sharp phase transitions showing when aggressive pruning outperforms full-data training—specifically, “keep hard” is optimal when the generator is strong and data is abundant, while “keep easy” or full-data training is better otherwise. The predictions are validated on synthetic data, ImageNet pseudolabeling experiments, and shown to reconcile contradictory findings in LLM mathematical reasoning (LIMO/s1 versus classical scaling laws). The paper also demonstrates analytically and empirically that strategic curation can prevent model collapse in iterative self-training loops.

## Strengths

- **Principled theoretical contribution**: The paper moves beyond heuristic curation by providing a rigorous, analytically tractable model (high-dimensional Gaussian, linear classifier, RMT-based limiting analysis) that yields exact test error formulas. This gives clear, testable predictions about when and why “less is more.”
- **Unifying explanation for recent empirical puzzles**: The theory successfully explains the seemingly contradictory results in LLM reasoning—why LIMO/s1 benefit from aggressive pruning on average performance yet fail on the hardest questions—by attributing it to the generator’s quality (ρ). This is a valuable conceptual insight.
- **Empirical validation beyond toy settings**: The ImageNet experiments use a realistic pipeline (pseudo-labels from a ViT, control over generator strength via training set size) to confirm the theory’s predictions, including the crossover from “keep easy” to “keep hard” as data scale increases and the mitigation of model collapse.
- **Clear presentation**: The paper is well structured, with each section building intuition, and the figures effectively illustrate the key phase transitions. The distinction between label-agnostic and label-aware curation is clearly motivated and connected to practical methods.

## Weaknesses

### Fatal
None.

### Major
- **Simplicity of the theoretical model**: The analysis assumes isotropic Gaussian features, a linear classifier with squared L2 loss, and binary classification. While this permits analytical tractability, the gap to realistic deep learning settings (nonlinear models, high-dimensional structured data, multi-class, multi-epoch optimization) is substantial. The paper acknowledges this limitation but does not provide evidence that the core insights survive in richer frameworks (e.g., random feature or kernel regimes). Without bridging this gap, the practical relevance of the exact scaling laws remains uncertain.

### Minor
- **Empirical validation of the ImageNet model collapse experiment (Figure 3)**: The experiment shows that "keep hard" stabilizes performance across rounds, but it only tracks a single run (no error bars) and uses 6 rounds. Model collapse in practice often requires many more iterations; longer-term stability is not demonstrated. Additionally, the "training on all data" baseline shows a clear degradation, but the mechanism could also be influenced by label noise accumulation beyond what the theory captures.
- **Over-reliance on qualitative alignment for LLM results**: The connection to LIMO/s1 and Sun et al. (2025) is compelling but purely conceptual. The paper does not attempt to estimate ρ, ρ_∗, or ρ_g for these models, nor does it run controlled experiments (e.g., varying the base LLM's strength across problem difficulty slices). The theory thus remains a plausible explanation rather than a verified quantitative prediction for LLMs.
- **Undefined constants in Theorem 1**: The functions m, m̃, and r are deferred to the appendix; while standard in RMT, the paper would benefit from stating their definitions in the main text to improve self-containedness. The proof sketch is too brief to assess correctness without the appendix.

### Trivial
- The remark about not having access to w_o (Section 2.2) is slightly redundant because it is already implied by the setup.

## Nice-to-Haves

- A synthetic experiment that varies the oracle quality ρ_∗ and generator-pruner alignment ρ_g independently to map out the full phase diagram predicted by the theory.
- A concrete example of how λ (regularization) interacts with pruning in the finite-n regime, as the paper focuses on the unregularized limit.
- A discussion of the computational overhead of the pruning oracle and how it compares to training on the full dataset.

## Novel Insights

Beyond the paper’s own theoretical results, a genuinely novel insight is the identification of a generator-quality threshold ρ_c that separates regimes where “keep hard” is optimal from regimes where “keep easy” or full-data training is optimal. This provides a unified, parameter-driven interpretation of apparently contradictory empirical strategies (e.g., LIMO’s aggressive pruning vs. classical scaling-law-driven scaling). The observation that the same framework can explain both the benefits of curation and the dynamics of model collapse—linking two previously separate phenomena—is a valuable conceptual contribution.

## Suggestions

- **Bridge to nonlinear models**: While the paper acknowledges this as a limitation, a natural and feasible next step is to extend the analysis to random features or the neural tangent kernel regime, which remain within the RMT toolkit. Showing that the phase transition structure persists would substantially strengthen the practical relevance.
- **Quantitative test on LLMs**: Even without running large-scale experiments, the authors could compute proxies for ρ (e.g., per-question accuracy of the base model) and check whether the “keep hard vs. keep easy” prediction holds on existing benchmarks using data from earlier papers. This would add rigor to the qualitative comparison.
- **Make main text more self-contained**: Include the definitions of m(z), m̃(z), r(z) and their dependence on p,γ,β,β̃ in the main text (even if brief) so that Theorem 1 is interpretable without the appendix.

## Score and Decision

**Score**: 8  
**Decision**: Accept

The paper presents a rigorous theoretical framework that resolves a central puzzle in data curation, with strong synthetic and moderate real-world validation. Its insights are timely and have the potential to influence both practice and future theory. The main weakness is the gap between the idealized model and deep learning practice, but this is openly acknowledged and does not invalidate the core contribution. I recommend acceptance.

MY FINAL SCORE: 8<score>8</score>
MY FINAL DECISION: <decision>Accept</decision>