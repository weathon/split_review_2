## Summary
This paper proposes SparseFW, a layer-wise pruning method for Large Language Models that relaxes the combinatorial mask selection problem into a convex optimization over the convex hull of binary masks, solved using the Frank-Wolfe (FW) algorithm. The method accounts for weight interactions that greedy heuristics like Wanda and SparseGPT ignore, and provides theoretical approximation guarantees connecting the relaxed solution to the original combinatorial problem. Empirically, SparseFW reduces per-layer pruning error by up to 80% compared to Wanda and shows consistent improvements in perplexity and zero-shot accuracy across multiple modern GPT architectures (LLaMA-3.1, Gemma-2, Yi-1.5, Qwen2.5, DeepSeek).

## Strengths
- **Novel formulation of LLM pruning as a convex relaxation solved via Frank-Wolfe**: The paper identifies that existing LLM pruning methods (Wanda, SparseGPT, RIA) all rely on greedy heuristics that ignore weight interactions, and proposes a principled alternative by relaxing the binary mask constraint to its convex hull. This is a genuinely new perspective on the problem.
- **Strong empirical results with consistent improvements**: SparseFW achieves up to 80% reduction in per-layer pruning error and delivers consistent perplexity and accuracy gains across five different model families (LLaMA-3.1-8B, Gemma-2-9B, Yi-1.5-9B, DeepSeek-7B, Qwen2.5-7B) at multiple sparsity levels (50%, 60%, 2:4). The improvements are particularly notable at higher sparsity regimes where pruning is most challenging.
- **Theoretical guarantees for the pruning mask**: The paper provides an approximation bound (Lemma 1) that decomposes the error into optimization error (controlled by FW iterations) and thresholding error, offering a principled understanding of why the method works. This is a significant advantage over purely heuristic methods.
- **Memory efficiency and scalability**: By precomputing G = XX^T and H = WG, the method's per-iteration cost is independent of the calibration dataset size and sequence length, making it practical for large models. The LMO is efficiently computable via a top-k operation.

## Weaknesses

### Major
- **Critical reliance on warm-starting and mask fixing (α=0.9)**: The paper honestly reports that vanilla FW without fixing high-saliency weights consistently performs worse than baselines. The method requires fixing 90% of weights (those with highest Wanda scores) and only optimizing over the remaining 10%. This is a substantial caveat: the method's success depends heavily on a heuristic (Wanda) to identify which weights to preserve, and the optimization only touches a small fraction of the mask. This raises questions about whether the method is truly "solving the mask selection problem" or rather making minor adjustments to an already good heuristic mask.
- **Inconsistent perplexity improvements**: In Table 1, SparseFW often underperforms the baseline it warm-starts from on perplexity. For example, SparseFW (Wanda) at 50% sparsity on DeepSeek-7B (7.89 vs 7.79), LLaMA-3.1-8B (10.21 vs 10.09), and Yi-1.5-9B (6.58 vs 6.58, tie). At 60% sparsity, SparseFW (Wanda) underperforms Wanda on DeepSeek-7B (11.99 vs 11.44). The paper claims "on par with or better than the baselines," but the pattern is mixed, and the improvements are often modest relative to the computational cost.
- **Computational cost vs. benefit trade-off not adequately addressed**: SparseFW requires 2000 FW iterations per layer, each involving matrix multiplications. For a model with ~32 layers and ~7-9 matrix types per layer, this is ~450,000-600,000 iterations total. The paper acknowledges this is "clearly more compute-intensive" but only provides a qualitative justification. Given that the perplexity gains are often small (e.g., 10.67 vs 11.19 for Gemma-2 at 50%), a quantitative analysis of the compute-perplexity Pareto frontier would be valuable.

### Minor
- **Theoretical bound is data-dependent and not empirically validated**: Lemma 1 depends on λ_max(Q), the largest eigenvalue of the Hessian w.r.t. the mask, which is not computed or estimated. The bound is not tight enough to provide practical guarantees (the thresholding error term includes √(2 d_in d_out k), which is large for LLM-scale matrices). The paper would benefit from discussing whether the bound is vacuous at scale.
- **Limited comparison to SparseGPT**: The paper explicitly excludes SparseGPT from comparison because it involves a reconstruction step, but SparseGPT is arguably the most widely used LLM pruning method. Many readers will want to know how SparseFW compares to the full SparseGPT pipeline (mask + weight reconstruction), not just the mask selection component.
- **Ablation of α is in the appendix**: The key hyperparameter α (fraction of fixed weights) is only ablated in the appendix (Table 2, referenced but not shown in the main text). Given its critical importance to the method's success, this ablation should be in the main paper.

### Trivial
- The paper states "SparseFW generally performs on par with or better than the baselines in terms of perplexity" but the data shows several cases where it is worse. More precise language would be appropriate.

## Nice-to-Haves
- An analysis of which weights get pruned differently by SparseFW vs. Wanda (e.g., do they tend to be in specific layers or attention heads?)
- A comparison of SparseFW's runtime vs. Wanda and RIA in absolute terms (e.g., GPU-hours for LLaMA-3.1-8B)
- An investigation of whether the thresholding error can be reduced by alternative rounding strategies (e.g., iterative rounding or randomized rounding)

## Novel Insights
The paper's key insight is that the local-global objective mismatch in LLM pruning is not merely a technical issue but a fundamental property: optimizing the per-layer reconstruction error can actually hurt final perplexity because the local objective does not align with the global language modeling objective. This is demonstrated by the fact that vanilla FW (α=0) reduces reconstruction error but increases perplexity, while fixing 90% of weights based on a simple heuristic (Wanda) and optimizing only the remaining 10% yields the best results. This suggests that the pruning problem has a "conservation of difficulty" property: the hard part is not finding the optimal mask under the local objective, but rather defining the right objective in the first place. The paper's contribution is therefore not just a new algorithm, but a clear empirical demonstration that local reconstruction error is a flawed proxy for global performance, and that successful pruning methods implicitly incorporate inductive biases (like Wanda's saliency scores) that compensate for this mismatch.

## Suggestions
1. Move the α ablation study (Table 2) to the main paper, as it is central to understanding the method's behavior and limitations.
2. Add a comparison to SparseGPT (full pipeline, not just mask selection) to give readers a complete picture of where SparseFW stands relative to the state-of-the-art.
3. Include a quantitative runtime comparison (e.g., GPU-hours for a representative model) to help readers assess the compute-benefit trade-off.
4. Clarify in the abstract and introduction that the method requires warm-starting from an existing heuristic and fixing a large fraction of weights, as this is a significant practical constraint.

## Score and Decision
The paper presents a novel and theoretically grounded approach to LLM pruning, with strong empirical results in terms of reconstruction error reduction and consistent (if sometimes modest) improvements in perplexity and accuracy. The main weakness is the method's heavy reliance on warm-starting and fixing 90% of weights, which limits the novelty of the core contribution. However, the paper is honest about this limitation and provides useful insights about the local-global objective mismatch. The theoretical guarantees, while not tight, are a genuine advantage over purely heuristic methods. Overall, this is a solid contribution that advances the state of the art in LLM pruning.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>