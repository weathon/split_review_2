Now I have all the information I need. Let me compile the final review.

## Summary

This paper proposes AdaBoN, a prompt-adaptive allocation strategy for Best-of-N sampling that distributes a fixed inference budget across a batch of prompts based on estimated reward distributions. The method uses a two-stage design: an initial exploration phase (75% of budget) samples uniformly from each prompt to estimate reward distributions via KDE, then greedily allocates remaining budget based on estimated marginal gains. The concavity of the max-of-samples expectation justifies greedy allocation. Experiments across 12 LM-RM pairs, 3 datasets, and 50 batches show AdaBoN outperforms uniform allocation with modest win rates.

## Strengths

- **Genuinely practical and well-motivated problem.** The lack of adaptivity in uniform Best-of-N allocation is a real inefficiency, and the two-stage design that maintains parallelizability is a thoughtful practical constraint. (weight: +2.93)

- **Clean, intuitive, and model-agnostic method.** AdaBoN requires no retraining for new LM-RM pairs, unlike Damani et al. (2024). The concavity result (Proposition 3.1) provides sound theoretical justification for greedy allocation. (weight: +3.72)

- **Broad empirical coverage.** The evaluation spans 12 LM-RM pairs (4 LMs × 3 RMs), 3 datasets, and 50 distinct batches per configuration — substantially broader than prior work (Damani et al., 2024, which used 1 LM, 1 RM, and 1 batch). (weight: +3.84)

- **Well-designed evaluation metrics.** BWR appropriately handles the ordinal nature of RM scores with fair tie-breaking (uniform vs. uniform = 0.50), and EST provides a natural interpretation of computational savings. (weight: +3.10)

- **Model-agnostic nature.** AdaBoN works out-of-the-box for any LM-RM pair without auxiliary training, making it practically deployable. (weight: +3.93)

## Weaknesses

### Fatal
None.

### Major

- **The exploration budget (d=0.75B) consumes 75% of compute, limiting practical significance.** The paper sets d=0.75B, meaning 75% of queries per prompt are allocated uniformly (non-adaptively), and only the remaining 25% are distributed adaptively. The ablation tunes d ∈ {0.60B, 0.70B, 0.75B, 0.80B} and finds 0.75B best — the method needs substantial exploration to work. The EST results (148-156 for B=120) show AdaBoN competes with uniform at only ~23-30% larger budget, consistent with the 25% adaptive fraction. This bounds practical savings and is not acknowledged as a limitation in Section 5. (weight: -1.64)

- **No comparison against any adaptive baseline.** The evaluation exclusively compares against uniform allocation. The paper discusses Damani et al. (2024) but does not compare against it; while the full training cost is prohibitive, a simplified comparison on a single LM-RM pair or budget would have been feasible. More importantly, no simple adaptive heuristic is tested (e.g., allocate remaining budget to prompts with highest current max reward, or continue sampling until max reward plateaus). Without such baselines, it is unclear whether the KDE-based marginal gain estimation drives improvements or whether any reasonable adaptive heuristic would achieve similar gains. (weight: -4.71)

### Minor

- **Effect sizes are modest and no statistical significance testing is reported.** Median BWRs range from 0.54 to 0.62, with some IQR lower bounds dipping to 0.51 (Table 1, Qwen-Armo), meaning 25% of batches barely beat uniform. The paper uses "significantly" colloquially (line 217) without p-values, confidence intervals, or sign tests. The "percent batches with BWR > 0.50" metric (76-100%) lacks error bars. Given 100 runs × 50 batches, variance is expected and significance is not obvious. (weight: -2.67)

- **EST values appear to primarily reflect the exploration budget fraction rather than method cleverness.** ESTs cluster tightly at 148-156 (B=120), i.e., ~23-30% above baseline, which directly mirrors the 25% adaptive fraction. The paper does not disentangle whether this reflects the method's allocation strategy or is a mechanical consequence of the fixed exploration/adaptive split. Reporting EST for a simpler baseline (e.g., randomly reallocating the adaptive portion) would clarify. (weight: -1.04)

### Trivial
None.

## Nice-to-Haves

- **Analyze sensitivity to smaller exploration budgets.** If d=0.25B or d=0.5B still yields BWR > 0.50, practical significance increases substantially. If performance collapses, this is itself an important finding.
- **Add at least one simple adaptive baseline** — e.g., allocate exploration uniformly, then allocate all remaining budget to the prompt with the lowest current max reward.
- **Report standard errors or confidence intervals** for aggregate BWR across 50 batches, and consider a sign test for whether median BWR exceeds 0.50.

## Removed Points

These points were removed during filtering; treat with caution.

1. **Bernoulli example is misleading** — The critic claimed the Bernoulli illustration (p=0.95 vs 0.05) overstates adaptivity benefits because real distributions are Gaussian and overlapping. REMOVED: this is a simple illustrative example to build intuition, not a claim about real distributions. The paper does not assert real distributions are Bernoulli-like.

2. **Smoothness claim based on only 3 histograms** — REMOVED: the paper references Appendix F for additional histograms across all LM-RM pairs and explicitly states the qualitative observation applies to all pairs considered.

3. **On-device motivation mismatch** — REMOVED: the contribution does not depend on this specific motivation.

4. **Missing KDE estimation quality analysis** — REMOVED: the paper compares KDE against parametric fits in Appendix K.3 and notes KDE works better. Additional diagnostics would be nice-to-have but are not necessary.

5. **Style/formatting/grammar nitpicks** — REMOVED per hard rules.

## Novel Insights

None beyond the paper's own contributions — the insights from the reviews (the 75% exploration budget dominating results, the absence of adaptive baselines) are observations the paper should address rather than novel findings about the field.

## Suggestions

1. **Acknowledge the exploration budget limitation in the main paper.** If the method needs 75% exploration to work, this should be honestly discussed as a bound on practical savings.
2. **Add a simple heuristic baseline** — e.g., after uniform exploration, allocate remaining budget greedily to prompts with the highest current max reward. This would isolate whether the KDE-based marginal gain estimation is the source of improvement.
3. **Report statistical tests** — confidence intervals for BWR across batches, or a sign test for whether median BWR > 0.50.

## Score and Decision

**Score calibration.** My round-1 bracket was [4.5, 5.5].

**Anchors retrieved:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| Damani et al. "Learning How Hard to Think" (6qUUgw9bAZ.md) | 6.50 | R1 | Yes | More comprehensive framework to the same problem; AdaBoN is simpler but has weaker baselines and 75% exploration issue |
| Inference-Aware Fine-Tuning for BoN (77gQUdQhE7.md) | 5.67 | R1 | Yes | Similar baseline weakness but narrower evaluation; AdaBoN has broader LM-RM coverage |
| Inference Scaling Laws (VNckp7JEHn.md) | 5.75 | R2 | Yes | Stronger theoretical framing but limited to math tasks; AdaBoN has broader domain coverage |
| Cost-Effective Online Multi-LLM Selection (JLDAWbzTUg.md) | 5.50 | R2 | Yes | Interesting problem but toy reward models; AdaBoN uses real LM-RM pairs |
| Large Language Monkeys (0xUEBQV54B.md) | 5.00 | R1 | Yes | Strong empirical work but trivial core claim; AdaBoN has clearer novelty |
| Inference-Time LLM Alignment (1Uem0nAWK0.md) | 4.25 | R2 | Yes | Novelty concerns (-8.96 weight); AdaBoN's method is genuinely new |
| Backoff Decoding (Yz7ts36V7A.md) | 3.67 | R1 | Yes | Limited experiments, weak comparison; AdaBoN has much broader evaluation |
| Polybasic Speculative Decoding (n7iwmPacDt.md) | 3.00 | R1 | No | Less relevant topic |

**Weighted-item comparison.** AdaBoN's strongest weakness (-4.71 for no adaptive baseline) is comparable to Damani et al.'s weak baselines (-4.63) and Inference-Aware Fine-Tuning's experimental concerns (-6.71). However, AdaBoN has an additional structural weakness (75% exploration budget, -1.64) that Damani et al. does not. AdaBoN's strengths (+3.84 for broad evaluation, +3.93 for model-agnostic) are solid but do not compensate for the lack of adaptive baselines and the exploration budget limitation. The paper sits below Damani et al. (6.50) and Inference Scaling Laws (5.75), and is comparable to or slightly above Large Language Monkeys (5.00), placing the final score at 5.0.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>