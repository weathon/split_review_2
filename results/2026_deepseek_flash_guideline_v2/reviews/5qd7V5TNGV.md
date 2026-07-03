**Calibration note:** The calibration_search tool was unavailable due to a file-system error, so score anchoring is based on internal calibration against known ICLR standards rather than retrieved anchor papers. I have done my best to calibrate using the paper's own content and the review guidelines.

---

## Summary

CP4D reformulates text-driven 4D scene generation as the composition of a static 3D background with physically simulated dynamic foreground objects. The three-stage pipeline (separate 3D reconstruction, hybrid physics+SDS motion synthesis, and depth-aware composition) is clearly motivated and has some genuine technical contributions, notably the two-pronged SDS correction loops and the sequential scale-then-translation optimization. However, the evaluation is insufficient to support the strong claims: it uses only 17 examples with no error bars, does not quantitatively validate the core 4D/novel-view capability, and presents entirely qualitative ablations for the key design choices.

## Strengths

1. **Hybrid motion synthesis with two distinct SDS-based correction loops (Sec 4.2):** The paper identifies two specific failure modes of pure physics simulation — imprecise VLM-estimated material parameters and grid-resolution collision artifacts (Fig 2) — and addresses each with its own SDS-based optimization (Eq 4 for material parameters Θ, Eq 5 for inter-object displacements ΔΓ). The qualitative ablation (Fig 5) provides visual evidence that removing either correction degrades the output, showing this goes beyond prior physics-based approaches.

2. **Depth-aware spatial initialization with sequential scale-then-translation refinement (Sec 4.3):** The frustum-constrained scale heuristic (Eq 8, Fig 3) derived from monocular depth, followed by sequential optimization (scale first, then translation) to avoid local minima from joint optimization, is a concrete algorithmic contribution that addresses a genuine ambiguity in composing independently-generated 3D assets.

3. **Competitive quantitative results across diverse baselines (Tables 1, 2):** CP4D achieves the best or second-best score on every metric across 8 baselines spanning three categories (video diffusion models, physics-driven methods, text-to-4D). On WorldScore it leads in Photo Consistency (97.42 vs. 93.07), 3D Consistency (95.55 vs. 92.99), and Motion Smoothness (93.52 vs. 92.88). The GPT-4o Physical Realism score (0.694) also leads.

4. **Zero-shot compositional editing (Sec 5.4, Fig 6):** The framework's separation of background and foreground representations naturally supports independent editing of scene elements, demonstrated qualitatively — a capability that entangled 4D representations do not offer.

## Weaknesses

### Major

1. **Evaluation on only 17 examples with no error bars or significance testing (Sec 5.1).** The paper states: "We curate a dataset of 17 examples for evaluation." All quantitative results in Tables 1 and 2 are single floating-point numbers with no variance, confidence intervals, or per-sample distributions. With N=17, a few favorable examples could drive the reported margins (e.g., 0.998 vs. 0.997 on VBench Motion; 97.42 vs. 93.07 on WorldScore Photo Consistency). Without any statistical quantification, the claim that CP4D "consistently outperforms" baselines is not adequately supported. At minimum, per-sample results, box plots, or bootstrap confidence intervals should be reported.

2. **No quantitative evaluation of the claimed 4D/novel-view capability.** The paper claims to generate "explorable and interactive 4D scenes" with "flexible viewpoint changes" (Sec 4, Overview), yet the quantitative evaluation is entirely on 2D rendered videos using VBench and WorldScore — metrics designed for video quality from a single rendered viewpoint. The paper compares against 2D video generators (Sora, Runway, CogVideoX) on these 2D metrics, which cannot produce novel views at all, so the comparison does not test the 4D claim. To validate the 4D framing, the paper should demonstrate and evaluate novel-view synthesis (e.g., multi-view video consistency, novel-view PSNR/SSIM/LPIPS across viewpoints, or a user study on scene explorability). Without this, the claimed advantage over 2D video generation methods is asserted rather than demonstrated.

3. **Ablation study is entirely qualitative (Sec 5.3, Fig 5).** The two central design choices — material parameter optimization and relative position optimization — are ablated only visually on a single example. Given that these SDS-based corrections are a core contribution, the paper should report quantitative ablation results using the same VBench/WorldScore/GPT-4o metrics across the full evaluation set, with and without each component.

4. **Insufficient comparison against contemporary 4D generation baselines (Sec 5.2).** Only one text-to-4D baseline is included: DreamGaussian4D (Ren et al., 2023), an early SDS-based method. More recent feed-forward 4D methods that the paper itself cites in the introduction and related work (Xie et al., 2024b; Ren et al., 2024; YU et al., 2025; Bai et al., 2025) are not evaluated. This weakens the claim of outperforming "prior methods" in 4D generation.

5. **Tension between physics-awareness claim and SDS refinement from video diffusion models (Sec 4.2).** The paper motivates the need for physics grounding because prior methods "lack an explicit characterization of the underlying physical principles," yet the refinement step uses SDS from video diffusion models trained on internet videos that frequently contain physically implausible content. The paper does not measure whether SDS refinement preserves or degrades physical fidelity, and provides no comparison against ground-truth physics (e.g., analytic solutions for simple cases like free fall or pendulum motion). The qualitative ablation in Fig 5 is suggestive but does not resolve this tension.

### Minor

1. **GPT-4o as a physics evaluator is unvalidated (Table 2).** The paper uses GPT-4o to score "physical realism, photorealism, and semantic alignment" but provides no evidence that GPT-4o's judgments of physical plausibility correlate with human ratings. Without validation or a complementary human evaluation, the leading Physical Realism score (0.694) is difficult to interpret.

2. **SDS gradient backpropagation through physics solvers is not explained (Sec 4.2).** The paper claims to use "differentiable simulators" (contributions list) but does not discuss how differentiability is achieved for the MPM, rigid-body, and PBD solvers used. This is a practical reproducibility concern.

3. **No runtime or compute requirements reported.** The pipeline involves multiple large models (LLM, text-to-image, image editing, segmentation, depth estimation, two image-to-3D models, physics simulation, SDS optimization). Not reporting the overhead makes it hard to assess practical usability.

4. **The composition optimization (Eq 9) depends on the quality of the image editing model** without discussion of this dependency or potential failure modes when the editing model produces geometrically inaccurate composites.

5. **No quantitative comparison of the 3D reconstruction quality in isolation.** The paper uses Trellis for foreground and Viewcrafter for background but does not evaluate these 3D models independently. Poor 3D geometry would cascade into downstream physics and composition failures.

### Trivial

None.

## Nice-to-Haves

- Measure physical accuracy directly with simple test cases (free fall, projectile motion, pendulum) against analytic solutions, to quantify whether SDS refinement helps or hurts physical fidelity.
- Expand the evaluation set significantly beyond 17 examples; even 50–100 diverse prompts would substantially strengthen the evidence.
- Add a limitations section discussing failure cases, the scope of physical phenomena handled, and reliance on off-the-shelf models.
- Report per-sample results or scatter plots to complement aggregated metrics.
- Add a small human evaluation to validate the GPT-4o-based metrics.
- Clarify how differentiability of physics solvers is achieved.

## Removed Points

These points were identified by reviewers but are removed from the main assessment for the following reasons:

| Removed Point | Reason |
|---|---|
| Criticism about missing appendix content (references to Appendix B,C,D,E,F) | Appendices are stripped by the PDF parser; they exist in the original submission. Hard Rule. |
| Claim that the paper's baselines are unfair because the evaluation "pits a 4D method against 2D video generators on 2D video metrics" as a critique of unfair comparison | If anything, this comparison is harder on CP4D (2D methods don't need 3D representations at all). The asymmetry favors the baselines, not the authors. Hard Rule. |
| Complaint about missing related work verification | I cannot confirm missing related works from external sources. Hard Rule. |
| "System cannot be independently verified" / reproducibility concerns about cited models | All cited models, tools, and benchmarks are assumed to exist as published. Hard Rule. |
| Speculative concern about SDS introducing "the very physical inconsistencies the paper claims to avoid" without evidence | This is reframed as a verified concern (Weakness #5, Major tier) because the paper indeed does not analyze the physical accuracy of SDS-refined trajectories — this is factual, not speculative. The purely speculative framing ("could introduce") is removed; the specific verifiable gap (no ground-truth physics comparison) is retained. |
| Generic complaints about needing a "larger dataset" without justification | Reframed as a specific verified weakness: 17 examples with no error bars makes the results uninterpretable — the issue is not just size but lack of statistical rigor. |
| Pure formatting/style nitpicks | Hard Rule. |
| Typos/grammar/punctuation complaints | Hard Rule — these are parser artifacts, not author errors. |

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add per-sample results or bootstrap confidence intervals** to all quantitative tables so readers can assess the stability of the reported margins.
2. **Add a quantitative evaluation of novel-view synthesis** — even a single metric like multi-view PSNR on the composed 4D scene under random camera motion — to directly validate the 4D claim.
3. **Add quantitative ablation** of material parameter optimization and position optimization across the full evaluation set, not just visual results on one example.
4. **Include at least one more recent 4D baseline** from the feed-forward methods cited in the related work (e.g., one of Xie et al., 2024b; Ren et al., 2024; YU et al., 2025; Bai et al., 2025).
5. **Add a simple controlled experiment** comparing simulator-only trajectories vs. SDS-refined trajectories on a test case with a known ground truth (e.g., free fall) to quantify whether SDS refinement helps or harms physical accuracy.
6. **Validate GPT-4o physics scoring** against human judgments or supplement it with a human evaluation.
7. **Add a limitations section** discussing failure cases, the scope of physics handled, and robustness to off-the-model failures.

## Score and Decision

This paper proposes a well-motivated pipeline with genuine technical contributions. The compositional formulation, the two-pronged SDS correction strategy, and the depth-aware composition mechanism are sensible and clearly described. However, the evaluation does not adequately support the strong claims. The core issues are: (1) conclusions are drawn from only 17 examples with no statistical rigor, (2) the claimed 4D/novel-view capability is never quantitatively evaluated, and (3) the key ablations are entirely qualitative. These are not minor gaps — they mean the paper as submitted has not convincingly demonstrated that CP4D reliably produces better 4D scenes than existing approaches. The underlying approach has promise, but the evidence is insufficient for acceptance at a top venue.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>