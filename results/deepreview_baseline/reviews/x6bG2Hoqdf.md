## Summary

CALM proposes a hybrid framework for Automatic Heuristic Design (AHD) that combines verbal guidance (evolutionary prompt manipulation) with numerical guidance (RL-based fine-tuning of the LLM via GRPO). The key innovation is that the LLM co-evolves with the heuristic search process: as heuristics are generated and evaluated, their performance signals are used as reinforcement learning rewards to fine-tune the LLM, enabling it to internalize characteristics of successful heuristics. The method runs locally on a single 24GB GPU using a quantized 7B model and demonstrates competitive or superior performance compared to API-based baselines across four optimization tasks (OBP, TSP, CVRP, OP).

## Strengths

- **Novel integration of RL fine-tuning into LLM-based AHD**: Prior methods treat the LLM as a frozen generator and only manipulate prompts; CALM is among the first to update the LLM parameters based on heuristic performance feedback, which is a principled and underexplored direction. The ablation study in Table 4 clearly shows that the GRPO component provides the largest performance improvement, validating the core idea.

- **Strong empirical results across diverse tasks**: The method demonstrates consistent improvement over state-of-the-art baselines (including MCTS-AHD using GPT-4o-mini) across four optimization problems with varying characteristics. Notably, CALM using a quantized 7B model outperforms methods that rely on much larger API-based models, which is a compelling demonstration of the approach's efficiency.

- **Comprehensive ablation studies**: The paper systematically ablates each component (RL, collapse mechanism, each operator, reward design variants) on two problems, providing clear evidence about which design choices matter most. The ablation on the collapse mechanism hyperparameters is particularly thorough.

- **Well-motivated and well-designed evolutionary operators**: The injection and replacement operators are designed with GRPO's token-level credit assignment in mind, encouraging the LLM to retain useful components while introducing controlled variations. The diversity-aware crossover with performance- and diversity-based sampling is a thoughtful mechanism for balancing exploration and exploitation.

- **Practical resource efficiency**: Running on a single 24GB GPU with a quantized 7B model significantly lowers the barrier to adoption compared to API-dependent methods, and the paper demonstrates that this efficiency does not come at the cost of performance.

## Weaknesses

### Fatal

None.

### Major

- **Limited novelty of the core insight**: The idea of using RL to fine-tune a generative model based on task performance is well-established in the RLHF/RL literature and has been explored in code generation and program synthesis (e.g., fine-tuning code LLMs with compiler feedback). The concurrent works cited (Surina et al., 2025; Liu et al., 2025) also explore fine-tuning LLMs for AHD. The paper's main contribution is the specific integration of evolutionary operators + GRPO for heuristic design, which is more of an engineering contribution than a fundamental algorithmic advance. The "co-evolution" framing is slightly overstated given that the RL fine-tuning is essentially standard RL applied to LLM outputs.

- **The reward function's assumption about performance comparison with the best base heuristic is not fully justified**: The reward in Equation (4) compares the generated heuristic to the best base heuristic used in the prompt. However, completely novel heuristics that are not derived from any base heuristic (e.g., via the initialization operator) would have no meaningful "best base" to compare against. The paper does not discuss how this edge case is handled. Additionally, Equation (3) uses the minimum of the two absolute performance values in the denominator, which can be unstable when either value is near zero (though this may not be relevant for the tested problems).

- **Statistical significance is relegated to the appendix**: The paper mentions p-values in Section 5.2 ("Additional Experimental Results") but does not provide any significance testing in the main results tables. Given that many of the method comparisons show small absolute differences (e.g., 0.71% vs 0.82% on OBP, or 13.41% vs 13.71% on TSP N=200), it is unclear whether the claimed improvements are statistically significant. The main tables report averages over only three runs, which is a small sample size.

- **The "verbal gradient" experiment is not a fair comparison**: The paper claims that the API-based variant of CALM (without GRPO) matches or exceeds prior methods, which is presented as evidence that CALM's verbal guidance is effective. However, this variant uses CALM's new operators (injection, replacement, diversity-aware crossover, collapse mechanism) which are themselves part of the CALM framework. The comparison with EoH, ReEvo, and MCTS-AHD conflates the contribution of the operators with the contribution of the RL fine-tuning, making it difficult to assess the incremental value of the operators alone. A cleaner comparison would remove all CALM-specific operators and test only the GRPO fine-tuning on top of a baseline operator set.

### Minor

- **Inconsistent baseline reporting**: In Table 3, EoH and HSEvo are each listed twice (though the second listing of HSEvo appears to be a typo). The OP column for EoH shows "HSEvo" as a method label in the first row, which appears to be a copy-paste error. This suggests careless table formatting that should be corrected.

- **The collapse mechanism reset is drastic**: Resetting to only two heuristics (the original seed and the current best) could discard useful diversity. The paper does not explore less aggressive reset strategies (e.g., keeping a percentage of top heuristics by diversity). The theoretical analysis in Equation (2) provides expected time to collapse but does not characterize the trade-off between exploration and wasted computation.

- **The paper does not discuss the computational cost of the GRPO fine-tuning**: While total LLM queries are reported (2,000), the fine-tuning itself requires additional gradient computation. The runtime analysis mentioned in the appendix should explicitly report total wall-clock time for CALM vs baselines, including training time.

- **Limited analysis of the learned heuristics**: The paper does not analyze the structure or behavior of the discovered heuristics in any depth. An analysis of what the LLM learns (e.g., does it learn specific decision rules, parameter choices, or structural templates?) would strengthen the claim that the model is "co-evolving" and provide insight into the fine-tuning's effect.

### Trivial

- The paper violates the "no missing appendix" rule by citing Appendix B, C, D, E, F, G, H, and I without them being available. This is noted as a parser issue.

## Nice-to-Haves

- An analysis of the KL divergence term in GRPO: Does the KL penalty against the reference model prevent the LLM from forgetting basic programming knowledge? The paper could report KL divergence values during training.
- A discussion of whether the approach works for black-box optimization settings where the heuristic structure is less well-defined.
- An investigation of scaling: does performance improve with more GRPO training steps beyond the fixed budget?

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Provide statistical significance tests (e.g., paired Wilcoxon or bootstrap tests) for the main results, especially where performance differences are small. Report p-values or confidence intervals in the main tables, not just the appendix.
- Include a controlled experiment that isolates the contribution of the RL fine-tuning by applying GRPO to the baseline operator set (e.g., EoH or MCTS-AHD operators) and comparing that to CALM's operators + GRPO.
- Clarify how the reward function handles the initialization operator (where there is no "best base heuristic").
- Add a brief analysis of the types of heuristics discovered and what the LLM learns during fine-tuning.
- Fix the table formatting issues in Table 3.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>