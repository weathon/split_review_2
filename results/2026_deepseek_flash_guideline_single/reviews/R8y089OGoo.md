Now I have all the information I need. Let me construct the final review.

## Summary

The paper proposes DIPOLE, an RL algorithm for fine-tuning diffusion policies. The core contribution is reformulating the KL-regularized RL objective to decompose the optimal policy into two "dichotomous" policies (one reward-maximizing π⁺, one reward-minimizing π⁻) with bounded sigmoid weights, enabling stable training and CFG-style controllable inference. The method is evaluated across 39 tasks on ExORL and OGBench benchmarks and scaled to a 1-billion-parameter VLA model for autonomous driving on NAVSIM.

## Strengths

- **Clean and mathematically sound theoretical derivation.** The progression from Eq. (5) through the closed-form solution in Eq. (6) to the dichotomous decomposition in Eqs. (7–8) is logically coherent. The insight that replacing unbounded exp(βG) weighting with bounded σ(βG) and 1 − σ(βG) weights provides training stability while preserving expressiveness via an ω-controlled combination is genuinely clever. This is a nontrivial theoretical contribution to diffusion policy optimization.

- **Well-articulated connection to classifier-free guidance.** The paper shows that the score combination in Eq. (10) takes the same form as CFG and traces this back to the greedified KL-regularized objective. This provides a principled explanation for why CFG-like mechanisms can be effective for policy optimization, rather than borrowing the technique heuristically.

- **Broad evaluation scope.** The paper evaluates on 39 tasks across two RL benchmarks (ExORL, OGBench) under both offline and offline-to-online settings, and scales to a 1-billion-parameter VLA model for autonomous driving on NAVSIM. This breadth is unusual for a method paper and strengthens the case for practicality.

- **Strong RL benchmark results.** On ExORL (Table 1), DIPOLE achieves the best results on 7/9 tasks, often by substantial margins (e.g., Walker-stand: 953 vs 873 for IFQL; Walker-walk: 910 vs 844). On OGBench (Table 2), it achieves best or near-best results on 4/6 task categories with large gains on cube-double-play (44 vs 29) and scene-play (60 vs 56). Results are averaged over 8 seeds with standard deviations.

## Weaknesses

### Fatal
None.

### Major

1. **Missing direct comparison with the exp-weighted regression baseline (Eq. 4).** The paper's entire motivation rests on the claim that the exp-weighted regression objective suffers from instability, loss explosion, and high-return-sample dominance. Yet the paper never directly compares DIPOLE against a method that uses Eq. (4) with the same base architecture. The baselines (IQL, IFQL, FQL, CFGRL) use different mechanisms — expectile regression, flow distillation, hard advantage filtering — none of which implement the simple exp-weighted diffusion loss described in Lemma 1. Without this comparison, the paper's central empirical claim — that the dichotomous decomposition resolves the instability of exponential weighting — cannot be directly validated from the presented evidence. A head-to-head comparison on a subset of ExORL/OGBench tasks is needed to substantiate the motivation. *(See Eqs. 3–4 and the limitations discussion in Section 3.1.)*

2. **NAVSIM test-split evaluation inflates the headline result without adequate caveats.** In Table 4, DIPOLE navtest achieves 94.8 PDMS (+6.5 over the 88.3 baseline), but this variant is explicitly stated to be "trained on the test split" (Section 4.2). All other methods in the table (UniAD, Hydra-MDP, Transfuser, etc.) are trained on the standard training split and evaluated on the test split. Training on the test split observations provides exposure to the evaluation distribution that no baseline receives, making this comparison apples-to-oranges. The paper's framing — "fine-tuning with DIPOLE on navtest scenarios yields a substantial 6.5-point PDMS improvement (from 88.3 to 94.8), demonstrating its potential for real-world autonomous driving applications" — does not adequately qualify this apples-to-oranges comparison. The clean navtrain result (89.7, +1.4 PDMS) is modest and does not clearly demonstrate superiority over DPPO (89.0 on navtest; DPPO was not evaluated on navtrain). *(See Table 4 and Section 4.2.)*

3. **Unexplained underperformance on Jaco manipulation tasks.** On the two Jaco tasks in ExORL (Table 1), DIPOLE achieves 117 ± 18 (reach-top-right) and 110 ± 12 (reach-top-left), roughly **half** the performance of IFQL (193, 181) and FQL (224, 222). Even the simpler DIPOLE w/o rs variant (84, 63) underperforms both baselines. The paper acknowledges that DIPOLE "outperforms other baselines in most domains" but does not discuss or hypothesize why it fails on these manipulation tasks. Since the method is architecture-agnostic, understanding this failure pattern is important for assessing general applicability. *(See Table 1 and surrounding text.)*

### Minor

- **No discussion of computational cost.** The method trains two diffusion models (or two LoRA modules) for π⁺ and π⁻, which at minimum doubles the training cost compared to single-model methods like FQL. For the RL benchmarks, it is unclear whether π⁺ and π⁻ are separate full models or share a backbone. The paper does not discuss this trade-off. *(See Section 3.3 and Eq. 9.)*

### Trivial
None.

## Nice-to-Haves

- **DPPO navtrain comparison.** Table 4 shows DPPO only on navtest (89.0). Running DPPO on navtrain would provide a fairer RL fine-tuning baseline against the DIPOLE navtrain result (89.7).
- **ω ablation study.** The paper claims flexible controllability via ω but provides no quantitative experiment varying ω. Since the paper references Appendix D.4 for ablation studies (removed by parser), this may be present in the full submission.

## Removed Points

These points were raised in the input review but are removed for the reasons indicated:

- *"Abstract highlights the 6.5 improvement"* — The abstract mentions NAVSIM evaluation but does not cite specific numbers. Removed as factually incorrect.
- *"DIPOLE w/o rs underperforms IFQL on 6 of 9 tasks"* — DIPOLE w/o rs underperforms IFQL on all 9 ExORL tasks, not 6. The underlying observation is valid but the framing is factually wrong; the point is subsumed by the Jaco weakness.
- *"Paper says 'better performance' but not true for all categories"* — The paper says "most categories." On OGBench, DIPOLE is best in 4/6 categories, consistent with "most." Removed as misreading.
- *"No ω controllability experiment"* — The paper references Appendix D.4 for ablation studies, which is stripped by the parser. Cannot verify absence.
- *Various section-by-section observations* that are opinions (e.g., "somewhat tautological," "overclaims") rather than verifiable weaknesses.
- *Formatting and style nitpicks.*

## Novel Insights

The input review surfaces one genuinely novel insight beyond the paper's own contributions: the connection between DIPOLE's dichotomous decomposition and CFGRL (Frans et al., 2025) is drawn more sharply than the paper itself draws it. The paper notes that CFGRL can be seen as setting π⁺ ∝ μ·𝕀{A≥0} and π⁻ = μ, and criticizes it as "lack[ing] theoretical backing" with "suboptimal performance." The reviewer's framing clarifies that DIPOLE's theoretical grounding is what distinguishes it from CFGRL's heuristic use of CFG, which is a substantive distinction worth emphasizing.

## Suggestions

1. **(Required)** Add a direct comparison with the exp-weighted regression objective (Eq. 4) on a representative subset of ExORL/OGBench tasks. This is the single most important piece of evidence for the paper's central claim.
2. **(Required)** In the NAVSIM discussion, clearly separate the navtrain and navtest results. State explicitly that the navtest result is not directly comparable to baselines trained only on the training split. Consider moving the navtest result to a separate clearly marked section.
3. **(Recommended)** Discuss the Jaco underperformance — offer a hypothesis (e.g., does the dichotomous decomposition struggle in sparse-reward manipulation settings where the value landscape is flat?) and whether it is a structural limitation.
4. **(Recommended)** Report the computational cost of training two diffusion models vs. single-model baselines.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Diffusion Actor-Critic (DAC) | 6.50 | 1 | Similar topic (KL-constrained offline RL + diffusion); DIPOLE has cleaner theory and broader eval but DAC doesn't have the NAVSIM issue |
| Score Regularized Policy Optimization (SRPO) | 6.25 | 1 | Similar topic; DIPOLE has stronger theoretical contribution and broader evaluation |
| Energy-Weighted Flow Matching (QIPO) | 6.25 | 1 | Similar weighted-regression approach; DIPOLE has more novel theory and stronger results |
| Value function estimation using conditional diffusion models | 6.25 (Rejected) | 1 | Mixed reviews despite high average; DIPOLE has fewer critical concerns |
| BDQL | 3.67 | 1 | Weaker evidence and less convincing results |
| Offline-to-Online RL with Classifier-Free Diffusion Generation | 3.00 | 1 | More applied, less theoretical contribution |

**Round 1 Bracket:** 5.5–7.5

**Narrowing:** Comparing to DAC (6.50, accepted), DIPOLE has a stronger theoretical derivation and broader evaluation, but also has the NAVSIM test-split issue and missing exp-weighted baseline which DAC does not. On balance DIPOLE is comparable in quality. Comparing to QIPO (6.25, accepted), DIPOLE's theoretical contribution is more novel and its RL results are stronger. The rejected 6.25 paper had substantially more internal disagreement (8,6,3,8) and methodological concerns that DIPOLE does not share. The final score of **6.5** reflects a paper with a genuinely novel core contribution, strong RL benchmark evidence, but uneven evaluation practices that prevent it from reaching the 7+ range.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>