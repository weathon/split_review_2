## Summary

This paper proposes CP4D, a compositional framework for physics-aware 4D scene generation. The key idea is to decompose a scene into a static 3D background and dynamic foreground objects, generate 3D representations for each using off-the-shelf models, simulate foreground motion with a hybrid strategy (physical simulators + video diffusion model refinement), and compose them into a coherent 4D scene. The main technical contributions are using SDS to refine VLM-estimated physical parameters and object displacements, and a depth-aware heuristic for scene composition.

## Strengths

- **Well-motivated problem framing.** The paper correctly identifies a genuine limitation of existing 4D generation methods — they produce physically inconsistent dynamics. The compositional decomposition into static background + dynamic foreground (Sec. 4) is a sensible high-level design that reflects real-world scene structure.

- **Conceptually clean hybrid motion synthesis strategy.** Combining physical simulators (for law-based dynamics) with video diffusion model priors (for visual refinement) is the most interesting aspect of the paper. The two failure modes it targets — inaccurate VLM-estimated material parameters and coarse grid-based collision detection — are real, and using SDS to address both is a coherent strategy (Sec. 4.2, Eq. 4–5).

- **Strong quantitative outcomes on the reported metrics.** Tables 1 and 2 show the method achieving the highest scores across most dimensions (VBench motion 0.998, WorldScore 3D consistency 95.55, GPT-4o physical realism 0.694), outperforming competitive baselines by visible margins in several cases.

## Weaknesses

### Fatal
None.

### Major

1. **Evaluation on only 17 examples with no error bars or significance testing.** The paper states "We curate a dataset of 17 examples for evaluation" (Sec. 5.1). For a generative pipeline with multiple stochastic components (T2I, image editing, image-to-3D, VLM prompting, SDS refinement, L2 optimization), 17 examples is far too few to draw reliable conclusions. No variance, error bars, or statistical significance measures are reported. The reported differences (e.g., VBench Motion 0.998 vs 0.997) may not be meaningful. This undermines the claim of "consistently outperforming" baselines.

2. **Mismatch between "4D scene generation" claims and what is actually evaluated.** The paper claims to produce "explorable and interactive 4D scenes" with "flexible viewpoint changes" (Abstract, Sec. 4 overview — line 66). Yet the evaluation relies entirely on rendered 2D video metrics (VBench, WorldScore, GPT-4o). There is no explicit evaluation of novel view synthesis quality, no free-viewpoint rendering demonstration, and no quantitative geometry metric. Additionally, the baselines include pure 2D video generators (Sora, Runway, CogVideoX, Wan) that produce no 3D representation at all — comparing them on "3D Consistency" (WorldScore) conflates fundamentally different problem statements. Only DreamGaussian4D is a proper 4D baseline, and it performs extremely poorly across the board (e.g., WorldScore 3D consistency 40.29 vs CP4D's 95.55), raising fairness questions.

3. **Unresolved differentiability gap in the physics simulation loop.** The paper claims to use "differentiable simulators" (Contributions, line 38) and optimizes material parameters Θ via SDS (Eq. 4). The gradient ∂V/∂Θ must flow through the physics simulation that produces G_f^t. However, the paper uses three solver types (Sec. 4.2): MPM (differentiable in principle), a rigid-body solver, and a Position-Based Dynamics (PBD) solver for fluids. Standard rigid-body solvers and PBD are **not** differentiable. The paper provides no discussion of how gradients are obtained through these solvers — whether they are implemented in a differentiable framework, whether gradients are approximated, or whether the optimization is only applied to MPM-simulated objects. This is a structural methodological gap: either the method does not work as claimed for non-MPM objects, or a crucial implementation detail is missing.

### Minor

4. **Incremental technical novelty relative to prior work.** The paper chains together many off-the-shelf components (GPT-4o, Qwen-Image, Qwen-Image-Edit, SAM, Depth Anything, Trellis, Viewcrafter, physical simulators, VLMs, video diffusion models). The actual methodological contributions are: (a) using SDS to refine VLM-estimated physical parameters (Eq. 4), (b) using SDS to refine object displacement variables for collision correction (Eq. 5), and (c) a depth-aware heuristic for scale initialization (Eq. 8). However, SDS-based optimization of material parameters is already present in prior work that the paper itself cites (DreamPhysics, PhysGen3D, cited in Sec. 2.2). The displacement refinement (Eq. 5) applies the same mechanism to a different variable. The depth-aware heuristic is straightforward geometry. The paper's real value lies in system integration, but it frames this as a "novel paradigm," which overstates the contribution.

5. **Ablation is limited to one qualitative example with two components.** The ablation (Fig. 5) tests only two components — material optimization and position optimization — on a single qualitative example (spheres). There is no ablation of Stage I's image editing approach, no ablation of the composition mechanism in Stage III, no ablation testing the contribution of the physics simulator itself (video diffusion only, without physics), and no quantitative ablation results. This makes it difficult to attribute performance to specific design choices.

6. **No limitations, failure analysis, or negative results.** The paper presents no limitations section and no discussion of failure modes. Given the pipeline's complexity (multiple pre-trained models, VLM-based parameter estimation, SDS optimization), failures must occur. The absence of any failure analysis makes it impossible to understand the method's practical boundaries.

### Trivial

- On VBench Imaging quality, CP4D (0.641) is second to Runway (0.644), which the paper reports honestly but downplays.

- GPT-4o-as-judge evaluations are known to have reliability concerns; with 17 examples and no inter-annotator metrics, the GPT-4o results (Table 2) are suggestive at best.

## Nice-to-Haves

- **Expanded evaluation.** The single most impactful improvement would be expanding the test set to 100+ examples with diverse scenes (rigid, deformable, fluid, multi-object), reported with error bars across multiple runs. This directly addresses the paper's own goals.

- **Evaluate actual 4D capability.** Rendering novel-view trajectories and measuring multi-view consistency (e.g., LPIPS between rendered views) would directly substantiate the claimed "explorable and interactive 4D scenes."

- **Computational cost reporting.** The paper does not report runtime or GPU hours for the full pipeline, which is relevant information for a multi-stage system.

- **Disclosure of failure cases.** A representative set of outputs including mediocre/ failing cases, with analysis of what goes wrong and why, would help readers understand the method's robustness.

## Removed Points

These points were raised in the input review but are removed per filtering rules:

- **Typo on line 27** ("foreground objects and foreground objects"): Removed per hard rule against formatting/style/typography nitpicks.
- **Missing appendix details** (Appendix B, C, D): Removed per hard rule — appendix content is stripped by the parser and exists in the original submission.
- **Dependency on image editing model quality**: Removed — this is a general concern applicable to any multi-component pipeline and is not a specific identified flaw in the paper's claims.
- **Data/code release status**: Removed per hard rule — questioning the availability of cited models/tools/references.
- **Paper not well-positioned in related work**: Removed per hard rule — do not mention missing related works without external sources to confirm.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Substantially expand the evaluation set (100+ examples) and report error bars or significance tests.
2. Clarify the differentiability of the physics solvers for each object type — or state explicitly which objects' parameters can be optimized with SDS and which cannot.
3. Add an explicit evaluation of novel-view rendering to substantiate the "4D" and "explorable" claims.
4. Add a limitations section with representative failure cases.
5. Provide a fairer comparison by including a proper 4D-consistent baseline (e.g., removing the physics simulator while keeping the rest, or removing the video diffusion refinement while keeping physics).

## Score and Decision

**Calibration Anchors** (all retrieved from deepreview_13k_calibration):

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| ElastoGen (j50c2tkQUu.md) | 4.33 | R1 | Knowledge-driven 4D elastodynamics, rejected for poor writing and insufficient evaluation; CP4D has stronger motivation but shares evaluation weakness |
| Sync4D (O0RIrM5iqX.md) | 4.50 | R1 | Physics-based 4D generation with video guidance, rejected for lack of quantitative metrics; CP4D has more metrics but on only 17 examples |
| Physics3D (k3JgQXtpJq.md) | 4.75 | R1 | Learning physical properties via video diffusion, rejected for limited novelty; CP4D has similar novelty concerns plus differentiability issue |
| OmniPhysGS (9HZtP6I5lv.md) | 6.40 | R1 | Accepted physics-based dynamics generation; has more extensive evaluation and clearer technical contribution |
| Consistent4D (sPUrdFGepF.md) | 5.00 | R2 | Accepted system paper; better evaluation standards though similar pipeline complexity |

**Round 1 Bracket:** 3.5 – 5.5. CP4D shares weaknesses with Sync4D (4.50) and Physics3D (4.75) — limited evaluation, incremental novelty — but has the additional unresolved differentiability gap that those papers do not. The core idea is well-motivated, but the evidence is insufficient to support the strength of the conclusions.

**Final Score Rationale:** The paper presents a well-motivated pipeline with strong initial results, but the evaluation is too narrow (17 examples, no error bars) to support the claimed superiority, the 4D capability asserted in the framing is not directly evaluated, and there is an unresolved technical gap regarding gradient flow through non-differentiable physics solvers. The novelty is primarily at the system-integration level, which has value but is overstated as a "novel paradigm." The paper is not ready for acceptance in its current form; major revisions — particularly expanding the evaluation and resolving the differentiability issue — would be needed.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>