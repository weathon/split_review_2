Now I have all the information needed to produce the final consolidated review.

## Summary

Blueprint-Bench introduces a benchmark that tests spatial intelligence by asking models to convert apartment photographs into structured 2D floor plans (symbolic connectivity graphs with size-ranked rooms). The paper evaluates 12 models/system configurations (LLMs, image generation models, and agents) on 50 apartments and reports that most perform at or near a "random" baseline while humans substantially outperform all models. The benchmark is model-agnostic, supporting comparisons across architectures, and targets a genuine gap in the numerical evaluation of image generation models.

## Strengths

- **Clever task design.** The photograph-to-floor-plan task occupies a useful niche: the input is in-distribution for multimodal models, but the output requires genuine spatial reconstruction (inferring room layouts, connectivity, and scale) that is almost certainly not part of any model's training objective. The paper's contrast with ARC (which uses alien grid patterns) effectively motivates why this tests a different kind of blind spot.

- **Model-agnostic, cross-architecture framework.** By allowing LLMs (via SVG generation), image generation models (direct image output), and agents (via Docker container + iterative refinement) to participate in the same benchmark, the paper enables comparisons that most benchmarks cannot support. The Docker-based agent protocol in Section 2.2 is a concrete, practical contribution.

- **Addresses a genuine gap in image generation model evaluation.** The paper correctly observes that image generation model releases lack numerical benchmarks (unlike LLM releases which routinely report scores on SWE-bench, MATH, etc.). Blueprint-Bench provides a concrete way to fill this gap, including the novel ability to compare an image generation model against its underlying LLM.

## Weaknesses

### Fatal
None.

### Major

- **Misleadingly labeled "random baseline."** The baseline (Section 2.2) is constructed by asking models to generate floor plans *without any image input*. This is a "no-vision prior baseline" reflecting training-data knowledge about typical floor plan structure — not a true random baseline (random graphs would score near zero). The headline claim that "most models perform at or below a random baseline" implies chance-level performance, whereas several models (GPT-5, Gemini 2.5 Pro at 0.42) outperform this prior-only baseline by ~50%. The paper describes the setup honestly in Section 2.2 but then uses "random" language in the abstract and throughout the results, creating a misleading impression of the findings.

- **Instruction-following confound makes the bottom of the leaderboard uninterpretable.** The paper acknowledges that NanoBanana (0.18) and GPT-4o (0.15) fail due to "poor instruction following" — their outputs cannot be parsed by the scoring algorithm. But if the two worst performers score low because of format compliance rather than poor spatial reasoning, the benchmark is not cleanly measuring what it claims. The paper asserts in Section 2.4 that "Blueprint-Bench should test spatial intelligence, not instruction following" but provides no evidence that these dimensions are empirically separable. Without an explicit analysis distinguishing instruction-following failures from spatial-reasoning failures, the bottom of the leaderboard is uninterpretable.

- **Size-ranking room identification creates cascading errors, and scoring weights are unvalidated.** Rooms are identified only by size rank (room 1 = largest, room 2 = second largest, etc.), so a mistake in ranking propagates into connectivity penalties even when spatial relationships are correctly understood. The paper reports that humans drew floor plans with correct connectivity but were penalized for size ranking errors, yielding a mean of only 0.547 rather than near-perfect. The scoring weights (50% edge overlap, 20% degree correlation, 10% density, 10% room count, 5% door count, 5% door orientation) are presented without any justification or sensitivity analysis. It is unknown whether model rankings would change under reasonable weight perturbations.

- **Benchmark lacks systematic validation.** The paper provides no internal consistency analysis (are the scoring components correlated? does the 50% edge overlap weight dominate all other signal?), no convergent validity (how do Blueprint-Bench scores correlate with established spatial reasoning tasks?), no reliability analysis (how consistent are scores across multiple runs of the same model on the same apartment?), and no human-judgment correlation (do raters agree with the algorithmic score?). For a paper whose contribution is a benchmark, this absence of validation makes it unclear what construct the scores actually measure.

### Minor

- **Limited human baseline.** The human baseline comes from only 12 apartments with a single annotator. This is a thin reference point for the paper's claims about human superiority.

- **Limited data accessibility.** The paper keeps most of the data private. While the motivation (preventing overfitting) is understandable, the consequence is that the central results cannot be independently reproduced or compared against by other researchers using standard test-set evaluation.

- **Table labeling error.** Claude Code (Opus 4.1) is listed under "Category" as "Image model" in the Figure 5 table, but Section 2.2 explicitly identifies Claude Code as an agent scaffold. Only CodeX is listed as "Agent," making the labeling inconsistent.

### Trivial
None.

## Nice-to-Haves

- Re-label the "random" baseline as a "no-vision prior" baseline and adjust the framing accordingly. A true random graph baseline would provide a principled floor.
- Manually annotate spatial correctness for the two instruction-following failures (NanoBanana, GPT-4o) to separate format errors from spatial reasoning errors.
- Conduct a sensitivity analysis of the six scoring weights to establish whether model rankings are robust.
- Release the full dataset with a submission server following standard benchmark practice.
- Run multiple human annotators on a larger apartment subset.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Claim about baseline inconsistency (0.279 vs 0.322):** The critic noted this as unexplained, but the paper explicitly states Figure 7 uses a subset of 12 apartments (vs 50 for Figure 5), making different values expected. Removed as factually incorrect.
- **Claim that the gap between humans and models is "inflated" by the size-ranking artifact:** The critic asserted the gap is inflated, but the paper's own analysis suggests the opposite — fixing size ranking would make the human lead *larger*. The direction of the claim is wrong. Underlying concern about cascading errors is retained in Major weaknesses.
- **Criticism about the ARC comparison being imprecise:** A framing preference, not a substantive weakness. Removed.
- **Criticism that "first numerical framework" overreaches:** Unverifiable without external sources. Removed.
- **Criticism that "epochs" are undefined:** Likely defined in the appendix, which was stripped by the parser. Removed.
- **Request for larger dataset / per-apartment difficulty analysis / comparison to other benchmarks:** Scope-creep demands. Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Rename and reframe the baseline: call it a "no-vision prior" baseline and treat the ~0.28 score as a meaningful level of prior knowledge, not "random."
- Add a proper random baseline (e.g., permuted room connectivity graphs) to establish a true floor.
- For the two worst-performing models, perform a manual annotation study to determine whether their low scores reflect spatial intelligence failures or format compliance failures.
- Run a sensitivity analysis perturbing the scoring weights (e.g., ±10–20 percentage points) to test whether model rankings are stable.
- Release the full dataset with an online evaluation server, holding only the ground-truth labels private rather than the images themselves.
- Expand the human baseline (more annotators, more apartments) and report inter-annotator agreement.
- Correct the "Category" column so Claude Code is listed as "Agent."

## Score and Decision

The paper proposes a genuinely interesting and well-motivated benchmark task, and its cross-architecture evaluation framework is a practical contribution. However, the evaluation methodology has four major issues: (1) the "random" baseline is misleadingly constructed and frames the results inaccurately; (2) the scoring conflates instruction following with spatial reasoning at the bottom of the leaderboard; (3) the size-ranking room identification creates cascading errors with unvalidated scoring weights; and (4) the benchmark lacks any systematic validation (internal consistency, convergent validity, reliability). These issues collectively mean the paper's empirical claims cannot be accepted at face value. Major revision addressing the evaluation methodology is needed before the findings are reliable enough to stand.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>