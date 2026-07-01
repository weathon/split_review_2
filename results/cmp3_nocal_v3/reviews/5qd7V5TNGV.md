## Summary

CP4D proposes a compositional pipeline for text-to-4D scene generation that decomposes the problem into static 3D background synthesis + physically grounded dynamic foreground synthesis + automated composition. The core technical contribution is a hybrid motion synthesis strategy that combines physics simulators (MPM, rigid-body, PBD solvers) with Score Distillation Sampling from video diffusion models to refine physical parameters and object positions. The paper evaluates against 8 baselines across multiple metrics.

## Strengths

- **Well-motivated problem decomposition.** The reformulation of 4D generation as static background + dynamic foregrounds (Sec. 1, Fig. 1) directly addresses a genuine limitation in prior work that treats scenes monolithically. This framing is intuitive and structurally sensible.

- **Hybrid motion synthesis is a genuine technical contribution.** The two-stage approach (Sec. 4.2) — physics simulator for coarse trajectories + SDS refinement using video diffusion priors — directly addresses known failure modes of each approach alone. Physics simulators produce accurate motion given correct parameters but struggle with parameter estimation and geometric fidelity; video diffusion models encode perceptual plausibility but no explicit physics. The combination is novel and well-reasoned.

- **Diverse and contemporary baselines.** Table 1 compares against 8 methods across three categories (physics-driven: PhysGen, PhysGen3D, OmniPhysGS; video generation: Sora, Runway, CogVideoX, Wan2.2; text-to-4D: DreamGaussian4D), including very recent models. This is more thorough than many papers in this area.

- **Consistent quantitative results on the metrics used.** The method achieves best or second-best scores across nearly all metrics in Tables 1 and 2, often by notable margins (e.g., WorldScore photo consistency 97.42 vs. 93.07, 3D consistency 95.55 vs. 92.99).

## Weaknesses

### Fatal

None.

### Major

- **Evaluation on only 17 self-curated examples with no statistical rigor.** The paper states it "curates a dataset of 17 examples for evaluation" (Sec. 5.1, line 160). For a paper claiming to "consistently outperform" 8 baselines on "physical plausibility," "photorealism," and "semantic alignment" — and reporting numbers to three decimal places in Tables 1 and 2 — this sample is thin. There are no confidence intervals, standard deviations, or per-example breakdowns. It is impossible to assess whether the reported improvements are meaningful or driven by a few favorable examples. The qualitative section shows only 2 examples (Fig. 4), raising cherry-picking concerns. This is the single most limiting weakness and substantially reduces confidence in the comparative claims.

### Minor

- **Purely qualitative ablation study.** The ablation (Sec. 5.3, Fig. 5) shows a single example with and without two components, with no quantitative metrics reported. For a pipeline with 10+ chained models/tools, the contribution of each component should be measured on the same metrics used in the main evaluation. The paper says "More ablation studies are provided in the Appendix D" (line 233), but the main paper's ablation lacks quantitative evidence.

- **No direct evaluation of the claimed 4D capabilities.** The paper claims CP4D generates "explorable and interactive 4D scenes" (abstract, line 9) — meaning viewpoint exploration and interactive scene manipulation — yet never measures these capabilities directly. All quantitative metrics (VBench, WorldScore, GPT-4o scoring) evaluate rendered 2D video quality. Novel-view synthesis quality, multi-view consistency under free viewpoints, and interactivity are demonstrated only qualitatively. This creates a gap between the claims and the evidence provided.

- **No discussion of failure cases or limitations.** The paper has no limitations section. For a pipeline chaining LLMs, text-to-image models, image editing, segmentation, depth estimation, image-to-3D ×2, VLMs, physics solvers, video diffusion SDS, and optimization — error propagation is essentially certain. How does the method behave when the image editing model fails? When SAM produces a bad mask? When the physics solver's material parameters are severely wrong and SDS cannot correct them? The absence of any failure analysis undermines confidence in robustness.

- **The distinction between physical plausibility and physical accuracy is not fully addressed.** The paper claims "faithful adherence to complex physical dynamics" (abstract), but the SDS refinement step (Eqs. 4-5) uses a video diffusion model that encodes human *perceptual* priors about what *looks* physically plausible — not necessarily what *is* physically correct. The paper acknowledges this indirectly by referring to "commonsense knowledge" and "human perceptual priors" (Sec. 4.2), but never explicitly addresses whether the refinement could introduce physically incorrect but perceptually pleasing artifacts, and provides no analysis distinguishing these cases.

### Trivial

- **GPT-4o appears in both the pipeline and the evaluation.** GPT-4o is used (or named as an example) for prompt decomposition in Sec. 4.1 and as an evaluator in Table 2. While the circularity is weak (decomposition and evaluation are different tasks, and Sec. 4.2 uses unspecified "VLMs" rather than confirmed GPT-4o for parameter estimation), the paper should acknowledge this limitation or use a human preference study to strengthen the evaluation.

## Nice-to-Haves

- A human preference study comparing CP4D against the best baselines on physical plausibility, visual quality, and novel-view consistency would be far more convincing than the GPT-4o-as-judge evaluation.
- Direct quantitative evaluation of multi-view consistency (e.g., PSNR/SSIM/LPIPS on held-out views) or interactivity would directly support the claimed 4D capabilities.
- If fluid solver support is claimed, a fluid demonstration would be beneficial; make it clear if fluid support exists in the appendix.

## Removed Points

The following points from the input review were removed with brief justification:

- **"Comparison with video generation baselines is structurally mismatched"** — This is reframed and subsumed by the weakness above about lack of direct 4D capability evaluation. Comparing against video models on common video-quality metrics is standard practice and not "apples-to-oranges"; the core issue is that the paper's unique claimed capabilities (viewpoint exploration, interactivity) are not measured, which the main weakness already captures.
- **"Line 27 typo ('foreground objects and foreground objects')"** — Removed as a formatting artifact / parser issue per the hard rules.
- **"No fluid demonstrations despite claiming PBD fluid solver support"** — The appendix was stripped during parsing; claims about absent demonstrations in the appendix cannot be verified from the paper as presented here.
- **"Specific suggestions to expand evaluation to 50-100 examples / add confidence intervals"** — These are evaluation suggestions, not verifiable weaknesses; they are reflected in the Nice-to-Haves section.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Expand the evaluation to at minimum 50 examples with diverse physical scenarios (rigid, elastic, multi-object) and report per-metric statistics with confidence intervals or per-example breakdowns.
- Add a quantitative ablation study measuring the contribution of each component (material optimization, position optimization, image-editing coherence step, depth-aware initialization) on the full evaluation set using the same metrics as the main tables.
- Include a limitations section that honestly discusses failure modes of the pipeline, error propagation scenarios, and types of physical phenomena the method cannot handle.
- Directly evaluate the claimed 4D capabilities: measure novel-view synthesis quality or at minimum demonstrate multi-view consistency quantitatively.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>