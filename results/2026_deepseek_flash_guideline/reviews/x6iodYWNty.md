## Summary

This paper proposes Neural Predictor-Corrector (NPC), an RL-based framework that replaces hand-crafted step-size and termination heuristics in homotopy/predictor-corrector solvers with learned neural policies. It unifies four problem domains (GNC for robust optimization, Gaussian homotopy for global optimization, homotopy continuation for polynomial root-finding, and annealed Langevin dynamics for sampling) under a shared PC formulation, and trains a separate PPO-based agent per domain. Experiments across all four tasks show that NPC reduces corrector iterations by 50–80% and runtime by comparable margins while maintaining solution accuracy on held-out test instances.

## Strengths

1. **First explicit unification of four homotopy problems under a shared PC framework.** Section 3.3 provides concrete homotopy interpolations (Equations 1–4) for robust optimization, global optimization, polynomial root-finding, and sampling, and identifies the shared predictor-corrector structure across all four. While individual PC methods are well-known in each domain, no prior work draws this cross-domain connection or uses it to design a common solver architecture.

2. **Cross-instance generalization is demonstrated across all four tasks.** Each experiment trains on one distribution and tests on held-out instances: GNC trained on Aquarius, tested on bunny/cube/dragon (Table 1); GH trained on randomized Ackley, evaluated on fixed Ackley/Himmelblau/Rastrigin (Table 3); HC trained on randomized 4-view triangulation, tested on katsura10/cyclic7/UPnP (Table 4); ALD trained on 10-mode GMM, tested on 40-mode GMM/funnel/DW-4 (Table 5). This separation between training and test distributions goes beyond per-instance learned solvers.

3. **Large and consistent efficiency gains across all four tasks.** The learned policy reduces corrector iterations by 70–80% for GNC (Table 1), ~30–50% for GH (Table 3), ~80% for HC (Table 4), and ~75% for ALD (Table 5). Runtime reductions are similarly large (e.g., GNC: 80–90% faster). These gains are achieved while maintaining comparable solution accuracy across nearly all metrics.

4. **Ablation study validates the RL state design (Table 6).** Systematically removing each state component (homotopy level, corrector tolerance, corrector iteration count, convergence velocity) causes measurable degradation (+21 to +64 more iterations). Corrector statistics are the most informative components (+64, +52), providing evidence that the chosen state representation is well-motivated.

5. **Efficiency-precision trade-off analysis (Figure 4) shows NPC finds a better operating point.** The learned policy's single operating point lies below the classical manual-tuning trade-off curves for both GNC and ALD, demonstrating that the RL-optimized policy jointly balances accuracy and efficiency.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or uncertainty reported despite "50 independent trials."** The paper states (Section 5.1) that all results average 50 independent trials, yet no table reports standard deviations, confidence intervals, or any measure of variance. For an RL-based method with policy stochasticity and environment randomness, the reader cannot assess whether improvements over baselines are statistically significant — especially where accuracy differences are small (e.g., Tables 1 and 3, where NPC accuracy is close to Classic GNC/GH). This omission is particularly consequential for the "superior stability" claim, which requires variance measurement.

2. **The "superior stability" claim is asserted without definition or measurement.** The abstract and introduction claim "superior stability across tasks" and "superior numerical stability," but the paper never defines what stability means quantitatively or reports any stability metric (e.g., variance across trials, failure rate on challenging instances, sensitivity to initialization). The closest evidence is the 100% success rate in Table 4 (which all methods achieve) and consistent accuracy — these are not measurements of stability. This claim should either be removed or explicitly defined and measured.

3. **Training costs are not reported, leaving the amortization claim unquantified.** The paper argues that NPC's one-time training is amortized across test instances, contrasting with per-instance methods like CPL (Table 3). However, no training cost is reported (number of episodes, wall-clock time, compute budget per domain). Without this, a practitioner cannot evaluate whether the amortization argument holds. The comparison to CPL in Table 3 is especially affected: CPL's 1701ms includes per-instance training, but if NPC requires thousands of RL episodes per domain, the break-even point is unknown. This is a significant barrier to practical adoption.

4. **Several baseline comparisons are not cleanly controlled, weakening the evaluation.** (a) iDEM (Table 5) runs on a more powerful RTX A6000 GPU versus the paper's RTX 3060, and the paper notes "runtimes are not directly comparable" — yet still includes a runtime column. iDEM achieves substantially better Wasserstein-2 distances on both GMM (7.42 vs. 11.91) and DW-4 (2.13 vs. 3.47), so the paper's framing that NPC is "comparable" holds only for KSD, not W2. (b) Simulator HC (Table 4) is implemented in C++ vs. Python for the other methods, making runtime incomparable. The paper is transparent about these issues, but including incomparable baselines in tables with numeric columns creates a misleading appearance of broad competitiveness.

### Minor

1. **The unification framing is somewhat overstated.** The paper claims to be "the first to unify diverse problems... under the homotopy paradigm" and that "no prior work has systematically unified these efforts." The observation that GNC, Gaussian homotopy, homotopy continuation, and ALD are all continuation methods with PC structure is a useful cross-domain connection, but it does not constitute a rigorous mathematical unification (e.g., a general convergence theorem or common representation language). The main technical contribution is the RL-based parameter control, which is valuable on its own and does not need inflated framing.

2. **No comparison against a simpler learned baseline within the NPC framework.** To isolate whether the RL optimization matters (vs. the flexibility of the neural architecture), the paper should compare NPC against a version with random policy weights or a fixed heuristic policy using the same network. This is a standard control in RL papers and would strengthen confidence that the RL training drives the observed improvements rather than just the added neural capacity.

3. **No sensitivity analysis on reward coefficients or PPO hyperparameters.** The reward coefficients λ₁ and λ₂ (Section 4.2) and the PPO hyperparameters (which use Stable Baselines3 defaults) are not analyzed. It is unclear whether the method is robust to these choices or requires careful per-task tuning. The small network (2×16 units) is reported without discussion of whether it was chosen by hyperparameter search or set arbitrarily.

4. **The IRLS baseline in Table 2 (multi-view triangulation) is clearly unfit for this task,** producing catastrophically poor accuracy (log(Ep) ≈ 0.5–1.7 vs. −4.6 to −5.2 for both Classic GNC and NPC). Including it adds no informative signal and makes NPC look stronger by contrast. Either omit it or explain why it is a meaningful comparison.

### Trivial
None.

## Nice-to-Haves

- Reporting both predictor iterations and corrector iterations separately would clarify the mechanism of efficiency gains.
- A discussion of scaling to higher-dimensional polynomial systems in HC would be useful.
- Cross-class generalization (train on one problem class, test on another) would strengthen the unification claim, though the paper does not make this claim.

## Removed Points

Points raised in the Harsh Critic or Strength Finder that were removed, with justification:

- *Harsh Critic: "CPL comparison — if NPC requires 10,000 episodes while CPL's per-instance cost is cheap, the comparison could flip."* This specific speculation is removed. The general concern about missing training costs is retained (Major #3).
- *Harsh Critic: "'Iter' meaning corrector iterations is unusual."* Removed as a legitimate design choice; the paper explicitly defines it in Section 5.1.
- *Harsh Critic: "No cross-class generalization experiments."* Moved to Nice-to-Haves; the paper does not claim cross-class generalization.
- *Harsh Critic: "Appendix A details on reward scaling are missing."* Removed per rule — the appendix is stripped by the parser, and this content exists in the original submission.
- *Harsh Critic: "The method section lacks key details about PPO hyperparameter tuning."* Retained but softened (Minor #3).
- *Harsh Critic: "No comparison against random/fixed policy within NPC."* Retained (Minor #2).
- *Strength Finder: All five strengths retained as they are concrete and evidence-based.*
- *Harsh Critic: "Network architecture is surprisingly small (2×16)."* Retained as part of Minor #3.

## Novel Insights

None beyond the paper's own contributions. The most novel perspective is the framing of PC parameter selection as an MDP amenable to RL, which is a genuine insight that connects numerical analysis to modern RL.

## Suggestions

1. **Report standard deviations or confidence intervals for all metrics (Tables 1–5).** This is essential for an RL method with stochastic policies.
2. **Either define and measure "stability" or remove the claim from the abstract/introduction.** A variance metric across trials or a failure-rate metric would suffice.
3. **Report training cost (number of episodes, wall-clock time) per problem domain** and, if possible, the break-even point (number of test instances needed to amortize training).
4. **Add an ablation comparing NPC against a random-weights or fixed-policy version** within the same neural architecture to isolate the effect of RL training.
5. **Re-frame the iDEM and Simulator HC comparisons more transparently.** Consider removing runtime columns where hardware/language differs substantially, or reporting only the metrics that are fairly comparable.
6. **Add a brief sensitivity analysis on reward coefficients (λ₁, λ₂).** A simple sweep over a small grid would suffice to show robustness.

## Score and Decision

**Round 1 bracket:** 4.0–5.5

**Anchor comparison:**
- *Learning to Relax (8.0, accepted)* — rigorous theoretical guarantees, regret bounds. NPC has no theory.
- *Adaptive Backtracking (6.25, accepted)* — convergence proofs, clean experiments on 15 datasets. NPC has no proofs, broader but less rigorous experiments.
- *A Reoptimization Framework for MILP (6.0, rejected)* — strong empirical results, missing theoretical guarantees. NPC similar quality but with more evidence gaps (no error bars, missing training cost).
- *Learning Multiple Initial Solutions (5.75, rejected)* — clean presentation, limited domains. NPC has broader domain coverage but more serious evidence quality issues.
- *Simulating, Fast and Slow (4.33, rejected)* — training cost accounting issues, unclear comparisons. Similar profile to NPC.
- *Accelerating SDP (4.0, rejected)* — overclaiming, insufficient experiments. Similar overclaiming pattern (stability without definition).

**Final score:** The paper has a genuinely novel idea (RL for homotopy PC parameter control) and demonstrates consistent efficiency gains across four diverse domains with cross-instance generalization. However, the absence of error bars (despite reporting 50 trials), missing training costs (undermining the central amortization claim), unsupported stability claims, and uncleaned comparisons collectively weaken the evidence below the bar for ICLR acceptance. The paper would be competitive with major revisions addressing experimental rigor.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>