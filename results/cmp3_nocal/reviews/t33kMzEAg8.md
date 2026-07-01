Now I'll write the final review.

## Summary

This paper proposes SWIREASONING, a training-free inference framework that dynamically switches between explicit chain-of-thought reasoning and continuous latent-space reasoning. Switching is driven by an entropy-based confidence signal: when confidence rises, the model consolidates via explicit token paths; when uncertainty persists, it explores in latent space. A switch-count controller limits overthinking. The method is evaluated on 11 benchmarks across 4 model families/scales (1.7B–32B), consistently improving average accuracy by 1.8%–2.7% over single-mode baselines and showing token efficiency gains under constrained budgets.

## Strengths

- **Training-free and practical.** SWIREASONING requires no retraining or fine-tuning — all operations occur at inference time. This is a genuine practical advantage over training-required latent reasoning approaches, particularly for large models (8B–32B) where retraining is expensive.

- **Well-motivated problem framing (Sec. 3.3).** The paper clearly articulates the complementary failure modes of pure-explicit and pure-latent reasoning — premature commitment vs. unfocused drift — and uses this insight to design an asymmetric dwell-window mechanism ($W_{L\rightarrow E}=0$, $W_{E\rightarrow L}>0$) that is principled rather than ad-hoc.

- **Broad evaluation scope.** The method is tested across 4 model families/scales (Qwen3-1.7B, Qwen3-8B, DeepSeek-R1-Distill-8B, Qwen3-32B) on 11 benchmarks spanning math (GSM8K, MATH500, AIME24/25), STEM (GPQA Diamond), coding (HumanEval, LeetCode-Contest, MBPP, LiveCodeBench), multi-hop QA, and commonsense reasoning — lending weight to the claim of generalizability.

- **Consistently positive results.** Across all comparison tables, SWIREASONING improves over every single-mode baseline (CoT sampling, CoT greedy, Soft Thinking). The improvements are modest but remarkably consistent (every benchmark, every model), which is more credible than a single large win on one benchmark.

## Weaknesses

### Fatal

None.

### Major

1. **No variance or statistical significance reporting.** The accuracy gains are small in absolute terms — e.g., +0.39% on GSM8K (Qwen3-1.7B), +0.46% on GSM8K (Qwen3-8B), +0.60% on MATH500 (DeepSeek-R1). On a benchmark of ~900 examples (GSM8K), a 0.39% gain represents 3–4 questions. No confidence intervals, standard deviations, or multiple-seed runs are reported anywhere in the paper. Since CoT sampling itself is stochastic (temperature-based), the reader cannot determine whether the observed improvements reflect genuine method behavior or noise. The gains on harder benchmarks (AIME24/25: +5.0%) are more substantial, but the overall evidence would be considerably strengthened by variance estimates.

2. **Token efficiency metric conflates switching with early stopping; no control baseline.** The switch-count controller (Sec. 3.4) force-injects answer prefixes after a budgeted number of switches. The resulting token efficiency gains (57%–84% reported) are measured against unrestricted CoT. There is no comparison against simpler baselines that also stop early — e.g., CoT with budget forcing (truncating at comparable token budgets) or CoT with early-exit heuristics. Without these controls, the efficiency advantage cannot be cleanly attributed to the *switching mechanism* as distinct from the trivial effect of using fewer tokens.

3. **Entropy-based switch criterion is not ablated against simpler alternatives.** The core algorithmic claim is that entropy-trend-based switching (Sec. 3.3) is beneficial. But there is no ablation comparing this against (a) random switching at the same rate, (b) a fixed alternating schedule, or (c) always-staying-in-explicit with the same switch-count controller. Without such controls, the marginal value of the entropy signal over the bounded-switching framework itself is unestablished. Given that the switch-count controller alone can produce large efficiency gains, this is a substantive evidential gap.

### Minor

4. **Hyperparameter sensitivity of the exit bias $\beta_0$ (Table 2).** At $\beta_0=0.0$, accuracy collapses to 8.33% on AIME24 and 9.17% on AIME25 — a drop of 30–40 absolute points from reasonable settings. The paper acknowledges this ("excessive interference") and proposes difficulty-aware adaptation as future work, but the narrow window of acceptable values remains a practical concern. This weakens but does not invalidate the method.

5. **Abstract overstates the accuracy range.** The abstract claims "1.8%–3.1%" average accuracy improvement. The highest per-model average observed in the tables is +2.70% (broader domains, Qwen3-8B). The 3.1% upper bound does not appear in any presented result. The abstract should reflect what the data actually shows.

6. **Baselines are limited to single-mode methods.** The paper compares only against pure-explicit (CoT) and pure-latent (Soft Thinking) reasoning. No comparison is made against methods that also combine or alternate between modes — though the paper acknowledges that such alternatives may be sparse or non-existent in the training-free setting. If any such method exists, it should be included; if not, this should be explicitly noted.

### Trivial

None.

## Nice-to-Haves

- A qualitative analysis showing example switching trajectories — how many switches per problem, at what semantic boundaries they occur, and what the entropy dynamics look like — would make the mechanism more interpretable.
- Reporting wall-clock time in addition to token efficiency would help practitioners assess the practical overhead of computing the soft embedding (Eq. 1) at each latent step.
- Failure analysis examining which problems SWIR gets wrong that CoT gets right (and vice versa) would clarify the method's strengths and limitations.

## Removed Points

- **"Underspecified entropy refresh"** — removed because the paper *does* specify (line 93): "We reset $\bar{H} \leftarrow H_t$ upon any switch." The reviewer's claim that this is undefined is incorrect.
- **"Training cost claim without citation"** (line 23) — removed because the surrounding paragraph cites multiple training-required approaches (Hao et al., 2024; Su et al., 2025; Liu et al., 2024, et al.). The claim about cost is self-evident from the cited methods.
- **"Soft embedding manifold limitation"** — removed because this is a speculation about a borrowed technique that the paper is not claiming to improve.
- **"RL future work doesn't follow from framing"** — removed as a subjective opinion about a single sentence in the conclusion.
- **"Missing qualitative analysis / failure analysis / wall-clock time"** — moved to Nice-to-Haves as they are supplementary improvements, not core weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report all main results with at least 3 random seeds and provide mean ± std (or bootstrapped confidence intervals). This is the single most important improvement.
2. Add ablation studies for the entropy-based switch criterion against random switching and fixed alternating schedules at the same switch rate.
3. For token efficiency experiments, include a baseline that applies budget forcing or early truncation to CoT at equivalent token budgets to isolate the effect of switching from the effect of early stopping.
4. Correct the abstract's accuracy claim (3.1% → 2.7%) and reconcile the token efficiency range (57%–79%) with the "+84%" figure caption.

## Score and Decision

The paper proposes a clean, well-motivated, training-free method with consistently positive results across broad evaluation. The core weaknesses — lack of variance reporting, missing ablations for the entropy criterion, and unconvincing efficiency baselines — are substantive but addressable. In its current form, the evidence is suggestive rather than conclusive, particularly for the small-margin improvements.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>