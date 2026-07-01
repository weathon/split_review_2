Now I'll produce the final review.

## Summary

The paper proposes SparseFW, a layerwise LLM pruning method that relaxes the combinatorial mask selection problem to a convex program over the convex hull of binary masks and solves it with the Frank-Wolfe algorithm to account for weight interactions. The method warm-starts from existing greedy masks (Wanda/RIA), fixes 90% of the highest-saliency weights using the heuristic's scores, and optimizes the remaining 10% with FW. Experiments across five GPT architectures at 50%, 60%, and 2:4 sparsity show consistent zero-shot accuracy gains and perplexity improvements, with up to 80% reduction in the local pruning objective. A theoretical bound connecting the FW solution to the original combinatorial problem is provided.

## Strengths

1. **Principled optimization formulation.** Casting mask selection as a convex relaxation over the convex hull of binary masks and solving with FW (whose LMO reduces to efficient Top-k selection) is conceptually sound. The precomputation of \(G = XX^\top\) removes dependence on sequence length, making per-iteration cost manageable. Section 2.2 presents this cleanly.

2. **Substantial reduction in the local pruning objective.** Figure 2 shows up to 80% relative reduction in per-layer pruning error compared to the Wanda warm-start. Figure 4 further validates that the continuous FW iterate consistently improves, and the analysis linking optimization error to thresholding error is empirically demonstrated.

3. **Consistent downstream gains across models.** Across Table 1, SparseFW almost always improves zero-shot accuracy over both Wanda and RIA warm-starts. Gains are modest (typically 1–3 percentage points) but consistent across five architectures and two sparsity regimes (60% unstructured, 2:4 semi-structured), which is meaningful.

## Weaknesses

### Major

1. **The pure convex relaxation (\(\alpha=0.0\)) fails; SparseFW succeeds only by fixing 90% of the greedy heuristic's decisions.** The paper explicitly states (line 157) that "setting \(\alpha = 0.0\) (full FW without any fixed weights) consistently yields worse results than the baselines." The working method fixes 90% of weights using Wanda saliency scores and optimizes only the remaining 10%. This means SparseFW is fundamentally a post-processing refinement of greedy masks — FW can only flip at most ~10% of the mask entries — rather than an independent solution to mask selection. The framing in the abstract ("we instead consider the convex relaxation") and introduction ("our approach, on the other hand, relaxes the combinatorial constraint and takes weight interactions into account") implies a more general replacement. While the paper is transparent about this in Section 2.3 and the Conclusion (lines 278–283), there is a meaningful gap between the advertised conceptual contribution and what actually works. The core insight — that the convex relaxation cannot outperform greedy heuristics on its own and requires their inductive biases — is understated in the paper's main messaging.

### Minor

2. **SparseGPT is excluded from comparison.** The paper states (line 192) it compares only with methods that "also aim to find a better pruning mask by solving (MASK SELECTION)" and excludes SparseGPT because it "involves a reconstruction step." This is an explicitly stated scope choice. However, SparseGPT is the most widely used LLM pruning baseline, and the reported metrics (perplexity, accuracy) are end-to-end. The omission limits the practical relevance of the evaluation.

3. **RIA 60% accuracy numbers appear to contain an error.** In Table 1, the RIA 60% sparsity accuracy row (63.19, 53.7, 50.51, 59.44, 63.58, 48.08) is **identical** to the Wanda row across all six models. At 50% sparsity the two methods differ, so this identity at 60% is highly suspicious and likely a copy-paste error. If RIA's baseline is incorrect, the SparseFW(RIA) improvements at 60% sparsity are comparisons against a strawman. The authors must clarify or correct this.

4. **No variance or statistical significance for main results.** Table 1 omits standard deviations ("for legibility"). With a single run per condition, it is impossible to assess whether small perplexity differences (e.g., DeepSeek-7B at 50%: Wanda 7.79 vs SparseFW(Wanda) 7.89; LLaMA-3.1-8B at 50%: RIA 9.88 vs SparseFW(RIA) 9.95) are reliable. Figure 3 does report min-max ranges for the iteration/sample ablation, but variance for the main experimental table is absent.

5. **No runtime or compute cost quantification.** The paper acknowledges (line 240) SparseFW is "clearly more compute-intensive than Wanda and RIA" but provides no timing data. With ~2000 FW iterations per layer, each requiring a gradient computation involving \((W \odot M_t)G\), the cost is orders of magnitude higher than a single forward pass. Without any runtime or FLOP measurement, practitioners cannot assess the cost-benefit trade-off.

6. **The \(\alpha=0.9\) detail is not in Algorithm 1.** The pseudocode shows a warm-start (\(M_0\)) but not the critical step of fixing 90% of the highest-saliency weights as unprunable before running FW. The paper relegates this to prose (line 157) with a reference to the appendix. Since this is arguably the most important design choice, it should be prominent in the main algorithm.

## Nice-to-Haves

- A comparison with SparseGPT (even if contextual, outside the stated scope) would substantially strengthen the empirical picture.
- An analysis of what characteristics the 10% of FW-optimized weights have — which weights get flipped relative to the greedy mask, and why? — would deepen the contribution considerably.
- Reporting wall-clock time or relative FLOPs for SparseFW vs. baselines across model sizes would help practitioners gauge the trade-off.

## Removed Points

- **"The theoretical bound is too loose"** — The reviewer calculated the thresholding error term as \(\sim 10^7 \times \lambda_{\max}(Q)\) for a typical layer. This observation is mathematically correct, but loose bounds are common in ML theory. The paper does not claim the bound is tight; the value is in establishing the formal connection between FW convergence and mask selection. This is not a weakness given the stated aims of the theory section.
- **"No SparseGPT comparison despite claiming general pruning superiority"** — The paper explicitly scopes to mask-only methods. The remaining weakness (#2) captures the practical limitation without overclaiming.
- **Several strengths removed as generic/superficial** (e.g., "addressed an important problem").
- **"The local pruning error claim is misleading because local improvement doesn't always translate to perplexity"** — The paper itself acknowledges this limitation (Section 2.3, Conclusion), so this is not a hidden weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the contribution.** The paper would be stronger if it honestly positions SparseFW as a **refinement method** for greedy pruning masks, rather than a replacement. This would resolve the disconnect between the rhetorical framing and the \(\alpha=0.9\) finding.
2. **Move the \(\alpha\) ablation (Appendix Table 2) to the main paper**, including the \(\alpha=0.0\) result, so readers can directly see the sensitivity to this crucial hyperparameter.
3. **Correct or clarify the RIA 60% accuracy data.**
4. **Report variance** for at least a subset of conditions (e.g., 3–5 seeds on one representative model at both sparsity levels).
5. **Provide runtime or FLOP measurements** to contextualize the computational overhead.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>