## Summary

EconAgentBench introduces a suite of three synthetic benchmarks (procurement, scheduling, pricing) that evaluate LLM agents in multi-turn economic decision-making under uncertainty. The environments are parameterized for scalable difficulty, the interaction protocol uses lightweight tool-use, and the paper evaluates seven frontier LLMs including GPT-5 and Gemini 2.5 Pro. The core contribution is the benchmark design itself and the demonstration that it can discriminate between models and supports difficulty scaling.

## Strengths

- **Well-motivated and economically grounded benchmark design.** The three tasks (combinatorial procurement, stable-matching scheduling, non-stationary pricing) each capture a distinct and practically important class of economic problems where LLM agents are increasingly being deployed. The mathematical formulations (Cobb–Douglas utility, Gale–Shapley stability, nested logit demand) are principled and the key unknowns (effectiveness scores, preferences, demand parameters) are naturally hidden from the agent, forcing genuine exploration.

- **Synthetic generation with demonstrated difficulty scaling.** The environments are parameterized (by number of products/workers/tasks, range of scores, etc.), and the paper validates that scores consistently decrease from BASIC to MEDIUM to HARD across all model–environment combinations (Table 2). This provides empirical support for the scaling mechanism, addressing the saturation problem that plagues static benchmarks.

- **Timely and broad model coverage.** The evaluation includes genuinely frontier models — GPT-5 and Gemini 2.5 Pro alongside o4-mini, GPT-4.1, GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro — making the results useful as a snapshot of current capabilities. The inclusion of both "reasoning" and non-reasoning models adds analytical value.

- **Built-in calibration via scoring metrics.** Procurement and pricing scores are normalized by the optimal solution; scheduling scores are normalized by a uniform random baseline (allowing negative scores when LLMs underperform random). This provides interpretability absent from raw accuracy benchmarks.

## Weaknesses

### Fatal
None.

### Major

- **No variance reporting, making between-model comparisons uninterpretable.** All results in Tables 2 and 3 are point estimates from 12 randomly generated instances with one run per instance at temperature 1. No standard deviations, confidence intervals, per-instance scores, or error bars are reported. The sole statistical statement — "scores on HARD instances are lower than scores on BASIC instances (p < 0.05, one-sided Welch's t-test)" — is vague (it is unclear whether this is a single aggregated test or multiple comparisons) and does not address the central question of whether reported gaps between models (e.g., GPT-5 at 75.0 vs. o4-mini at 60.9 on procurement HARD, or GPT-4.1 at 66.8 vs. Gemini 2.5 Pro at 62.8 on pricing HARD) are signal or noise. For a benchmark paper whose claims include ranking models and demonstrating non-saturation, this is the most significant evidential weakness.

### Minor

- **The "non-saturation" claim is stronger than the evidence supports.** The paper claims "arbitrary difficulty scaling (to forestall saturation)" (Section 5) but only tests three difficulty levels. GPT-5 scores 90.5/100 on scheduling HARD — leaving only 9.5 points of headroom, which suggests this level may already be near ceiling for the best model. The claim would be more convincing if the paper demonstrated that performance degrades further at a difficulty level beyond HARD while remaining discriminative. The design *enables* arbitrary scaling, but the paper does not demonstrate it.

- **Pricing evaluation ambiguity.** The instantiation paragraph (line 171) states that the environment varies parameters "according to a predictable pattern (either linear shifts or periodic shifts)" without specifying which pattern(s) were used in the experiments. Table 2 reports a single pricing score per model per difficulty level. If both patterns were tested and aggregated, the results conflate two cognitively different tasks; if only one was used, the paper should say which. This ambiguity undermines reproducibility of the pricing experiments.

- **The economic insights analysis (Section 4.3) adds limited value beyond the raw scores.** The budget utilization metric for procurement is useful but largely tautological (spending near the budget is necessary for a high score). The adaptability metric for pricing is acknowledged by the authors to be confounded (Gemini 1.5 Pro's high adaptability is "driven by poor-quality actions in the first 10 periods," line 238). The best-so-far rate for scheduling correlates closely with scores and does not cleanly separate search efficiency from final quality. These metrics would be more informative if accompanied by qualitative examples of model strategies or failure modes.

- **No analysis of the notes-tool usage.** The paper introduces `write_notes` and `read_notes` as a key architectural component for cross-period memory (line 75) but never examines whether models actually use these tools, how effectively, or whether failure to use them explains performance differences. This is a natural analysis given the paper's own framing.

### Trivial
None.

## Nice-to-Haves

- **Multiple runs per instance.** With temperature 1, trajectories are stochastic. Running each instance with multiple random seeds would disentangle instance-level variance from trajectory-level variance and enable proper statistical testing.
- **Simple algorithmic baselines.** The scoring normalization provides some calibration, but adding even a random-sampling agent that uses the same tool interface would help practitioners judge whether a given score is impressive relative to a non-LLM approach.
- **Qualitative trajectory examples.** Representative examples of model behavior (e.g., how models set prices over time in response to linear vs. periodic shifts) would be more illuminating than the confounded adaptability metric.

## Removed Points

- **Criticism about missing non-LLM baselines being a "methodological gap" that "limits interpretability of all results."** The paper's scoring metrics already normalize by optimal solutions (procurement, pricing) and by a uniform random baseline (scheduling), which provides calibration. The benchmark's stated purpose is to evaluate LLM agents; demanding comparison to bespoke algorithmic agents is outside the paper's scope. Weakened to Minor/Nice-to-have.
- **Criticism about computational costs not being reported.** The paper states these are in Appendix A (line 187), which was stripped by the parser. Removing per rule about missing appendix content.
- **Criticism about "one run per instance is insufficient" as a major issue.** While valid, this is standard practice in benchmark evaluations due to the high cost of multi-turn LLM queries (100 periods × 12 instances × 7 models). Demoted to Nice-to-have.
- **Claim that strengths 1 and 2 are generic.** Strength 1 ("well-motivated benchmark domain") is supported with specific citations and problem framing in the paper. Strength 2 ("synthetic instance generation with explicit difficulty scaling") is backed by the mathematical parameterization (Section 3.3) and empirical validation (Table 2). Both are concrete and retained.
- **Section-by-section notes about RL bandit benchmarks missing from related work.** This is a request to expand scope beyond what the paper targets. Removed as scope creep.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add standard deviations, per-instance score distributions, or confidence intervals to Tables 2 and 3. This is the single highest-impact improvement: without it, readers cannot assess whether model differences are meaningful.
- Specify in the main text which pricing pattern(s) were used and, if both, report results separately for linear shifts and periodic shifts.
- Test at a difficulty level beyond HARD (or at least frame the "non-saturation" claim more modestly, acknowledging that only three levels were tested).
- Include a representative qualitative example of model behavior per environment to strengthen the economic insights analysis.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>