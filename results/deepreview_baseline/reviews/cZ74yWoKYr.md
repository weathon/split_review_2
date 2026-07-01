##Summary

This paper formalizes the problem of identifying critical KV cache entries in LLM inference by minimizing output perturbation. The authors derive an upper bound on the perturbation that depends on both attention weights and projected value states, showing that attention weights alone are insufficient. They propose a two-stage greedy perturbation-constrained selection algorithm that first selects high-attention entries to satisfy a coverage condition, then selects entries based on a combined metric of attention and value norm. The algorithm is integrated into three SOTA cache eviction methods (SnapKV, AdaKV, HeadKV) and evaluated on 29 datasets from Ruler and LongBench across three LLMs, demonstrating consistent and substantial reductions in compression loss.

## Strengths

- **Formal grounding of critical cache selection.** The paper provides a theoretical framework for cache eviction that goes beyond the empirical heuristics of prior work. The derivation of the output perturbation bound and the identification of value states and the output projection matrix as important factors is a clear conceptual contribution.
- **Simple, effective, and plug-and-play algorithm.** The proposed two-stage greedy algorithm is straightforward, introduces negligible computational overhead, and can be integrated into existing cache eviction methods without changing their accumulation or budget allocation mechanisms. The empirical results show consistent improvements across three different eviction methods and three LLMs.
- **Comprehensive and convincing evaluation.** The paper evaluates on 29 datasets (Ruler and LongBench) plus multi-turn QA (SCBench), covering synthetic and real-world tasks. The improvements are large and consistent: for example, on Ruler with 40% cache, the algorithm increases AdaKV’s average score from 71.09 to 83.87 on Qwen2.5-32B, and reduces loss by more than half on average across all settings.
- **Empirical validation of the theoretical motivation.** The head-wise, layer-wise, and budget-wise perturbation analyses (Figures 4–6) directly confirm that the algorithm reduces practical output perturbation, bridging the gap between the theoretical bound and actual behavior.

## Weaknesses

### Fatal
None.

### Major
- **The two-stage algorithm is heuristic and the theoretical guarantee is limited.** Stage 1 selects purely by attention weights, which is not derived from the perturbation bound. The justification (Assumption 3.4) is empirically verified but not theoretically guaranteed. Stage 2 minimizes an upper bound given stage 1, but the overall algorithm does not directly minimize the original perturbation bound. While the empirical results are strong, the theoretical contribution would be stronger with a more direct optimization or a tighter analysis.
- **Sensitivity to the hyperparameter α.** The sensitivity analysis (Table 4) shows that for Mistral-7B, setting α=0 causes severe degradation (score drops from 42.85 to 31.94), while for Llama-3.1-8B, α=0 works well. This indicates that the two-stage safeguard is necessary for some models but not others, and the paper does not provide guidance on how to choose α beyond the fixed 0.5. The claim of “universal” enhancement is somewhat weakened by this sensitivity.

### Minor
- **The claim “more than half on average” is supported but depends on the specific aggregation.** The average relative loss reduction across all 9 model-method combinations in Figure 1 is about 62%, which is indeed more than half. However, for Mistral-7B with SnapKV, the reduction is only about 20%, which is less than half. The paper should be more precise about the aggregation method.
- **The theoretical analysis uses L1 distance, but the attention output is used with softmax and subsequent layers.** The paper acknowledges that other metrics are compatible, but does not discuss whether L1 is the most appropriate choice for the downstream task. The bound derivation relies on the L1 norm, and the algorithm’s effectiveness may depend on this choice.
- **The scope of “universal” is limited to methods that use attention-weight-based selection.** The algorithm is integrated into SnapKV, AdaKV, and HeadKV, which all share the same underlying selection mechanism (accumulated attention weights with observation window and pooling). It is not demonstrated on other types of eviction methods (e.g., random, frequency-based, or methods that use different criteria).

### Trivial
- The paper uses “more than half” in the abstract and Figure 1 caption, but the exact numbers are provided in the tables. This is a minor imprecision.

## Nice-to-Haves
- A discussion of how tight the derived upper bound is (e.g., empirical gap between the bound and actual perturbation) would strengthen the theoretical analysis.
- An ablation study that directly compares the two-stage algorithm with a single-stage version that uses the combined metric (i.e., α=0) across all models, to better understand when the two-stage safeguard is necessary.
- A comparison with other recent methods that also consider value states or use perturbation-based criteria (e.g., KIVI, or quantization-aware selection) would help position the work more broadly.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the output perturbation of self-attention under cache eviction can be bounded by a term that involves both attention weights and the L1 norm of the projected value states. This reveals that value states and the output projection matrix are not just passive components but actively influence which cache entries are critical. The two-stage greedy algorithm, while heuristic, effectively operationalizes this insight by first ensuring a coverage condition on attention weights and then optimizing the combined metric. The empirical demonstration that this reduces perturbation across heads, layers, and budgets provides a concrete validation of the theoretical perspective.

## Suggestions
- Clarify the aggregation method for the “more than half” claim and report relative loss reduction per model-method combination.
- Provide guidance on choosing α or show that α=0.5 is robust across a wider range of models and budgets (the current sensitivity analysis is only for 20% cache on LongBench).
- Discuss the limitations of the L1-based bound and whether other norms (e.g., L2) lead to different algorithmic choices.

## Score and Decision

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>