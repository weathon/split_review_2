## Summary

The paper formalizes the problem of identifying critical KV cache entries in LLM inference from an output perturbation perspective. It derives an upper bound on the L₁ perturbation introduced by cache eviction, revealing that attention weights alone are insufficient—value states projected through the output matrix also matter. Based on this bound, the authors propose a two-stage greedy selection algorithm that first captures high-attention entries (to satisfy an assumption about cumulative weight) and then additionally selects entries that minimize the worst-case perturbation bound. The algorithm is a plug-and-play enhancement integrated into three SOTA cache eviction methods (SnapKV, AdaKV, HeadKV) and evaluated on 29 datasets across three LLMs, consistently reducing compression loss by more than half on average. Empirical analysis confirms that the method reduces practical output perturbation across heads, layers, and cache budgets.

## Strengths

- **Principled problem formulation:** The paper moves beyond heuristic attention-weight-based selection and formally defines critical KV cache identification as minimizing output perturbation, providing a theoretically grounded objective.
- **Novel insight and simple effective algorithm:** The analysis shows that value states and the output projection matrix are essential components of the selection criterion. The resulting algorithm (attention weight × L₁ norm of projected value state) is both computationally cheap and consistently effective.
- **Extensive and convincing experiments:** Results span three LLMs (Llama-3.1-8B, Mistral-7B, Qwen2.5-32B), three cache eviction methods, two major benchmarks (Ruler with 13 tasks, LongBench with 16 datasets), and multiple cache budgets. The improvements are consistent and large—often halving the loss relative to the full cache.
- **Thorough analysis of perturbation reduction:** Head-wise, layer-wise, and budget-wise visualizations convincingly demonstrate that the proposed method actually reduces the practical output perturbation, connecting theory to practice.
- **Low overhead and plug-and-play integration:** The method adds negligible computational cost (≤1% TTFT increase) and can be directly dropped into existing eviction pipelines, making it practical for deployment.

## Weaknesses

### Major

- **Theoretical derivation has limited scope.** The bounding in Theorem 3.3 uses a multiplicative mask formulation that does not exactly replicate the effect of hard eviction (it renormalizes the softmax after removing entries). The bound is also not proven to be tight, and the two-stage algorithm is a heuristic that minimizes a further upper bound under an unverified assumption (Assumption 3.4). While empirical results validate the approach, the theoretical contribution is modest.
- **Sensitivity to the hyperparameter α.** The two-stage design with fixed α=0.5 relies on the assumption that the first stage captures >50% of attention weight. The sensitivity analysis (Table 4) shows that setting α=0.0 on Mistral-7B causes a 10-point drop, indicating that the assumption can be violated (especially for models with flatter attention distributions). The paper does not provide an adaptive mechanism to detect or correct such cases.
- **Limited comparison with other recent methods.** The paper only integrates with three specific eviction methods (SnapKV, AdaKV, HeadKV). There are numerous other recent cache eviction techniques (e.g., KeyFormer, PyramidKV, StreamingLLM variants) that are not compared. Without a broader baseline, it is unclear whether the improvement is universal or limited to these architectures.

### Minor

- **Compression scenario choice.** The main experiments use “context compressed independently before question is introduced.” While practical, this is not the most common inference setting. The “simple compression” (context and question compressed together) results are relegated to the appendix. Showing those results in the main paper would strengthen the claim of generality.
- **Model scale diversity.** The largest model evaluated is 32B. Including results for a 70B+ model or a non-transformer architecture (e.g., Mamba) would better demonstrate universality across architectures and scales.
- Lack of ablation isolating the two-stage components. It would be informative to compare against variants that use only Stage-1, only Stage-2 (without attention safeguard, i.e. α=0.0 when assumption holds poorly concatenated with proposed metric vs. attention-only or value-only metrics to verify incremental gain from each term The absence of such an ablationWeaknesses the evalutionary design slightly incomplete analyses, e.g., ablations separating attention term and    norm value term.

None beyond the paper's;own contributions). Overall this is a solid contribution that realistically addresses the stated KV cache eviction selection problem and offers a most effective plug-in solution.

## Novel Insights

Beyond its own contributions, the paper reinforces that output perturbation is a powerful lens for designing compression criteria in LLMs. The key insight—that the softmax normalization couples all attention weights and projected values—suggests that selection metrics should account for both the raw attention mass and the magnitude of the associated value states after the output projection. This perspective could inspire similar perturbation-constrained selection in other transformer compression tasks (e.g., sparse attention, pruning).

## Suggestions

- Perform an ablation that separates the two stages and the two components of the score (attention weight vs. value norm). This would clarify the marginal benefit of each.
- Report results for the “simple compression” setting (context and question compressed together) in the main paper, not just the appendix.
- Consider evaluating on a larger-scale model (e.g., Llama-3.1-70B) or a different architecture (e.g., Mamba) to strengthen generalizability.
- Explore an adaptive α setting per head or per layer, possibly based on the cumulative attention weight observed after Stage-1.
- Include a comparison against one or two additional recent cache eviction methods beyond the three selected.

## Score and Decision

**Score: 8**

The paper presents a novel, theoretically motivated approach to KV cache eviction that yields consistent and substantial improvements across extensive experiments. The weaknesses (heuristic two-stage design, sensitivity to α, limited baseline scope) are non-fatal and partially addressed by the empirical validation. The work is clearly presented, practically relevant, and likely to influence future research in efficient LLM inference.

**Decision: Accept**

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: Accept