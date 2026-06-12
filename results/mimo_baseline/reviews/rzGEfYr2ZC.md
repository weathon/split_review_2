## Summary

This paper proposes SparseFW, a method for layerwise LLM pruning that relaxes the combinatorial binary mask selection problem into a convex program over the convex hull of feasible masks and solves it using the Frank-Wolfe algorithm. The method accounts for weight interactions ignored by greedy baselines like Wanda and RIA, provides theoretical approximation guarantees connecting the relaxed solution to the original problem, and achieves consistent improvements in perplexity and zero-shot accuracy across five modern GPT architectures.

## Strengths

- **Clean and unified formulation of existing methods.** The paper clearly demonstrates that Wanda, RIA, and SparseGPT can all be understood as greedy approximations to the same (MASK SELECTION) problem. The derivation showing Wanda is equivalent to greedy single-weight pruning (Equations 4-5) and that RIA is Wanda applied to a rescaled weight matrix (Equation 7) provides genuine clarity and positions the contribution well.

- **Genuine theoretical contribution.** Lemma 1 provides a data-dependent approximation guarantee decomposing the error into optimization error (controlled by FW iterations T) and thresholding error (controlled by mask dimensions and sparsity k). This is a meaningful advantage over greedy heuristics, which lack such guarantees for this problem.

- **Comprehensive and convincing empirical evaluation.** Experiments span five modern architectures (LLaMA-3.1-8B, Gemma-2-9B, Yi-1.5-9B, DeepSeek-7B, Qwen2.5-7B), three sparsity regimes (50%, 60%, 2:4), and both unstructured and semi-structured sparsity. Zero-shot accuracy improvements are notably consistent across models and sparsity levels.

- **Efficient implementation via precomputation.** Precomputing G=XX^T and H=WG eliminates dependence on sequence length and calibration batch size during iterations, reducing the problem to operations on d_in×d_in matrices. The LMO (Top-k selection) is also efficient.

## Weaknesses

### Fatal
None.

### Major

- **The full convex relaxation alone fails; the α trick is essential.** The paper reveals that setting α=0 (pure FW without fixing any weights) "consistently yields worse results than the baselines." The best results require α=0.9, meaning 90% of weights are determined by Wanda's saliency criterion and only 10% are optimized by FW. This significantly undermines the paper's central narrative — "don't be greedy, just relax" — since the method fundamentally relies on the greedy warm-start to identify which weights to protect. The paper should more prominently acknowledge and analyze this tension. The improvement is real, but the method is better described as "use Wanda to fix a coarse mask, then refine the remaining 10% via convex optimization" rather than replacing greedy methods entirely.

- **No comparison to SparseGPT or other reconstruction-based methods.** The paper explicitly states it does not compare to SparseGPT because it also performs weight reconstruction, not just mask selection. However, SparseGPT is arguably the most important baseline in the LLM pruning literature and a practitioner would want to know how SparseFW compares end-to-end. The scope limitation is defensible but leaves a significant practical gap.

### Minor

- **Computational cost is not quantified.** The paper uses 2000 FW iterations per layer, which is substantially more expensive than Wanda's single-pass approach. While the paper argues this is justified for deployed models, no wall-clock timing comparisons or FLOPs counts are provided, making it difficult for practitioners to assess the cost-benefit tradeoff.

- **Theoretical bound is loose.** The thresholding error term in Lemma 1 involves k + √(2d_in·d_out·k), which can be very large for typical LLM layer dimensions. The bound also depends on λ_max(Q), which is not characterized in terms of model properties. The empirical behavior (Figure 4) is illustrative but the theory does not tightly predict the observed improvements.

### Trivial
None.

## Nice-to-Haves

- A table or figure comparing wall-clock time and peak memory of SparseFW vs. Wanda/RIA across models would strengthen the practical contribution.
- Analysis of why the full relaxation (α=0) fails — is it due to the local-global objective mismatch, the thresholding step, or something else? This would help the community understand when convex relaxations are suitable for pruning.

## Novel Insights

The paper's most novel insight is that Wanda and RIA are both greedy approximations to the same quadratic binary optimization problem (MASK SELECTION), differing only in how they handle single-weight pruning decisions. This unification is non-obvious and clarifies the relationship between these methods. Additionally, the observation that the convex relaxation solution converges monotonically but the thresholded solution initially degrades before improving (Figure 4) provides practical insight into when to stop FW iterations — one should monitor the threshold residual rather than just the continuous objective.

## Suggestions

- Provide wall-clock timing comparisons with Wanda/RIA to help practitioners assess the tradeoff.
- Investigate and report on the α=0 failure mode more carefully: is the issue in the thresholding step, or does the continuous relaxation itself optimize the wrong thing relative to the global objective?
- Consider comparing end-to-end against SparseGPT at a few representative settings, even if the paper's scope is mask selection.

## Score and Decision

The paper presents a clean, well-motivated formulation with genuine theoretical contribution and consistent empirical improvements. However, the critical reliance on the α trick (fixing 90% of weights via Wanda's saliency scores) significantly weakens the central claim that convex relaxation replaces greedy methods. The method is better understood as a refinement of greedy approaches rather than a replacement. Combined with the lack of comparison to SparseGPT and absent compute analysis, this places the paper at the borderline.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>