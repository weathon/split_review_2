Now I will finalize the review with score and decision.

## Summary

CP4D proposes a compositional pipeline for text-to-4D scene generation that decomposes the problem into: (1) independent 3D generation of static background and dynamic foreground objects using pre-trained models, (2) hybrid motion synthesis combining physics simulators with SDS refinement from video diffusion models, and (3) automated composition via monocular depth estimation and optimization. The paper addresses a genuine limitation of existing 4D generation methods that lack physical grounding.

## Strengths

- **Compositional reformulation is well-motivated.** Decomposing 4D generation into static background + dynamic foreground (Sec. 4, Fig. 1) is a clean architectural choice that avoids jointly learning spatial structure, temporal dynamics, and physics from scratch. The paper correctly identifies that independent text-to-3D generation yields stylistically incoherent results (e.g., realistic backgrounds with cartoon-like foregrounds) and addresses this via image editing before 3D reconstruction.

- **Hybrid motion synthesis targets a real limitation of pure physics simulation.** The observation that VLM-estimated material parameters are imprecise and that grid-based physics solvers produce spurious collisions due to geometric discretization (Sec. 4.2, Fig. 2) is valid. Using SDS from a video diffusion model to refine these estimates is a reasonable proposal for combining the strengths of both approaches.

- **Automated composition mechanism is practical and clearly specified.** The depth-aware heuristic for scale initialization (Eq. 8, Fig. 3) and sequential refinement strategy (scale first, then position) address the real challenge of fusing independently generated 3D assets. The optimization objective (Eq. 9) and the motivation for sequential refinement are clearly explained.

## Weaknesses

### Fatal
None.

### Major

1. **SDS-based optimization of physical parameters requires differentiable physics simulators, but the mechanism is not explained in the main methodology section.** The core technical operation defined in Eq. 4 computes ∇_Θ L_SDS = 𝔼[ω(ζ)(ε̂_ψ(V; T_f; ζ) − ε) ∂V/∂Θ]. The term ∂V/∂Θ requires differentiating through the physics simulator Φ (MPM, rigid-body, or PBD) with respect to material parameters Θ, because V is rendered from G_f^t = Φ(G_f, Q, Θ, t). While the contributions list (line 38) mentions "differentiable simulators," Sec. 4.2 provides no explanation of how any of the three solver types are made differentiable, how the gradient ∂G_f^t/∂Θ is computed, or whether approximations are used. For MPM, differentiable implementations exist in the cited literature (Hu et al., 2018), but this is not stated; for the rigid-body and PBD solvers, no reference or mechanism is given. Details are likely deferred to Appendix C, but the main methodology section should at minimum state the approach (e.g., "we implement all solvers in a differentiable framework such as Warp" or "we use adjoint methods") rather than leaving readers to infer it from a single bullet-point mention.

2. **The evaluation is too small and too weakly controlled to support the paper's strong claims.** The entire quantitative evaluation rests on **17 examples** (Sec. 5.1) for a pipeline involving at least nine distinct pretrained components. No variance, confidence intervals, or statistical significance tests are reported for any metric in Tab. 1 or Tab. 2, making it impossible to assess whether the reported improvements are reliable artifacts of the small sample. Furthermore, several of the most relevant 4D generation methods cited in the paper's own related work (TC4D, 4D-fy, Consistent4D) are **not compared against** — the only text-to-4D baseline is DreamGaussian4D (2023), which is substantially outdated given the rapid progress in this area. While the 2D video generation baselines address a different task, their inclusion is not harmful; the omission of directly comparable 4D methods is a significant gap that undermines the claim of "consistently outperforming state-of-the-art baselines."

3. **The ablation study is purely qualitative and does not validate the claimed components.** The ablation (Sec. 5.3, Fig. 5) shows a single qualitative example comparing "full model" against "w/o material opt." and "w/o position opt." No quantitative ablation results are reported for VBench, WorldScore, or GPT-4o metrics. Since the ablation tests the two core novel components of the pipeline (SDS-based material parameter optimization and position optimization), this is a significant evidentiary gap. "More ablation studies" are deferred to Appendix D, but the main paper should include quantitative ablation results to support the central claims.

### Minor

1. **GPT-4o-based "physical realism" evaluation lacks validation.** Tab. 2 relies on GPT-4o scores for "physical realism," but there is no evidence that GPT-4o's judgments correlate with actual physical correctness. GPT-4o is a general-purpose vision-language model, not a physics evaluator. While following the evaluation protocol of PhysGen3D (Chen et al., 2025a) is defensible, the paper should at minimum acknowledge this limitation or correlate GPT-4o scores with human judgments on a subset of examples.

2. **Claims of "complex physical dynamics" are oversold.** The abstract and introduction claim "faithful adherence to complex physical dynamics" (lines 9, 29, 37), but the demonstrated examples are physically simple: an orange dropping, a bottle falling and rebounding, spheres colliding, T-shirts swaying. These do not constitute "complex" dynamics by any reasonable standard. The framing should be calibrated to what is actually shown.

3. **No discussion of limitations or failure modes.** The pipeline involves many components (LLM, text-to-image, image editing, segmentation, image-to-3D, VLM, physics simulator, video diffusion model, depth estimator), each of which can introduce errors. None of these potential failure modes are acknowledged in the paper.

### Trivial
None.

## Nice-to-Haves
- Quantitative ablation results (VBench/WorldScore/GPT-4o scores for each ablated variant) would substantially strengthen the paper.
- Reporting variance or confidence intervals for the main results would improve interpretability.
- A runtime or computational cost analysis would help assess practical feasibility.

## Removed Points
These points are flagged to be removed; treat them with caution.
- Criticism about "no runtime or computational cost analysis" — demoted to nice-to-have; not a core methodological weakness.
- Criticism that multi-object interaction handling is "quite simple" and novel-view capability "inherits entirely from 3D representations" — these are opinion-based judgments about contribution size, not specific technical flaws.
- Comments about "3-4 decimal places on scores suggesting ceiling effects" — speculative; VBench scores commonly report at this precision in the literature.
- "The conclusion re-states the pipeline without acknowledging any limitations" — subsumed by the limitations weakness above.
- Section-by-section note about the paper's differentiation from Omni-PhysGS and PhysGen3D — the paper does differentiate in Sec. 2.2 (lines 50-51), stating existing methods lack multi-material/multi-object support and have fixed viewpoints. Whether this differentiation is adequate is a matter of interpretation, not a factual flaw.
- "SDS from a video diffusion model may produce blurry results" — generic speculation, not a verified weakness.

## Novel Insights
None beyond the paper's own contributions. The input review primarily identifies gaps in explanation and evaluation rather than surfacing novel observations about the method.

## Suggestions
1. **Explain the differentiable physics mechanism in Sec. 4.2.** State explicitly how ∂V/∂Θ is computed through each physics simulator type. If using specific frameworks (e.g., Warp, DiffTaichi, adjoint methods), name them. If using gradient approximations (e.g., finite differences), state this and discuss the impact.
2. **Expand the evaluation.** Increase the dataset size, report variance across runs or random seeds, and include comparisons against more directly relevant 4D generation methods (TC4D, 4D-fy, Consistent4D).
3. **Add quantitative ablation results** for the material optimization and position optimization components, using the same metrics (VBench, WorldScore, GPT-4o) as the main evaluation.
4. **Add a limitations section** acknowledging potential failure modes of each pipeline component.
5. **Calibrate the claims** in the abstract and introduction to match the demonstrated complexity of the physical dynamics.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>