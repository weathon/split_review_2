## Summary

This paper proposes CARL (Constraint-aware Reward Relabeling), a simple wrapper method for offline safe RL. The core idea is to iteratively relabel rewards with a large negative penalty for state-action pairs whose estimated cost-to-go exceeds a budget κ, transforming the constrained optimization into an unconstrained reward-maximization problem. CARL requires no Lagrangian multipliers, no constrained optimization loops, and can be wrapped around any batch-update offline RL algorithm with minimal modification. Empirical results on the DSRL benchmark demonstrate strong performance, particularly in the tight-budget regime, including the ability to learn safe policies from datasets containing only unsafe trajectories.

## Strengths

1. **Genuinely simple and elegant formulation.** The reformulation of state-action-wise safety constraints into an unconstrained reward-relabeling problem (Equations 2–3) is conceptually clean. The method requires no Lagrangian multipliers, constrained optimization loops, or auxiliary safety modules — it is a wrapper applicable to any batch-update offline RL algorithm.

2. **Strong empirical results in the tight-budget regime.** On the 8 Bullet Gym tasks (κ=5), CARL is the *only* method that satisfies the safety constraint on every task (Table 1). On Safety Gym tasks (κ=10), CARL is safe on 8/11 tasks, which is the best consistency among all methods tested.

3. **Compelling unsafe-trajectories ablation (Section 6.2, Figure 3).** CARL can learn safe policies from datasets containing *only* unsafe trajectories. This non-trivial demonstration shows that the reward relabeling mechanism actively redirects behavior away from unsafe regions rather than simply amplifying existing safe patterns in the data.

4. **No additional hyperparameters beyond the backbone algorithm.** The M=K=1 schedule eliminates the oscillation problem shown in Figure 1 without introducing extra knobs.

## Weaknesses

### Major

1. **Proof of Theorem 1 contains a gap that undermines the claimed theoretical foundation.** The proof attempts to show that if π* (a solution to the unconstrained problem (3)) violates the pointwise safety constraint, then a safe policy π̃* (a solution to the constrained problem (2)) achieves higher value under the relabeled reward r_{π*}. The critical step claims V_{r_{π*}}^{π̃*}(s) = V_{r_{π̃*}}^{π̃*}(s), justified "by the safety of π̃*." However, r_{π*} is defined using Q_c^{π*} (the cost-to-go under π*), while the safety of π̃* only guarantees Q_c^{π̃*}(s, π̃*(s)) ≤ κ. It does **not** guarantee Q_c^{π*}(s, π̃*(s)) ≤ κ, so the claimed equality is not justified by the reasoning provided. The theorem may still be true, but the proof as written is insufficient. Since Theorem 1 is presented as the central theoretical motivation ("we show in the Theorem below that it suffices to solve the unconstrained optimization in (3)"), this gap needs addressing. (Verified in paper lines 91–95.)

2. **Characterization of FISOR is overstated.** Section 3 states "FISOR produces safe policies in this regime, but it achieves low reward." The data in Table 1 partially supports this — on 5/6 κ=5 tasks where both methods are safe, CARL has higher reward. However, on AntRun (κ=5), FISOR achieves higher reward (0.43 vs. 0.36) *and* lower cost (0.27 vs. 0.60) than CARL. The blanket claim "achieves low reward" is not consistently supported and should be qualified. (Verified in paper line 67 and Table 1.)

### Minor

3. **Loose connection between Theorem 1 and Algorithm 1.** Theorem 1 motivates a *policy iteration* scheme: fully evaluate Q_c^{π_t}, relabel all rewards, then fully optimize a new policy π_{t+1}. Algorithm 1 instead alternates one gradient step on Q_c and one policy gradient step per mini-batch (M=K=1), with no full evaluation or optimization at any point. The paper candidly acknowledges that "theoretical convergence guarantees are unclear" for M=K=1 (line 166), which is appreciated. But this means Theorem 1 does not actually justify the deployed algorithm — the connection is motivational rather than formal.

4. **High variance on some Safety Gym tasks is not discussed.** On CarCircle1 (κ=10), CARL's normalized cost is 4.15 ± 8.93. The standard deviation is more than double the mean, indicating the policy is sometimes safe and sometimes catastrophically unsafe across seeds/episodes. This is a concerning result for a safety method and deserves analysis rather than just reporting.

5. **R_max vs. V_max design choice is underexplored in the main text.** Section 6.2 mentions using R_max instead of V_max and references an ablation in Table 5 (appendix). However, the rationale and impact of this choice are not discussed in the main paper, making it unclear whether this choice significantly affects the method's performance or the "no additional hyperparameters" claim.

### Trivial

None.

## Nice-to-Haves

- A comparison with the simplest possible baseline: offline RL with a *fixed* Lagrangian penalty (r' = r − λ·c with tuned λ). This is the most natural ablation for CARL and would directly demonstrate whether the iterative relabeling mechanism provides benefit over a fixed penalty.
- Statistical significance testing (e.g., confidence intervals) for the main comparisons, given the high variance observed on several tasks.

## Removed Points

The following points from the input review were filtered:

- **"No comparison with offline RL + Lagrangian reward shaping"**: The paper references Lagrangian variants in Table 5 (appendix). Since the appendix is stripped from the accessible file, this criticism cannot be verified and may be addressed in the full submission.
- **"Missing the relationship between κ and penalty magnitude"**: This is a reasonable question but is a speculation about a design choice rather than a concrete flaw in the paper's evaluation. Moved to a nice-to-have observation.
- **"Algorithm-theory disconnect framed as a critical/structural issue"**: The paper openly acknowledges the gap ("theoretical convergence guarantees are unclear"). This is a valid limitation but the paper is transparent about it; more appropriate as a Minor weakness than a structural flaw.
- **Various formatting/style nitpicks and speculation about appendix content**: Removed per filtering rules.
- **Generic strengths about "addressing an important problem" or "targeting an interesting question"**: Removed as superficial; only kept concrete, evidence-backed strengths.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the proof gap in Theorem 1 and the overstatement regarding FISOR, but these are corrective observations rather than novel analytical insights.

## Suggestions

1. **Repair the proof of Theorem 1.** Either close the gap with a correct argument (e.g., by adding necessary assumptions about the relationship between Q_c^{π*} and Q_c^{π̃*}, such as Lipschitz continuity with respect to policy changes) or reframe the theorem as motivational rather than a formal equivalence. Without a valid proof, the paper overclaims theoretical justification.

2. **Correct the FISOR characterization** in Section 3 to reflect the actual comparative results (e.g., "FISOR is safe on many tasks but generally achieves lower reward than CARL").

3. **Discuss the CarCircle1 cost variance** (4.15 ± 8.93). If this is due to specific seeds or episodes, analyzing what causes the catastrophic failures would strengthen the paper's claims about reliability.

4. **Clarify the R_max vs. V_max choice** and show that it does (or does not) materially affect performance, to preserve the "no additional hyperparameters" claim.

## Calibration

**Round 1 bracket:** 5.5 – 7.0

**Anchor papers retrieved:**

| Path | Avg Human Score | Round | Comparison |
|------|:-:|:-----:|-----------|
| CCAC (nrRkAAAufl.md) | 6.50 | R1 | Direct OSRL competitor used as a baseline in CARL's experiments. CCAC is more complex (CVAE + classifier) with minor weaknesses (limited environments, missing baselines). CARL has a cleaner method but a more significant theory gap. Comparable quality. |
| SEABO (MNyOI3C7YB.md) | 7.00 | R2 | Simple offline IL wrapper method, similar spirit to CARL. No theory problems, thorough evaluation. CARL is slightly weaker due to the proof gap. |
| FOSP (dbuFJg7eaw.md) | 7.00 | R2 | Offline-to-online safe RL with real robot validation. More complex but higher-impact evaluation. CARL is purely offline without real-world validation. |
| Self-Alignment (ZtOnddFVT3.md) | 4.67 | R1 | OSRL paper with theory issues and weak experiments. CARL is substantially stronger. |
| Low-Switching Primal-Dual (G0uhaIXmFw.md) | 4.75 | R1 | Theory-heavy safe RL with unclear practical benefits. CARL's empirical contribution is stronger. |
| Reliable Offline RL (fWx1CKgPCc.md) | 4.00 | R1 | Limited contribution and inadequate experiments. CARL is clearly stronger. |
| Provably Safe RL (RAdBtquPiI.md) | 3.40 | R1 | Theory paper with weak empirical validation. CARL's empirical work is more comprehensive. |
| Penalizing Infeasible Actions (Zk8PNvzWQY.md) | 5.75 | R2 | Related reward-relabeling approach for offline RL (not safe RL). Comparable quality. |

**Narrowing:** After round 2, the most comparable accept papers (CCAC at 6.5, SEABO at 7.0) suggest CARL sits at the lower end of this range due to the theory proof gap, which is a more significant flaw than any weakness in those papers.

**Final score:** 6.0 — The paper has a meaningful empirical contribution and a genuinely simple method, but the incomplete proof of the central theorem and the overstated FISOR characterization prevent it from ranking higher.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>