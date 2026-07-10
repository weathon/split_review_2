Now I have all the data I need. Here is the final consolidated review.

---

## Summary

CALM is a framework for automatic heuristic design (AHD) that co-evolves an LLM with the search process by combining evolutionary operators over prompts ("verbal guidance") with GRPO-based RL fine-tuning of the LLM using heuristic performance feedback ("numerical guidance"). Running a quantized 7B model on a single 24GB GPU, it demonstrates results competitive with or superior to API-based methods using GPT-4o-mini across Online Bin Packing, Traveling Salesman Problem, Capacitated Vehicle Routing Problem, and the Orienteering Problem.

## Strengths

- **Well-motivated core idea.** The observation that existing LLM-based AHD methods keep the LLM frozen and only steer it via prompt manipulation is accurate. Extending the feedback loop to update the LLM's weights via RL is a natural next step, and the paper's framing of "verbal gradients" vs. "numerical gradients" is conceptually clear and useful.

- **Impressive practical instantiation.** Running an INT4-quantized Qwen2.5-7B-Instruct model (1.15% of weights fine-tuned) on a single 24GB GPU and outperforming API-based methods using GPT-4o-mini is a genuine engineering achievement, well-supported by the comparison in Tables 1–3.

- **Comprehensive ablation study.** Table 4 ablates the RL component, collapse mechanism, reward function alternatives, and each evolutionary operator individually on two tasks. This level of diagnostic information is rare in this area and meaningfully informs which design choices matter.

- **Clean separation of contributions.** The API-based variant (CALM without GRPO, using GPT-4o-mini) isolates the contribution of the evolutionary operator design from the RL component, demonstrating that the operators are independently valuable — the variant is competitive with MCTS-AHD without using tree search or RL.

## Weaknesses

### Fatal

None.

### Major

- **Budget comparison is confusing and potentially unfair.** The paper reports "1,000 heuristic evaluations for baselines" and "2,000 LLM queries for CALM" as "comparable evaluation budgets" without justifying this claim. These are incommensurate units: a "heuristic evaluation" for a baseline involves one or more LLM queries plus execution on the training set, while an "LLM query" for CALM produces one response that is then evaluated. If each of CALM's 2,000 queries leads to a heuristic evaluation, CALM evaluates 2,000 heuristics vs. baselines' 1,000 — a potential 2× advantage in number of heuristics considered. On OBP, the picture is even more opaque: baselines use 4,000+ queries for 2,000 evaluations while CALM uses 2,000 queries. Wall-clock time or GPU-hours are deferred to the appendix. The core results cannot be fully interpreted until the resource comparison is made transparent.

### Minor

- **The claim that RL has "the most significant impact" is overstated without qualification.** On OBP the claim is well-supported (removing GRPO causes a 1.07 pp drop vs. the next largest at 0.64 pp). But on OP, removing GRPO causes a 2.48 pp drop (17.41%→19.89%), which is comparable to removing collapse (2.16 pp drop) or simplification (2.04 pp drop). The margin is not dramatically larger, and the claim should not be presented as uniformly true across tasks.

- **Results are uneven across tasks/scales, yet the abstract claims uniform outperformance.** On TSP N=50 (in-domain), CALM (10.04%) underperforms MCTS-AHD (9.69%). On OP N=50 (in-domain), CALM (24.22%) underperforms HSEvo (23.98%). CALM is genuinely strong on CVRP and OBP and on out-of-domain scales, but "outperforms SOTA baselines across various optimization tasks" should be qualified to reflect where and by how much.

- **The value of G (number of GRPO samples per prompt) is not stated in the main paper.** This directly determines the effective number of evolutionary rounds (2,000 / G). Without G, the reader cannot evaluate the budget comparison or the search efficiency.

- **Reward hyperparameters (α₁, α₂, r_invalid) are specified only as ranges, not concrete values.** The paper gives α₁,α₂ ∈ (0,1) and r_invalid ∈ (-1,0) but does not state the actual numbers used (sensitivity analysis is in the appendix).

- **The fine-tuning mechanism is under-specified.** The paper states "fine-tuning just 1.15% of its weights" via GRPO using Unsloto, but does not explain which parameters are updated (LoRA adapters at what rank on which modules? specific layers?). This limits reproducibility of the resource and memory claims.

- **Statistical significance is deferred entirely to the appendix.** With only 3 runs per condition and sub-1 pp differences on some tasks, the reader cannot assess whether the improvements are stable. Reporting p-values or confidence intervals in the main tables would substantially strengthen the paper.

### Trivial

None.

## Nice-to-Haves

- Extend the ablation table (Table 4) to include TSP and CVRP so that the claim about RL's impact can be evaluated across all four tasks.
- Provide wall-clock time or GPU-hours in the main paper to resolve the budget comparison.
- Report whether the collapse mechanism's analytical guarantee (Equation 2) offers a practical advantage over a simpler fixed-round stagnation threshold.

## Removed Points

These points from the input review were removed after verification against the paper:

- **"Removing replacement on OP (17.57%) even slightly improves performance over the full system."** Factually incorrect. Table 4 shows the full system at 17.41% on OP; w/o replacement at 17.57% is a *worse* gap (higher is worse), so removing replacement degrades performance.
- **Criticism about the collapse mechanism's analytical guarantee being "presented as a benefit but its practical role marginal."** The formalism provides insight into the mechanism's behavior; many papers include such analysis without it being a weakness.
- **Claim about CALM being "clearly not SOTA on TSP compared to NCO methods."** The paper explicitly scopes its comparison to LLM-based AHD methods and acknowledges POMO's superior TSP N=50 result (0.39% vs. 10.04%). This is a legitimate scoping choice, not a flaw.
- **Speculative concerns about missing appendix content or unreleased baselines.** Removed per policy.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the budget-comparison ambiguity and the task-dependence of the RL contribution as areas needing clarification, but do not introduce genuinely novel observations about the paper.

## Suggestions

1. Clarify the budget comparison: either explain how "1,000 heuristic evaluations" and "2,000 LLM queries" are commensurate, or report wall-clock time / GPU-hours directly in the main paper.
2. State the value of G explicitly in the main paper.
3. Specify which parameters are fine-tuned (LoRA rank, target modules, or specific layers).
4. Report concrete values for reward hyperparameters (α₁, α₂, r_invalid) in the main text.
5. Include statistical significance measures (confidence intervals or p-values) in the main result tables.
6. Qualify the outperformance claims in the abstract and conclusion to reflect task-specific and scale-specific results.

**Overall assessment:** The paper tackles a well-motivated problem with a sensible approach and genuine engineering skill. The ablation is thorough, the API-based variant cleanly separates contributions, and the core idea — adapting the LLM via RL during evolutionary search — is sound. The main weakness is the opaque budget comparison, which prevents full interpretation of the results. The remaining issues (overstated claims, missing parameter values, under-specified fine-tuning mechanism) are addressable. With clarifications, this could be a strong paper.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>