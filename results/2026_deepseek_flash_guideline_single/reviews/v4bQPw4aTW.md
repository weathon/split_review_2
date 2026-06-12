## Summary

This paper proposes AdaBoN, a two-stage adaptive Best-of-N sampling strategy for allocating inference compute across a batch of prompts. In the first stage, a uniform exploration budget d is used to sample responses per prompt and estimate reward distributions via Gaussian KDE. In the second stage, Monte Carlo sampling from the KDEs estimates marginal gains, and a greedy algorithm allocates the remaining budget to maximize cumulative max reward. Evaluation spans 12 LM-RM pairs across 3 datasets with 50 batches per setting.

## Strengths

1. **Clean, practical problem formulation (Sections 1, 2).** The inference allocation problem — given a batch of prompts and a fixed total query budget, how to allocate per-prompt sample counts adaptively — is well-motivated. The focus on latency (two-stage design enabling parallelization) is a genuinely practical design constraint the paper takes seriously from the outset.

2. **Genuinely simple method with clear description (Section 3, Algorithms 1–2).** AdaBoN is well-explained and implementable: sample d per prompt, estimate reward distributions via KDE, compute marginal gains via Monte Carlo from the KDE, then greedily allocate the remaining budget. Gaussian KDE with Scott's rule means exactly one tunable hyperparameter (d).

3. **Comprehensive empirical coverage for the uniform baseline.** The paper evaluates 4 LMs × 3 RMs = 12 pairs across 3 datasets with 50 distinct batches per setting, varying both batch size K and per-prompt budget B. This is significantly broader than the closest prior work (Damani et al., 2024), which evaluated only 1 LM, 1 RM, and 1 batch for the real-valued reward setting.

4. **Honest limitations section (Section 5).** The paper identifies three concrete limitations: reliance on KDE for distribution estimation, lack of dynamic refinement during allocation, and the requirement for batched prompts.

## Weaknesses

### Major

1. **No experimental comparison against any existing adaptive method.** The paper only compares against uniform (non-adaptive) allocation and against itself with different hyperparameter choices. The closest prior work (Damani et al., 2024) addresses the same allocation problem, but the paper does not compare against it experimentally. The stated reasons — no public implementation, computationally prohibitive to reimplement (216,000 MLPs) — are understandable but do not change the fact that there is no comparison against ANY other adaptive allocation strategy, not even a simple heuristic. A trivial baseline such as "allocate more samples to prompts whose first d samples have higher variance" or "allocate more samples to prompts with higher observed max reward" would clarify whether the KDE+greedy machinery adds value over obvious heuristics. Without this, it is impossible to tell whether the gains come from the specific AdaBoN design or from *any reasonable adaptive allocation*.

### Minor

2. **The exploration budget consumes 75% of total compute, with no testing at lower ratios.** AdaBoN sets d = 0.75B, meaning 75% of the total budget is spent uniformly (same as the baseline) and only the remaining 25% is allocated adaptively. The paper varies d only in {0.60B, 0.70B, 0.75B, 0.80B} — all above 0.60B. Without testing d=0.5B or lower, we do not know whether the method's success depends on the generous exploration budget or whether it would work with less. The finding that BWR increases with K is partly a consequence of the fact that (B-d)K grows with K, giving the greedy algorithm more adaptive budget to work with.

3. **BWR discards effect size; expected cumulative reward is not reported.** The BWR metric measures only the probability of beating uniform, not the margin. A BWR of 0.58 means AdaBoN beats uniform roughly 58% of the time and loses 42% of the time. The paper never reports the expected cumulative max reward directly (Equation 1), which would show the magnitude of improvement. The EST metric partially addresses this but is an indirect measure.

4. **No analysis of computational overhead.** The method requires fitting KDE per prompt and Monte Carlo sampling (m=1024) to estimate marginal values. The paper should report wall-clock time or inference overhead of this computation relative to the actual LM calls.

5. **No investigation of when AdaBoN fails.** BWRs are above 0.50 on average, but the paper does not analyze the batches where BWR < 0.50 (e.g., 24% of batches for Gemma-Mistral per Table 2b). Understanding what characterizes these failure cases would strengthen the paper.

6. **Chain of approximations with limited error analysis.** The method involves: (1) d samples from the true distribution → (2) KDE approximation → (3) Monte Carlo sampling from KDE to estimate marginal values → (4) greedy allocation on estimated values. Proposition 3.1 guarantees concavity for the *true* f(n), and Federgruen & Groenevelt guarantee greedy optimality on *true* V values, but the paper runs greedy on *estimated* values. The paper acknowledges this ("it still serves as an efficient heuristic") but provides no analysis of how estimation error propagates.

### Trivial

None.

## Nice-to-Haves

- Test a simple heuristic adaptive baseline (e.g., allocate remaining budget proportional to variance or mean reward after exploration) to clarify whether the KDE+greedy machinery is needed.
- Test AdaBoN at smaller d/B ratios (e.g., d=0.4B, d=0.5B) to demonstrate robustness of the adaptive component.
- Report expected cumulative max reward alongside BWR.
- Analyze batches where BWR < 0.50 to characterize failure modes.
- Report wall-clock overhead of the KDE+MC+greedy computation.

## Removed Points

These points from the harsh critic input were removed with brief justification:

- **"Abstract framing elides the fact that 75% of budget is spent uniformly"** — Already covered by Minor Weakness #2 (d/B exploration). The abstract accurately describes the two-stage design.
- **"Method is better described as 'uniform allocation with a 25% adaptive top-up'"** — Framing preference; the paper is transparent about the two-stage design.
- **"BWR increasing with K is 'nearly a tautology'"** — Overstated. The relationship is expected given the design, but presenting it as an empirical finding is standard practice.
- **"On-device inference motivation is not validated"** — Scope creep. The paper mentions this as motivation but does not claim to validate it empirically.
- **"Bernoulli example uses binary rewards, not continuous"** — The example is illustrative.
- **"Figure 1 only shows 3 histograms from 1 pair"** — Paper references Appendix F for additional histograms, which were stripped by the parser.
- **"EST result ~150 vs B=120 is 'suspiciously convenient'"** — Speculative; not grounded in any evidence of data manipulation.
- **"Damani et al. claim is not verified"** — It is a citation of another paper's findings; this is standard academic practice.
- **Formatting/appendix-deferred content criticisms** — Parser artifacts, not author errors.
- **"No testing of whether KDE is necessary"** — Already covered by the missing adaptive baseline major weakness.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's framing: a clean, well-executed empirical study on a practical problem, whose main gap is the absence of any comparison against an adaptive baseline, which limits assessment of whether the specific AdaBoN design is necessary or merely sufficient.

## Suggestions

1. Add at least one simple heuristic adaptive baseline (e.g., allocate remaining budget proportional to observed variance or mean reward after the exploration phase).
2. Test AdaBoN at smaller d/B ratios (e.g., d=0.4B, d=0.5B) to demonstrate robustness of the adaptive component.
3. Report expected cumulative max reward directly alongside BWR to give readers effect size information.
4. Include a brief analysis of failure cases (batches where BWR < 0.50).
5. Report the wall-clock overhead of the KDE+MC+greedy computation relative to LM inference calls.

## Score and Decision

**Calibration anchors (retrieved across rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6qUUgw9bAZ.md (Damani et al. - "Learning How Hard to Think") | 6.50 | 1 & 2 | Most directly comparable paper; same problem. AdaBoN has broader evaluation (12 LM-RM pairs vs 1) but lacks ANY adaptive baseline comparison (Damani at least had best-of-k and random baselines). |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/77gQUdQhE7.md ("Inference-Aware Fine-Tuning for Best-of-N") | 5.67 | 1 & 2 | Different angle (fine-tuning, not allocation). Narrower evaluation (1 model, 1 dataset). AdaBoN has stronger evaluation breadth. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0xUEBQV54B.md ("Large Language Monkeys") | 5.00 | 1 & 2 | About scaling sampling, not adaptive allocation. Criticized for trivial findings. AdaBoN has more specific, non-trivial contribution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VNckp7JEHn.md ("Inference Scaling Laws") | 5.75 | 2 | About compute-optimal inference configurations. Broader scope but less specific contribution. |

**Round 1 bracket:** 5.5–6.5
**Narrowing (Round 2):** Anchored by Damani et al. at 6.50 and Inference-Aware Fine-Tuning at 5.67. AdaBoN is weaker than Damani et al. due to the absence of any adaptive baseline comparison, but stronger than the inference-aware fine-tuning paper in evaluation breadth and practical relevance.

**Final score:** 6.0

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>