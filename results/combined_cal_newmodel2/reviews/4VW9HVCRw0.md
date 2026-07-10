Now I have all the information I need to produce the final review. Let me compile everything.

## Summary

This paper introduces Free-Form HOI generation, extending hand-object interaction synthesis beyond grasping to include non-grasping actions (pushing, poking, rotating, tipping). The authors contribute (1) WildO2, an in-the-wild 3D HOI dataset (4.4k samples, 92 intents, 610 object categories) built via a clever O2HOI frame-pairing pipeline from internet videos, and (2) TOUCH, a three-stage framework with explicit contact prediction, multi-level conditioned diffusion, and physical refinement with cycle-consistency loss.

## Strengths

- **Well-motivated problem definition.** The paper correctly identifies that existing HOI generation is overwhelmingly grasp-centric and that real-world interactions include non-grasping actions that prior methods and datasets do not cover. Section 1 clearly articulates this gap. *[favorability=8.83]*

- **Novel and practically motivated dataset pipeline.** The O2HOI frame pairing strategy (Sec. 3.1) is a clever solution to the occlusion problem that has limited in-the-wild 3D HOI dataset construction. By transferring object masks from unoccluded reference frames to interaction frames via dense matching rather than diffusion-based inpainting, the pipeline achieves scalability while avoiding geometric inconsistencies. The resulting WildO2 dataset (4.4k samples, 92 intents, 610 object categories, multi-level annotations including 17-part hand segmentation) is a genuine resource contribution. *[favorability=15.55]*

- **Sound architectural motivations.** The three-stage framework — explicit contact prediction → multi-level conditioned diffusion → physical refinement — is well-reasoned for the task. The coarse-to-fine conditioning injection (Eqs. 4-5) where global context drives early diffusion stages and local details refine later stages is a sensible design. The cycle-consistency loss (Eq. 7) for refinement is a novel self-supervised idea. *[favorability=16.08]*

- **The ablation study is thorough** and the discussion of the 'w/o refiner' row achieving misleadingly low PD/PV values is an honest analysis that demonstrates understanding of the task's nuances. *[favorability=15.61]*

## Weaknesses

### Major

- **Limited baseline comparison.** The paper compares against only two adapted baselines (ContactGen, Text2HOI) while citing several contemporary HOI generation works in its own references (Yang et al. 2024a;b, Yu et al. 2025, Christen et al. 2024, Zhang et al. 2025a;b). Section 5.2 provides only a vague justification ("existing methods have not explored fine-grained controlled HOI generation") without specific analysis of why these cited works could not be adapted. The claim of "superiority" is therefore not adequately supported. *[favorability=-2.40]*

- **The VLM evaluation metric is not specified.** Tables 1-2 report "VLM↑" scores but the paper never states which VLM is used for evaluation, what prompt is used, or how the score is computed. This makes the metric uninterpretable and irreproducible. *[favorability=-1.48]*

- **Out-of-domain generalization is supported only by qualitative examples.** The Objaverse experiment (Sec. 5.4.2, Fig. 7) shows four qualitative results with no quantitative metrics (contact accuracy, physical plausibility, or semantic consistency) reported for held-out objects or unseen intents. The claim of "strong generalization capability" is broader than the evidence supports. *[favorability=-0.90]*

- **No statistical significance or variance reporting.** Tables 1 and 2 report single-point estimates for every metric with no confidence intervals or standard deviations. With only 677 test samples, it is impossible to assess which reported differences are reliable. This is especially problematic in Table 2 where some ablation conditions show close values. *[favorability=-0.50]*

### Minor

- **Human evaluation details are insufficient.** The perceptual score (PS) is based on only 10 users (Sec. 5.1, line 162) with no information about their expertise, the number of samples rated, instructions provided, or inter-annotator agreement. The 1.3-point difference (8.8 vs 7.5) may not be statistically meaningful. *[favorability=0.79]*

- **Dataset manual refinement process is opaque.** Section 3.2 states the pipeline yields 4,414 samples "after a final stage of manual inspection and refinement" but does not describe what was corrected, how many samples required manual intervention, what criteria were used, or whether annotator agreement was measured. Combined with the 55% automated reconstruction success rate (Fig. 3), this makes it difficult to assess the true level of automation and potential biases. *[favorability=4.91]*

- **The refiner network is underspecified.** Section 4.3 states it "inherits the Transformer architecture of our diffusion model" and that diffusion parameters are frozen during refiner training, but does not clarify whether the refiner shares any weights with the diffusion model, its parameter count, or the computational cost of the full pipeline vs. baselines. *[favorability=5.80]*

- **No runtime or computational cost comparison.** Given that TOUCH is a three-stage pipeline (contact prediction → diffusion → refinement with TTA iterations), a comparison of inference time vs. baselines would help assess practical utility. *[favorability=5.81]*

### Trivial

None.

## Nice-to-Haves

- Add at least one contemporary diffusion-based HOI baseline (e.g., from Yang et al. 2024a, Yu et al. 2025, or Zhang et al. 2025a) with appropriate adaptation.
- Report results with error bars (mean ± std over 3-5 seeds) for all quantitative metrics.
- Provide quantitative out-of-domain evaluation on Objaverse objects (contact accuracy, penetration metrics).
- Specify the VLM used for evaluation, the prompt template, and the scoring protocol.
- Expand the human evaluation and report inter-annotator agreement.
- Provide runtime comparisons with baselines.

## Removed Points

These points are flagged to be removed, treat them with caution:

- The critic's mention of "Pore Estimation Failure" (Fig. 3) as a typo for "Pose Estimation Failure" is removed — this could be a parser artifact from the figure rendering.
- The criticism about PointNet being "oddly dated" without ablation is removed — the paper does not claim SOTA in point cloud encoding and this is a secondary architectural choice that does not threaten the core claims.
- The criticism about "text encoder differences being small" is removed — the paper presents the ablation results transparently in Table 2 and discusses them in Sec. 5.4.1.
- The harsh critic's suggestion to "soften or provide specific critique" about LLM-based methods in the intro is removed — the paper's characterization of these methods as grasp-oriented is a reasonable stated position.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Substantially broaden the baseline comparison to include at least one contemporary diffusion-based HOI generation method from among the works cited in the paper itself, with clear justification for any omissions.
2. Report all quantitative results with variance estimates (standard deviations over multiple seeds).
3. Specify the VLM used for evaluation and the scoring protocol. Make the human evaluation more rigorous with larger sample sizes and inter-annotator agreement.
4. Provide quantitative generalization metrics on Objaverse objects to support the generalization claims.
5. Clarify the refiner network's relationship to the diffusion model (shared/frozen/trained parameters) and report per-sample inference time.

## Score and Decision

I conducted calibration against the human-review corpus. The most topically similar anchor is **HOI-Diff** (avg score 5.25, reject) — a text-driven 3D HOI generation paper using diffusion that had similar weaknesses around baseline comparison and evaluation. My paper's strengths (dataset contribution, problem framing) are stronger than HOI-Diff's, earning higher favorability ratings (15-16 vs 7-11). However, the evaluation gaps are more pronounced here: the baseline comparison issue has nearly identical severity to **HandsOnVLM** (favorability -2.40 vs -2.38, score 6.33/reject), and the underspecified VLM metric (-1.48) is unique to this submission. Papers at the 6.0-7.0 level (InterMask 6.00/accept, EgoHOIBench 7.00/accept) all had stronger comparisons with more baselines and clearer evaluation protocols.

The round-1 bracket was 5.5–7.5. Round-2 narrowing compared against HOI-Diff (5.25), 3D Interacting Hands Diffusion (5.50), and InterMask (6.00). My paper's strongest weakness (baseline comparison, -2.40) is more severe than the worst weakness in InterMask (-2.10) and comparable to HOI-Diff's weakest areas. However, my paper's strengths (dataset, task novelty, architectural design) are meaningfully stronger than any of these anchors' strengths. The paper makes genuine contributions but the evaluation is not yet strong enough to support the method claims at the level expected for acceptance. A major revision with expanded baselines, clarified metrics, and quantified OOD evaluation could lift it.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>