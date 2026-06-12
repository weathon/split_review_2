## Summary

The paper introduces ASPEC, a framework for automated agent design that reconciles static task-level architecture search with adaptive per-query regeneration. It proposes a two-stage lifecycle—evolutionary discovery of specialist agent archetypes followed by experiential cultivation of those specialists through memory accumulation—governed by a lightweight "retain-then-escalate" meta-controller that decides when to reuse established architectures versus resample new ones. Experiments across five benchmarks show ASPEC achieves best or near-best performance with significantly lower training and inference costs compared to existing approaches.

## Strengths

- **Well-identified research gap with clear framing**: The paper convincingly argues that task-level (ADAS, AFlow) and query-level (MaAS, FlowReasoner) agent design paradigms each have fundamental limitations—rigidity versus rediscovery cost—and positions ASPEC as a principled reconciliation. This framing is well-motivated and the prior art discussion is thorough.

- **Comprehensive experimental evaluation**: The paper evaluates against 13 baselines across 5 benchmarks spanning three domains (math, QA, code), with cross-model transfer (Gemini, GPT-4o-mini, Llama) and cross-benchmark transfer experiments. This breadth of evaluation is genuinely impressive and goes well beyond what most agent design papers provide. The efficiency analysis in Table 2 is particularly valuable, showing ASPEC's training cost on GPQA is only $1.38 versus $20.14 for AFlow.

- **Thorough ablation study**: The ablations (Figure 6 left) cleanly isolate contributions of each component. The 5.4% drop from removing specialist operators (62.8→57.4%) and the near-tripling of cost (0.88→2.26 USD) provides strong evidence that specialists drive both performance and efficiency. The comparison against alternative control policies (random, cosine similarity, LLM-as-gate) is well-designed and demonstrates the meta-controller's value: the LLM-as-gate achieves 62.5% accuracy but at 4.25× the cost.

- **Interesting transferability findings**: The cross-benchmark experiment (Figure 5 right) showing that specialists trained on GPQA transfer effectively to HumanEval and MMLU is a valuable empirical finding. The paper's explanation—that restricting the pool to specialists prevents the Architect from defaulting to safe but less capable generalist operators—is plausible and insightful.

## Weaknesses

### Fatal
None.

### Major

- **No error bars or statistical tests on main results**: Table 1 presents single-point results without variance estimates for a method that involves stochastic evolutionary search. The sensitivity analysis (Figure 6) shows 4-run means, confirming variance exists, but the main comparison table lacks this. Given that several margins are small (e.g., +0.8% over AFlow on MATH, -0.5% on MMLU), it is unclear which differences are statistically meaningful. This significantly weakens the empirical claims.

- **Underspecified meta-controller training**: The paper formalizes the meta-controller as an MDP (Equations 3-4) but provides almost no detail on how the policy π_θ is actually trained. What RL algorithm is used? How are rewards shaped? How many training episodes? What is the reward signal—accuracy, cost, or some combination? Given that the meta-controller is central to the paper's "retain-then-escalate" contribution, this is a notable gap. The training details appear to be relegated entirely to the appendix, which limits the reader's ability to assess the approach.

### Minor

- **Modest margins on several benchmarks**: While GPQA (+1.5% over AFlow) and SciCode (+2.3% over MaAS) show meaningful improvements, ASPEC actually underperforms AFlow on MMLU (90.0 vs 90.5) and MaAS on HumanEval (91.4 vs 91.6). The average improvement over AFlow is 69.6 vs 68.4 (+1.2), which is real but not dramatic for a substantially more complex system. The paper would benefit from a more honest discussion of where the approach does and does not help.

- **Lack of analysis on when the meta-controller retains vs. resamples**: Beyond the confusion matrices in Figure 8, there is no analysis of what drives the meta-controller's decisions. Is resampling correlated with query difficulty, domain shift, or specialist coverage? Understanding this behavior would strengthen the paper's contributions and provide useful design insights.

### Trivial
None.

## Nice-to-Haves

- A per-benchmark breakdown of specialist types discovered (beyond the GPQA case study in Figure 4) would help readers understand what the evolutionary process finds across different domains.
- An analysis of how the meta-controller's retain/resample decisions correlate with query features (difficulty, domain similarity to training) would provide valuable design insights.
- Comparing ASPEC against a simple performance-based heuristic baseline (e.g., retain if the previous query was answered correctly) would contextualize the learned policy's value.

## Novel Insights

The paper's most novel insight is that the lifecycle of agent systems—discovery, cultivation, and adaptive deployment—can be formalized as a hierarchical RL problem where the high-level policy governs *when* to invoke the expensive low-level architectural redesign. This framing exposes a previously underexplored trade-off: aggressive per-query adaptation prevents the accumulation of agent-level expertise, while static architectures cannot adapt. The "retain-then-escalate" policy provides a practical resolution, and the empirical finding that a lightweight MLP-based controller can effectively approximate an LLM-as-gate oracle at a fraction of the cost is practically valuable. The observation that restricting the operator pool to cross-domain specialists can improve performance (ONLYSPEC in Figure 5) is also genuinely surprising and suggests that forcing specialist utilization can be more beneficial than maintaining flexible generalist fallbacks.

## Suggestions

- Add error bars (at least 3-5 runs) to all results in Table 1 and report significance tests where margins are small.
- Provide a dedicated subsection (or expand the existing one) describing the meta-controller training procedure, including the RL algorithm, reward function, and training details.
- Include a qualitative analysis of meta-controller decisions: what kinds of queries trigger resampling, and does this correlate with domain difficulty or novelty?
- Discuss the limitations of the approach more concretely—under what conditions would one expect ASPEC to underperform simpler alternatives?

## Score and Decision

The paper makes a meaningful conceptual contribution by formally bridging two paradigms in agent design automation with a well-structured lifecycle framework. The experimental evaluation is among the most comprehensive I've seen for agent design papers, covering multiple benchmarks, models, and transferability settings. However, the lack of error bars on main results for a stochastic method, underspecified meta-controller training details, and only modest margins on several benchmarks temper enthusiasm. The strong results on expert-level benchmarks (GPQA, SciCode) and the compelling efficiency gains push this above average, but not enough for a clear accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>