## Summary

The paper introduces EconAgentBench, a suite of benchmarks for evaluating LLM agents on three core economic tasks (procurement, scheduling, and pricing) in unknown environments that require exploration and learning over multiple interactions. The benchmarks are synthetically generated with scalable difficulty levels to forestall saturation, and the paper evaluates a range of frontier LLM agents (including GPT-5 and Gemini 2.5 Pro) to demonstrate non-saturation and to derive economically meaningful behavioral insights beyond aggregate scores.

## Strengths

- **Timely and relevant benchmark design.** The focus on multi-turn economic decision-making (procurement, scheduling, pricing) under partial information addresses a gap in existing LLM evaluation, as real-world deployment increasingly involves such tasks. The synthetic generation and difficulty scaling are well-motivated to combat saturation.
- **Rigorous evaluation across multiple frontier models.** The paper tests seven LLMs, including cutting-edge models (GPT-5, Gemini 2.5 Pro), and the results clearly show that even the strongest models do not saturate the hardest difficulty, validating the benchmark’s future-proofness.
- **Behavioral analysis beyond aggregate scores.** By introducing metrics like budget utilization, best-so-far rate, and adaptability, the paper provides deeper insight into *why* agents differ in performance, which is valuable for guiding model development.
- **Solid grounding in economic theory.** The three environments are based on standard economic models (Cobb-Douglas procurement, stable matching, nested logit demand), lending credibility and interpretability to the benchmark tasks.

## Weaknesses

### Fatal

None.

### Major

- **Small number of instances per condition.** Only 12 instances are used per difficulty level and per benchmark. With such a small sample, the reported $p$-values for difficulty scaling and inter-model comparisons may be underpowered, and variance estimates are unreliable. For a benchmark that claims to support arbitrary instance generation, larger N would strengthen the conclusions.
- **No non-LLM baselines.** The paper does not compare LLM agents to simple algorithmic baselines (e.g., random search, Bayesian optimization, or classical solvers for the economic models). Such baselines would help contextualize the difficulty of the tasks and disentangle whether LLM shortcomings stem from reasoning versus exploration challenges.

### Minor

- **Simple scaffolding may understate LLM capabilities.** The paper uses a deliberately minimal agent architecture (tool use + notes). While this allows fair comparison, real-world deployments would likely use more sophisticated scaffolding, prompting, or fine-tuning. The paper’s results may therefore underestimate the potential of LLMs on these tasks.
- **Pricing environment appears overly difficult.** The best LLM scores only ~67% on HARD pricing. While this avoids saturation, it also makes the benchmark less discriminative at present and raises the question of whether the task structure (non-stationary nested logit with many unknown parameters) is learnable within 100 periods with the provided feedback.

### Trivial

- Table 2 uses a horizontal line separator that could be made more consistent.

## Nice-to-Haves

- Add a baseline comparison with a simple algorithmic method (e.g., random search with a fixed number of evaluations) to calibrate task difficulty.
- Consider increasing the number of instances per difficulty to at least 30 for stronger statistical reliability.
- Discuss potential negative societal implications of deploying LLM agents for pricing (e.g., algorithmic collusion), even briefly, given the paper’s applied framing.

## Novel Insights

The paper demonstrates that even frontier LLMs struggle with economic environments requiring sustained learning and adaptation (especially non-stationary pricing, where no model exceeds 67%). A key insight is that reasoning models (o4-mini, GPT-5) excel in stationary tasks (procurement, scheduling) through high budget utilization and best-so-far rates, but do not necessarily outperform non-reasoning models in non-stationary pricing, suggesting that current LLMs lack robust strategies for detecting and responding to environmental change. This highlights an important frontier for future LLM agent research.

## Suggestions

- Release the benchmark code and instance generation parameters to enable community use and extension.
- Include a small-scale ablation study on the effect of the number of periods (e.g., 50 vs. 100 vs. 200) on agent scores, to inform future users about appropriate run lengths.
- For the pricing environment, consider providing limited structural hints (e.g., “demand depends on quality, price sensitivity, and outside option”) to make the task more accessible to current LLMs without undermining the exploration requirement.

## Score and Decision

The paper makes a clear and original contribution by designing economic benchmarks that address a real need in LLM agent evaluation. The experiments are well-executed and the analysis provides actionable insights. The main limitations (small number of instances, lack of non-LLM baselines) are not fatal and can be addressed in future iterations. I recommend acceptance.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>