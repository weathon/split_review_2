## Summary

This paper provides the first theoretical analysis of the training dynamics and in-context learning (ICL) generalization of one-layer Mamba models, including robustness to outliers in prompts. The authors characterize the convergence and sample complexity of training Mamba on binary classification tasks, prove that Mamba can maintain accurate ICL generalization even when the fraction of outlier-containing context examples approaches 1, and compare these guarantees to those of linear Transformers, showing Mamba's superior robustness at the cost of slower convergence. The theoretical findings are supported by synthetic experiments.

## Strengths

- **First theoretical analysis of Mamba ICL training dynamics:** The paper provides the first rigorous theoretical characterization of how a one-layer Mamba model can be trained to perform in-context learning, including convergence guarantees and sample complexity bounds. This fills an important gap in the theoretical understanding of Mamba architectures.

- **Novel theoretical comparison with Transformers:** The paper provides a clean theoretical comparison between Mamba and linear Transformers under the same setting, showing that Mamba's nonlinear gating enables robustness to a much higher fraction of outliers (α approaching 1) compared to Transformers (α < 1/2), while Transformers converge faster. This is a non-trivial theoretical contribution.

- **Mechanistic understanding of Mamba's ICL:** The analysis decomposes Mamba's ICL mechanism into two components: the linear attention layer selects context examples sharing the same relevant pattern as the query, while the nonlinear gating suppresses outliers and induces a local bias. This provides a clear, interpretable explanation for Mamba's behavior.

- **Empirical validation:** The synthetic experiments support the theoretical claims, particularly the robustness comparison (Figure 2) and the mechanistic analysis (Figures 3, 4, Table 1).

## Weaknesses

### Fatal
None.

### Major
- **The theoretical analysis is limited to a highly simplified one-layer Mamba with linear attention and binary classification on orthogonal patterns.** While the authors acknowledge this limitation, the gap between this setting and practical Mamba models (which use multi-layer architectures, selective state spaces, and softmax-free gating) is substantial. The paper's core claims about "Mamba" as a general architecture are based on this simplified model. The extension to multi-layer Mamba in experiments (Section 4.2) is empirical only and lacks theoretical backing.

- **The comparison with Transformers is against a linear attention Transformer, not a standard softmax Transformer.** The paper explicitly sets G=1 to obtain a linear Transformer, but this is a significant simplification. Modern Transformers use softmax attention, which provides inherent normalization and robustness properties. The paper's claim that "Mamba outperforms Transformers" is therefore misleading, as it compares against a weakened Transformer variant. The brief discussion in Appendix B.1 about softmax attention is insufficient to bridge this gap.

- **The theoretical results rely on numerous strong assumptions that collectively limit the practical relevance.** These include: orthogonal patterns, equal norm patterns, specific initialization schemes, balanced labels, specific outlier structure (linear combinations of training outliers), and the requirement that test-time outliers must have positive linear coefficients summing to a positive value. The accumulation of these assumptions makes it difficult to assess whether the theoretical insights would hold in more realistic settings.

## Minor

- **The paper's claims about being "first" are somewhat overstated.** While the paper is the first to analyze training dynamics of Mamba for ICL, there is existing theoretical work on Mamba-like models (Li et al., 2024b; 2025b; Joseph et al., 2024; Bondaschi et al., 2025) that the authors acknowledge but dismiss as not addressing training dynamics. The novelty is incremental rather than foundational.

- **The experimental validation is limited to synthetic data.** While synthetic experiments are appropriate for validating theoretical claims, the paper would benefit from at least one real-world experiment to demonstrate that the theoretical insights translate to practical settings. The authors mention additional experiments in Appendix B.2 but these are not described in the main text.

- **The paper's claims about "first theoretical analysis" should be more carefully qualified.** The analysis is for a one-layer Mamba with specific simplifications (A = -I, specific initialization, etc.), which is a significant departure from the full Mamba architecture. The paper would benefit from a clearer statement of what aspects of the full Mamba are captured and what are not.

## Nice-to-Haves

- Extending the analysis to multi-layer Mamba or to the full selective SSM formulation would significantly strengthen the paper's claims about Mamba as a general architecture.
- Including experiments on real-world datasets (e.g., text classification with poisoned prompts) would help bridge the gap between theory and practice.
- A more detailed discussion of how the theoretical conditions (e.g., orthogonal patterns, specific initialization) could be relaxed or verified in practice would be valuable.

## Novel Insights

The paper's key insight is that Mamba's nonlinear gating mechanism serves a dual role in ICL: it suppresses outlier-containing examples while inducing a local bias that emphasizes examples closer to the query. This provides a mechanistic explanation for why Mamba can be more robust to outliers than linear Transformers, despite being harder to optimize. The theoretical characterization of the trade-off between optimization difficulty and robustness is a genuinely novel contribution.

## Suggestions

- Clarify in the abstract and introduction that the theoretical analysis is for a one-layer Mamba with linear attention and specific simplifications, and that the comparison is against a linear Transformer (not a standard softmax Transformer). This would prevent overclaiming.

- Add a discussion of how the theoretical conditions (orthogonal patterns, specific initialization, etc.) could be relaxed or what the implications are if they are violated.

- Consider adding a small-scale real-world experiment (e.g., text classification with poisoned prompts) to demonstrate that the theoretical insights have practical relevance.

## Score and Decision

The paper makes a solid theoretical contribution by providing the first analysis of Mamba's training dynamics for ICL, with a clear mechanistic understanding and a fair comparison to linear Transformers. The theoretical results are non-trivial and the experiments support the claims. However, the analysis is limited to a highly simplified one-layer Mamba with linear attention, and the comparison is against a linear Transformer rather than a standard softmax Transformer. These limitations, while acknowledged, significantly constrain the generality of the claims. The paper is a good theoretical contribution but not a breakthrough.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>