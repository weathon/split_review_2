## Summary

This paper introduces **EconAgentBench**, a suite of benchmarks that evaluate LLM agents on three core economic tasks—procurement, scheduling, and pricing—under unknown environment conditions that must be learned through multi-turn exploration. The benchmarks are synthetically generated with scalable difficulty levels (BASIC, MEDIUM, HARD) to forestall saturation. The authors evaluate a range of frontier LLMs (GPT-4o, GPT-4.1, GPT-5, Gemini 1.5 Pro, Gemini 2.5 Pro, Claude 3.5 Sonnet, o4-mini) and show that difficulty scaling is effective and that even the best models do not saturate the HARD level. Additional metrics (budget utilization, best-so-far rate, adaptability) provide economically motivated insight beyond overall scores.

## Strengths

- **Timely and important domain**: The paper addresses a gap in existing LLM evaluation by focusing on multi-turn economic decision-making in unknown environments—a realistic and growing use case for LLM agents.

- **Well-designed, scalable benchmarks**: The three environments (procurement, scheduling, pricing) cover stationary and non-stationary settings, and the synthetic generation with controllable parameters (number of products/workers, preference distributions, etc.) allows difficulty scaling that demonstrably avoids saturation.

- **Thorough evaluation across frontier models**: The authors test a diverse set of recent LLMs, including GPT-5 and Gemini 2.5 Pro, and the results provide a clear picture of current capabilities and model-specific strengths/weaknesses.

- **Rich beyond-score analysis**: The introduction of action-quality metrics (budget utilization, best-so-far rate, adaptability) adds economic relevance and helps explain score differences—a valuable feature for benchmarking.

- **Lightweight, future-proof interaction protocol**: Using tool use (function calling) rather than a bespoke API makes the benchmarks easily applicable to new models and agent frameworks.

## Weaknesses

### Fatal

- None identified.

### Major

- **No error bars or confidence intervals on main results**: Table 2 reports only point estimates (averages over 12 instances) without any measure of variability (standard deviation, standard error, or confidence intervals). This makes it impossible to assess the statistical significance of differences between models or difficulty levels beyond the one reported p‑value for BASIC vs. HARD. The lack of variance information weakens the reliability of the core experimental claims.

- **Small number of instances per condition (n=12)**: While 12 random instances may be acceptable for a proof‑of‑concept, the paper does not justify this sample size. Given the stochastic nature of both environment generation and LLM sampling (temperature 1), more instances (or a power analysis) would be expected to support generalizable conclusions.

- **No non‑LLM baselines**: The paper only compares LLM agents to each other. Including simple baselines (e.g., random search, greedy optimization, or a basic multi‑armed bandit algorithm) would help disentangle whether observed performance stems from LLM‑specific reasoning abilities or from general exploration strategies. This omission makes it unclear how much added value the LLM provides.

- **Pricing non‑stationarity pattern not clearly specified**: The text describes two kinds of patterns (linear shifts and periodic shifts) but does not state which pattern (or combination) is used in the reported experiments. This ambiguity hinders reproducibility.

### Minor

- **Economic insight analysis is relatively shallow**: While the additional metrics (budget utilization, best‑so‑far rate, adaptability) are useful, they remain high‑level. Deeper qualitative analysis (e.g., example trajectories, failure modes, or exploration strategies) would strengthen the claimed “economically meaningful insights.”

- **No discussion of computational cost or inference time**: Multi‑turn evaluation with 100 periods is expensive, but the paper provides no information on token usage, cost, or wall‑clock time. Such details would help practitioners assess practical feasibility.

- **Agent scaffolding details are minimal**: The paper states that prompts and scaffolding are “deliberately simple and neutral” but does not provide the exact prompts or a description of how the notes tool is used. This limits reproducibility.

### Trivial

- None of note beyond parser‑related artifacts, which are not criticized.

## Nice-to-Haves

- Add error bars (standard error or bootstrap confidence intervals) to all tables and figures.
- Include non‑LLM baselines (e.g., random assignment, greedy search, Bayesian optimization) to contextualize LLM agent performance.
- Provide the exact prompt templates and tool‑calling details for the LLM agent scaffolding.
- Specify which non‑stationarity pattern(s) were used in the pricing experiments, and report results separately for each pattern.
- Increase the number of benchmark instances (or justify the sample size statistically) and release the full suite.
- Include a discussion of the sample complexity or theoretical lower bounds for each task.

## Novel Insights

None beyond the paper’s own contributions: the benchmark design and the observation that performance across the three tasks reveals distinct model strengths (e.g., reasoning models excel at stationary procurement/scheduling, while a different model leads in non‑stationary pricing). The action‑quality metrics provide a useful decomposition but do not constitute a fundamentally new insight about LLM behavior.

## Suggestions

1. Add standard errors or confidence intervals to the numerical results to support claims about model ordering and difficulty scaling.
2. Include at least one simple optimization baseline (e.g., random search with the same number of trials) to clarify the unique value of LLM agents.
3. Clarify the exact non‑stationarity pattern used in the pricing experiments and report scores separately for linear and periodic shifts.
4. Increase the number of random instances (e.g., to 50 or 100) to reduce variance and improve statistical reliability.
5. Provide a public repository with instance generators, agent scaffold code, and exact prompts to ensure full reproducibility.

## Score and Decision

**Score**: 6.0

**Decision**: Accept

The paper makes a solid contribution by introducing a well‑motivated, scalable benchmark suite for evaluating LLM agents in complex economic environments—an area that is currently underserved by existing benchmarks. The evaluation is broad and includes frontier models, and the design choices (synthetic generation, difficulty scaling, tool‑based interaction) are forward‑looking. However, the experimental rigor is weakened by the lack of error bars, small instance count, and absence of non‑LLM baselines. These issues are addressable in a revision and do not invalidate the core contribution, but they prevent the paper from reaching the level of a strong accept (8‑10). A score of 6 reflects a borderline‑to‑clear accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>