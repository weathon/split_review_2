## Summary

This paper investigates whether common sparse autoencoder (SAE) evaluation metrics—particularly auto-interpretability scores—can distinguish between SAEs trained on fully trained transformers versus those trained on randomly initialized transformers. The authors find that across multiple Pythia model sizes (70M to 6.9B parameters) and randomization schemes, aggregate metrics like AUROC for "fuzzing" and "detection" tasks, reconstruction cosine similarity, and explained variance are surprisingly similar between trained and randomized models. The paper argues that high auto-interpretability scores alone do not guarantee discovery of learned, computationally relevant features, and recommends routine randomized baselines and alternative measures like token distribution entropy to capture feature "abstractness."

## Strengths

- **Important sanity check for the field**: The paper addresses a fundamental methodological concern in mechanistic interpretability—whether SAE evaluation metrics actually measure what researchers think they measure. This is a timely and important question given the widespread adoption of SAEs in interpretability research.

- **Comprehensive experimental design**: The authors test multiple randomization schemes (re-randomized with/without embeddings, step-0 initialization, Gaussian control), multiple model sizes (70M to 6.9B), multiple layers, and multiple metrics. The inclusion of the "control" variant (Gaussian embeddings) provides a clear lower bound for comparison.

- **Clear negative result with practical implications**: The finding that auto-interpretability scores for trained and randomized models overlap substantially (Figure 1) is striking and well-documented. The paper correctly identifies that this does not invalidate SAEs but rather reveals limitations in current evaluation practices.

- **Toy model analysis provides mechanistic intuition**: Section 4's toy models help explain *why* random networks might preserve or amplify superposition, moving beyond mere empirical observation to provide theoretical grounding for the results.

## Weaknesses

### Fatal
None.

### Major

- **The paper overstates the novelty of the core finding**: Prior work (Bricken et al., 2023) already showed that auto-interpretability scores discriminated between random and trained one-layer transformers, and the paper's own results show that for smaller models (Pythia-70m), the gap is relatively large. The paper's main claim is that this gap narrows for larger models, but the mechanism for *why* this happens is not well-explored. The paper would be stronger if it systematically investigated what drives the convergence at larger scales.

- **The "token distribution entropy" metric is underdeveloped as a proposed solution**: The paper presents entropy as a proof-of-concept for measuring feature "abstractness," but the analysis is preliminary. The entropy measure is computed only on maximally activating examples used for explanation generation, which may introduce selection bias. Moreover, the paper does not demonstrate that entropy actually correlates with human judgments of feature quality or computational relevance. Without validation, this remains a suggestive but unproven alternative.

- **Limited exploration of why the results differ from prior work on board games (Karvonen et al., 2024c)**: The paper mentions this discrepancy in Section 2 but dismisses it with the claim that "language is sparse" while board game concepts are not. This is a speculative explanation that deserves more rigorous treatment. If the paper's central claim is that language data's sparsity structure drives the results, this should be tested more directly (e.g., by comparing SAEs on language data with different sparsity characteristics).

### Minor

- **The paper does not systematically vary the SAE training data size**: The primary experiments use 100M tokens, with only a subset of experiments at 1B tokens (mentioned in Appendix C). Given that SAE quality improves with more data, it would be informative to see whether the convergence between trained and random models persists with much larger SAE training budgets.

- **The "CE Loss Score" metric is only shown for the trained variant**: The paper correctly notes that this metric "only makes sense for the trained variant," but this limits the comparison. A more informative approach might be to report the raw cross-entropy loss for all variants, which would show that random models have poor loss regardless of SAE reconstruction.

- **The paper uses a single explanation model (Llama-3.1-70B)**: While this is a reasonable choice, the results might depend on the specific capabilities of this model. The paper acknowledges this in the limitations but does not explore how results might change with different explanation models.

### Trivial
- The paper's title is slightly misleading: the claim is not that metrics "do not distinguish" trained from random transformers in all settings, but rather that they "may not reliably distinguish" them, especially at larger model scales.

## Nice-to-Haves

- A more systematic investigation of what drives the convergence at larger model sizes (e.g., is it the increased number of SAE latents, the deeper residual stream, or something else?)
- Validation of the token distribution entropy metric against human expert judgments of feature quality
- Testing on non-Pythia model families to assess generality
- Analysis of whether the results hold for different SAE architectures (e.g., Gated SAEs, JumpReLU SAEs) beyond TopK SAEs

## Novel Insights

The paper's most novel insight is that the failure of auto-interpretability metrics to distinguish trained from random models is not simply a measurement artifact but may reflect genuine properties of how random neural networks process sparse linguistic data. The toy model analysis in Section 4 suggests that random weight matrices can preserve or even amplify the superposition structure present in input data, meaning that SAEs trained on random models may be recovering *real* statistical structure—just not structure that arises from learned computation. This reframes the problem: the issue is not that SAEs fail on random models, but that they succeed too well, and current metrics cannot distinguish between different *sources* of the structure being recovered. This is a more nuanced and interesting claim than a simple "metrics are bad" argument.

## Suggestions

1. **Strengthen the entropy analysis**: Validate the token distribution entropy metric against human annotations or against known ground-truth features (e.g., in synthetic settings where the true features are known). Show that entropy correlates with human judgments of feature "interestingness" or with downstream task relevance.

2. **Test the "language sparsity" hypothesis directly**: Compare SAE performance on language data with artificially manipulated sparsity (e.g., subsampling rare tokens) versus data with different sparsity characteristics (e.g., code, mathematical text). This would test whether the convergence at larger scales is driven by data sparsity.

3. **Investigate the scaling behavior more systematically**: The paper shows that the gap between trained and random models narrows with model size, but does not explain why. Is it because larger models have more layers, larger residual streams, or because the SAEs have more capacity? Controlled experiments varying these factors independently would be informative.

4. **Consider alternative null models**: Beyond random weights, consider null models that preserve some statistical properties of the trained model (e.g., models with shuffled weights, or models with the same weight distribution but no training). This would help isolate what aspects of "trainedness" the metrics are (or are not) capturing.

## Score and Decision

The paper addresses an important and timely question in mechanistic interpretability with a well-designed experimental setup. The core finding—that aggregate auto-interpretability metrics can be similar for trained and random models, especially at larger scales—is a valuable sanity check for the field. However, the paper's contributions are somewhat incremental given prior work (Bricken et al., 2023) already established that this distinction can fail, and the proposed solution (token distribution entropy) is underdeveloped. The paper would benefit from deeper investigation into *why* the convergence occurs and from validation of the proposed alternative metric. Despite these limitations, the paper's clear empirical demonstration and practical recommendations (routine randomized baselines) make it a useful contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>