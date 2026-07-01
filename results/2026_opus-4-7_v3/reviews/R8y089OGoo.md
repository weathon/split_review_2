Now let me check a few more specific sections to verify claims about the NAVSIM protocol and ExORL results:Now I have a thorough understanding of the paper. Let me draft the review.Now let me proceed to calibration. Round 1 — Bracketing:Let me read the most relevant anchor papers to calibrate:Now I have enough to establish my initial bracket. Let me analyze the comparisons:

**Round 1 Bracket Analysis:**

- **Strong reject (<1.5)**: Papers like `Uj0h13lVrR.md` (1.0) are fundamentally incomplete. DIPOLE is far stronger.
- **Reject (1.5-3.5)**: Papers like `mzJAupYURK.md` (3.0, "Stable Consistency Tuning") have significant methodological issues. DIPOLE is clearly better.
- **Borderline reject (3.5-5.5)**: `CKqiQosLKc.md` (3.75, "DQS") was criticized as lacking novelty; `StkLULT1i1.md` (5.0, "Q-Score Matching") had novel ideas but weak experiments (2 baselines, 6 tasks). DIPOLE has substantially stronger experiments and novelty.
- **Borderline accept (5.5-7.5)**: `xCRr9DrolJ.md` (6.25, "SRPO") was accepted but called "incremental over IDQL." `svp1EBA6hA.md` (6.5, "CTRL") was accepted with concerns about scalability. `Nvw2szDdmI.md` (7.0, "DDO") had rigorous theory with convergence guarantees. DIPOLE has broader experiments than SRPO and CTRL, but less rigorous theory than DDO.
- **Accept (7.5-8.5)**: `fV0t65OBUu.md` (8.0) had strong theoretical + empirical contributions.

**Initial bracket: 6.0 to 7.0**

DIPOLE's mathematical decomposition is more novel than SRPO (6.25) and its experimental breadth (39 tasks + 1B NAVSIM model) exceeds CTRL (6.5), but the missing direct stability evidence and unacknowledged approximation prevent it from reaching DDO's level (7.0).

Now let me write the final consolidated review:Now I have all the information needed. Let me compile the final review.

## Summary
DIPOLE proposes a novel RL algorithm for diffusion policy optimization that decomposes the optimal policy—under a modified KL-regularized objective—into two "dichotomous" policies trained with bounded sigmoid regression weights: one reward-maximizing (π⁺) and one reward-minimizing (π⁻). At inference, the optimized policy is recovered by linearly combining scores of both policies, mirroring classifier-free guidance (CFG) and enabling inference-time control of greediness via a tunable parameter ω. The method is evaluated across 39 offline RL tasks (ExORL + OGBench), 4 offline-to-online tasks, and a 1-billion-parameter VLA model on the NAVSIM autonomous driving benchmark.

## Strengths
- **Mathematically clean decomposition with bounded weights.** The factorization of the optimal policy into sigmoid-weighted dichotomous terms (Eqs. 7–9) eliminates loss explosion from exponential weighting (Eq. 4) by construction. The weights σ(βG) and 1−σ(βG) are bounded in [0,1], which is not a clipping heuristic but emerges from the objective's structure. This directly and elegantly addresses the stated instability problem.

- **Genuine and practically useful connection to CFG.** The score combination in Eq. 10, ε̃ = (1+ω)ε⁺ − ω·ε⁻, precisely mirrors the CFG mechanism. This is not a surface-level analogy: the entire CFG infrastructure (tuning guidance scale at inference time without retraining) applies to the RL setting. Competing methods that must retrain with different β lack this flexibility.

- **Broad evaluation and demonstrated scalability.** The paper covers 39 offline RL tasks, 4 offline-to-online tasks, and scales to a 1B-parameter VLA model on NAVSIM (Section 4.2). The LoRA-based implementation (Section 3.3) avoids full model duplication, and the 1.4-point PDMS improvement on navtrain (88.3→89.7) under comparable conditions confirms the method works at scale.

- **Dual utilization of data.** π⁺ learns from high-return samples while π⁻ learns from low-return samples (Eq. 9), resolving the data inefficiency of exp-weighted regression where low-return samples are wasted and high-return samples dominate the loss.

- **Clear differentiation from CFGRL.** The paper (line 119) explicitly shows that CFGRL can be viewed as setting π⁺ ∝ μ·𝕀_{A≥0} and π⁻ = μ, using binary indicator weights and identical positive/negative weights. DIPOLE's smooth sigmoid reweighting provides a theoretically grounded improvement.

## Weaknesses

### Fatal
None

### Major
- **Central stability claim lacks direct empirical evidence.** The paper's primary selling point is "stable and controllable diffusion policy optimization" (abstract, introduction). Stability is argued theoretically via bounded sigmoid weights (Section 3.1–3.2, Figure 1), but no training loss curves, gradient norms, or any direct stability comparison with exp-weighted regression is presented anywhere in the main paper. The paper states that exp-weighted regression causes "exploding loss and destabilizing the training process" (line 74 on Section 3.1) but never directly shows this happening with competing methods or its absence with DIPOLE. For a paper whose main narrative arc centers on stability, this gap between the theoretical argument and empirical demonstration is significant.

- **Score combination at intermediate diffusion timesteps is approximate but presented as exact.** Eq. 10 derives the score relationship for the *clean distribution* π\*. However, during inference (line 115), the combined noise predictor ε̃(a_t, s, t) = (1+ω)ε⁺(a_t, s, t) − ω·ε⁻(a_t, s, t) is applied at every diffusion timestep t, operating on noisy marginals p⁺_t and p⁻_t. There is no guarantee that combining noisy marginal scores corresponds to the noisy marginal of a single coherent distribution at all timesteps. This is the well-known approximation underlying CFG, and it works empirically, but the paper transitions from the clean-distribution derivation (Eq. 10) to the practical implementation without acknowledging the approximation. The theoretical grounding is overstated relative to what the derivation actually establishes.

### Minor
- **Persistent gap on Jaco manipulation tasks.** Even with rejection sampling, DIPOLE scores 117/110 on Jaco reach tasks vs. IFQL's 193/181 and FQL's 224/222 (Table 1). This is a substantial gap on a specific task category that the paper does not discuss. Some analysis of why the method struggles on these manipulation tasks—whether due to the sigmoid weighting, the score combination approximation, or data characteristics—would help readers understand the method's limitations.

- **Greedified objective (Eq. 5) motivated primarily by downstream properties.** The paper explicitly states: "At first glance, it appears to be complex; however, as we will show in the later derivation, its resulting closed-form optimal solution can lead to a remarkably elegant form" (Section 3.2, line 81). While the paper provides some independent motivation (regularizing towards greedier reference policies, line 89), the primary justification for Eq. 5 is the decomposition it enables. This is common practice in ML algorithm design, but more transparent framing—acknowledging the objective was designed to yield bounded terms—would be more honest than the current "greedified policy optimization" narrative.

### Trivial
None

## Nice-to-Haves
- Direct training stability analysis (loss curves, gradient norms) comparing DIPOLE vs. exp-weighted regression with various β values—this would convert the major weakness into the paper's strongest empirical argument.
- Analysis of what π⁻ actually learns in practice (e.g., visualizing preferred actions) to confirm the dichotomous decomposition genuinely separates good from bad behavior.
- Systematic performance-vs-ω sweep across tasks to substantiate the "controllable generation" claim.
- Wall-clock time comparison of training two models/LoRA adapters vs. single-model baselines.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"NAVSIM navtest results involve training on test-split data, complicating the comparison"**: Removed. Table 4 includes "DP-VLA w/ DPPO navtest" (89.0 PDMS) trained under the identical protocol, making the within-protocol comparison fair (DIPOLE 94.8 vs. DPPO 89.0). The paper also reports navtrain results (89.7) for comparison with standard baselines. The paper clearly describes the navtest setting as an "RL application scenario where RL can be applied in human take-over situations" (Section 4.2, line 211).

- **"DIPOLE w/o rejection sampling underperforms IFQL and FQL on several ExORL tasks" as a major issue**: Demoted. IFQL itself uses rejection sampling by default (line 136: "utilize imitation pre-trained diffusion or flow models with rejection sampling during inference"). Comparing DIPOLE w/o rs to IFQL is apples-to-oranges. The fair comparison is DIPOLE (with RS) vs. IFQL (with RS), where DIPOLE wins on most tasks. The w/o rs variant is an ablation, not the primary method. The remaining Jaco gap is retained as a minor weakness.

- **"Sigmoid weighting might introduce information loss near the midpoint"**: Removed. This is speculative—no evidence that this actually degrades performance, and the strong results across most tasks suggest it does not.

- **"LoRA may have insufficient capacity to capture the difference between π⁺ and π⁻"**: Removed. The strong NAVSIM results (94.8 PDMS) empirically demonstrate LoRA has sufficient capacity for this decomposition.

- **"Reward function for NAVSIM is underspecified / may be optimizing a proxy for the test metric"**: Removed. This concern applies to essentially all RL-for-driving papers and is not specific to DIPOLE. The paper mentions safety, progress, and comfort components (line 125), which are standard.

## Novel Insights
The paper's central insight—that a sigmoid-augmented KL-regularized objective decomposes into two bounded-weight policies whose scores combine via the CFG mechanism—bridges two previously distinct literatures (RL policy optimization and diffusion generation control) in a way that yields practical benefits. The observation that exp(βG) = σ(βG)/(1−σ(βG)) · exp((ω-1)βG) can be restructured to yield bounded training losses while preserving greedy optimality is elegant. The resulting ability to tune greediness at inference time without retraining is a concrete practical advantage that, to my knowledge, is novel in the diffusion RL literature.

## Suggestions
- Add training loss/gradient norm comparison between DIPOLE and exp-weighted regression (Eq. 4) as primary empirical evidence for the stability claim. This is the single highest-impact revision.
- Explicitly acknowledge in Section 3.2 that applying Eq. 10 at all diffusion timesteps is an approximation (as in CFG), even though it works well empirically.
- Analyze Jaco task underperformance to characterize method limitations.
- Frame the derivation of Eq. 5 more transparently as "we seek an objective whose solution decomposes into bounded terms" alongside the greedified regularization motivation.

## Score and Decision

**Anchor papers retrieved (all rounds):**

| Paper | Path | Avg Score | Round | Comparison to DIPOLE |
|-------|------|-----------|-------|---------------------|
| KL Divergence GFlowNets | Uj0h13lVrR.md | 1.0 | 1 | Far weaker: fundamentally incomplete work |
| IC-Light | u1cQYxRI1H.md | 10.0 | 1 | Different domain (image editing), not comparable |
| Clothing-Irrelevant ReID | 5lUdTogEL3.md | 1.0 | 1 | Far weaker: different domain, fundamental issues |
| NEMESIS Jailbreaking | 5kMwiMnUip.md | 1.4 | 1 | Far weaker: different domain, fundamental issues |
| CL-DiffPhyCon | PiHGrTTnvb.md | 3.0 | 1 | Weaker: diffusion control but much narrower evaluation |
| No MCMC Teaching | 46tjvA75h6.md | 3.0 | 1 | Weaker: EBM+diffusion training, limited experiments |
| Stable Consistency Tuning | mzJAupYURK.md | 3.0 | 1 | Weaker: MDP framing of diffusion, insufficient experiments |
| D³PM Causal Discovery | TRHyAnInUC.md | 3.25 | 1 | Weaker: different domain, instability concerns |
| DQS (Energy-based) | CKqiQosLKc.md | 3.75 | 1 | Weaker: limited novelty ("diffusion in SAC"), few benchmarks |
| BDQL | gEdg9JvO8X.md | 3.67 | 1 | Weaker: offline RL + diffusion but less novel decomposition |
| Latent Weight Diffusion | XLCqhdaMpy.md | 4.5 | 1 | Weaker: narrower contribution, less rigorous |
| Q-Score Matching | StkLULT1i1.md | 5.0 | 1 | Weaker: novel idea but much weaker experiments (2 baselines, 6 tasks) |
| SRPO | xCRr9DrolJ.md | 6.25 | 1 | Comparable: accepted but called "incremental over IDQL"; DIPOLE has more novelty and broader experiments |
| CTRL | svp1EBA6hA.md | 6.5 | 1 | Comparable: RL+diffusion control; DIPOLE has broader experiments and scales to 1B model |
| DDPP | Ombm8S40zN.md | 6.25 | 1 | Comparable: steering diffusion with RL; DIPOLE has cleaner decomposition |
| DDO | Nvw2szDdmI.md | 7.0 | 1 | Stronger theory with convergence guarantees; DIPOLE has stronger practical evaluation |
| Complex Fluid Diffusion | uKZdlihDDn.md | 7.6 | 1 | Different domain; stronger empirical rigor within its scope |
| Optimal Covariance Matching | fV0t65OBUu.md | 8.0 | 1 | Stronger: tight theory + empirical; different focus |
| SAR Diffusion LM | tyEyYT267x.md | 8.0 | 1 | Stronger: SOTA language modeling results; different domain |
| Policy Gradient Confounded POMDPs | 8BAkNCqpGW.md | 8.0 | 1 | Stronger theory; different focus |

**Round 1 bracket: 6.0–7.0**

DIPOLE is clearly stronger than rejected diffusion RL papers (QSM at 5.0, DQS at 3.75, BDQL at 3.67) due to its more novel contribution and much broader evaluation. It is comparable to or slightly above accepted papers like SRPO (6.25) and CTRL (6.5) in novelty and experimental scope. It falls below DDO (7.0) which provides rigorous convergence guarantees that DIPOLE lacks. The missing stability evidence and unacknowledged approximation prevent it from reaching the upper end of the bracket.

**Final calibrated score: 6.5**

The paper presents a genuinely novel and mathematically elegant decomposition that addresses a real problem (exponential weight instability in diffusion RL) with practical utility (inference-time tunability via CFG). The experimental breadth is strong, including scaling to a 1B model. However, two major weaknesses prevent a higher score: (1) the central stability claim is argued only theoretically, never measured empirically, and (2) the score combination approximation at intermediate timesteps is presented as exact. These are addressable weaknesses that do not invalidate the contribution, but they represent meaningful gaps between claims and evidence. The paper is a solid borderline accept.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>