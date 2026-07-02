## Summary
This paper introduces CausalNovo, a model-agnostic framework for de novo peptide sequencing that incorporates causal principles to disentangle true signal ions from spurious noise peaks in tandem mass spectra. Grounded in Structural Causal Models and Reichenbach’s Common Cause Principle, CausalNovo derives two key properties—independence and sufficiency—and operationalizes them via causal intervention (replace-based perturbation of noise peaks) and information-theoretic objectives (contrastive and cross-entropy losses) to learn causal representations. Extensive experiments on three benchmark datasets demonstrate consistent and significant improvements (up to 10%) across amino acid, peptide, and PTM-level metrics for multiple state-of-the-art baseline models.

## Strengths
- **Novel and principled formulation**: Formalizing de novo peptide sequencing within a Structural Causal Model and deriving clear causal principles (independence, sufficiency) is a well-motivated and theoretically grounded contribution that addresses a genuine limitation of existing statistical approaches.
- **Strong empirical evidence**: The paper provides comprehensive evaluations on three public datasets, including amino acid, peptide, PTM-level metrics, cross-species validation, vulnerability analysis, and generalization across varying noise-signal ratios. CausalNovo consistently and substantially improves multiple baseline models (CasaNovo, AdaNovo, π-HelixNovo), with relative improvements of up to 14% under perturbation.
- **Model-agnostic and practical**: The framework is designed to be integrable with any encoder-decoder architecture, requiring no architectural changes to the base model. The causal intervention uses domain knowledge (theoretical spectra) in a straightforward and effective manner, with negligible inference overhead.
- **Thorough ablation and analysis**: The ablation studies clearly isolate the contributions of each component (independence, purification, symmetric training, replace vs. enhance vs. drop). The attention analysis further provides mechanistic evidence that CausalNovo increases focus on causal peaks.

## Weaknesses
### Fatal
None.

### Major
- **Reliance on ground-truth labels for intervention**: The causal intervention step requires peptide-level ground truth to compute theoretical spectra and identify non-causal ions. While this is acceptable for supervised training (and common in related work), the paper does not discuss how this requirement limits applicability in settings where training labels are scarce or noisy, nor does it explore semi-supervised or self-supervised extensions.
- **Contrastive approximation for independence**: The independence objective is approximated via contrastive learning conditioned on Y (as a proxy for C). The paper does not analyze potential biases or failure cases of this approximation, nor does it compare with alternative mutual information estimators. The theoretical gap between the ideal independence condition and the practical contrastive loss is not fully bridged.

### Minor
- **Limited baseline diversity**: The three baseline models (CasaNovo, AdaNovo, π-HelixNovo) share similar Transformer-based architectures. Showing effectiveness on more diverse architectures (e.g., CNN-based PepNet or graph-based GraphNovo) would strengthen the claim of model-agnosticity.
- **Training overhead quantification**: The paper mentions a ~2.3× training time increase but does not provide specific wall-clock times or relative comparisons, making it difficult to assess the practical cost.
- **Attention analysis scope**: The analysis in Table 7 only examines the top-3 most attended peaks. A more granular analysis (e.g., attention weight distributions or per-position behavior) could provide deeper insight into how causal representations improve predictions.

### Trivial
- The notation in equation (5) uses a contrastive form that includes positive and negative sets; the denominator structure could be clarified (e.g., explicit reference to the NT-Xent family).
- Some table entries use inconsistent decimal places (e.g., Table 2 shows 0.706 vs. 0.671, while Table 1 shows consistent three-digit formatting).

## Nice-to-Haves
- Explore automatic determination of the m/z tolerance threshold γ or learn it as part of the model.
- Test CausalNovo on the recent "real-world" evaluation protocol (training on large-scale external corpora, evaluating on out-of-distribution test sets) as the paper notes in the conclusion.
- Provide theoretical analysis of when the independence–sufficiency trade-off guarantees identification of the true causal representation.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Extend the vulnerability analysis to include a comparison with other robust training techniques (e.g., adversarial training, spectral peak filtering) to contextualize the benefits of the causal approach.
- Report training time and inference time quantitatively with standard deviations.
- Discuss potential negative societal impacts or misuse (e.g., false positive peptide identifications in clinical proteomics) in the ethics statement.

## Score and Decision
**Score**: 8  
**Decision**: Accept  

The paper presents a well-motivated, principled, and empirically strong framework that addresses a significant limitation in de novo peptide sequencing. The causal formulation is novel and the experiments convincingly demonstrate the value of incorporating causality into proteomics. Minor weaknesses do not detract from the overall contribution.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: Accept