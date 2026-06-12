## Summary

This paper provides the first theoretical analysis of the training dynamics and in-context learning (ICL) generalization of one-layer Mamba models, including scenarios where prompts contain additive outliers. The authors characterize convergence conditions, sample complexity, and robustness guarantees, showing that Mamba can maintain accurate ICL even when the fraction of outlier-containing examples approaches 1. They compare Mamba to linear Transformers theoretically and empirically, demonstrating that while Mamba may require more training iterations, it exhibits superior robustness to outliers, and they characterize the dual mechanism of linear attention (selecting informative examples) and nonlinear gating (suppressing outliers and inducing local bias).

## Strengths

- **First theoretical analysis of Mamba ICL training dynamics.** The paper fills a significant gap in the literature by providing provable guarantees for Mamba's ICL capabilities, including convergence rates and generalization bounds, which had only been studied empirically before.

- **Rigorous theoretical comparison with Transformers.** The analysis cleanly isolates the effect of the nonlinear gating mechanism by comparing Mamba to linear Transformers under identical data conditions, providing formal conditions under which Mamba's robustness advantage emerges (outlier fraction > 1/2).

- **Mechanistic understanding of Mamba's ICL.** Corollaries 1 and 2 provide interpretable insights into how the linear attention layer selects pattern-matching examples while the gating layer suppresses outliers and induces locality, which is validated by experiments in Figures 3 and 4.

- **Well-designed experiments.** The synthetic experiments in Figure 2 directly validate the theoretical prediction that Mamba tolerates outlier fractions up to ~0.8 while linear Transformers fail beyond 0.5, and the multi-layer experiments in Table 1 reveal an interesting sensitivity to outlier position that aligns with the theory.

## Weaknesses

### Major

- **The theoretical setting is highly simplified relative to practical Mamba.** The analysis assumes a one-layer Mamba with linear attention (no softmax), diagonal A = -I, and binary classification with orthogonal patterns. While this is standard for theoretical work, the gap between this setting and the actual Mamba architecture used in practice (with selective SSM, multiple layers, softmax attention variants, and continuous-valued outputs) is substantial. The paper acknowledges this but does not discuss how the results might extend.

- **The outlier generalization condition (Theorem 2, Condition a) is restrictive.** The requirement that test-time outliers must be positive linear combinations of training outliers (with coefficients summing to L > 0) is quite specific. Many realistic outlier patterns (e.g., completely novel perturbations, adversarial attacks with different structure) would not satisfy this condition. The paper would benefit from discussing how this condition might be relaxed or what happens when it is violated.

- **The comparison with Transformers is limited to linear attention.** The paper compares Mamba only to linear Transformers (without softmax), which are known to be less expressive and less robust than standard softmax Transformers. The claim that "Mamba outperforms Transformers" is therefore overstated for practical settings, as the paper acknowledges in Remark 6 but does not adequately address. The experiments in Appendix B.1 with softmax attention are mentioned but not given sufficient weight.

### Minor

- **The batch size and iteration requirements for Mamba are quite large.** Theorem 1 requires batch size scaling with V² and iterations scaling with M₁, which could be prohibitive. The paper does not discuss whether these are tight or could be improved.

- **The experimental validation is limited to synthetic data.** While synthetic experiments are appropriate for validating theoretical predictions, the paper would be strengthened by at least one real-world ICL experiment (e.g., on a standard NLP benchmark with injected outliers) to demonstrate that the theoretical insights translate to practical settings.

### Trivial

- The paper uses "Mamba" to refer to the simplified one-layer model throughout, which could cause confusion with the full Mamba architecture.

## Nice-to-Haves

- A discussion of how the results might extend to multi-layer Mamba, perhaps with a conjecture or preliminary analysis.
- An ablation study isolating the effect of the gating mechanism vs. the linear attention in the synthetic experiments.
- A comparison with softmax attention Transformers in the main experiments (not just appendix) to make the comparison more practically relevant.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is that the nonlinear gating mechanism in Mamba serves a dual role that is fundamentally different from attention mechanisms in Transformers: it simultaneously acts as a *hard filter* (suppressing outlier examples to near-zero weight) and a *soft locator* (imposing exponential decay based on index distance). This is distinct from how Transformers handle outliers, which typically rely on attention scores that can be manipulated by outlier inputs. The finding that this gating mechanism makes Mamba more robust to outlier *density* but more sensitive to outlier *position* (Table 1) is a nuanced and practically important observation that could guide prompt engineering for Mamba-based models.

## Suggestions

- Add a discussion of the practical implications of the outlier position sensitivity (Table 1) for users of Mamba models, including potential mitigation strategies.
- Clarify in the abstract and introduction that the theoretical comparison is with *linear* Transformers, not standard softmax Transformers, to avoid overclaiming.
- Consider adding a small-scale real-data experiment (e.g., sentiment classification with injected outliers) to demonstrate the practical relevance of the theoretical findings.

## Score and Decision

The paper makes a solid theoretical contribution by providing the first rigorous analysis of Mamba's ICL training dynamics and robustness, with clean mechanistic insights and well-designed experiments that validate the theory. The major weaknesses are the simplified setting (which is standard for theoretical work) and the limited comparison (only linear Transformers). However, the paper is honest about these limitations and the core contribution—understanding how the gating mechanism enables outlier robustness—is novel and valuable. The paper is within the scope of ICLR and represents a meaningful advance in theoretical understanding of efficient architectures.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>