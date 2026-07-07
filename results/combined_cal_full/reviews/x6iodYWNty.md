## Summary

This paper proposes Neural Predictor-Corrector (NPC), which uses reinforcement learning (PPO) to learn adaptive policies for predictor step sizes and corrector termination criteria in homotopy solvers. The method unifies four problem classes under a common PC structure — robust optimization (GNC), global optimization (Gaussian homotopy), polynomial root-finding (homotopy continuation), and sampling (annealed Langevin dynamics) — and is evaluated across multiple benchmarks in each domain. Amortized training enables a single policy to generalize to unseen instances without per-instance fine-tuning.

## Strengths

- **Genuinely cross-domain experimental evaluation.** NPC is evaluated on four distinct problem classes (GNC, GH, HC, ALD), each with multiple benchmarks. The cross-instance generalization results (e.g., training on Ackley and testing on Himmelblau/Rastrigin in Sec. 5.3; training on 4-view triangulation and testing on katsura10/cyclic7 in Sec. 5.4) provide legitimate evidence that the RL policy learns a non-trivial adaptive strategy. This breadth of evaluation is unusual and is the paper's strongest empirical feature.

- **The RL-based adaptive PC formulation is well-motivated.** The observation that predictor step sizes and corrector termination criteria are hand-tuned in classical homotopy solvers (Section 4.1), and that these decisions are naturally sequential, frames the MDP formulation cleanly. Algorithm 1 provides a clear description of the NPC solver loop.

- **The ablation study (Table 6) is clean and informative.** Removing any single state component increases iterations, and the relative ordering (corrector tolerance > corrector iteration > convergence velocity > homotopy level in terms of impact) provides useful insight into what the learned policy relies on.

## Weaknesses

### Major

- **Missing adaptive heuristic baseline makes it impossible to attribute improvement to RL.** The paper compares NPC exclusively against fixed-schedule classical methods (Classic GNC, Classic GH, Classic HC, Classic ALD) and specialized baselines. Since any adaptive mechanism — including a simple rule-based heuristic (e.g., reducing Δt when convergence velocity drops below a threshold, or a PID-style controller) — would likely outperform a fixed schedule on problems where optimal step size varies along the trajectory, the reader cannot tell whether the benefit comes from *adaptivity itself* or from the *learned RL policy specifically*. This directly undermines the paper's central claim that learned policies are needed to replace hand-crafted heuristics. The paper should include a straightforward adaptive heuristic baseline tuned on the training distribution for each domain.

- **Unsubstantiated "superior numerical stability" claim.** The abstract, introduction, and conclusion all claim "superior stability" or "superior numerical stability." Yet the experimental section contains: (a) no variance measures, standard deviations, confidence intervals, or error bars in any table (results are reported as averages over 50 trials but without any dispersion metric); (b) no analysis of trial-level success/failure rates (Table 4 shows 100% for all methods, which does not differentiate); (c) no quantitative stability metric of any kind. Stability is asserted without definition or evidence. It should either be substantiated with appropriate metrics (variance across trials, failure rates, convergence consistency) or removed.

- **The paper's narrative of "consistently outperforming existing approaches" is not fully supported by the numbers.** Specific counterexamples: (a) In Table 3 (GH), PGS on Ackley achieves 200 iterations vs NPC's 359 with comparable accuracy (0.07 vs 0.05) — a non-RL baseline is more efficient on this task. (b) In Table 5 (ALD), on the 40-mode GMM, NPC achieves W2=11.91, which is *worse* than Classic ALD's 11.57 and substantially worse than iDEM's 7.42. On DW-4, NPC's W2=3.47 sits between Classic ALD (3.77) and iDEM (2.13). The paper downplays iDEM as "not directly comparable in runtime," but the *quality* comparison is unfavorable and should be discussed honestly. The paper would benefit from a more nuanced discussion of where NPC underperforms baselines on quality or where simpler methods are competitive on efficiency.

### Minor

- **Reward design lacks an explicit final-accuracy term.** The reward (Section 4.2) consists of a step-wise accuracy reward based on convergence velocity and a terminal efficiency bonus, but does not include a reward for the quality of the *final* solution at t=1. The agent could learn to make intermediate tracking look good while failing to produce an accurate final solution. The empirical results suggest this did not happen in practice, but the paper does not justify why the step-wise accuracy reward is sufficient to ensure final accuracy, nor does it analyze whether the learned policy actually drives the solution to convergence at t=1.

- **PPO hyperparameters are under-specified.** The paper states "all other hyperparameters use the default values provided by Stable Baselines3" (Section 5.1), but SB3's default PPO parameters differ across versions and are designed for continuous control benchmarks, not this task. Learning rate, clip range, entropy coefficient, training steps, minibatch size, and GAE lambda are not reported. Training cost (wall-clock time, number of episodes) is also not reported, which is essential for practitioners evaluating whether amortized training is practical.

- **IRLS GNC on multi-view triangulation is not an informative baseline.** In Table 2, IRLS GNC is evaluated on multi-view triangulation despite being designed for point cloud registration, leading to catastrophic failure (positive log error). The paper acknowledges this ("IRLS, tailored for a specific task, performs poorly on triangulation and lacks generalization"), but including a baseline on a task it was never designed for makes the comparison look favorable to NPC without being informative. The meaningful comparison is between NPC+GNC and Classic GNC alone.

- **The efficiency-precision trade-off curves (Figure 4) are not adequately explained.** It is unclear how the classical "trade-off curves" were generated — were they created by manually tuning homotopy parameters across a grid? How many points along each curve? What parameter range was explored? Without this information, plotting a single NPC point against a fitted curve is not properly interpretable.

### Trivial

None.

## Nice-to-Haves

- The state representation (Section 4.1) excludes the current solution x, its gradient, or any measure of local curvature. The policy makes decisions based on convergence statistics from the *previous* step, which is a deliberate design choice for generalization, but discussing it as a limitation would improve clarity.
- An analysis of the learned policy's behavior (e.g., does it take small steps in high-curvature regions and large steps in smooth regions?) would strengthen the claim that the RL agent discovers meaningful strategies beyond simple heuristics.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. "The unification is not a technical contribution — it is an observation that existing methods already use homotopy/PC concepts." REMOVED because the paper does more than observe: it proposes a single RL-based solver framework that demonstrably operates across all four domains, which is a concrete technical contribution. The cross-instance generalization results (training on one task, testing on another within the same domain) go beyond a mere observation of similarity.
2. "CPL comparison: training cost comparison may favor CPL for practitioners with few instances." REMOVED as speculation about a counterfactual scenario. The paper reports CPL's wall-clock time (1701ms on Ackley), which is far larger than NPC's, and this comparison is adequate.
3. "The paper should analyze the learned policy's behavior." Moved to Nice-to-Haves rather than a weakness.

## Novel Insights

None beyond the paper's own contributions. The reviewer's observations are accurate and well-grounded but follow from careful reading rather than providing a genuinely novel perspective.

## Suggestions

1. **Add a simple adaptive heuristic baseline** for each of the four problem domains (e.g., reduce Δt when convergence velocity drops below a threshold α; increase corrector tolerance when convergence is fast). Tune α on the training distribution. If NPC outperforms this baseline, the claim about learned policies is well-supported. If not, the contribution shifts — still publishable but requiring honest reframing.
2. **Remove or substantiate the "superior stability" claim.** Define stability (variance across trials? failure rate? sensitivity to initialization?) and provide measurements.
3. **Add variance/confidence intervals** to all tables. Results are averaged over 50 trials — reporting standard deviations would cost little and greatly improve credibility.
4. **Report training cost** (wall-clock time, number of episodes) for each experiment.
5. **Report full PPO hyperparameters** rather than relying on "SB3 defaults."
6. **Reframe the narrative** to acknowledge cases where baselines are competitive on efficiency (PGS on Ackley) or superior on quality (iDEM).

## Score and Decision

**Initial bracket (Round 1):** 4.0–5.5. The paper sits between lower-scored papers with missing rigorous baselines (e.g., "Simulating, Fast and Slow" at 4.33, continuation paper at 4.50) and the mid-scored papers with stronger empirical/theoretical validation (e.g., "Metamizer" at 5.25, "Learning a Neural Solver" at 5.60). The cross-domain breadth is a genuine strength shared with only the best anchors, but the missing adaptive baseline and unsubstantiated stability claims are heavy negatives (model weights -7.18 and -5.90 respectively) that place it in the lower portion of this bracket.

**Narrowing:** Compared to "Metamizer" (5.25), which was accepted despite missing baselines, the current paper has *two* comparably severe shortcomings (missing baseline and unsubstantiated stability claims) rather than one, and lacks the theory/evaluation depth of "Learning to Relax" (8.00). Compared to the 4.33 "Simulating, Fast and Slow" paper (rejected), the current paper has broader evaluation and a cleaner ablation study, giving it a slight edge.

**Final calibration anchors:**
- `5t57omGVMw.md` (8.00) — far stronger theory and evaluation; not directly comparable in rigor.
- `vLJcd43U7a.md` (6.50) — stronger empirical validation with cleaner claims; SYMBOL is a stronger paper.
- `60TXv9Xif5.md` (5.25) — similar missing-baselines weakness but accepted; current paper has broader domain coverage but more unaddressed claims.
- `nrDRBhNHiB.md` (4.50) — similar quality level; both have interesting ideas with limited experimental support.
- `O9TTAoySaG.md` (4.33) — comparable in that the training-vs-inference cost question undermines the central claim; current paper has a similar attribution problem.
- `XTxdDEFR6D.md` (3.40) — weaker; limited novelty and missing comparisons.
- `BdmVgLMvaf.md` (6.50) — stronger experimental execution and clearer writing.

**Final score:** The weighted-item comparison shows that the paper's strongest negative (-7.18 for missing baseline) is on par with the strongest negatives in the 4.3–5.25 anchors, while its strongest positive (+5.09 for the ablation study) is slightly weaker than the strongest positives in the accepted anchors. The cross-domain evaluation (+4.21) is a legitimate differentiator but is counterbalanced by multiple unaddressed weaknesses. The paper makes a reasonable contribution with a well-motivated approach, but the evidential gaps — particularly the missing adaptive baseline and unsubstantiated stability claim — are too significant to support acceptance in the current form.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>