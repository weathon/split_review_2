Now let me finalize the review with the correct format.

## Summary

This paper proposes SparseFW, a layerwise LLM pruning method that relaxes the combinatorial binary mask-selection problem to a convex program and solves it with the Frank-Wolfe (FW) algorithm. Compared to greedy methods like Wanda and RIA that ignore weight interactions, SparseFW aims to account for these interactions through convex optimization. The paper also provides an insightful unifying analysis showing that Wanda's saliency score emerges as the optimal single-weight pruning criterion, and RIA is Wanda applied to a rescaled weight matrix.

## Strengths

1. **Clean, well-motivated core idea (Sections 1, 2.2).** The observation that existing pruning methods (Wanda, SparseGPT, RIA) use greedy heuristics that ignore weight interactions is accurate and important. The proposed alternative — relaxing the binary mask constraint to its convex hull and solving the resulting quadratic program with FW — is intellectually appealing, principled, and worth exploring. The linear minimization oracle (LMO) for the convex hull of k-sparse binary masks (Equation 12) is simple and elegant.

2. **Insightful unification of greedy methods (Section 2.1).** The paper provides a genuine contribution by showing that Wanda's saliency score emerges as the optimal single-weight pruning criterion under the per-layer quadratic objective (Equations 4–5), and that RIA is equivalent to Wanda on a rescaled weight matrix. This conceptual unification was not clearly articulated before and is useful beyond this paper's core method.

3. **Transparency about limitations.** The paper candidly acknowledges the local-global objective mismatch (Section 2.3, lines 157–158; Section 5, lines 278–283), reports the α=0.0 (pure FW) ablation showing it performs worse than baselines, and discusses the caveat that "vanilla FW substantially reduces per-layer pruning error, this does not reliably yield lower perplexity." This level of transparency is commendable.

4. **Local reconstruction error reduction (Figure 2).** SparseFW achieves up to 80% reduction in per-layer pruning error relative to Wanda. This is a genuine optimization success — the FW iterates do make the continuous objective decrease substantially.

5. **Theoretical guarantees (Section 4).** Even though the bound is loose (discussed below), the fact that SparseFW comes with any convergence guarantee at all for the mask selection problem is a real advantage over Wanda and RIA, which have no theoretical grounding beyond being optimal for single-weight decisions.

## Weaknesses

### Fatal
None.

### Major

1. **Framing overstates the contribution; the method's success depends heavily on a greedy heuristic (Section 2.3, lines 157–158).** SparseFW as actually deployed fixes **90% of the mask using Wanda's saliency scores** and only optimizes the remaining 10% using FW. The paper itself reports that "setting α = 0.0 (full FW without any fixed weights) consistently yields worse results than the baselines." This is a significant tension: the method titled "Don't Be Greedy, Just Relax!" relies on a greedy heuristic for 90% of its decisions. The honest framing would be: "Use Wanda to decide 90% of the mask, then use convex relaxation on the remaining 10%." The claim that SparseFW "accounts for weight interactions" is true only for the 10% of weights that FW actually touches; for the other 90%, the method is exactly Wanda. This does not invalidate the contribution — the paper is transparent about this detail — but it substantially weakens the narrative that convex relaxation replaces greedy heuristics.

### Minor

2. **Empirical gains are modest and inconsistent in several settings (Table 1).** At 50% unstructured sparsity, SparseFW variants lose to the best baseline on 2 of 6 models (DeepSeek-7B where Wanda wins at 7.79 vs. 7.89/7.93; LLaMA-3-8B where RIA wins at 9.88 vs. 9.95). At 2:4 sparsity on DeepSeek-7B, SparseFW essentially ties Wanda (11.73 vs. 11.76). Improvements are more consistent at higher sparsity (60%) and on zero-shot accuracy, but margins are typically small. The omission of standard deviations ("for legibility") makes it difficult to assess statistical significance of the reported differences.

3. **No runtime or computational cost comparison.** The paper acknowledges SparseFW is "clearly more compute-intensive" (line 240) and uses 2000 FW iterations per layer, but provides no wall-clock time or FLOPs measurements. Given that Wanda is a single-pass method, a practitioner cannot evaluate the cost-benefit tradeoff of the additional computation.

4. **Exclusion of SparseGPT from comparison (line 192).** The paper states "we hence do not compare directly to methods that involve a reconstruction step, such as SparseGPT." While this is a reasonable scope choice (SparseGPT jointly solves mask selection and weight reconstruction), it limits the paper's empirical claims. SparseGPT is the most widely used LLM pruning method and its exclusion means the strongest practical claim ("outperforms state-of-the-art") cannot be fully substantiated. Including SparseGPT results — or at minimum a post-hoc reference point — would strengthen the paper considerably.

5. **Theoretical bound is quantitatively loose (Lemma 1, lines 246–248).** The bound's thresholding error term 2(k + √(2 d_in d_out k)) is constant in T and scales with the square root of the product of dimensions times k. For a typical LLM layer this term is very large, and the "arbitrarily small optimization error" touted on line 268 applies to the continuous relaxed solution, not to the final binary mask that is deployed. The paper is honest about the two sources of error, but the practical value of the bound is limited. This weakens the claim of "strong theoretical justification."

### Trivial

6. **Algorithm 1 does not explicitly show the α parameter** that controls how many weights are fixed from the warmstart. This key practical detail is only described in prose (Section 2.3). Readers skimming the algorithm box would miss how SparseFW actually works.

## Nice-to-Haves

- A systematic analysis of when the FW refinement helps most (e.g., by layer type — attention vs. MLP — or by sparsity regime) would turn the α=0.9 finding from a limitation into a scientific insight.
- Including SparseGPT as a reference point in Table 1 (even with a note that it solves a different problem) would significantly strengthen the empirical claims.
- Wall-clock time comparison and/or FLOPs breakdown would help practitioners evaluate the cost-benefit tradeoff.

## Removed Points

These points are flagged to be removed — treat them with caution:
- **"The name 'SparseFW' is already used in prior work":** Removed as Trivial — the paper cites the relevant prior work (Miao et al. 2022, Zimmer et al. 2025) and is aware of the naming overlap.
- **"The local-global mismatch is a fundamental conceptual problem":** Merged into Weakness 1. This is the same underlying issue as the α=0.9 / reliance-on-Wanda concern, not a separate weakness.
- **"SparseGPT also accounts for weight interactions" as a criticism of the paper's framing:** The paper's exclusion of SparseGPT is a scope decision. While debatable, it does not constitute a factual error in the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the paper around what SparseFW actually demonstrates: that FW can provide a meaningful refinement on top of Wanda at higher sparsity levels, and that the local-global mismatch in per-layer pruning objectives is quantitatively significant. The current title and framing overstate the role of convex relaxation versus the greedy warmstart.
- Report standard deviations in Table 1, or at minimum include confidence intervals for the main comparisons.
- Add a runtime comparison with Wanda/RIA to quantify the computational overhead.
- Include the α parameter explicitly in Algorithm 1 so that the core practical detail is not buried in prose.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>