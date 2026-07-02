Now I have sufficient calibration data. Let me write the final consolidated review.

## Summary

AdaBoN proposes a two-stage adaptive allocation strategy for Best-of-N inference-time alignment. The method uses a first-stage exploration budget (d per prompt) to estimate reward distributions via KDE with Scott's rule, then greedily allocates the remaining budget across prompts based on estimated marginal gains. The paper evaluates 12 LM-RM pairs across 3 datasets with 50 batches each.

## Strengths

- **Well-motivated problem.** The paper identifies a genuine inefficiency in uniform Best-of-N: easy prompts receive more samples than needed while hard prompts are undersampled. The batch allocation framing (total budget BK distributed across K prompts) and the connection to on-device inference (small K, large per-prompt B) give the setting practical relevance.

- **Clean, theoretically grounded method.** The two-stage design is simple and principled. Proposition 3.1 (concavity and monotonicity of expected max as a function of sample count) correctly justifies the greedy algorithm's optimality on true expectations. KDE with automatic bandwidth selection reduces hyperparameter tuning to a single scalar (d).

- **Broad evaluation scope.** The paper tests 12 LM-RM pairs (4 LMs × 3 RMs) across 3 datasets and 50 prompt batches per setting. This is substantially more comprehensive than the closest prior work (Damani et al., 2024), which evaluates only 1 LM, 1 RM, and 1 batch in its real-valued reward setting. Two thoughtfully defined metrics (BWR and EST) are appropriate for the task.

- **Latency-awareness.** The explicit two-stage design (rather than fully sequential/bandit-based allocation) minimizes latency, which is a practical consideration for deployment.

## Weaknesses

### Major

1. **Exploration budget is 75% of total — not "small", and the paper does not isolate the effect of adaptation.** The abstract and contribution list describe the exploration budget as "small" (lines 9, 28), but the main experiments use d = 0.75B = 90 out of 120 (line 215). The paper only sweeps d ∈ {0.60B, 0.70B, 0.75B, 0.80B} (line 242), never testing smaller proportions. Since 75% of the budget is spent before any adaptation occurs, the method is closer to "mostly uniform allocation with a modest adaptive tail." Critically, there is no ablation comparing AdaBoN against a uniform allocation with N = d (i.e., stopping after the exploration stage). Without this, it is unclear whether the gains come from the adaptive allocation of the remaining 25% or simply from the first-stage allocation being already close to the full budget. The motivating Bernoulli example (Section 2.3) uses d = 0.4B (10 out of 25), illustrating adaptivity in a regime that the experiments never evaluate, which further highlights this gap.

2. **No comparison against any adaptive baseline.** AdaBoN is compared only against uniform allocation. There is no comparison against a simple heuristic (e.g., allocate remaining budget proportional to per-prompt reward variance from exploration), a random allocation with the same total budget, or any bandit-based allocation. The paper explains why it cannot compare with Damani et al. (2024) — no available implementation and prohibitive training cost (line 188) — which is reasonable for that specific method. However, the absence of *any* adaptive baseline means the paper shows that *some* adaptive scheme beats uniform, but cannot distinguish whether its specific design choices (KDE estimation, greedy allocation on estimated marginal gains) are important or whether a much simpler heuristic would achieve similar results. This weakens the core claim that AdaBoN is an effective *adaptive* strategy, not just evidence that uniform allocation can be improved upon.

### Minor

3. **Scott's bandwidth rule is stated with an incorrect formula.** Line 150 states h = σ̂ d^{1/5}. The standard Scott's rule for 1D data uses a negative exponent: h ≈ σ̂ · n^{-1/5} (or with a 1.06 constant factor). The positive exponent causes bandwidth to *increase* with sample size rather than decrease — a factor-of-6 difference when d = 90. If this is only a typo in the paper and the implementation used the correct formula, the paper should state this explicitly. If the implementation matches the formula as written, the impact on Monte Carlo estimates of V_{i,j} needs discussion.

4. **Per-batch statistical significance not reported.** With 100 runs per batch, the paper could report how many individual batches have BWR significantly > 0.50 (e.g., via binomial test or confidence intervals). Given that Q1 values for several LM-RM pairs are 0.51–0.54 (Table 1), some batches may not be individually distinguishable from chance. Reporting this would strengthen the aggregate results.

### Trivial

None.

## Nice-to-Haves

- A simple adaptive heuristic baseline (e.g., variance-proportional reallocation of the remaining budget) would substantially strengthen the paper's claims about the value of its specific design choices.
- Quantify the runtime overhead of the Monte Carlo estimation step (m = 1024 samples per V_{i,j} for up to 150 values per prompt on K = 5 prompts), which is asserted to be efficient but not measured.
- Test smaller exploration budgets (d = 0.1B, 0.2B, 0.3B) to map the regime where adaptivity would be most impactful and to validate the "small exploration budget" framing.

## Removed Points

- "BWR measures comparison against a specific uniform draw, not expected uniform allocation" — The BWR definition (Equation 3) is explicitly an expectation over both reward draws and policy randomness; this is technically correct and not a flaw.
- "The paper does not establish that the smoothness observation generalizes beyond 8B-scale models" — Scope creep; the paper explicitly focuses on 8B-scale models and does not claim broader generalization.
- "No discussion of whether effectiveness depends on reward distribution properties" — The paper does discuss this (Qwen-Armo case, left-skewed distributions, Appendix G.1).
- Missing appendix content or broken formatting — Parser artifacts; these exist in the original submission.
- Typos/grammar/style nitpicks — Parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add an ablation comparing AdaBoN (d = 0.75B) against uniform allocation with N = d** (i.e., just the exploration stage). This isolates whether the adaptive second stage contributes meaningful gains or whether the results are driven by the first-stage allocation already being close to the full budget.
2. **Add at least one simple adaptive baseline** (e.g., allocate remaining budget proportional to per-prompt reward variance observed during exploration, or a random allocation with the same total budget).
3. **Correct the Scott's rule formula** and clarify whether the implementation used the correct formula or the one stated.
4. **Test smaller exploration budgets** (d = 0.1B, 0.2B, 0.3B) to validate the method in the regime where adaptivity is most valuable and to align the experiments with the paper's "small exploration budget" framing.
5. **Report per-batch statistical significance** (e.g., fraction of batches where BWR's 95% CI excludes 0.50) to quantify how many individual batches show meaningful improvements.

**Calibration anchors (from deepreview_13k_calibration):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `6qUUgw9bAZ.md` (Damani et al. 2024) | 6.50 | R1 | Directly comparable — same allocation problem, different method. Damani et al. had similar baseline weaknesses but not the exploration budget issue. AdaBoN has broader evaluation but weaker evidence of adaptation's value. |
| `77gQUdQhE7.md` (Inference-Aware BoN) | 5.67 | R1 | BoN-related but different problem (fine-tuning vs. allocation). AdaBoN has broader evaluation but similar evidence gaps. |
| `8sSqNntaMr.md` (RouteLLM) | 6.33 | R1 | Adaptive allocation for LM routing. Similar baseline weaknesses. AdaBoN is less mature in comparison. |
| `7igPXQFupX.md` (CoTFormer) | 5.75 | R1 | Budget-adaptive computation. Accepted despite concerns about insufficient evidence. AdaBoN has comparable strengths and similar gaps. |
| `am5Z8dXoaV.md` (LazyLLM) | 5.00 (Reject) | R1 | Inference efficiency via token pruning. AdaBoN has broader evaluation and cleaner theory but similar evidence gaps. |
| `n7iwmPacDt.md` (Polybasic Spec Decoding) | 3.00 (Reject) | R1 | LLM inference efficiency. AdaBoN is clearly stronger — broader evaluation, real theory, practical framing. |

**Round 1 bracket:** 4.0 – 6.5 (AdaBoN is clearly stronger than low-3.x papers but has significant evidence gaps that prevent it from reaching the 6-7 range of the Damani et al. paper).

**Final score determination:** AdaBoN's core method is clean and principled, its evaluation is broad, and the problem is well-motivated. However, the two major weaknesses — (1) the 75% exploration budget with no ablation isolating adaptation, and (2) the absence of any adaptive baseline comparison — meaningfully undermine the central claim. The paper is closest in character to CoTFormer (5.75, accepted) but with slightly stronger gaps, and weaker than Damani et al. (6.50, accepted) which had similar baseline issues but not the exploration budget framing problem. This places AdaBoN in the lower half of the borderline-accept range.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>