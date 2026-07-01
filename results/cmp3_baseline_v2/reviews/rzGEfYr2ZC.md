## Summary
This paper proposes SparseFW, a method for pruning Large Language Models (LLMs) by relaxing the combinatorial mask selection problem into a convex optimization over the convex hull of binary masks, solved using the Frank-Wolfe (FW) algorithm. The approach accounts for weight interactions that greedy heuristics like Wanda and SparseGPT ignore, and provides theoretical approximation guarantees connecting the relaxed solution to the original combinatorial problem. Empirically, SparseFW reduces per-layer pruning error by up to 80% compared to Wanda and shows consistent improvements in perplexity and zero-shot accuracy across multiple modern GPT architectures (LLaMA-3, Gemma-2, Yi-1.5, Qwen2.5, DeepSeek).

## Strengths
- **Novel formulation with theoretical grounding**: The paper provides a principled convex relaxation of the combinatorial mask selection problem and connects it to the original problem via approximation guarantees (Lemma 1). This is a clear theoretical advance over greedy heuristics that lack such guarantees.
- **Strong empirical results**: SparseFW consistently outperforms Wanda and RIA baselines across 5 model families, 3 sparsity regimes, and both perplexity and zero-shot accuracy metrics. The per-layer error reductions of up to 80% are substantial and well-documented.
- **Methodological clarity**: The paper clearly explains how existing methods (Wanda, SparseGPT, RIA) can be viewed as greedy approximations to the same objective, and provides a clean derivation of the FW-based relaxation. The LMO for the convex hull of binary masks is elegantly simple and computationally efficient.
- **Practical considerations**: The paper honestly addresses the local-global objective mismatch and the need for warm-starting with fixed high-saliency weights (α=0.9), which is a nuanced and practical insight rather than a hidden failure.

## Weaknesses
### Fatal
None.

### Major
- **The warm-starting requirement undermines the core claim**: The paper states that without fixing 90% of weights (α=0.9), SparseFW "consistently yields worse results than the baselines." This means the method's success depends critically on preserving the greedy baseline's decisions for the vast majority of weights. The method is essentially optimizing only 10% of the mask, which significantly weakens the claim that "classical constrained optimization is a scalable and effective alternative to greedy heuristics." The contribution is more accurately described as a refinement of greedy masks rather than a replacement.
- **Inconsistent perplexity improvements**: In Table 1, SparseFW often underperforms the baseline it warm-starts from (e.g., SparseFW (Wanda) at 50% sparsity on DeepSeek-7B: 7.89 vs Wanda's 7.79; on LLaMA-3-8B: 10.21 vs RIA's 9.88). The improvements are not uniform, and the paper does not adequately explain when/why SparseFW helps versus hurts.
- **Computational cost not properly contextualized**: The paper acknowledges SparseFW is "clearly more compute-intensive than Wanda and RIA" but provides no runtime comparisons. 2000 FW iterations per layer with gradient computations involving matrix-matrix multiplications of size d_in × d_in is non-trivial. For a 32-layer model with d_in=4096, this is substantial. The paper should report wall-clock time or FLOPs relative to baselines.

### Minor
- **The theoretical bound (Lemma 1) is stated informally and the key term √(2 d_in d_out k) is very large for LLM-scale dimensions (e.g., d_in × d_out ≈ 16M for a single layer), making the bound vacuous in practice.** The paper would benefit from acknowledging this limitation or providing a tighter analysis.
- **The paper does not compare to SparseGPT**, which is arguably the most popular LLM pruning method. The justification (SparseGPT involves reconstruction, not just mask selection) is reasonable but limits the empirical scope.
- **The ablation of α (fraction of fixed weights) is relegated to the appendix** and only briefly mentioned. Given its critical importance, this should be a main-text figure.

### Trivial
- The paper uses "pruning error" and "reconstruction error" somewhat interchangeably without precise definition.

## Nice-to-Haves
- A runtime/FLOPs comparison table between SparseFW, Wanda, and RIA.
- An analysis of which layers benefit most from SparseFW optimization (e.g., attention vs. MLP, early vs. late layers).
- A study of how the optimal α varies with model size, sparsity level, or layer type.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- **Reframe the contribution**: The paper should more honestly characterize SparseFW as a "post-processing refinement of greedy masks" rather than a "replacement for greedy heuristics." The warm-starting requirement is not a bug but a feature—it shows that greedy methods capture important structure that pure optimization misses. This is actually an interesting finding about the local-global objective mismatch.
- **Provide runtime analysis**: Report the wall-clock time for SparseFW (with 2000 iterations) versus Wanda/RIA for at least one model size, so readers can assess the cost-benefit trade-off.
- **Clarify the theoretical bound's practical meaning**: Acknowledge that the bound in Lemma 1 scales with √(d_in d_out), which is large, and discuss whether tighter bounds are possible under additional assumptions (e.g., low-rank structure of G).

## Score and Decision
The paper presents a novel and theoretically motivated approach to LLM pruning, with clear empirical benefits in per-layer error reduction and competitive final performance. However, the critical dependence on warm-starting with 90% fixed weights from greedy baselines significantly limits the claimed contribution. The method is better understood as a refinement of existing masks rather than a fundamentally new pruning paradigm. The empirical gains, while real, are modest in many settings and inconsistent across models. The paper is solid but not transformative.

MY FINAL SCORE: 6.0
MY FINAL DECISION: Accept