## Summary

AdaBoN proposes a two-stage adaptive allocation strategy for Best-of-N sampling at inference time. Given a batch of K prompts and a total inference budget, the method first spends a fixed exploration budget (d samples per prompt) to estimate each prompt's reward distribution via Gaussian KDE, then uses a greedy algorithm (grounded by a concavity proof) to allocate the remaining budget adaptively across prompts. The paper evaluates on 12 LM-RM pairs, 3 datasets (AlpacaEval, HH-RLHF, PKU-SafeRLHF), and 50 batches per setting.

## Strengths

1. **Broad and systematic empirical evaluation**: The paper evaluates AdaBoN across all combinations of 4 LMs and 3 RMs, on 3 datasets, with 50 distinct batches per configuration (Sec 4.1). Results are reported with median [Q1, Q3] across batches, providing a nuanced picture. This breadth substantially exceeds that of the closest prior work (Damani et al., 2024), which evaluated a single LM, single RM, and single batch in the real-valued reward setting.

2. **Training-free, black-box approach with concretely quantified cost advantage**: AdaBoN requires no auxiliary model training and works out-of-the-box for any LM-RM pair. The paper quantifies the alternative cost: faithful comparison with Damani et al. would require training thousands of MLPs (Sec 4.2), honestly motivating the practical appeal.

3. **Formal theoretical grounding**: Proposition 3.1 proves that the expected-max function is concave and monotonically increasing for any distribution with finite first moment, directly justifying why the greedy algorithm (Algorithm 1) is optimal when true distributions are known (Sec 3, proof in Appendix E). This is non-trivial and useful.

4. **Robustness evidence for the estimation procedure**: The paper uses automatic bandwidth selection (Scott's rule) and compares against MLE-fitted Gaussian and Skew-Normal alternatives, finding KDE consistently performs best (Sec 3.1, Appendix K.3). The single hyperparameter (exploration budget d) is ablated over a range and a single fixed value (d=0.75B) performs well across settings (Sec 4.3).

5. **Honest discussion of limitations**: The paper explicitly acknowledges limitations including compatibility with discrete RMs, the two-stage vs. bandit trade-off, and the batch-dependent setting (Sec 5). This candor is valuable and rare.

## Weaknesses

### Fatal

None.

### Major

1. **The exploration budget dominates total compute, and the adaptive component's contribution is not isolated.** In the primary evaluation setting (K=5, B=120, d=0.75B), 75% of the total budget (450 out of 600 LM calls) is spent on uniform exploration — every prompt gets 90 samples before any adaptivity begins. Only the remaining 25% (150 calls) is allocated adaptively. The paper does not report the BWR of a "uniform-d" policy (exploration stage only, no second-stage allocation) against the full uniform B=120 baseline. Without this, the contribution of the *adaptive* allocation is conflated with the benefit of the exploration phase itself. The ablation over d ∈ {0.60B, 0.70B, 0.75B, 0.80B} stays in a narrow band near the top; testing with substantially smaller d (e.g., 0.25B, 0.50B) would better characterize the regime where adaptivity actually matters most. This is the paper's most significant limitation.

2. **No empirical comparison with the most closely related prior work (Damani et al., 2024).** The paper gives practical reasons for not comparing (no public implementation, insufficient hyperparameter details, computational cost). While the practical constraints are genuine, even a comparison on a subset of LM-RM pairs (e.g., 1–2 pairs with a single budget value) would help the reader assess whether AdaBoN's simplicity comes at a meaningful performance cost relative to the learned approach, or whether the two methods are similar in their overlapping regime.

### Minor

3. **BWR metric omits magnitude information.** The Batch Win Rate (Eq. 3) measures only the *probability* of exceeding the uniform allocation, not by how much. The paper provides a well-reasoned justification (line 172: RM scores are often meaningful only comparatively under the Bradley-Terry model), and the EST metric partially addresses magnitude. However, reporting the expected cumulative max reward (Eq. 1) alongside BWR would resolve the concern that a BWR > 0.50 could theoretically coexist with lower expected utility (e.g., winning by tiny margins on 58% of runs but losing badly on 42%). The paper would be stronger with both metrics.

4. **No heuristic baseline beyond uniform allocation.** A simple heuristic (e.g., allocate proportional to the variance of rewards observed in the exploration phase, or proportional to the maximum observed reward so far) would help assess whether the KDE + greedy machinery adds value over cheaper alternatives that also use the exploration phase.

### Trivial

5. The MLP count for the Damani et al. comparison is stated as "216,000" but the calculation (12 LM-RM pairs × 3 datasets × 600 values of b) yields 21,600. Both figures are prohibitive, but the authors should correct the arithmetic.

## Nice-to-Haves

- Report the BWR of a "uniform-d" policy (exploration stage only) against the full uniform B=120 baseline.
- Test with smaller exploration budgets (e.g., d=0.25B, 0.50B) to characterize the regime where adaptivity contributes most.
- Add a simple heuristic baseline using exploration-phase statistics (e.g., variance-based allocation).
- Show sensitivity analysis for the Monte Carlo sample size m (currently fixed at 1024 without ablation).
- Report wall-clock runtime of the estimation phase (KDE + Monte Carlo) to clarify overhead.

## Removed Points

- **Greedy optimality violated by Monte Carlo estimation**: The paper explicitly acknowledges this (line 121: "While the greedy procedure may not be optimal when run on the estimated vectors, it still serves as an efficient heuristic"). This is a reasonable acknowledgment, not an oversight. Removed.
- **Concavity proof missing**: The proof is in Appendix E, which was stripped by the PDF parser. The criticism speculates about missing content that exists in the original submission. Removed.
- **"Larger batches provide more reallocation opportunities" comment**: This is a statement about expected behavior, not a weakness. Removed.
- **"Damani et al.'s 'does not observe significant improvements' claim is rhetorical"**: This is an opinion about framing, not a verifiable weakness. Removed.
- **Strength Finder's generic/superficial strengths** (e.g., "the paper addresses an important problem", "the BWR metric choice is careful"): The first is generic; the second conflicts with verified weakness #3 (weakness wins per conflict rule). Removed.

## Novel Insights

The reviews surface an interesting tension: AdaBoN's designed regime (small K, large B) is one where adaptive allocation *should* matter less because each prompt already gets many samples — yet AdaBoN still shows measurable gains (BWRs consistently >0.50, ESTs ~150 for B=120). This suggests that between-prompt variance in reward distributions is meaningful enough that even modest reallocation (25% of budget) yields detectable improvements. This is a genuinely useful empirical finding that supports the method's core thesis. The paper's honesty about its limitations (discrete RMs, two-stage vs. bandit trade-offs, batch-dependent setting) is also noteworthy and rare in this space.

## Suggestions

1. Add a "uniform-d" baseline (exploration phase only, skip second-stage allocation) against the full uniform B=120 baseline to isolate the adaptive component's contribution.
2. Report expected cumulative max reward (Eq. 1) alongside BWR.
3. Correct the MLP count for Damani et al. comparison (21,600, not 216,000).
4. Add at least one simple heuristic baseline using exploration-phase statistics (e.g., allocate proportionally to the variance of initial d samples per prompt).
5. Test with smaller exploration budgets (e.g., d=0.25B, 0.50B) to characterize the efficiency frontier.

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Damani et al. "Learning How Hard to Think" | 6.50 | R1, R2 | Most directly comparable — same problem, learned approach. AdaBoN has broader evaluation, is training-free, but lacks empirical comparison with it. Comparable quality. |
| RouteLLM | 6.33 | R1 | Inference-time routing for cost-performance. AdaBoN is at least as strong technically. |
| RAIN | 6.00 | R1 | Inference-time alignment via self-evaluation. Accepted. AdaBoN is comparable. |
| Inference-Aware Fine-Tuning for BoN | 5.67 | R2 | Training-time method to improve BoN. Accepted despite single-model evaluation. AdaBoN is stronger (broader evaluation, cleaner setup). |
| Inference Scaling Laws | 5.75 | R1 | Empirical analysis of compute-optimal inference. Accepted. Different type of contribution. |
| CARDS (Cascade Reward Sampling) | 5.75 | R2 | Decoding-time alignment. Rejected — unfounded theoretical claims. AdaBoN is stronger (honest limitations, sounder theory). |
| Nudging | 6.00 | R1 | Inference-time token-level alignment. Rejected due to practical utility concerns. AdaBoN is comparable. |
| LASeR | 5.25 | R1 | RM selection with bandits. Rejected — weak baselines. AdaBoN is stronger. |

**Round 1 bracket:** 5.5–6.5. **Narrowing:** The most directly comparable paper (Damani et al., avg 6.50, accepted) addressed the same problem. AdaBoN compares favorably on evaluation breadth and simplicity but has the exploration budget issue and lacks Damani comparison. Other accepted papers in the band (5.67–6.33) confirm AdaBoN sits comfortably in accept territory. The rejected papers in the space had more severe issues (unfounded theoretical claims, very limited evaluation).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>