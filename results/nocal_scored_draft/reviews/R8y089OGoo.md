Now I have all the signals I need. Let me write the final consolidated review.

---

## Summary

This paper proposes DIPOLE (Dichotomous Diffusion Policy Improvement), a new RL algorithm for diffusion policy optimization. The key theoretical insight is that by introducing a greedified KL-regularized objective, the optimal policy can be decomposed into a pair of dichotomous policies — one maximizing and one minimizing return — whose scores can be linearly combined at inference time in a manner analogous to classifier-free guidance. This decomposition replaces the unbounded exponential weighting in standard KL-regularized RL with bounded sigmoid weights, addressing training instability and sample dominance issues. Empirical evaluations on ExORL (9 tasks) and OGBench (30 tasks) under offline and offline-to-online settings, plus a scale demonstration on a 1B-parameter vision-language-action model for autonomous driving on NAVSIM, show consistent improvements over strong baselines.

## Strengths

- **Clean theoretical derivation connecting KL-regularized RL to classifier-free guidance.** The chain from Eq. (2) → Eq. (5) → Theorem 1 (Eq. 6) → dichotomous decomposition (Eqs. 7–8) → CFG-style inference (Eq. 10) is mathematically tight, and the connection between RL optimality and CFG is genuinely novel and insightful.

- **Well-motivated practical improvement over exp-weighted regression.** The paper clearly identifies two concrete problems with Eq. (4): exploding loss under large β and sample dominance by high-return exemplars. The sigmoid-based dichotomous decomposition directly addresses both (bounded weights, stable losses, utilization of both high- and low-return samples).

- **Strong empirical results on standard RL benchmarks.** On ExORL (Table 1), DIPOLE substantially outperforms all baselines across most tasks (e.g., 953 vs. 873 on Walker-stand, 910 vs. 844 on Walker-walk, 657 vs. 595 on Quadruped-run). On OGBench (Table 2), DIPOLE achieves the best or near-best aggregate scores in 5 out of 6 task categories. These gains are consistent and non-negligible.

- **Scale demonstration to a 1B-parameter VLA model on a real-world driving benchmark.** Applying DIPOLE to fine-tune a billion-parameter vision-language-action model (DP-VLA) for autonomous driving on NAVSIM demonstrates the method works at scale, not just on Gym-style tasks.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **NAVSIM navtest result is not an apples-to-apples comparison and risks overstatement.** The DIPOLE variant trained on the navtest split achieves 94.8 PDMS (+6.5 over baseline), but this split is the held-out test set of the NAVSIM benchmark — training on it means the model has seen test data during training. The paper acknowledges this (lines 211–212) and justifies it under a different usage scenario, but Table 4 places this result alongside standard baselines (UniAD, Transfuser, Hydra-MDP, etc.) that were *not* trained on the test split, and the text emphasizes the 6.5-point gain. The honest comparison is the navtrain result (+1.4 PDMS), which is modest. The presentation conflates two fundamentally different evaluation regimes.

- **No computational cost comparison despite criticizing prior methods for inefficiency.** The paper criticizes PPO-based diffusion methods (DDPO, DPPO) for requiring "sufficiently small denoising steps" leading to "prolonged training" and criticizes gradient-backprop methods for being "extremely costly." Yet DIPOLE trains *two* diffusion models (positive and negative), roughly doubling the parameter count compared to single-model methods. No wall-clock time, FLOP, or convergence-step comparison is provided against any baseline, leaving the efficiency claims untested.

- **The ω parameter conflates regularization and greediness control.** The greediness factor ω appears both in the KL denominator of Eq. (5) (controlling regularization strength) and in the closed-form solution via exp(ω·βG) in Eq. (6) (controlling greediness). This means ω simultaneously influences two distinct effects, making it difficult to independently control regularization and greediness. This is a subtle but real limitation worth discussing.

### Trivial

- **Flow matching mentioned but not evaluated.** The abstract and preliminaries reference "diffusion/flow matching policies," but all experiments use only diffusion models. No flow matching experiments are shown, making the framing broader than the evaluation.

## Nice-to-Haves

- An ablation on ω values (e.g., ω ∈ {0, 0.5, 1.0, 2.0}) on one or two tasks would substantiate the "controllable greediness" claim.
- An ablation comparing DIPOLE against a version using Eq. (4) directly (exp-weighted regression with the same architecture) would directly test whether the dichotomous decomposition solves the claimed stability problems.
- Sensitivity analysis on β (temperature) would strengthen the practical guidance.

## Removed Points

The following points from the input review are removed per filtering rules:

1. **"Value/advantage function estimation completely unspecified"** — REMOVED. The paper explicitly states "The algorithm pseudocode and additional implementation details are provided in Appendix C and D" (line 123). The parser strips appendices; these details exist in the original submission.
2. **"Missing comparison with exp-weighted regression baseline (Eq. 4)"** — REMOVED. The paper states "We refer to Appendix D.4 for ablation studies" (line 207). The parser strips appendices; this ablation may be present there.
3. **"Missing ablation on ω"** — REMOVED. Same reason: Appendix D.4 is stripped.
4. **"Offline-to-online comparison weaker than it appears"** — REMOVED. The reviewer misreads the paper's claim: the paper states "Compared to IFQL, it achieves a higher performance upper bound" (line 205, emphasis added), which is a correct characterization of Table 3. The claim about FQL is specifically "competitive performance," which is accurate.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Restructure the NAVSIM presentation: clearly separate the navtrain (standard evaluation) and navtest (exploratory scenario) results into distinct paragraphs or tables, with the navtrain result as the primary comparison.
2. Add a brief computational cost analysis — even a single table showing wall-clock training time or convergence steps across methods — to contextualize the efficiency discussion.
3. Include a brief discussion of the ω conflation issue (dual role in regularization and greediness) as a limitation, and whether this design choice has practical consequences.

---

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>