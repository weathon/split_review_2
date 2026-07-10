## Summary

This paper proposes Neural Predictor-Corrector (NPC), a reinforcement learning framework that replaces hand-crafted step-size and termination heuristics in homotopy/predictor-corrector solvers with learned adaptive policies. NPC formulates the PC process as an MDP where an agent observes the homotopy level, corrector statistics, and convergence velocity, then outputs a step size and termination criterion. The method is demonstrated across four problem families — robust optimization (GNC), global optimization (Gaussian homotopy), polynomial root-finding (homotopy continuation), and sampling (annealed Langevin dynamics) — with amortized training enabling generalization to unseen instances.

## Strengths

- **Broad cross-domain scope with compelling empirical results.** NPC is demonstrated on four distinct problem families (robust optimization, global optimization, polynomial root-finding, sampling) with generalization from a training instance to unseen instances within each family. The GNC point cloud registration results (Table 1) are the strongest evidence: a single policy trained on Aquarius reduces iterations by ~70–80% on bunny, cube, and dragon while maintaining equivalent accuracy.

- **Well-motivated, parsimonious state representation.** The choice of homotopy level, corrector statistics (tolerance + iteration count), and convergence velocity as the MDP state (Section 4.1) is grounded in the common structure of PC methods. The ablation study (Table 6) credibly shows each component contributes, with corrector statistics being most informative — a clean empirical finding.

- **Honest efficiency-precision trade-off framing.** Figure 4 plots the NPC-accelerated method against a curve of classical operating points, correctly framing the comparison as finding a better operating region rather than cherry-picking a single point.

## Weaknesses

### Major

- **No comparison against classical adaptive PC heuristics.** The paper compares NPC exclusively against baselines with *fixed* schedules (Classic GNC, Classic GH, Classic HC, Classic ALD). Classical homotopy continuation has well-known adaptive step-size methods (e.g., based on corrector convergence rate, local error estimates, or chord slope changes — see Allgower & Georg, 2012, which the paper itself cites). These are the relevant scientific comparison for an RL-based adaptive controller. Without this comparison, the paper demonstrates only that RL-guided control outperforms *fixed* heuristics — leaving the marginal benefit of RL training over existing adaptive methods unclear. This is the most significant evaluation gap.

- **No variance or uncertainty reported.** The paper states "All results represent the average over 50 independent trials" (line 230) but reports no standard deviations, confidence intervals, or error bars in any table or figure. For the sampling (ALD) experiments where Wasserstein-2 distance naturally varies across trials, this is a serious omission — the reader cannot assess whether reported differences are meaningful or noise.

### Minor

- **NPC training cost is not reported.** The amortized training narrative is central to the paper ("one-time offline training and efficient, training-free deployment on new instances"), yet no training cost is given (number of episodes, CPU/GPU hours, wall time). The CPL comparison in Table 3 is explained (CPL requires per-instance training so total time is reported), but without NPC's own training cost, the reader cannot assess the amortization break-even point. NPC's runtime advantage over CPL is presented as "orders of magnitude," but this only reflects inference-only cost.

- **No analysis of failure cases.** The paper reports 100% success for HC and comparable accuracy for GNC, but does not discuss failure modes: does the learned policy ever take a step size that causes the corrector to diverge? How does the agent handle the edge of the homotopy (t → 1)? This is important for understanding the method's practical limitations.

- **The "unification" claim (contribution 1) is somewhat overstated.** The paper observes that diverse homotopy solvers share a PC structure — a useful pedagogical insight but one already implicit in the homotopy literature (Allgower & Georg, 2012). The paper's actual technical contribution is the RL-based adaptive controller applied independently per domain with domain-specific correctors, not a single unified solver. Reframing this claim would align better with what is actually built.

### Trivial

- The action space notation in Algorithm 1 uses `{Δt_n, ε_n or t_n^{max}}` without fully specifying how the two-part action is instantiated per domain (e.g., how a tolerance action is interpreted for Langevin dynamics, which differs structurally from the Levenberg-Marquardt convergence criterion). The appendix likely addresses this, but the main text could be clearer.

## Nice-to-Haves

- Visualize the learned policy's step-size schedule across a representative trajectory to clarify whether NPC learns meaningful adaptive behavior or converges to a near-constant step size.
- Report the residual or tracking accuracy for the HC experiments (Table 4), where "success" could span a wide tolerance range.
- Add a brief discussion of why the wall-clock speedup is more modest for ALD (~1.75×) than for GNC (~5–10×), as the corrector (Langevin dynamics) dominates runtime.

## Removed Points

These points were raised in the input review but are removed with justification:

1. **"CPL comparison is fundamentally unfair and misleading"** — The paper transparently explains *why* CPL training time is included: CPL requires per-instance training, making amortization impossible (line 244). This is a reasonable methodological justification. The related point about NPC training cost being unreported is retained as a Minor weakness above.

2. **"IRLS GNC on triangulation (Table 2) is a straw-man baseline"** — The paper explicitly states IRLS is "tailored for a specific task" and shows it fails to generalize on triangulation (line 236). This demonstrates a generalization gap, directly supporting the paper's claims. Not a weakness.

3. **"Method under-specification" as Critical Issue about the action space** — The action space is described in the text (lines 168–171). The "or" in Algorithm 1 is clarified by the description ("convergence threshold ε or maximum number of updates"). The appendix (stripped by the parser) likely provides full per-domain implementation details.

4. **Missing appendix details** (reward scaling coefficients λ₁, λ₂) — The parser strips appendix sections; these details exist in the original submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add classical adaptive baselines** — Compare NPC against simple adaptive heuristics (e.g., adjust step size based on corrector convergence rate). If NPC outperforms these, the RL training is doing something meaningful beyond what existing methods already achieve.

2. **Report variance** — Add standard deviations or confidence intervals for all metrics, especially for the ALD experiments where stochasticity is inherent.

3. **Disclose NPC training cost** and discuss the amortization break-even point (how many test instances are needed to offset the one-time training cost).

4. **Temper the unification claim** to match what is actually built: an RL-based adaptive controller applicable across homotopy problems that share a PC structure, rather than a single unified solver.

## Score and Decision

**Calibration summary:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| Learning to Relax (5t57omGVMw) | 8.00 | R1 | Yes | Much stronger theoretical guarantees and rigorous analysis; my paper is well below this |
| Adaptive Backtracking (SrGP0RQbYH) | 6.25 | R1/R2 | Yes | Cleaner empirical methodology with theory; my paper's worst weakness (-2.85) is more negative than this anchor's worst (-1.41) |
| Greedy L2O (FK8tl47xpP) | 6.25 | R2 | Yes | Comparable experimental scope but stronger theory; my paper has broader domain coverage |
| Learning Neural Solver (jqVj8vCQsT) | 5.60 | R2 | Yes | My paper's strengths (9-10 favorability) comparable; my paper's worst weakness (-2.85) is less severe than this anchor's worst (-9.09) |
| Multiobjective Continuation (nrDRBhNHiB) | 4.50 | R1 | Yes | More severe weaknesses; my paper is above this |
| Simulating Fast and Slow (O9TTAoySaG) | 4.33 | R2 | No | Lower-scored paper in similar area |
| MetaOptimize (VRbypIkXrt) | 5.00 | R2 | No | Related but scope different |

**Round 1 bracket:** Paper sits between ~4.0 and ~6.25.

**Round 2 narrowing:** Comparing item favorability: my paper's strengths (9.32–10.62) match the 5.60–6.25 range, but the -2.85 weakness (missing adaptive baselines) is more negative than any weakness in the 6.25 anchors. This places the paper below 6.25. The paper's worst weakness is less severe than the 5.60 anchor's worst (-9.09), placing it above 5.60.

**Final placement:** 5.5 — a borderline paper with genuine novelty (RL for PC parameter control across four domains) and strong cross-domain generalization evidence. However, the missing comparison against classical adaptive heuristics is a significant evaluation gap that makes it difficult to assess the marginal value of the RL approach. The absence of variance reporting further weakens confidence in the comparisons. These issues are addressable but require substantial revision.

<score>5.5</score>
<decision>Reject</decision>