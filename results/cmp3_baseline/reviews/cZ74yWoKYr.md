## Summary

This paper introduces a formal framework for identifying critical KV cache entries in LLM inference, moving beyond heuristic attention-weight-based methods. The authors derive an upper bound on the output perturbation caused by cache eviction, showing that value states projected through the output parameter matrix are as important as attention weights. They propose a perturbation-constrained two-stage selection algorithm, which is integrated as a plug-and-play enhancement into existing eviction methods (SnapKV, AdaKV, HeadKV) and demonstrates substantial reductions in compression loss across three LLMs and 29 datasets.

## Strengths

- **Formal grounding of critical cache selection.** The paper casts the problem as minimizing output perturbation and provides a theoretical analysis that reveals the insufficiency of attention-only criteria, identifying the role of projected value states (\(VW^O\)). This is a significant step beyond the empirical heuristics dominant in prior work.

- **Strong and consistent empirical gains.** Across 29 datasets from Ruler and LongBench, the proposed algorithm reduces the average loss of three SOTA eviction methods by more than half. Improvements hold for three different LLMs (8B–32B), at various cache budgets (20%–80%), and in multi-turn QA on SCBench. The extensive evaluation builds confidence.

- **Practical, lightweight integration.** The additional overhead from computing \(\|VW^O\|_1\) is minimal (a few percent increase in TTFT), and the algorithm works as a drop-in replacement for the selection step of existing methods, making adoption straightforward.

- **Diagnostic analysis confirms the hypothesis.** Head-wise, layer-wise, and budget-wise perturbation measurements directly show that the algorithm reduces actual output perturbation, linking the theoretical worst-case bound to practical behavior.

## Weaknesses

### Major

- **Mismatch between theoretical description and actual algorithm.** The paper states that stage 1 selects entries based *only* on attention weights to satisfy Assumption 3.4, but Algorithm 1 (line 3 and line 5) uses the combined score \((A+\epsilon)\cdot\|\mathbf{V}_{i,:}\|_1\) for *both* stages. This disconnect invalidates the theoretical justification for the two-stage design (Theorem 3.5 assumes stage 1 selects by pure attention). The authors should either modify the algorithm to match the narrative or revise the theory to cover the actual selection metric.

- **Missing ablation study.** It is unclear whether the improvement comes from the two-stage greedy splitting (with hyperparameter \(\alpha\)) or simply from using the combined score \(A_i\cdot\|\mathbf{V}_{i,:}\|_1\) instead of attention alone. A direct comparison of: (a) top-\(b\) from the combined score, (b) two-stage (attention then combined), (c) two-stage (combined then combined, as currently implemented) would significantly strengthen the paper and justify the algorithmic choices.

### Minor

- **Choice of \(L_1\) distance is not deeply justified.** The theoretical bound is derived for \(L_1\) perturbation; although the appendix reports similar gains with \(L_2\), the paper does not discuss why \(L_1\) is the most natural metric for this problem or whether the bound holds under other divergence measures.

- **Hyperparameter \(\alpha=0.5\) is fixed across all budgets and models.** While robustness is shown for 20% cache, there is no analysis for very small budgets (e.g., 5%) where the assumption of capturing ≥50% attention weight with 50% of the budget may fail. The paper would benefit from addressing this limitation or recommending an adaptive scheme.

- **SCBench evaluation only covers AdaKV.** To fully demonstrate universality, multi-turn results for SnapKV and HeadKV should be included or justified.

### Trivial

- Algorithm 1 overwrites the input variable \(V\) with \(VW^O\), which is confusing for readers. Separating the projected variable (e.g., \(\hat{V}\) or \(\mathbf{V}\)) would improve clarity.

## Nice-to-Haves

- An ablation that isolates the effect of the two-stage structure (e.g., compare single-stage combined score vs. two-stage) to clarify the role of each stage.
- A discussion of whether the value norm term could be efficiently approximated (e.g., cached or quantized) to further reduce overhead.
- A comment on how the proposed selection interacts with quantization or other compression techniques applied to the KV cache.

## Novel Insights

Beyond the paper’s own contributions, the key insight—that the criticality of a KV entry depends not only on its attention weight but also on the norm of its value state after the output projection—highlights how the final vocabulary distribution is affected by cache eviction. This suggests that future cache management methods should consider not only which keys are attended to, but also how strongly the corresponding values influence the output after projection. The derivation of an explicit upper bound on output perturbation offers a principled tool for designing and analyzing eviction policies.

## Suggestions

1. **Align algorithm with theory.** Either change stage 1 to select by pure attention weights (matching Assumption 3.4) and keep stage 2 for the combined score, or adjust the theoretical exposition to match the actual combined-score-based algorithm and provide a corresponding bound.
2. **Add an ablation** comparing the two-stage implementation against a simpler top-\(b\) selection using \(A_i\cdot\|\mathbf{V}_{i,:}\|_1\) to isolate the benefit of the greedy two-stage procedure.
3. **Provide a brief discussion** on the behavior at very small budgets (e.g., ≤10%) and whether the \(\alpha=0.5\) setting still ensures the theoretical condition.
4. **Improve notation** in Algorithm 1 to avoid variable overwriting (e.g., use \(\mathbf{V}'\) for \(VW^O\)).

## Score and Decision

**MY FINAL SCORE:** <score>8</score>  
**MY FINAL DECISION:** <decision>Accept</decision>