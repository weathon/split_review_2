## Summary

This paper addresses multimodal sentiment analysis under frame-level missing data by proposing HiTNet, a dual-stream network inspired by hippocampal memory retrieval and thalamic perceptual regulation. The hippocampal-inspired stream uses a semantic memory module and sparse activation network to recover modality-specific information, while the thalamic-inspired stream employs confidence perception and adaptive cross-modal completion to integrate high-quality multimodal cues. Experiments on MOSI, MOSEI, and SIMS show consistent improvements over state-of-the-art methods, with average accuracy gains of 1.5–2.0% across missing rates and strong robustness even under 90% missing data.

## Strengths

- **Problem relevance**: Frame-level missingness in multimodal sentiment analysis is a practical and underexplored challenge compared to modality-level missingness. The paper clearly motivates the problem and the limitations of existing cross-modal consistency methods.

- **Technically well-designed architecture**: The dual-stream design is modular and principled—the intra-modal stream uses a dynamically updated key-value memory with a gating mechanism to suppress retrieval noise, and a sparse activation network with a utilization balance loss to encourage diverse sub-network usage. The inter-modal stream uses a learned confidence score to weight cross-modal contributions, which is a natural way to handle heterogeneous data quality.

- **Thorough experimental evaluation**: Experiments cover three diverse benchmarks (MOSI, MOSEI, SIMS) with multiple metrics, missing rates from 0 to 0.9, and extensive ablations of components and losses. The confusion matrix visualization (Figure 5) and feature distance analysis (Figure 4) provide useful qualitative insights into why the method works.

- **Consistent and non-trivial improvements**: The method outperforms all compared baselines across nearly all metrics and datasets, with particularly noticeable gains at high missing rates. The 2.56% improvement in Acc-7 on MOSEI (Table 1) and 4.53% improvement in Acc-3 on SIMS (Table 2) are substantive in this domain.

- **Reproducibility**: The paper provides detailed implementation settings, publicly released code, and uses standard datasets, making the work verifiable.

## Weaknesses

### Fatal

None.

### Major

1. **Overclaimed biological inspiration**: The hippocampal and thalamic analogies are used at a purely metaphorical level. The semantic memory module is a standard key-value memory with cosine similarity retrieval and a learnable gating mechanism—no known hippocampal dynamics (e.g., pattern separation, place cell coding) are modeled beyond the general idea of “memory retrieval.” Similarly, the confidence-perception module is a simple MLP classifier on top of Transformer features, which does not reflect thalamic gating mechanisms. The paper would lose little technical content if the biological framing were removed, which weakens the claimed novelty of “brain-inspired” design and raises questions about whether the contribution is more than an engineering combination of existing techniques (memory networks + confidence-weighted fusion).

2. **Lack of statistical significance**: Results are reported as averages over three random seeds, but no standard deviations, confidence intervals, or significance tests are provided. Given that the average improvements over strong baselines are modest (1.5–2.0% for many metrics), it is impossible to assess whether the gains are statistically meaningful. This is a critical omission for a paper making “state-of-the-art” claims.

3. **Hyperparameter sensitivity across datasets**: The loss weights (α, β, γ) vary dramatically between datasets (e.g., α=10 on MOSI vs. 1.5 on MOSEI; γ=0.1 on MOSI vs. 9.0 on MOSEI). This suggests that the method requires careful per-dataset tuning to achieve the reported performance, which reduces confidence in its general applicability. The paper does not provide a principled justification for these choices beyond presenting ablation results in the appendix.

4. **Potentially unfair baseline comparison**: The paper relies on results reported in the LNLN paper for almost all baselines, rather than re-implementing and evaluating all methods under the same training conditions. Crucially, HiTNet uses a training strategy where half the samples have zero missing rate to avoid overfitting. It is unclear whether the baselines used the same training protocol or a different one. If not, the comparison may be biased.

### Minor

- The “hierarchical fusion” design choice of placing language last is justified only by intuition about language dominance. No ablation comparing different fusion orderings or concurrent fusion is provided.
- In Table 3, the row label “w/o $L_{abs}$” appears to be a typo (should be $\mathcal{L}_{ubl}$). While minor, this suggests incomplete proofreading.
- The statement in the abstract that the method handles “simultaneous random frame-level missingness across all modalities” is somewhat misleading; the actual procedure treats each modality independently with independently sampled missing rates.

### Trivial

- Figure 1 and some other figure captions are repeated verbatim in the text, which is unnecessary but not harmful.

## Nice-to-Haves

- Include standard deviations or confidence intervals for all main results to enable statistical assessment.
- Provide an ablation comparing HiTNet with a version that replaces the memory module with a simple MLP predictor to isolate the benefit of memory retrieval, and compare with a non-biological gated recurrent completion baseline.
- Study the sensitivity of the learned confidence scores across different missing rates and datasets to better understand the confidence-perception module’s behavior.
- Evaluate on additional missing patterns (e.g., block missingness, modality-level missingness is already partially covered in Table 4 but could be expanded).

## Novel Insights

None beyond the paper’s own contributions. The key technical insight—that separately recovering intra-modal semantics via memory and then adaptively fusing cross-modal information with learned confidence weights outperforms pure cross-modal consistency methods—is a sensible engineering principle but is not a fundamentally new theoretical or algorithmic concept. The biological framing does not generate additional insight beyond what the architecture already provides.

## Suggestions

- Tone down the biological claims in the abstract and introduction; the paper is stronger if presented as a dual-stream architecture with memory-guided intra-modal completion and confidence-weighted cross-modal fusion.
- Provide error bars or statistical significance tests for the main results, especially for the averaged metrics across missing rates.
- Update the experimental protocol to either re-implement all baselines under identical training conditions (including the zero-missing-rate augmentation) or clearly state the protocol used by the baselines and justify comparability.
- Perform a hyperparameter sensitivity analysis (e.g., across a grid of α, β, γ) to show that performance is not overly dependent on specific values.

## Score and Decision

**Score**: 6  
**Decision**: Borderline Accept

**MY FINAL SCORE**: <score>6</score>  
**MY FINAL DECISION**: <decision>Reject</decision>