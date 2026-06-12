##Summary

This paper introduces CausalNovo, a model-agnostic framework for de novo peptide sequencing that aims to learn causal representations from mass spectra by focusing on signal fragment ions and ignoring spurious noise peaks. Grounded in a Structural Causal Model (SCM), the framework derives two principles—independence and sufficiency—and implements a Causality Extraction Module (CEM) with information-theoretic objectives to disentangle causal factors from noise. Extensive experiments on three public datasets show consistent improvements over multiple state-of-the-art baselines at the amino acid, peptide, and PTM levels, with particularly strong gains under noisy conditions.

## Strengths

- **Principled causal framework**: The paper formalizes de novo peptide sequencing within an SCM, deriving clear principles (independence and sufficiency) that guide the design of the CEM. This provides a solid theoretical foundation for the method.
- **Model-agnostic and broadly effective**: CausalNovo is integrated with three different baseline models (CasaNovo, AdaNovo, π-HelixNovo) and yields consistent improvements across all three datasets and multiple evaluation metrics, demonstrating its general applicability.
- **Thorough experimental evaluation**: The paper includes extensive experiments: comparison with SOTA, ablation studies of each component, vulnerability analysis under noise perturbation, cross-species validation, generalization across varying noise-signal ratios, and attention analysis. The results convincingly show that CausalNovo reduces reliance on spurious correlations.
- **Clear motivation and problem diagnosis**: The preliminary vulnerability analysis (Figure 1) effectively demonstrates that existing models depend on non-causal peaks, motivating the need for a causality-informed approach. This makes the contribution well-grounded.

## Weaknesses

### Fatal
None.

### Major
- **Reliance on theoretical spectrum for intervention**: The causal intervention requires identifying non-causal ions by comparing peaks to a theoretical spectrum computed from the ground-truth peptide sequence. While this is a standard approach, it assumes the theoretical spectrum accurately captures all causal ions. The paper tests with 18 ion types to mitigate this, but the intervention quality is inherently tied to the completeness of the theoretical model. A more thorough discussion of potential biases introduced by this step would strengthen the paper.
- **Clarity of the sufficiency/purification objective**: The paper maximizes \(I(z_s; Y)\) to "purify" \(z_c\), but the reasoning that this indirectly leads to purification is not fully explained. Maximizing mutual information between the non-causal representation and the label could encourage \(z_s\) to also contain label-relevant information, potentially undermining disentanglement. The ablation shows it helps, but a deeper theoretical or empirical analysis of why this works would be valuable.

### Minor
- **Evaluation protocol scope**: The paper follows the NovoBench protocol, which trains and tests on the same set of species (with yeast as test). While cross-species validation is provided, the paper acknowledges that recent methods (e.g., ContraNovo, RankNovo) use a more realistic protocol with large-scale external training corpora and out-of-distribution test sets. Not evaluating under that protocol limits the assessment of real-world utility, though this is noted as future work.
- **Training overhead**: The paper mentions a ~2.3x increase in training time but does not provide detailed runtime comparisons or discuss scalability. This is a practical concern for adoption.
- **Comparison with recent methods**: The paper compares with several baselines but does not include some recent methods like ContraNovo or RankNovo under the same retrained setting. The comparison with SearchNovo uses results from NovoBench, which may have different training configurations. A more comprehensive comparison would strengthen the empirical claims.

### Trivial
None.

## Nice-to-Haves

- An analysis of the learned importance scores \(M\) (e.g., visualization of which peaks are assigned high scores) would provide additional interpretability and validate that the model indeed focuses on causal ions.
- A discussion of the sensitivity to the hyperparameter \(\alpha\) (fraction of noise peaks replaced) and the tolerance threshold \(\gamma\) would help practitioners apply the method.

## Novel Insights

Beyond the paper's own contributions, the key insight is that de novo peptide sequencing models can be made more robust by explicitly modeling the causal structure of the data generation process. The paper demonstrates that even simple causal principles (independence and sufficiency) can be operationalized via contrastive learning and information-theoretic objectives to yield significant performance gains. This suggests that many existing biological sequence prediction tasks that suffer from noisy inputs could benefit from similar causality-informed frameworks.

## Suggestions

- Provide a more detailed theoretical justification for why maximizing \(I(z_s; Y)\) helps purify \(z_c\), possibly with a toy example or additional ablation.
- Include runtime comparisons (training time per epoch, total training time) for the baselines with and without CausalNovo to quantify the overhead.
- Consider evaluating under the more realistic protocol (training on large-scale corpora, testing on out-of-distribution data) in a follow-up study, as this would strengthen the claim of real-world utility.

## Score and Decision

**Score**: 8  
**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>