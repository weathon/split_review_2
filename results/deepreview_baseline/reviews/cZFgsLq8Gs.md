## Summary

This paper introduces DeepScientist, an autonomous AI system designed to conduct goal-oriented scientific discovery on frontier AI research tasks over month-long timelines. The system formalizes scientific discovery as a Bayesian optimization problem, using a cumulative Findings Memory to balance exploration and exploitation, and demonstrates its capabilities by surpassing human-designed state-of-the-art methods on three tasks (Agent Failure Attribution, LLM Inference Acceleration, and AI Text Detection). The paper claims this is the first large-scale empirical demonstration of an automated system that continuously advances scientific frontiers on complex AI tasks, rivaling human researchers.

## Strengths

- **Ambitious and important research direction**: The paper tackles the significant challenge of fully autonomous scientific discovery on complex, real-world AI tasks rather than synthetic or simplified problems, which is a meaningful step forward for the field.

- **Comprehensive system design**: DeepScientist's three-stage iterative workflow (Strategize & Hypothesize, Implement & Verify, Analyze & Report) coupled with the Findings Memory represents a well-thought-out architecture that addresses key challenges in automated discovery, including learning from failure and balancing exploration vs. exploitation.

- **Thorough experimental evaluation**: The paper evaluates across three diverse tasks with strong human SOTA baselines, provides multiple analyses (success rates, scaling laws, search space visualization), and includes both automated and human expert review of the generated papers.

- **Transparent reporting of limitations**: The paper honestly reports the low success rate (21 progress findings from ~5000 ideas), the 60% failure rate due to implementation errors, and provides realistic discussion of current bottlenecks.

## Weaknesses

### Fatal
None.

### Major
1. **Insufficient evidence that the system truly "redesigns core methodologies" rather than performing sophisticated combinatorial search**: The paper claims DeepScientist autonomously redesigned core methodologies, but the descriptions of the discovered methods (e.g., A2P using abduction-action-prediction, ACRA using stable suffix patterns, PA-TDT using wavelet analysis) appear to be combinations and adaptations of existing techniques from the literature rather than fundamentally novel scientific paradigms. The Bayesian optimization framework with LLM-based surrogate modeling is a form of guided search over a pre-existing idea space, not genuine scientific creativity.

2. **Lack of rigorous baseline comparisons and reproducibility details**: The reported improvements (183.7%, 1.9%, 7.9%) use different metrics across tasks, and the 183.7% improvement figure is misleading as it represents relative improvement on very low absolute accuracy (from ~12% to ~29%). The paper does not provide standard deviations, confidence intervals, or statistical significance tests for the results. Critical implementation details (e.g., exact LLM prompting strategies, temperature settings, the specific retrieval model used, hyperparameter settings beyond the basic UCB configuration) are not provided, making reproduction difficult.

3. **The "two weeks vs. three years" claim is overstated**: The comparison between DeepScientist's 15-day run and three years of cumulative human research on AI text detection is not properly controlled. The human timeline spans multiple distinct methods developed by different teams with different compute budgets and resource constraints, while DeepScientist starts from a strong 2024 baseline (Binoculars) and benefits from accumulated prior human knowledge embedded in its initial codebase and the LLM's training data. A fair comparison would require controlling for starting point, compute budget, and task difficulty.

4. **Limited validation of the core Bayesian optimization claim**: The paper formalizes discovery as Bayesian optimization but the surrogate model is simply "an LLM" contextualized with findings memory, and the acquisition function uses a simple UCB with fixed, untuned weights (w_u = w_q = κ = 1). There is no ablation study comparing this approach to simpler alternatives (e.g., random selection, round-robin, simpler heuristic selection), no comparison to other acquisition functions, and no evidence that the surrogate model's valuations (v_u, v_q, v_e) are meaningful or calibrated. The "Bayesian optimization" framing appears largely cosmetic.

### Minor
1. **The human evaluation protocol has limitations**: The program committee consists of only three reviewers, one of whom is described as a senior volunteer, but it is unclear if any have direct expertise in the specific tasks (Agent Failure Attribution, LLM Inference Acceleration, AI Text Detection). The Krippendorff's alpha of 0.739, while acceptable, indicates non-trivial disagreement. The paper also does not conduct a blind comparison where human experts compare DeepScientist's papers against human-written papers on the same topics.

2. **The scaling law analysis is preliminary**: The one-week scaling experiment (Figure 6) shows only 5 data points per task, uses a different setup (parallel exploration with periodic synchronization rather than the full system), and does not control for the fact that more GPUs allow more simultaneous exploration of different limitations. The "near-linear" claim is based on a single curve with no error bars or replication.

3. **The comparison against other AI Scientist systems (Table 2) is weakened by using an automated reviewer**: The paper uses DeepReviewer-14B to evaluate papers from other systems, but these papers may be curated selections (as the paper itself notes), and the automated review scores may not reflect actual reviewer opinions. The human evaluation (Table 3) is more credible but only evaluates DeepScientist's own papers, not those of competing systems.

### Trivial
None.

## Nice-to-Haves

- An ablation study comparing DeepScientist's selection strategy against simpler baselines (e.g., random selection, first-in-first-out, round-robin) would strengthen the claim that the Bayesian optimization framing provides meaningful benefits.

- A cost-effectiveness analysis comparing the 20,000 GPU hours used by DeepScientist against what human researchers could achieve with the same compute budget on the same tasks would help contextualize the results.

- Discussion of the environmental impact of 20,000 GPU hours of computation would be appropriate for a paper advocating automated scientific discovery at scale.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Provide statistical significance measures (confidence intervals, p-values) for all reported improvements over baselines, and include standard deviations across multiple runs where applicable.

- Conduct a controlled comparison between DeepScientist's idea selection mechanism and simpler baselines (random selection, round-robin, greedy exploitation-only) to validate the claimed benefits of the Bayesian optimization approach.

- Clarify the precise role of the "surrogate model" and provide evidence that its valuations (v_u, v_q, v_e) are well-calibrated and useful for selection.

- For the "two weeks vs. three years" claim, either provide a more careful controlled comparison or tone down the claim to avoid misleading readers.

- Release additional implementation details (exact prompts, retrieval model specifics, hyperparameter search, failure mode analysis) to support reproducibility.

## Score and Decision

This paper tackles an important and timely problem—fully autonomous scientific discovery—with an ambitious system design and extensive experimental evaluation. The core contributions—the three-stage workflow, Findings Memory, and large-scale demonstration on real AI tasks—are meaningful advances over prior work that operated on simpler problems. The transparent reporting of low success rates and implementation bottlenecks is commendable.

However, the paper suffers from several significant weaknesses that prevent it from being a top-tier contribution. The claimed "Bayesian optimization" formalism is not convincingly validated (no ablation against simpler alternatives, no evidence that the surrogate model valuations are meaningful). The key claims about "redesigning core methodologies" and compressing "three years of human research into two weeks" are overstated relative to the evidence provided. The experimental comparisons lack statistical rigor, and critical reproducibility details are missing.

Given these issues, the paper represents solid, incremental progress in an important direction but does not fully deliver on its ambitious claims. It would benefit from additional validation and more measured presentation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>