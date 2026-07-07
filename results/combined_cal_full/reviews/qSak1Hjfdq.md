Now I have the calibration data. Let me compare my draft's weighted items against the anchors.

**Weight comparison:**

My draft: strengths all strongly positive (+3.17 to +4.99), weaknesses all modestly negative (-0.16 to -1.68). Net strongly positive.

**Closest anchor: `2oKkQTyfz7.md` — GSA-VLN, avg 6.40.** That paper had a -9.94 weakness (reviewer claiming limited novelty), plus several other negative items. The current paper has no weakness approaching that severity. The current paper's method (TuKA tensor decomposition) is more technically novel than GSA-VLN's GR-DUET (graph+memory extension), and the experiments cover 12 baselines vs. fewer for GSA-VLN.

**Anchor `OALIb8oNfl.md` — PEFT via structural integrity, avg 5.75 (scores 6,6,6,5).** Conceptually similar in using higher-dimensional parameterizations, but this paper has stronger experimental validation and a concrete downstream application (VLN).

**Anchor `YR79EyejsG.md` — Task-unaware lifelong learning, avg 5.75.** Had severe weaknesses including statistical significance concerns (-5.23) and simulation-only evaluation (-5.20). The current paper includes real-world deployment and has no such concerns.

The current paper's weaknesses are all minor/trivial, while its strengths are substantial and well-supported. The closest topical anchor is GSA-VLN at 6.40, and this paper is clearly stronger. I place it at **7.0**.

**Bracket:** Round 1 placed the paper between 6.5 and 7.5. Round 2 calibration narrowed this to 7.0 based on weighted-item comparison against the GSA-VLN anchor (6.40), where the current paper lacks any heavy-negative item comparable to GSA-VLN's -9.94 novelty criticism, while sharing similar strong positive weights for problem formulation and experimental rigor.

---

## Summary

This paper formalizes the AML-VLN (All-Day Multi-Scenes Lifelong VLN) problem, where an embodied agent must continually learn to navigate across multiple scenes × multiple degraded imaging environments (normal, low-light, overexposure, scattering) without forgetting. The authors propose Tucker Adaptation (TuKA), which uses a 4th-order Tucker decomposition to encode multi-hierarchical navigation knowledge: a shared core tensor and encoder/decoder capture common skills, while separate factor matrix rows serve as scene-specific and environment-specific experts. A decoupled knowledge incremental learning (DKIL) strategy with EWC, consistency, and orthogonality losses manages forgetting. The resulting agent, AllDayWalker, is evaluated on 24 navigation tasks across simulation and real-world scenes, consistently outperforming 12 LoRA-based baselines by large margins (65% avg SR vs 44% for the best baseline, 11% F-SR vs 36%).

## Strengths

- **Novel and well-motivated problem formulation.** The AML-VLN setting — lifelong learning across the combinatorial space of scenes × degraded environments — is a natural and practically relevant extension of prior VLN work, which has only studied single-scene adaptation or simple domain shifts. The paper correctly identifies why separate LoRA modules or MoE-LoRA variants cannot efficiently share knowledge across both dimensions.

- **Tucker decomposition is a structurally clean fit.** Factorizing along a scene axis (U³) and an environment axis (U⁴) with shared encoder/decoder (U¹, U²) and core tensor (G) enables combinatorial parameter sharing: for any new (scene, environment) pair, only the two corresponding expert rows need to be learned or retrieved. This is architecturally more natural than flattening both dimensions into a single task ID.

- **Extensive and well-designed experiments.** The benchmark spans 24 tasks (5 simulation scenes × 4 environments + 2 real-world scenes × 2 environments), compares against 12 baselines including recent methods (SD-LoRA, BranchLoRA, HydraLoRA, O-LoRA), and reports both standard metrics (SR, SPL, OSR) and forgetting metrics (F-SR, F-SPL, F-OSR). The generalization test on 6 completely unseen scenarios (Table 5) is a particularly strong addition that demonstrates compositional zero-shot transfer.

- **Large and consistent improvements.** AllDayWalker achieves 65% average SR vs 44% for the best baseline (BranchLoRA), with 11% forgetting rate vs 36% for BranchLoRA and 46% for HydraLoRA. These margins are substantial and unlikely to be artifacts of hyperparameter tuning. Real-world deployment on two additional scenes further validates the approach beyond simulation.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Missing oracle upper bound.** The paper acknowledges (Sec 2, line 36) that storing all past adaptation weights separately and loading them during inference is a trivial solution, but does not evaluate this baseline. An oracle with per-task parameters (no sharing) would calibrate the cost of parameter sharing and make the 11% F-SR more interpretable. While the 12-baseline comparison is already strong, this control would sharpen the evaluation.

- **No hyperparameter sensitivity analysis.** The loss function (Eq. 9) balances four terms with λ₁=0.2, λ₂=0.2, λ₃=0.1, giving the primary navigation loss a weight λ=0.5 — equal to the combined regularization. Without any sensitivity analysis, the reader cannot assess whether the reported improvements are robust to these values or depend on careful tuning that might benefit other methods as well.

- **No limitations discussion.** The paper does not discuss limitations such as: (a) U³ and U⁴ are fixed-size matrices requiring the number of scenes M and environments N to be known in advance; (b) CLIP-based expert retrieval could fail when an unseen scene is visually similar to a trained scene but semantically different; (c) sensitivity to task ordering in the lifelong sequence; (d) computational/memory overhead of the core tensor (262k parameters per layer with r₃=64, r₄=64).

### Trivial

- **Notational issue in Eq. 6.** F_θ,t appears on both sides of the exponential moving average update, which is technically incorrect (it should distinguish the new and old Fisher estimates).

- **Near-duplicate row in Table 3.** The configuration "✓ ✓ ✓" appears twice (rows 3 and 6) with the same SR (65), F-SR (11), SPL (58), F-SPL (18) but slightly different OSR (69 vs 68). This needs clarification.

## Nice-to-Haves

- An analysis of task ordering effects on final performance.
- A computational cost comparison (training time, memory usage) between TuKA and the baselines.
- Reporting absolute forgetting drops alongside the relative F-SR metric.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **Table 3 internal inconsistency (per-task params should yield near-zero forgetting)** — REMOVED. The reviewer assumed ✗✗✗ (separate G, U¹, U² per task) means fully per-task parameters. However, U³ and U⁴ expert rows are always shared across tasks that share the same scene or environment (the ablation controls only G, U¹, U²). A 10% F-SR in ✗✗✗ is expected because scene/environment expert rows get overwritten when revisited.

2. **"High-dimensional vs 2D" framing inflation** — REMOVED. The paper's description is technically accurate: the Tucker decomposition operates on a 4th-order tensor 𝒳 ∈ ℝ^{a_l × b_l × M × N}, which is genuinely a higher-order tensor. The final ΔW is a 2D matrix (required to interface with the backbone), but this is standard for tensor methods and does not make the framing misleading.

3. **Various section-by-section observations** (extending MoE-LoRA without tensor framework, Table formatting, rank comparability, synthetic degradation realism) — REMOVED as speculative, parser artifacts, or standard practices.

## Novel Insights

The most interesting observation from the review process is that the generalization experiment (Table 5) — where TuKA composes previously learned scene and environment experts for zero-shot adaptation to unseen (scene, environment) pairs — is the strongest evidence for the decoupled expert structure actually working as intended. The 55% average SR on unseen scenarios vs 39–40% for baselines is arguably more compelling than the main benchmark results, because it directly validates the compositional knowledge sharing claim. The paper presents this as one of several ablations, but it could be elevated to a central result.

## Suggestions

1. Add the oracle baseline (per-task parameters with no sharing) to calibrate the cost of parameter sharing.
2. Include a hyperparameter sensitivity study for λ₁, λ₂, λ₃.
3. Add a limitations section covering fixed expert matrix sizes, CLIP retrieval failure modes, and task ordering sensitivity.
4. Correct the notational issue in Eq. 6 and resolve the near-duplicate row in Table 3.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>