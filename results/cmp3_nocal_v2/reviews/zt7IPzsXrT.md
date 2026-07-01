Now let me write the final consolidated review.

## Summary

ScaPre proposes a closed-form framework for large-scale concept unlearning in diffusion models. It combines a spectral trace regularizer with Bures-distance geometry alignment (conflict-aware stable design) and a mutual-information-based channel selection mechanism (Informax Decoupler) to produce single-step weight updates that scale to many concepts while maintaining precision. The method is evaluated across object unlearning at two scales (Imagenette with 10 classes, ImageNet-Diversi50 with 50 classes), precise disentanglement of visually similar concepts (ImageNet-Confuse5), artistic style unlearning (50 artists), and explicit content (I2P).

## Strengths

1. **Closed-form formulation provides a genuine scalability advantage.** The Sylvester-equation-based solution (Eq. 9–10) enables single-step weight updates, avoiding the iterative fine-tuning required by training-based methods like MACE and SPM. This is a principled design choice for the large-scale setting the paper targets.

2. **Bures distance for geometry alignment is theoretically well-motivated and goes beyond prior work.** Matching covariance structures (Eq. 5) rather than raw ℓ₂ weight differences is a principled way to preserve global feature correlations during unlearning. Prior closed-form approaches (UCE, RECE) use only Frobenius-norm regularization, making this a clear methodological advance.

3. **Strong empirical results on the hard case of precise disentanglement.** On ImageNet-Confuse5 (Table 4), ScaPre achieves **84.3% overall accuracy** (harmonic mean of unlearn and preserve accuracies) vs. 50.3% for the next best baseline (SP), while maintaining competitive CLIP_coco of 30.15 (vs. SD v1.5 baseline of 31.43). This is the most challenging evaluation setting — requiring fine-grained separation of visually similar ImageNet categories — and the improvement is substantial and credible.

4. **Broad evaluation coverage.** The paper evaluates on four distinct scenarios (objects at two scales, precise disentanglement, styles, explicit content) with multiple metrics per setting, covering the main use cases for concept unlearning.

## Weaknesses

### Fatal

None.

### Major

1. **Efficiency numbers are reported ambiguously, undermining a central claim.** Section 5.5 states that ScaPre "completes the unlearning of 50 concepts within only **120 seconds**" (line 25, line 248). However, Figure 3 reports ScaPre's "Execution Time (Hours)" as **~1.5 hours**. These refer to different quantities (weight-editing time vs. total experimental pipeline including evaluation), and the paper never clarifies what each measurement includes or excludes. Since UCE and RECE — also closed-form methods — similarly show ~0.5 and ~1.5 hours in the same table, the "Execution Time" column clearly includes more than weight editing. But the figure caption inconsistently labels it "GPU-hours" while the table header says "Execution Time (Hours)." The numbers are not contradictory when properly scoped, but the current presentation leaves the reader unable to determine which quantity is being reported where.

2. **The "×5 more concepts" scalability claim is not operationalized.** The abstract and contribution list state ScaPre "can forget up to ×5 more concepts than the best baseline within the limits of acceptable generative quality." "Acceptable generative quality" is never defined — no threshold on CLIP score, FID, or any other metric is provided. Figure 4 shows scalability curves, but the ×5 claim is not tied to any specific data point or quality threshold. Without an operational definition, this claim is not verifiable.

### Minor

3. **The UQ metric is relative to the baseline set and non-standard.** UQ (Section 5.2) normalizes accuracy and CLIP score by their mean and std across the *specific methods being compared*, applies a sigmoid, and takes the harmonic mean. This means UQ values are tied to the current baseline set and cannot be compared across papers — adding or removing a baseline changes the scores. The paper does present raw (accuracy, CLIP) numbers alongside UQ in all tables, so the raw data is accessible; the reliance on UQ as a headline metric is unnecessary and shifts attention from the concrete trade-offs visible in the raw numbers.

4. **"No additional data" claim is slightly overstated.** The paper repeatedly claims ScaPre requires "no additional data or auxiliary sub-models" (abstract, Section 4 intro). The Informax Decoupler (Section 4.2) requires inference on target-concept and neutral text prompts to compute activations and set per-channel thresholds τ_i. While this is much lighter than the training datasets needed by LoRA-based methods (MACE, SPM), the absolute phrasing could be clarified (e.g., "requires no additional *training* data or auxiliary datasets beyond the target concept prompts").

5. **No variance or error bars reported.** All results in Tables 1–4 are point estimates without standard deviations or confidence intervals. Unlearning accuracy, CLIP scores, and FID all have inherent stochasticity. For strong comparative claims, some measure of variance is needed to assess whether reported differences are meaningful relative to noise.

6. **"SP" baseline is never explicitly defined in the main text.** The abbreviation "SP" appears in all main tables (Tables 1–4) but is not defined. Based on the related work (Section 2.2 cites "Sculpting Memory (Li et al., 2025a)" separately from "SPM (Lyu et al., 2024)"), SP likely refers to Sculpting Memory, but this should be stated explicitly.

### Trivial

- The choice of max aggregation over mean or sum for per-concept MI scores (Line 107: MI_i = max_k MI_i^{(k)}) is not discussed. This choice implies that if a channel is highly relevant to any single concept, it is treated as fully relevant for all concepts — the rationale for this design decision would strengthen the exposition.

## Nice-to-Haves

- Clarify the threshold-setting procedure τ_i for the Informax Decoupler (e.g., fixed quantile, median activation, data-driven). The paper says "adaptive threshold" (line 99) but provides no details.
- Include a brief limitations section covering: (a) the geometry alignment is handled as a post-hoc proximal refinement, not integrated into the closed-form solution (the paper acknowledges this at line 131), (b) the method modifies only cross-attention layers, (c) the MI computation requires model inference on concept prompts.
- Present a scatter plot of Accuracy vs. CLIP score across methods for each benchmark as a supplement to the tabular results — this would make the trade-offs immediately visible and reduce reliance on the UQ metric.

## Removed Points

These points were raised in the review but are removed after verification against the paper:

- **"Fatal contradiction" (120 seconds vs. 1.5 hours as incompatible figures for the same quantity):** These are not the same quantity. The 120 seconds refers to weight-editing time for unlearning. The ~1.5 hours in Figure 3 clearly includes the full evaluation pipeline — UCE and RECE (also closed-form, taking seconds for weight editing) show 0.5–1.5 hours. The numbers are reconcilable; the issue is unclear reporting, not a contradiction. Demoted from "Structural/Critical" to Major #1 above.

- **"No additional data claim contradicted by Informax Decoupler":** The prompts used by the Informax Decoupler (target-concept prompts and neutral prompts) are inherent to the unlearning task — every method must specify which concepts to unlearn. The claim distinguishes ScaPre from methods needing trainable modules and auxiliary training datasets. The phrasing could be more precise (Minor #4 above), but this is not a "methodological gap."

- **"First closed-form framework" priority claim vs. UCE/RECE:** The paper qualifies this as "the first closed-form framework *specifically designed for large-scale* concept unlearning," which is a legitimate distinction from UCE and RECE that were designed for a smaller scale.

- **Section-by-section notes on UCE/RECE model collapse on ImageNet-Diversi50:** These baselines are included transparently for completeness; the paper does not claim superiority from cherry-picked comparisons.

- **Geometry alignment as a "two-stage pipeline" undermining the "unified framework" claim:** The paper acknowledges this honestly (line 131: "this makes the overall objective no longer purely quadratic and therefore incompatible with direct closed-form optimization") and describes the proximal refinement explicitly. This is transparent methodology, not a flaw to penalize.

- **General framing/scope-creep criticisms** (e.g., demanding the paper address problems outside its stated scope, requesting theoretical proofs beyond the paper's empirical contribution, speculating about missing appendix content).

## Novel Insights

The reviewer's critique of the UQ metric as baseline-relative is the most useful insight that goes beyond the paper's own discussion. The observation that normalizing by statistics computed *across the compared methods* makes UQ scores non-transferable between papers is a valid methodological point. The paper should either justify why this metric construction is appropriate for its purposes or de-emphasize UQ in favor of the raw metric tuple.

## Suggestions

1. **Clarify efficiency reporting:** State explicitly what "120 seconds" measures (weight editing only) and what "~1.5 hours" in Figure 3 includes (e.g., full experimental pipeline: weight editing + image generation for evaluation + metric computation). Ensure the figure caption and table header agree on labeling ("Execution Time" vs. "GPU-hours").

2. **Define "acceptable generative quality"** with a concrete threshold to make the ×5 scalability claim verifiable.

3. **De-emphasize the UQ metric** as a headline result and let the raw (accuracy, CLIP, FID) tuple tell the story. The raw numbers already support the claims.

4. **Add error bars** to at least the main results (Tables 1, 3, 4) across multiple runs or seeds.

5. **Rephrase "no additional data"** to "no additional training data or auxiliary sub-models."

6. **Define "SP"** as Sculpting Memory (Li et al., 2025a) explicitly in the experimental setup.

## Score and Decision

<score>7</score>
<decision>Accept</decision>