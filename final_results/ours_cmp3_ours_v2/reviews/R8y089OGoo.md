## Summary

DIPOLE proposes a dichotomous diffusion policy optimization framework for RL fine-tuning of diffusion policies. The key idea is to replace the unstable exponential weighting in KL-regularized RL with a bounded sigmoid weighting, which decomposes the optimal policy into a pair of "dichotomous" policies (positive/reward-maximizing and negative/reward-minimizing) that can be stably trained and combined at inference time via a classifier-free-guidance-style linear combination. The method is evaluated on 39 RL tasks across two benchmarks (ExORL, OGBench) in offline and offline-to-online settings, and scaled to a 1B-parameter vision-language-action model for autonomous driving on NAVSIM.

## Strengths

1. **Clean theoretical derivation (Sections 3.1–3.2).** The paper correctly identifies the two key problems with exp-weighted KL-regularized RL (Eq. 4): unbounded weight explosion and loss domination by high-return samples. The proposed fix — replacing the unstable exponential weight with a bounded sigmoid weight via a greedified KL objective (Eq. 5) — is conceptually elegant. The derivation from Eq. (5) through Theorem 1 to the dichotomous decomposition (Eqs. 7–8) and the inference rule (Eq. 10) is mathematically sound and self-contained. The explicit connection drawn to classifier-free guidance (Section 3.2) provides genuine insight into why the method works.

2. **Extensive RL benchmark evaluation.** The paper evaluates on 39 tasks across ExORL and OGBench with 8 seeds each — this is a thorough empirical study. On ExORL (Table 1), DIPOLE with rejection sampling achieves the highest score on 8 of 9 tasks, often by a clear margin. The offline-to-online evaluation (Table 3) further demonstrates practical utility.

3. **Scaling to a billion-parameter VLA model (Section 4.2).** Demonstrating DIPOLE on a 1B-parameter real-world driving model (DP-VLA) using LoRA-based dichotomous policy fine-tuning goes well beyond standard RL benchmarks and provides strong evidence that the method is practical for realistic applications.

## Weaknesses

### Fatal
None.

### Major

1. **NAVSIM "navtest" evaluation is ambiguous and potentially invalid (Table 4, Section 4.2).** The paper states: *"We also consider an RL application scenario where RL can be applied in human take-over situations or complex environments lacking ground-truth supervision. To address this, we provide a variant of our model trained on the test split without using any ground-truth."* (line 211). The resulting "DP-VLA w/ DIPOLE navtest" achieves 94.8 PDMS — the paper's best score (bolded) and the basis for the claim of a "substantial 6.5-point PDMS improvement." If "test split" here refers to the same "public test split" used for evaluation (as stated earlier in the same paragraph), this constitutes test-set contamination. The paper does not clarify whether navtest is a separate data split used only for generating RL training rollouts (distinct from the evaluation set) or whether it is the evaluation set itself. Either way, the presentation is ambiguous, and the headline result lacks the standard guarantees of a clean evaluation. The navtrain-trained variant (89.7, a clean 1.4-point gain) provides cleaner evidence. The authors should (a) explicitly clarify the relationship between navtest, navtrain, and the evaluation split, or (b) reframe the autonomous driving claims around the navtrain result.

2. **No direct comparison against the exp-weighted regression method it aims to replace (Tables 1–3).** The paper's entire motivation (Section 3.1) is that the simple exp-weighted regression objective (Eq. 4, from Zheng et al. 2024, Kang et al. 2023, Lee et al. 2023) suffers from instability and loss domination. Yet none of the baselines implement this approach. The comparisons are against methods using different mechanisms entirely (expectile regression in IFQL, value maximization in FQL, indicator-function-based CFG in CFGRL). Without an exp-weighted regression baseline (a diffusion policy trained with Eq. 4 and appropriate β clipping), the reader cannot assess whether the dichotomous decomposition actually solves the problem it was designed for, or whether DIPOLE works well for other reasons (e.g., the two-model ensemble or rejection sampling). This gap decouples the paper's motivation from its evidence.

### Minor

1. **Jaco task failures are undiscussed.** On two of nine ExORL tasks (jaco reach-top-right and reach-top-left), DIPOLE with rejection sampling scores 117 and 110, substantially below IFQL (193, 181) and FQL (224, 222). These are manipulation tasks (as opposed to locomotion), and the failure may indicate a systematic limitation. The paper claims DIPOLE "fully surpasses IQL" but does not discuss these underperformances.

2. **The DP-VLA base model drives much of the apparent SOTA on NAVSIM.** The imitation-pretrained DP-VLA (88.3 PDMS) already exceeds all prior published methods (best prior: Hydra-MDP at 86.5). DIPOLE fine-tuning on the clean navtrain split adds only 1.4 points. This means the primary source of improvement over prior work may be the architecture/pretraining, not the RL algorithm. The paper should more clearly separate architectural contributions from algorithmic ones.

3. **No computational cost comparison.** Training two diffusion models (or two LoRA modules) doubles per-step compute relative to single-model approaches. The paper does not report wall-clock time, FLOPs, or training steps to convergence, so the reader cannot assess whether the performance gains justify the additional cost.

### Trivial
None.

## Nice-to-Haves
- An ablation of ω sensitivity in the main paper (currently deferred to the stripped appendix) would strengthen the claim of controllable generation.
- The connection to classifier-free guidance is insightful; a more explicit comparison to CFGRL's indicator-function-based approach would further clarify the differences.
- A brief discussion of why DIPOLE underperforms on Jaco manipulation tasks (compared to locomotion) would improve completeness.

## Removed Points

The following points from the Harsh Critic's input were removed after cross-checking against the paper:

1. **"Inference-time combination of scores reintroduces unboundedness"** — REMOVED because the same linear combination is used in standard classifier-free guidance (Eq. 10 explicitly mirrors CFG). The paper's stability claims apply to training; the CFG-style inference is a standard, well-understood procedure. The critic's concern conflates training stability with inference behavior in a way that, if valid, would also invalidate CFG itself.

2. **"OGBench results are more mixed than text suggests"** — REMOVED because the paper claims "best or near-best performance," which accurately describes Table 2: DIPOLE leads in 4/6 categories and is competitive (within error bars) in the other 2. The claim is appropriately qualified.

3. **"The greedifier claim (Eq. 5) needs more justification"** — REMOVED because Theorem 1 provides the closed-form solution of Eq. (5). The "greedier" nature follows from the value-weighted reference policy (σ(βG)/Z-weighted μ) instead of the flat μ in Eq. (2). This is adequately explained. The proof in the (stripped) Appendix B would further clarify.

4. **Formatting/style nitpicks and missing appendix/proof concerns** — REMOVED per policy (parser artifacts and stripped appendix are not author errors).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
1. Add an exp-weighted regression baseline (Eq. 4 with appropriate β clipping) to the RL experiments to directly test the paper's core thesis.
2. Clarify the NAVSIM protocol: explicitly state whether navtest is a separate training rollout split or the evaluation test split, and ensure headline claims are anchored to the clean navtrain result.
3. Discuss the Jaco task failures to improve evaluation completeness and provide insight into the method's limitations.
4. Report wall-clock time or relative compute costs to help readers assess the practical trade-off of training two models.

---

**Calibration anchors retrieved across rounds:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Diffusion Actor-Critic (DAC) | 6.50 | R1 | Similar in having clean theory + extensive experiments + some baseline concerns; DIPOLE has a stronger theoretical contribution but a more concerning evaluation gap (NAVSIM) |
| Score Reg. Policy Opt. (SRPO) | 6.25 | R1 | Similar theory + experiments; DIPOLE has broader evaluation scope (39 vs D4RL tasks) and a real-world large-scale demonstration |
| Energy-Weighted Flow Matching (EFM) | 6.25 | R2 | Similar weighted-regression approach; DIPOLE's dichotomous decomposition + CFG connection is more novel, but EFM had fewer evaluation concerns |
| Offline-to-Online RL w/ CFDG | 3.00 | R1 | Much weaker — incremental contribution with marginal gains; DIPOLE is clearly stronger in both theory and empirical scope |

**Initial bracket (Round 1):** Between 5.5 and 7.5 — DIPOLE has stronger theory and broader experiments than the 3.0–5.0 papers, but two significant weaknesses prevent it from reaching the 7.5+ tier.

**Narrowing (Round 2):** Comparing against DAC (6.50) and EFM (6.25) — DIPOLE's NAVSIM ambiguity is a more serious evaluation concern than DAC's Q-ensemble confounding or EFM's missing baselines, which pulls the score slightly lower. However, DIPOLE's theoretical novelty (dichotomous decomposition + CFG connection) is stronger than either comparator. Balanced: **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>