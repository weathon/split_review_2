## Summary

The paper introduces DeepScientist, an LLM-based multi-agent system for goal-oriented, autonomous scientific discovery on modern AI tasks. It formalizes the discovery process as a Bayesian Optimization problem with a persistent *Findings Memory* that balances exploitation and exploration, and demonstrates the system on three frontier tasks (Agent Failure Attribution, LLM Inference Acceleration, AI Text Detection), claiming SOTA improvements of up to 183.7% using 20,000 GPU hours. DeepScientist also produces full research papers, which are evaluated via both automated and human review.

## Strengths

- **Timely and ambitious problem.** Automating scientific discovery on complex, realistic tasks is an important research direction, and the scale of effort (20,000 GPU hours, 5,000 generated ideas) is substantial.
- **Architectural integration.** The three-stage cycle (hypothesize, implement, analyze) coupled with a persistent memory that accumulates both successes and failures is a reasonable design choice for long-horizon exploration.
- **Multi-faceted evaluation.** The paper attempts to validate not just task performance but also the quality of generated papers using both automated reviewers and a human program committee, which is more thorough than typical AI scientist evaluations.

## Weaknesses

### Fatal

1. **Non-existent foundational models.** The paper states that DeepScientist uses "Gemini-2.5-Pro" for core logic and "Claude-4-Opus" for code generation. As of the paper's apparent time frame (early–mid 2025), neither of these models exists or has been publicly released. The experimental results depend entirely on these unverified models, and the paper provides no evidence that they could be accessed or reproduced. This invalidates the core experimental claims and violates the fundamental principle of reproducibility.

### Major

2. **Misleading comparison framing.** The claim that "in just two weeks [DeepScientist achieved] progress on AI text detection that is comparable to three years of cumulative human research" is deceptive. The human trajectory shows progress from ~0.66 to ~0.80 AUROC (a gain of 0.14), while DeepScientist improves from ~0.80 to ~0.86 (a gain of 0.06). The system starts from a stronger baseline and makes a smaller absolute improvement. The visual presentation (Figure 1) further exaggerates the comparison by using different axis scales.

3. **Heavy human supervision contradicts autonomy.** The paper states "three human experts supervise the process to verify outputs and filter out hallucinations." This level of manual intervention conflicts with the claim of "fully autonomous scientific discovery" and raises questions about how much of the system's success is attributable to the AI versus undereported human guidance.

4. **Superficial Bayesian Optimization framing.** The surrogate model is simply a prompted LLM that produces integer scores (0–100) on "utility, quality, and exploration," with no training or calibration against actual experimental outcomes. The acquisition function is a basic UCB with arbitrarily set weights (w_u = w_q = κ = 1) that are not tuned or ablated. This does not constitute a genuine Bayesian Optimization procedure and overclaims the theoretical contribution.

5. **Weak baselines inflate relative improvements.** The Agent Failure Attribution baseline ("All at Once") achieves only 12.07% and 16.67% accuracy, which are extremely low. The claimed 183.7% improvement brings accuracy to 47.46%—still far from reliable. On LLM Inference Acceleration, the improvement is a meager 1.9% (3.65 tokens/second). The practical significance of these advances is questionable.

### Minor

6. **Evaluation of generated papers is limited.** The human program committee consists of only three individuals (two self-identified ICLR reviewers, one area chair), selected by the authors. No blinding or conflict-of-interest handling is described. The automated reviewer (DeepReviewer) may favor the system's own style since it is from the same lab (Zhu et al., 2025a). The 60% acceptance rate for DeepScientist compared to 0% for all other systems is suspicious and demands independent validation.

7. **Success rate is extremely low.** Only 21 of ~5,000 ideas (0.4% ) become "Progress Findings," and even fewer (5) become full papers. The paper attributes 60% of failures to implementation errors rather than flawed hypotheses, indicating a fundamental limitation of the executor, not the planner. This suggests the current approach is far from reliable scientific discovery.

8. **Scaling analysis methodology.** Figure 6 reports "progress findings" per week across different numbers of GPUs, but the "Overall" line sums across three very different tasks, which is not a meaningful aggregate. The one-week time window is short, and the near-linear scaling claim may not generalize to longer timelines or more complex tasks.

### Trivial

- The paper uses hyperbolic language ("heralding an era," "foundational shift") that is not justified by the evidence.

## Nice-to-Haves

- Provide an ablation study that isolates the effect of the surrogate model, acquisition function, and Findings Memory against simpler alternatives (e.g., random selection, round-robin).
- Compare against a human-baseline of similar GPU-hour cost rather than only human-published SOTA methods.
- Release the full execution logs and model-generated code to enable independent replication.

## Novel Insights

None beyond the paper's own contributions. The idea of using a memory of past experiments to guide LLM hypothesis generation has been explored in prior AI scientist systems. The Bayesian optimization framing is not executed in a way that yields new theoretical understanding.

## Suggestions

- Clarify the exact models used and provide evidence of their existence/availability. If the paper refers to models under development, this must be stated explicitly and the results caveated accordingly.
- Replace the misleading "three years vs. two weeks" comparison with a more honest presentation of absolute improvements and baselines.
- Reduce the level of human supervision and report the system's performance with and without it, or acknowledge the system as human-in-the-loop.
- Provide confidence intervals, error bars, and statistical tests for all claimed improvements.
- Rephrase claims of "first" and "foundational shift" to match the scope and reliability of the evidence.

## Score and Decision

**Score: 4**

**Decision: Reject**

The paper addresses an important goal and presents a system of considerable scale and complexity. However, the fatal reliance on non-existent foundation models invalidates the core experimental evidence. Even setting that aside, the superficial Bayesian Optimization framing, misleading progress comparisons, heavy human supervision, and modest absolute improvements on weak baselines make the paper's claims far stronger than what is actually demonstrated. The work may serve as a useful engineering effort but does not meet the bar for scientific rigor and reproducibility required at ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>