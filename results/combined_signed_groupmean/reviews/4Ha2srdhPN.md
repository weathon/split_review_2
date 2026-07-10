## Summary

GRAID is a framework for generating high-fidelity spatial reasoning VQA data from 2D bounding boxes alone, avoiding the 3D reconstruction errors and generative hallucinations that plague prior methods. The paper operationalizes this through a predicate-based question realization pipeline (SPARQ), generates 8.5M VQA pairs across three driving datasets, and shows through human evaluation (91.16% validity) and fine-tuning experiments that models learn transferable spatial concepts that generalize across question types, datasets, and real-world benchmarks.

## Strengths

- **Clean methodological insight (Section 3.1).** The core idea — that qualitative spatial relationships can be reliably determined from 2D bounding boxes alone, without 3D reconstruction or generative models — is sound and well-motivated. This design choice directly addresses cascading errors from depth estimation and camera calibration that plague prior pipelines.

- **Cross-type and cross-dataset generalization experiments (RQ1 and RQ2, Section 5) are well-designed.** Training on 6 question types yields improvements on over 10 held-out types (Figure 3), providing genuine evidence of transferable spatial concept learning. The cross-dataset transfer from BDD to NuImages (different cities, scenes, object distributions) further supports generalization rather than template memorization. These experiments directly address the natural concern about template-based data being brittle.

- **Human evaluation directly contrasts GRAID with prior work using comparable methodology (Section 4).** The same evaluator pool assessed both GRAID data and OpenSpaces data with the same criteria. The gap (91.16% vs 57.6%) is large enough to be meaningful even allowing for measurement noise.

- **SPARQ's predicate-based early rejection (Section 3.2) is a practical engineering contribution** that makes large-scale generation feasible. The 1407× speedup for certain templates is notable, and the principle (cheap predicates rejecting infeasible candidates before expensive realization) is well-motivated.

- **Experimental breadth across models and benchmarks.** The paper fine-tunes four different VLM backbones (Llama 3.2 11B, Gemma 3 4B, Qwen2.5 VL 3B, Qwen3 VL 8B) and evaluates on five benchmarks (BLINK, A-OKVQA, RealWorldQA, NaturalBench, VSR) spanning indoor and outdoor scenes far beyond the driving domain.

## Weaknesses

### Fatal
None.

### Major

- **The "similar planes" check is described in prose but absent from Algorithm 1.** The paper states (line 138) that the RightOf question realization checks whether candidate object pairs "should lie on similar planes" and calls this "necessary in the process of realizing a question." However, Algorithm 1's pseudocode only checks `x_min > x_max` and IoU = 0 — there is no "similar planes" check. It is unclear how this condition is determined without 3D information, which would seem to require the kind of reconstruction the paper claims to avoid. This is a concrete inconsistency that must be resolved: either define the condition in 2D terms (e.g., y-axis overlap threshold) or acknowledge any 3D assumptions.

- **The headline 91.16% vs 57.6% comparison conflates question difficulty with data quality.** GRAID generates qualitative yes/no questions, while SpatialVLM generates metric questions (distances, sizes) that are intrinsically harder. The paper partially acknowledges this (noting SpatialVLM's [50%,200%] acceptance tolerance in Section 2) but presents the comparison in the abstract and introduction as a primary selling point without sufficiently caveating that the two methods target fundamentally different question difficulty regimes. This does not invalidate GRAID's contribution — the method is valuable for qualitative spatial reasoning — but the framing overstates the advantage.

### Minor

- **Small human evaluation sample with no inter-annotator agreement.** The evaluation uses n=317 VQA pairs for a dataset of 8.5M pairs, and no inter-annotator agreement is reported. The 91.16% figure is directionally sound but the numerical precision implies more certainty than the sample supports.

- **RQ3 lacks a control for training data volume.** The comparison against OpenSpaces is relevant (both are spatial VQA datasets), but a non-spatial VQA dataset of comparable size would clarify whether gains come specifically from spatial content rather than from any additional fine-tuning. This is a missing experiment, not a flaw in the existing results.

- **No confidence intervals or statistical significance reported** for any numerical comparison throughout the paper.

- **No ablation of predicted vs. ground-truth detections.** Since the paper argues GRAID works with any object detector, an experiment showing how data quality degrades with detector accuracy would strengthen the claims about practical deployability.

### Trivial
None.

## Nice-to-Haves

- Compare GRAID against a version of SpatialVLM that generates qualitative questions for an apples-to-apples comparison.
- Add a matched-data-volume non-spatial control in RQ3.
- Clarify the "similar planes" check — either define it in 2D terms or acknowledge any 3D assumptions.
- Report confidence intervals for the human evaluation and key experimental results.

## Removed Points

These points are flagged to be removed; treat them with caution:
1. **"Human evaluation number inconsistencies"** — Removed because the paper's three numbers (95.58% question-only validity, 93.69% answer-only validity, 91.16% overall pair validity) are consistent different slices of the same 317-pair evaluation, not contradictory as the reviewer claimed.
2. **"Tables 4, 5, 6 not visible"** — Removed because the parser strips appendix content; these tables exist in the original submission.
3. **"Missing related works about 2D-layout methods"** — Removed per instructions (cannot verify existence without external sources).
4. **"Learning rate notation concern"** — Removed because 2^{-4}=0.0625, while high, is plausible for LoRA fine-tuning and the reviewer's speculation about a formatting error is not verifiable.
5. **Formatting/style nitpicks** — Removed as parser artifacts.
6. **"Missing appendix content"** — Removed per instructions (parser strips appendices from all papers).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the inconsistency between the prose description (which mentions a "similar planes" check) and Algorithm 1 (which omits it) — either add the check to the pseudocode or clarify the discrepancy.
2. Add a caveat to the abstract and Section 1 stating that the 57.6% vs 91.16% comparison involves different question types (metric vs. qualitative), not just different methods.
3. Report inter-annotator agreement for the human evaluation and consider a larger sample for the headline validity claim.
4. Include an ablation comparing GRAID data generated from ground-truth annotations vs. predicted detections.

## Score and Decision

**Round-1 bracket:** After reviewing anchors in all bands, the paper clearly surpasses the 4–5 score range (STUPD at 4.33, Sparkle at 4.50), which have weaker methods and narrower experiments. It sits alongside GeoDiffusion at 6.50 (Accept) in terms of experimental thoroughness and contribution quality. **Bracket: [5.5, 7.5].**

**Narrowing:** Comparing itemized impact scores against GeoDiffusion (6.50): GRAID has a stronger top-level strength profile (+9.70 for method insight, +9.97 for generalization experiments, +9.99 for human evaluation) than GeoDiffusion's top strengths (+10.00 for writing/extensive experiments). GRAID's critical weakness ("similar planes" inconsistency, -9.99) is comparable in severity to GeoDiffusion's missing-baselines weakness (-9.56 to -10.00). However, GeoDiffusion's page-limit violation and missing-baselines issues are harder to fix post-hoc, while GRAID's "similar planes" gap is a documentation issue resolvable in rebuttal. The comparison-framing weakness (-2.85) is moderate and addressable. **Final placement: 6.5.**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>