## Summary

CP4D proposes a three-stage pipeline for text-to-4D scene generation: (1) constructing 3D representations of background environments and foreground objects using pre-trained expert models, (2) producing physically grounded motions via a "hybrid motion synthesis" that integrates physical simulators (MPM, rigid-body, PBD) with video diffusion priors through SDS refinement, and (3) an automated composition mechanism using depth-aware heuristics and optimization to fuse foregrounds with backgrounds. The key idea is to decompose 4D generation into static background + dynamic, physically-simulated foreground objects.

## Strengths

+ **Well-motivated problem and sensible decomposition (Sec. 1).** The observation that existing 4D generation methods produce visually plausible but physically inconsistent results is genuine and important. The compositional decomposition into static environment + dynamic foreground is structurally sensible and practically useful.

+ **The automated composition mechanism (Sec. 4.3, Eq. 6-9) is a concrete practical contribution.** The depth-aware heuristic for initializing scale and position (Eq. 8) and the sequential refinement strategy (scale first, then translation) address a real integration problem that arises when independently generated 3D assets must be fused into a coherent scene. The qualitative evidence (Fig. 5) shows this matters.

+ **Clear description of a complex multi-stage pipeline (Sec. 4).** The paper is lucidly written. Each stage's motivation and mechanism are described in sufficient detail: Stage I (Sec. 4.1) explains the text-to-image \(\to\) image-editing \(\to\) segmentation \(\to\) image-to-3D flow; Stage II (Sec. 4.2) describes the hybrid simulation+SDS approach with specific solver choices; Stage III (Sec. 4.3) gives the depth-aware composition equations.

+ **The hybrid motion synthesis idea (Sec. 4.2) is conceptually sound.** Combining physical simulators (for basic law compliance) with video diffusion priors (for perceptual naturalness) addresses real limitations of each approach in isolation, namely VLM parameter inaccuracy and grid-based collision artifacts.

## Weaknesses

### Major

+ **The evaluation does not directly measure the paper's central claim of physical accuracy.** The paper's headline value proposition is "faithful adherence to complex physical dynamics" (Abstract, Sec. 1). Yet the quantitative evaluation uses VBench and WorldScore metrics that measure *video quality* (motion smoothness, subject consistency, imaging quality), not physical correctness. The only metric targeting physics directly is GPT-4o scoring for "physical realism" (Table 2), but the paper itself cites VideoPhys (Bansal et al., 2024) which demonstrates that LLMs/VLMs make systematic errors when assessing physical common sense in video. No trajectory error against ground-truth physics, no conservation-law verification, and no human perceptual study of physical realism are reported. For a paper whose core contribution is physics adherence, this is the most critical evidential gap.

+ **Limited statistical rigor and dataset size (Sec. 5.1).** The evaluation uses only 17 examples with no reported variance — no standard deviations, confidence intervals, or significance tests. Many claimed advantages are very narrow (e.g., VBench Motion Smoothness: 0.998 vs. 0.997 for PhysGen3D; GPT-4o Photorealism: 0.759 vs. 0.753 for Runway; GPT-4o Semantic Alignment: 0.747 vs. 0.732 for Runway). Without variance estimates, the reader cannot assess whether these differences are meaningful or noise.

+ **Qualitative-only ablation (Sec. 5.3, Fig. 5).** The paper claims three contributions (compositional formulation, hybrid motion synthesis, automated composition), but the ablation is purely visual and covers only the SDS-based refinements (material optimization and position optimization). No quantitative ablation results (VBench/WorldScore/GPT-4o scores for each ablation variant) are reported, making it impossible to assess the marginal contribution of each component numerically.

### Minor

+ **Claims of "explorable and interactive 4D scenes" are not evaluated (Abstract, Sec. 4 overview).** The paper claims support for "flexible viewpoint changes" and interactivity, but provides no novel-view synthesis evaluation (no PSNR, SSIM, LPIPS from held-out views) and no user study. The only interactivity demonstrated is background/object swapping (Fig. 6). The quantitative metrics are computed on rendered 2D videos, not on the 4D representation itself.

+ **The SDS refinement's effect on physical accuracy is not directly validated (Sec. 4.2).** The hybrid motion synthesis refines physics simulation using a video diffusion prior trained on internet video (which contains edited content and non-physical effects). The paper provides qualitative ablation evidence that removing the refinement degrades visual plausibility (Fig. 5), but does not directly measure whether the refinement *preserves or improves* physical correctness vs. merely making outputs more visually appealing. These two goals could in principle diverge.

+ **Baseline comparison framing (Sec. 5.1).** The comparison against pure 2D video generation models (Sora, Runway, CogVideoX, Wan) as "4D generation" baselines is somewhat mismatched — these methods have no 3D/4D representation and no novel-view synthesis capability. While comparing output video quality is informative, the framing conflates different tasks. The more relevant baselines (PhysGen3D, PhysGen) show narrower margins (e.g., WorldScore 3D Consistency: 95.55 vs. 92.99; VBench Motion: 0.998 vs. 0.997).

### Trivial

None.

## Nice-to-Haves

- A direct measurement of physical accuracy (e.g., trajectory error against ground-truth simulation, conservation law checks) would substantially strengthen the paper's core claims.
- A human perceptual study comparing physical realism would be more convincing than GPT-4o scoring alone.
- Reporting per-example scores or distributions would help assess variance across the 17 examples.
- Runtime and computational cost reporting would help readers assess practical utility.
- An error analysis / failure case discussion would help assess robustness given the many pipeline components that could cascade-fail.

## Removed Points

These points from the input review were removed for the following reasons:

- *"The paper overstates limitations of prior work"* — The paper accurately characterizes existing methods; PhysGen3D is acknowledged as physics-driven but noted to have specific limitations (elastic-only simulation). This is fair scope-setting, not overstatement.
- *"The hybrid motion synthesis is sequential, not truly hybrid"* — A semantic nitpick; the paper clearly describes a two-stage process whose description as "hybrid" (combining two approaches) is reasonable.
- *"DreamGaussian4D inflates apparent advantage"* — Including a representative baseline from a different category is standard practice; the paper groups baselines transparently and readers can see expected lower performance.
- *"Video model comparison is apples-to-oranges"* — Partially true but the VBench/WorldScore metrics are output-video-quality metrics applicable to any video output. The concern is retained in weakened form under Minor weaknesses.

## Novel Insights

None beyond the paper's own contributions. The reviews converge on the paper's own framing rather than uncovering hidden issues or alternative interpretations.

## Suggestions

1. **Add direct physics metrics.** On a controlled benchmark (e.g., falling objects, collisions, pendulums with known ground truth), report trajectory error (e.g., mean displacement error against Newtonian simulation) or energy conservation metrics. This would directly validate whether the hybrid SDS refinement preserves or degrades physical accuracy.
2. **Report variance.** Add standard deviations or bootstrapped confidence intervals to all quantitative tables. Report per-example scores in the appendix.
3. **Add quantitative ablation.** Report the same VBench/WorldScore/GPT-4o metrics for the ablation variants (w/o material optimization, w/o position optimization).
4. **Clarify baseline inputs.** State explicitly what input each baseline received (same composite image? same text prompt?).
5. **Tone down claims** about "significantly outperforming" and "faithful adherence to physical dynamics" to match the evaluation evidence.

## Score and Decision

**Calibration anchors used:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| Sync4D (O0RIrM5iqX.md) | 4.50 | R1 | Yes | Most similar: physics-based 4D generation with mixed quantitative/qualitative evaluation. Sync4D lacked quantitative baselines (weight=-6.08); CP4D has more numbers but the metrics don't match its claims. |
| Consistent4D (sPUrdFGepF.md) | 5.00 | R1 | Yes | 4D generation from monocular video with better ablations. CP4D has clearer pipeline but weaker evaluation relative to claims. |
| MagicPose4D (wF9Cz2PknU.md) | 4.75 | R1 | Yes | Complex pipeline integrating multiple components. Both share the weakness that pipeline complexity outpaces the evidence for novelty. |
| GenXD (1ThYY28HXg.md) | 6.25 | R1 | Yes | 3D/4D scene generation with more comprehensive evaluation and larger-scale experiments. CP4D has narrower scope and weaker evaluation. |
| Diffusion² (fectsEG2GU.md) | 6.25 | R1 | Yes | 4D generation via score composition; stronger theoretical grounding and more thorough evaluation. |

**Round 1 bracket:** 3.5 – 5.5. The paper has clear merit (well-motivated pipeline, practical composition mechanism) but significant evaluation gaps relative to its core claims.

**Final score derivation:** The paper's strengths (pipeline design, clear writing, practical composition mechanism) are comparable to Sync4D (4.50) and MagicPose4D (4.75). However, CP4D's weakness profile is heavier in the dimensions that matter most: the largest-negative-weighted item in CP4D is the lack of evaluation for "explorable and interactive 4D scenes" (-8.42), and the evaluation-gap items (-5.02, -5.14) directly undermine the paper's central claim of physics adherence. This mismatch between claimed contribution and evaluated evidence is more severe than in Sync4D (whose evaluation gaps were about missing quantitative baselines for motion transfer, not about the paper's core thesis). The paper sits below Consistent4D (5.00) because Consistent4D's evaluation, while imperfect, at least targeted its reconstruction task directly. CP4D's claims about "faithful adherence to complex physical dynamics" require physics-specific evidence that the paper does not provide.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>