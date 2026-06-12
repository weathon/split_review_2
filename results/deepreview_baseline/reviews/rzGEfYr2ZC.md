## Summary

The paper proposes SparseFW, a method for pruning LLMs by relaxing the combinatorial mask selection problem into a convex optimization over the convex hull of binary masks and solving it with the Frank-Wolfe (FW) algorithm. The method accounts for weight interactions, provides theoretical guarantees connecting the relaxed solution to the original combinatorial problem, and shows improvements in per-layer pruning error and some gains in perplexity and zero-shot accuracy over Wanda and RIA on several modern GPT architectures.

## Strengths

- **Novel application of Frank-Wolfe to LLM pruning.** The paper introduces a principled optimization-based alternative to the greedy heuristics (Wanda, RIA) that dominate current LLM pruning. This is a fresh perspective in a field that has largely relied on simple saliency scores.
- **Theoretical guarantees.** The paper provides a data-dependent error bound that connects the relaxed solution (after rounding) to the optimal binary mask, offering a formal justification that greedy methods lack. This is a valuable contribution even if the bound is not tight.
- **Empirical reduction in per-layer pruning error.** SparseFW consistently reduces the local reconstruction error by 20–80% relative to Wanda across layers and models, demonstrating that the convex relaxation effectively optimizes the intended objective.
- **Memory efficiency and flexibility.** The method precomputes the Gram matrix \(G = XX^\top\), making the per-iteration cost independent of sequence length and sample count. It supports both unstructured and semi-structured sparsity patterns.

## Weaknesses

### Fatal
None.

### Major
- **Heavy reliance on warmstart and fixed high-saliency weights.** The method requires fixing 90% of weights (those with highest Wanda scores) as unprunable to achieve good perplexity; without this, FW performs worse than baselines. This indicates a severe local–global objective mismatch and means SparseFW is essentially a refinement of existing masks rather than a standalone discovery method. The claim of being a “principled” optimization approach is significantly undermined.
- **Limited baseline comparison.** SparseGPT, a state-of-the-art LLM pruning method, is excluded because it involves weight reconstruction. However, the paper’s goal is to improve final perplexity/accuracy, and SparseGPT is a natural competitor. The omission weakens the empirical evaluation, especially since SparseGPT often outperforms Wanda and RIA at higher sparsities.
- **Computational cost not adequately addressed.** SparseFW requires 2000 FW iterations per layer, which is substantially more expensive than the one-shot Wanda or RIA. No runtime or memory comparisons are provided, and scalability to larger models (e.g., 70B+) is not demonstrated. The paper’s argument that this cost is “worthwhile” is not supported by concrete numbers.

### Minor
- **Modest and inconsistent perplexity gains.** In several cases (e.g., DeepSeek-7B at 50% sparsity, LLaMA-3.1-8B at 50% sparsity with Wanda warmstart), SparseFW yields worse perplexity than the baseline. Zero-shot accuracy improvements are also small (often <2%). The claim of “strong empirical performance” is overstated.
- **Theoretical bound may be weak in practice.** The error bound includes a term scaling with \(\sqrt{d_{in}d_{out}k}\), which can be very large for LLMs (e.g., \(d_{in}=4096, d_{out}=4096, k=0.6 \times 4096^2\)). This makes the guarantee loose and of limited practical use.
- **Fixed hyperparameters without thorough ablation.** The paper uses 2000 iterations and 256 samples for all experiments, but the trade-off between compute and performance may vary across model sizes. An ablation on iteration count and sample size for different models would strengthen the analysis.

### Trivial
- Code is not provided for reproducibility (though the paper states it will be released).

## Nice-to-Haves

- Comparison with SparseGPT in terms of final perplexity/accuracy, or a clear justification for its exclusion.
- Runtime and memory usage comparisons against Wanda and RIA.
- Ablation on the warmstart fraction \(\alpha\) for different models and sparsity levels.
- Deeper analysis of the local–global objective mismatch and potential ways to mitigate it without fixing a large fraction of weights.

## Novel Insights

None beyond the paper’s own contributions. The key insight—that convex relaxation with Frank-Wolfe can be applied to LLM pruning—is interesting, but the need for warmstarting reveals that the local pruning objective is insufficient for global performance. This observation is important for future work but is not deeply explored here.

## Suggestions

1. Include SparseGPT as a baseline for final perplexity/accuracy, or provide a clear argument for why it is not comparable.
2. Provide runtime and memory usage comparisons to help readers assess the practical cost of SparseFW.
3. Investigate the local–global mismatch more thoroughly, perhaps by using a different objective (e.g., incorporating a global loss proxy) or by reducing the fraction of fixed weights.
4. Release the code to ensure reproducibility.

## Score and Decision

**Score:** 4.5  
**Decision:** Reject

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>