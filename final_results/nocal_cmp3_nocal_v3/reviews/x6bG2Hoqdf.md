## Summary

This paper proposes CALM, a framework that combines verbal guidance (prompt engineering) with numerical guidance (RL fine-tuning via GRPO) for Automatic Heuristic Design (AHD). Unlike prior LLM-based AHD approaches that keep the LLM frozen and manipulate only prompts, CALM fine-tunes a local 7B LLM using prompt-response-performance triples naturally produced by the evolutionary search loop. The method runs on a single 24GB GPU with INT4 quantization and outperforms API-based baselines on OBP, CVRP, and OP, with more marginal gains on TSP.

## Strengths

1. **Novel integration of RL fine-tuning into the LLM-based AHD loop.** Prior work manipulates only prompts ("verbal gradients"); CALM additionally uses GRPO to adapt the LLM's parameters based on heuristic quality signals ("numerical gradients"). The co-evolution framing (Section 4, Figure 1) clearly distinguishes this from fixed-model approaches.

2. **Ablation study cleanly isolates the RL contribution.** Table 4 shows that removing GRPO causes the largest performance drop (OBP: 0.71% → 1.78%; OP: 17.41% → 19.89%), with each other operator removal also degrading performance but less severely. This directly supports the paper's central claim.

3. **The API-based variant (G=1, no GRPO) demonstrates competitive performance.** Matching or outperforming MCTS-AHD across most settings while using only prompt-level innovations (fine-granularity mutation, diversity-aware crossover, collapse). This shows the verbal guidance contributions have independent value and the framework advances the state of the art on multiple fronts.

4. **Practical local deployment on a single 24GB GPU.** Using an INT4-quantized 7B model, CALM outperforms methods using GPT-4o-mini (a more capable model). The paper is transparent about the model quality gap (Section 5, paragraph 1), making the comparison conservative.

## Weaknesses

### Fatal

None.

### Major

1. **The evaluation budget units are not commensurate between CALM and baselines, and G is not specified for the main GRPO experiments.** The paper states "comparable evaluation budgets—specifically, 1,000 heuristic evaluations for baselines and a fixed budget of 2,000 LLM queries for CALM" (Section 5, paragraph 3). These are different quantities: each LLM query generates G responses that are evaluated (Section 4, paragraph 1: "G responses are sampled from the local LLM"). If G > 1, CALM performs many more heuristic evaluations than the baselines. The paper only specifies G = 1 for the API-based variant (Section 5.2); G for the main GRPO experiments is never stated in the manuscript. Even if G is documented in the appendix, the paper should clarify the comparison logic and explicitly justify why LLM queries and heuristic evaluations are treated as comparable units.

2. **TSP results do not consistently support the claimed superiority.** On N=50 (in-domain), CALM (10.04%) is worse than MCTS-AHD (9.69%). On N=100 and N=200 (out-of-domain), improvements over MCTS-AHD are 0.21 and 0.30 percentage points respectively (Table 2). These margins are small enough that they could fall within run-to-run variability. Meanwhile, POMO (an NCO method) achieves 0.39% at N=50 and 3.01% at N=100, showing the LLM-based AHD class still has substantial room for improvement on this problem. The paper would benefit from acknowledging this inconsistency explicitly rather than treating it as a uniform success.

### Minor

3. **EvoTune's poor performance relative to CALM is not explained.** EvoTune (Surina et al., 2025) is a concurrent AHD method that also fine-tunes the same base model (Qwen2.5-7B-Instruct-INT4) using DPO. Yet EvoTune scores 2.40% on OBP (vs. CALM's 0.71%), 5.82% on CVRP N=50 (vs. 3.83%), and 20.32% on OP N=200 (vs. 12.58%). On OBP, EvoTune is essentially indistinguishable from the hand-crafted Best Fit baseline (2.40%). Because the two methods share the same base model and the same goal (fine-tuning an LLM for AHD), the large gap requires discussion. Without it, the comparison appears to stack the deck in favor of CALM's fine-tuning approach.

4. **Collapse mechanism hyperparameters show high sensitivity.** Table 4 shows that the configuration δ₀=0.005, C=15 degrades OBP from 0.71% to 1.93% and OP from 17.41% to 27.22% — a 2–3× degradation on OBP. The paper acknowledges this briefly but provides no practical guidance for selecting these hyperparameters, which limits the method's usability for practitioners.

### Trivial

None.

## Nice-to-Haves

- A qualitative analysis of how the LLM's generations change during GRPO fine-tuning (e.g., before/after case studies on the same prompt) would strengthen the claim that the model "internalizes characteristics of successful heuristics" (Section 1). The paper currently shows that RL helps but not what the RL learns.
- Wall-clock time or GPU-hours for training would help practitioners assess practicality (likely deferred to the appendix).

## Removed Points

- **Weakness about G being "missing" from main text** — removed because this detail is likely in Appendix H / C, which the parser strips from all papers; the rule about missing appendix content applies. The budget *fairness* concern (different units) is retained above as Major.
- **Weakness about fine-tuning details (LoRA rank, learning rate) missing** — removed per the same rule; these are standard implementation details likely in the appendix.
- **Weakness about HSEvo duplicate row in Table 3** — removed per the formatting-nits rule.
- **Weakness that EvoTune performs "far worse than hand-crafted heuristics"** — factually inaccurate: EvoTune outperforms hand-crafted heuristics on TSP, CVRP, and OP; on OBP it matches them. The broader (valid) concern about unexplained discrepancy is retained as Minor.
- **Strength about addressing an important problem / being novel** — retained as framed with specific evidence.
- **Various speculative "could be..." framing in the harsh critic** — removed per the rule against unanchored speculation.
- **"Strengthening the Paper" qualitative analysis request** — moved to Nice-to-Haves above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Disclose G for the main GRPO experiments and either match the total number of heuristic evaluations to baselines or clearly justify why the different units constitute a "comparable" budget.
2. Add a paragraph discussing the EvoTune discrepancy — why does DPO-based fine-tuning perform so much worse than GRPO-based fine-tuning on the same base model? Even a brief hypothesis (different prompts, training budget, or limitations of DPO for this setting) would address the concern.
3. Discuss the TSP results more candidly: acknowledge the small margins on out-of-domain sets and the reversal on N=50 (in-domain), and report whether the differences are statistically significant.
4. Provide practical guidance for setting the collapse hyperparameters δ₀ and C, given the sensitivity shown in Table 4.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>