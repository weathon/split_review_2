## Summary

AdaBoN proposes a two-stage adaptive allocation strategy for Best-of-N sampling across a batch of prompts. In Stage 1, a fixed exploration budget *d* per prompt collects initial reward samples, from which Gaussian KDE estimates the reward distribution for each prompt. In Stage 2, these estimates are used to compute expected marginal gains, and the remaining budget is allocated greedily using Algorithm 1. Experiments across 12 LM-RM pairs, 3 datasets, and 50 batches per setting show that AdaBoN outperforms uniform allocation at the same budget and remains competitive against uniform allocations with ~20% larger budgets.

## Strengths

1. **Well-motivated problem formulation.** The paper formalizes prompt-adaptive Best-of-N as a resource allocation problem (Section 2.3) and clearly distinguishes non-adaptive (minimax optimal uniform) from adaptive policies. This framing is a clean conceptual contribution that will be useful to the community.

2. **Latency-aware design is principled.** The two-stage architecture (parallel exploration, then one-shot commitment) requires only two serial calls to the LM, making it practical for deployment where fully sequential bandit approaches would incur prohibitive latency. This is a genuine engineering virtue over methods like Manvi et al. (2024).

3. **Proposition 3.1 provides formal grounding.** The concavity and monotonicity guarantee for the expected-max function (proved in Appendix E) justifies the optimality of the greedy procedure on true V-vectors. While the paper is upfront that the procedure is a heuristic when run on *estimated* vectors, the theory provides a clear connection to known optimal algorithms.

4. **Broad empirical coverage.** The evaluation spans 12 LM-RM pairs, 3 datasets, 50 batches per setting, and multiple batch sizes and budgets (B ∈ {80, 100, 120, 140, 160}, K ∈ {3, 5, 10, 15, 20}). This is substantially broader than the closest prior work (Damani et al., 2024), which reports results for 1 LM, 1 RM, and 1 batch.

5. **Informative evaluation metrics.** The Expected Survival Time (EST, Equation 5) translates win rates into a concrete measure of computational savings. The finding that AdaBoN (budget 120) is competitive with uniform allocation at budget ~150 (Table 2a, ESTs ~148–156) is the paper's most practically compelling result.

## Weaknesses

### Major

1. **No comparison against any adaptive baseline.** AdaBoN is compared only against uniform (non-adaptive) allocation. The paper justifies not comparing to Damani et al. (2024) due to the prohibitive cost of training 216,000 MLPs (lines 186–188), which is a reasonable excuse for that specific comparison. However, there is no comparison against *any* adaptive heuristic — not even simple ones that would require no additional LM calls. For example: (i) after the exploration phase, allocate all remaining budget to the prompt with the highest observed max reward; (ii) allocate remaining budget proportionally to the sample variance of each prompt's observed rewards; (iii) a random allocation over the remaining budget. Without such baselines, the reader cannot assess whether the specific KDE+greedy design drives the gains, or whether any reasonable adaptive strategy would achieve similar results. This weakens the paper's claim that its *specific design choices* matter. The paper is still a useful demonstration that *some* adaptive strategy beats uniform, but it stops short of validating the method as designed.

### Minor

2. **The exploration budget d = 0.75B leaves limited room for adaptivity.** With d = 0.75B, B = 120, and K = 5, each prompt receives 90 exploration samples before any adaptive decision, meaning 450/600 = 75% of total LM calls are allocated uniformly. The method is better described as "75% uniform with a 25% adaptive adjustment." The paper frames the method as "prompt-adaptive" but spends most of its budget non-adaptively. The paper does not report a breakdown of how much of the gain comes from the exploration phase alone vs. the adaptive phase, which would directly quantify adaptivity's contribution. This is not a fatal issue — the paper is transparent about d — but it should be discussed more explicitly.

3. **The hyperparameter d is tested only in a narrow range (0.60B–0.80B).** All four tested values are large fractions of the budget; the smallest is 60% of B. No experiments are reported for d = 0.1B, 0.25B, or 0.5B, so we cannot evaluate whether the two-stage design works when the adaptive component has more room to operate. Testing smaller d values (which require no additional LM calls, only re-running the allocation on existing exploration data) would substantially strengthen the paper's claims about adaptivity.

4. **Claim that reward distributions are "smooth and easy to learn" is supported only by visual inspection.** Contribution (1) states this as a finding, but the evidence consists of histograms (Figure 1, Appendix F). No quantitative goodness-of-fit evaluation is provided. The comparison with parametric alternatives (Table 16 in Appendix K.3) shows KDE outperforms Gaussian and Skew-Normal MLE, but this only establishes relative superiority, not absolute accuracy. A direct comparison between allocations produced from estimated distributions and those from true distributions (approximated with very large samples) would substantiate the claim.

### Trivial

5. **EST cap at 2B is mentioned but not justified.** The paper states it caps Equation 5's sum at 2B (line 215) but does not explain why or discuss whether this affects results. Since all ESTs (~148–153) are well below 2B = 240, the cap likely does not affect findings, but stating this explicitly would improve clarity.

## Nice-to-Haves

- Report the breakdown of cumulative max reward: from the d=90 exploration phase alone, from the full AdaBoN allocation, and from uniform at B=120. This would directly show how much the adaptive component contributes over the exploration phase.
- Report standard errors alongside the [Q1, Q3] intervals in Tables 1 and 2. With 100 runs per batch and 50 batches, these are computable and would strengthen the quantitative assessment.

## Removed Points

- **Bernoulli example is a poor proxy for real distributions.** REMOVED: The paper presents this as a pedagogical motivating example (Section 2.3, lines 84–86), not as evidence that real distributions behave the same way. It is standard practice to use simple illustrative examples.
- **Missing computational cost of Monte Carlo estimation.** REMOVED: The paper reports m = 1024 Monte Carlo samples (line 215). The computational cost of 768,000 KDE samples is negligible relative to LM calls. This is a trivial implementation detail.
- **Batch construction procedure could introduce selection bias.** REMOVED: The paper explains batches are sampled without replacement, with distinct prompts per batch size. This is a standard experimental design choice; the concern is speculative.
- **Default decoding strategy should be discussed.** REMOVED: The paper states it uses "the standard generation function from Hugging Face" and "default decoding strategy" (line 215). This is properly disclosed for replicability.
- **Strength about problem importance.** REMOVED: Generic (many papers address important problems). The remaining strengths are specific and evidence-grounded.
- **Failure of AdaBoN on some batches is not deeply analyzed.** REMOVED FROM WEAKNESSES: The paper acknowledges this and Appendix G.1 discusses the left-skewed distributions for the Qwen-Armo pair. This is adequate.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add at least one simple adaptive baseline — e.g., after exploration, allocate all remaining budget to the prompt with the highest observed max reward, or allocate proportionally to sample variance. These require no additional LM calls and would establish whether the KDE+greedy machinery is necessary.
2. Test smaller d values (e.g., d = 0.1B, 0.25B, 0.5B) using existing exploration data to evaluate the method when adaptivity has more budget.
3. Report the breakdown of cumulative max reward across phases to quantify the adaptive contribution.
4. Strengthen the "smooth and easy to learn" claim with a quantitative comparison of allocations from estimated vs. true distributions on a held-out set with large samples.

## Score and Decision

**Round 1 bracket:** 5.0–6.0.

**Anchors consulted:**

| Paper | Score | Round | Comparison |
|-------|-------|-------|------------|
| Learning How Hard to Think (Damani et al.) | 6.50 | R1 (5.5–7.5) | Same problem, trained predictor. More sophisticated method but narrower eval (1 LM/RM/batch). AdaBoN has broader eval but no adaptive baselines. AdaBoN is slightly weaker. |
| Large Language Monkeys | 5.00 | R1 (3.5–5.5) | Empirical scaling study, rejected. AdaBoN has a stronger contribution (actual method + theory). |
| Towards Optimal Multi-draft Speculative Decoding | 5.25 | R1 (3.5–5.5) | Theoretical + empirical, accepted. Similar quality level; AdaBoN has broader experiments but weaker baselines. |
| Inference Scaling Laws | 5.75 | R1 (5.5–7.5) | Empirical analysis of compute-optimal inference, accepted. AdaBoN is comparable in quality. |

**Final score determination:** The paper has a clear, practical contribution and solid empirical evidence for its core claim (beats uniform). The major weakness — no adaptive baseline comparison — prevents full validation of the method's specific design but does not invalidate the main result. The paper is stronger than rejected papers in the 3–5 range but weaker than top papers in the 7+ range. Calibrated against directly comparable anchors, the paper sits near the lower end of the accept range.

<score>5.5</score>
MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>