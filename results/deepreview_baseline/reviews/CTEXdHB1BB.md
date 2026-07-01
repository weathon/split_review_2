## Summary
The paper proposes CANON (Conditional advaNtage estimatiON), a novel advantage estimation method for reinforcement learning with verifiable rewards (RLVR) in large reasoning models. CANON regroups sampled responses by a target metric (e.g., entropy, response length) into two groups and computes inter-group and intra-group advantages, allowing the training signal to amplify the metric’s influence without a pre-defined directional prior (higher-is-better or lower-is-better). Experiments on three LLMs across math reasoning and complex logic tasks show that CANON improves accuracy and token efficiency, and that a scheduled combination (CANON-Dynamic) can balance performance across both task types.

## Strengths
+ **Novel and well-motivated idea.** The conditional regrouping approach is a clean, principled way to incorporate training metrics into advantage estimation without hand-crafted penalty terms. The observation that DR.GRPO is a special case (μ=0.5) provides a strong theoretical foundation.
+ **Extensive empirical evaluation.** The paper tests CANON on three different LLMs, six math benchmarks, and three challenging logic reasoning subsets, comparing against several baselines (ReMax, RLOO, GRPO, DR.GRPO, Entropy Adv, Clip-Cov). The efficiency analysis (CANON-Eff) is thorough and includes Pareto frontier comparisons.
+ **Rich analysis of training dynamics.** Figures 2, 5, and 6 offer insight into how inter-group and intra-group advantages affect entropy, length, and reflection behavior, supporting the claims about selective amplification.
+ **Practical value.** The method is simple to implement on top of existing GRPO-like frameworks, requires no additional model components, and yields consistent improvements in both performance and efficiency.

## Weaknesses

### Fatal
- **Inconsistency between radar chart (Figure 3) and Table 2.** The radar chart and its accompanying table present values (e.g., Llama-8B CANON-Dynamic logic 35.2%) that do not match the numbers in Table 2 (Llama-8B CANON-Dynamic logic 18.9%). DR.GRPO logic for Llama-8B is also listed as 18.9% in the radar table, which is actually the CANON-Dynamic value from Table 2. This misrepresentation undermines the central claim that CANON-Dynamic “outperforms DR.GRPO across all models and tasks” and suggests either a computational error or selective normalization that is not explained. The paper cannot be accepted with such a data inconsistency.

### Major
- **No statistical significance or variance reported.** Evaluation results for small benchmarks (AIME, AMC) are given as point estimates (Avg@10), but no confidence intervals, standard deviations, or multiple-seed experiments are provided. Given the modest improvements (e.g., +1.0 pt math, +3.0 pt logic for Qwen-7B), it is unclear whether these gains are statistically reliable.
- **Ad-hoc scheduling strategy for CANON-Dynamic.** The paper tries four scheduling heuristics and selects the best per model (Cosin-First-Inter-Later-Intra for two models, First-Inter-Later-Intra for the third). No principled guide is offered for choosing or tuning the schedule, which limits the method’s generality and reproducibility.

### Minor
- **Limited exploration of metrics.** The method is tested only on entropy and response length. While these are well-motivated, the claim that CANON “amplifies the impact of the target metric without presuming its direction” would be stronger with evidence on other metrics (e.g., confidence, uncertainty).
- **Theoretical analysis relies on independence assumption.** Theorem 2 assumes independent conditions, which may not hold in practice. The proof is deferred to an appendix and not verifiable in the main text.
- **Table 1 vs. Table 2 DR.GRPO numbers differ** (53.8 math Acc in Table 1 vs. 55.7 in Table 2 for Qwen-7B). The paper does not explain whether these come from different runs or changed settings, causing confusion.

### Trivial
- The radar chart axes are labeled 0–100, but the actual accuracy values are well below 100 (e.g., 22.6%). This is not incorrect, but it exaggerates visual differences.

## Nice-to-Haves
- Provide results with multiple random seeds and report error bars or confidence intervals for the main comparisons.
- Include a simple guideline or default choice for the scheduling hyperparameters (e.g., μ = training accuracy works reasonably across models).
- Test CANON on one additional metric (e.g., per-step confidence) to strengthen generality claims.

## Novel Insights
The key insight is that by splitting responses into two groups based on a metric and defining both cross-group (inter) and within-group (intra) advantages, the advantage signal can be directionally amplified for that metric while still allowing the opposite trend to be rewarded when it leads to correct answers. This contrasts with previous reward-shaping approaches that impose a fixed direction (higher-is-better or lower-is-better). The paper also shows empirically that inter-group advantage benefits math tasks (where exploiting lower entropy improves accuracy) while intra-group advantage benefits complex logic tasks (where higher entropy exploration matters), and a dynamic schedule can capture both regimes.

## Suggestions
1. **Fix the radar chart data discrepancy.** Either correct the values to match Table 2 or clearly explain any normalization that was applied. Without this correction, the paper’s main claim about CANON-Dynamic is unverifiable.
2. **Add statistical measures.** Report average and standard deviation over at least three training seeds, especially for the small AIME/AMC benchmarks where variance can be high.
3. **Provide a default scheduling rule.** For example, “set μ = 1 − Λ (training accuracy) and clamp to [0,1]” worked well for two of three models. Offering such a simple rule would improve practical usability.

## Score and Decision
The core idea of CANON is sound and the empirical results (apart from the radar chart) show consistent improvements. However, the data inconsistency in Figure 3 is a fatal flaw that misrepresents the main results of Section 5.2. The paper cannot be accepted in its current form. I therefore recommend rejection, with the hope that the authors correct the error and resubmit.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>