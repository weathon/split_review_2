Now I have strong calibration. Let me write the final review.

## Summary

This paper presents PLAGUE, a plug-and-play framework for multi-turn LLM jailbreak attacks that decomposes the attack into three phases (Planner → Primer → Finisher) augmented with a lifelong-learning memory component. The framework can incorporate existing attacks (GOAT, Crescendo, ActorBreaker) as drop-in modules. Evaluations on frontier models (o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3-70B) show strong headline ASR numbers, including 81.4% SRE on o3 and 97.8% on Deepseek-R1.

## Strengths

- **Architectural novelty.** The three-phase decomposition (Planner → Primer → Finisher) with lifelong learning is a genuine design contribution. Disentangling plan initialization, gradual context escalation, and final-goal exploitation is a more principled decomposition than prior work provides, and the plug-and-play claim is supported by showing that different Finishers (GOAT, Crescendo) can be swapped in (§3.3–3.5, Tables 3–4). [weight: +6.66]
- **Strong headline results.** In Table 2, PLAGUE achieves 81.4% SRE on OpenAI o3 and 97.8% on Deepseek-R1, substantially exceeding prior published numbers on these highly safety-aligned models. [weight: +5.34]
- **Clean ablation path.** Table 3 shows monotonic improvement as each component (BT, R, P, RSS) is added to the GOAT baseline, giving a clear picture of what each piece contributes. [weight: +4.14]
- **Per-model component analysis.** §5.1 shows that different components matter for different models (reflection most important for o3, backtracking for Claude), providing actionable insights for red-teamers. [weight: +4.78]
- **Efficiency accounting.** Table 5 tracks Target, Evaluator, and Planner LLM calls, showing PLAGUE's total call count is comparable to or lower than Crescendo and ActorBreaker, addressing the concern that a more complex framework would be prohibitively expensive. [weight: +3.19]

## Weaknesses

### Major

- **Diversity metric is undefined in the main text.** The paper claims "diversity improves by 15% (Figure 3)" but never defines the diversity metric (embedding diversity? Jaccard similarity of plans? action-type diversity?). A 15% improvement claim is uninterpretable without knowing what is being measured. Since diversity is a stated design goal (§1: "sample adaptively with diversity"), this is a significant methodological gap. [weight: -6.41]
- **Baseline modifications likely disadvantage competitors without evidence.** GOAT is run "without history enabled for the Attacker" and the paper claims the impact is "negligible" but provides no A/B comparison or ablation to support this (§4). Crescendo has "explicit backtracking counts" removed (§4), which is part of its mechanism for recovering from dead ends. Both modifications consistently reduce expected baseline performance. Without empirical evidence that these changes are harmless, the claimed improvement margins (32–40%) may be inflated. [weight: -2.10]
- **32.14% improvement number is attributed to the wrong baseline.** The paper claims to "outperform the previous best — GOAT by a factor of 32.14%" (§5.1). From Table 2, GOAT SRE on o3 is 0.587 and PLAGUE SRE is 0.814, yielding (0.814−0.587)/0.587 = 38.7%. The 32.14% figure actually corresponds to improvement over **ActorBreaker's** SRE of 0.616: (0.814−0.616)/0.616 = 32.14%. The claimed baseline is incorrect. [weight: -2.92]
- **Lifelong learning contribution has thin empirical support.** While RSS (the lifelong-learning component) shows improvement in Table 3 (+5.3% SRE on o3, +7.9% on Claude), no learning trajectory is shown — how ASR improves as the memory bank grows from 0 to N stored strategies. The lifelong-learning claim is in the title and highlighted in Table 1 as the only method with this feature, but without a trajectory, the evidence reduces to "in-context examples of past successes help modestly," which prior work (AutoDAN-Turbo) already demonstrates. [weight: -4.52]

### Minor

- **No variance reporting for main results.** Table 2 reports single numbers with no standard deviations, confidence intervals, or error bars. The paper states scores are "averaged over three runs for robustness" (§4) but never shows the variance. Given the stochastic nature of jailbreak evaluations (sampling noise in both attacker and target LLMs), this makes it hard to assess whether margins over baselines are statistically reliable. [weight: -1.87]
- **ASR@K treatment across baselines is not fully transparent.** The paper uses ASR@2 (best-of-2 selection) for PLAGUE and explicitly matches this for ActorBreaker (K=2), but it is not clear whether GOAT and Crescendo receive the same best-of-2 selection (§4 describes GOAT stopping early if a high rubric score is obtained, and Crescendo following its official implementation). If baselines do not get the same selection procedure, the comparison is structurally asymmetric. [weight: -1.48]

## Nice-to-Haves

- Provide A/B comparison for GOAT with/without history and Crescendo with/without backtracking to validate that baseline modifications are harmless.
- Include standard deviations or 95% CIs for all main results across the three runs.
- Show the lifelong learning trajectory — plot ASR vs. number of stored strategies in the memory bank.
- Report ASR@1 alongside ASR@2 for all methods to enable direct comparison with prior published results.
- Define the diversity metric explicitly and report it in a quantitative table.
- Test with a weaker attacker model (e.g., Llama-3-70B) to probe whether the framework's benefits generalize beyond using Deepseek-R1 as the attacker.

## Removed Points

These points are flagged to be removed; treat them with caution:

- "LLM-as-judge without human validation" — removed because this is standard practice in the jailbreak literature; the paper uses StrongREJECT, a well-established evaluation framework, and the field widely accepts automated evaluation.
- "ActorBreaker limited to K=2 compresses its performance" — removed because the paper explicitly matches this to PLAGUE's K=2 for a fair comparison; the claim that this "likely compresses its performance" is speculative.
- "Lifelong learning novelty questioned relative to AutoDAN-Turbo" — removed because the paper addresses this distinction in §2.3, noting that AutoDAN-Turbo is a single-turn method whose learned strategies show minimal improvement.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the 32.14% claim: either attribute it to improvement over ActorBreaker's SRE (which the math supports) or recalculate against GOAT (38.7%).
2. Run all baselines at their full original configurations and show those numbers alongside the modified versions. If the modifications are truly harmless, this directly validates the claim.
3. Define the diversity metric and present it quantitatively in a table rather than only in a figure whose caption is inaccessible.
4. Show the learning curve of ASR over accumulated strategies in the lifelong memory bank to substantiate the title claim.

## Score and Decision

**Score:** 6.0
**Decision:** Borderline Accept (Reject → Accept)

### Calibration Anchors

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| 5kMwiMnUip (NEMESIS) | 1.40 | R1 | No | Far below — that paper is a simple prompt collection with no experimental rigor. |
| KyKTjRtyNG (Incremental Exploits) | 3.00 | R1 | Yes | Below — that paper had severe novelty (-8.19) and dataset (-13.76) issues; PLAGUE has much stronger architectural contribution (+6.66 vs +5.83 max). |
| kvvvUPDAPt (Derail Yourself) | 5.33 | R1 | Yes | Below — that paper had weak technical contribution (-7.87) and missing multi-turn baselines (-6.69); PLAGUE's positives are stronger and negatives less severe. |
| fFtmpqLFvw (Multi-Turn Red Teaming) | 5.75 | R1 | Yes | Slightly below — PLAGUE has stronger positives (+6.66 vs +4.47) but more accumulated evaluation concerns. |
| jCDF7G3LpF (MAB Context Switching) | 6.25 | R2 | Yes | Comparable — that paper had severe missing-baseline issues (-8.35, -7.64) and poor readability (-11.07); PLAGUE has stronger positives but more moderate negatives. |
| hXA8wqRdyV (Simple Adaptive Attacks) | 6.14 | R2 | Yes | Comparable — that paper had very severe novelty concerns (-9.78, -9.30) while PLAGUE's negatives are more moderate but more numerous. |
| bhK7U37VW8 (AutoDAN-Turbo) | 7.17 | R2 | Yes | Above — that paper had stronger positives (+7.51, +6.19) and milder negatives, and was published at ICLR. PLAGUE has more concrete evaluation gaps. |

### Calibration Narrative

Round 1 bracketing placed PLAGUE between 5.5 and 7.0 based on comparison to KyKTjRtyNG (3.00), kvvvUPDAPt (5.33), fFtmpqLFvw (5.75), and 4KqkizXgXU (8.00). Round 2 narrowing compared against jCDF7G3LpF (6.25), hXA8wqRdyV (6.14), and bhK7U37VW8 (7.17).

Compared to bhK7U37VW8 (AutoDAN-Turbo, 7.17), PLAGUE has a comparable positive-weight profile (max +6.66 vs +7.51) but more numerous and concrete verification-grounded weaknesses: the diversity metric is undefined (-6.41 vs that paper's mild scalability concern -8.12 which was speculative), the lifelong learning evidence is thin for a title claim (-4.52), and there is a factual error in the reported improvement figures (-2.92). Compared to jCDF7G3LpF (6.25) and hXA8wqRdyV (6.14), PLAGUE's weaknesses are more distributed but less severe in magnitude (-6.41 max vs -9.78, -11.07). The paper's architectural contribution (+6.66) is genuinely strong and the ablation is clean (+4.14), but the evaluation issues — particularly the undefined diversity metric and baseline modifications — prevent it from reaching the 7+ tier. A score of 6.0 reflects a paper with real contributions that require non-trivial revisions to fully substantiate its claims.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>