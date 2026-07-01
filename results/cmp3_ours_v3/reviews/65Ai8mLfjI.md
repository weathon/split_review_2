Now I'll compile and write the final consolidated review.

## Summary

This paper investigates the role of the pooled CLIP embedding in modern diffusion transformers (FLUX, SD3.5, HiDream, etc.). It empirically finds that the pooled embedding contributes little when used conventionally—especially for long prompts—but can be repurposed as a guidance signal via a simple modulation-space extrapolation (Eq. 3) to improve generation quality across aesthetics, complexity, object counting, hands correction, color, and position. The method is evaluated on 4 T2I models, 2 T2V models, 1 image-editing model, and compared against several baselines, with human side-by-side evaluation supporting the key results.

## Strengths

1. **Clean empirical finding about CLIP's conditional inactivity (Table 1, Figure 1).** The paper clearly documents that the pooled CLIP embedding is near-inactive for long prompts in FLUX and fully inactive in HiDream-Fast across all prompt lengths. This is a reproducible observation that was previously only tacitly assumed by practitioners who dropped global text conditioning.

2. **Exceptionally broad evaluation across models and modalities (Tables 2–4).** The method is tested on FLUX schnell, FLUX dev, SD3.5 Large, HiDream, COSMOS (T2I), Hunyuan and CausVid (T2V), and FLUX Kontext (image editing). Very few test-time guidance papers span this range of architectures with consistent results, making the claim that modulation guidance generalizes substantially more credible.

3. **Human evaluation with side-by-side comparisons (Table 2).** The paper does not rely solely on automatic metrics but includes human judgments of relevance, aesthetics, complexity, and defects across 128+ prompts. This raises the evidence bar relative to papers reporting only CLIP Score and FID.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Imprecise "training-free" claim in the abstract.** The abstract and Section 5 describe the approach as "training-free." For models that already include CLIP-based modulation (FLUX, SD3.5, HiDream, Hunyuan), this is accurate — Eq. 3 is applied at inference time. However, for COSMOS and CausVid, the paper fine-tunes a small MLP (4K / 1K iterations on 500K synthetic samples) to reintroduce the pooled embedding before modulation guidance can be applied. The paper does not hide this training step (it is described in the "Integrating the pooled text embedding" subsection and the experiments), but the unqualified "training-free" framing in the abstract is imprecise. **Fix:** Qualify the abstract to clarify that the guidance formula itself is training-free while noting that a light fine-tuning step is needed for models without pre-existing CLIP-based modulation.

2. **Statistical test not reported for human evaluation.** Table 2's caption states "green indicates statistically significant improvement" but no test name, p-value, or confidence interval is reported in the main paper. Even if details are deferred to Appendix J, the main paper should at minimum state which test was used and the significance threshold. This is a straightforward methodological gap that is easily fixed.

3. **Interaction with CFG not analyzed.** The paper states that modulation guidance "complements CFG" (line 27) and "can be applied on top of CFG guidance" (line 100), but provides no experimental analysis of how the two interact — whether they compound, interfere, or are orthogonal. Since both operate as guidance mechanisms on different representations, a brief ablation would strengthen the paper.

### Trivial

- The conclusion defers limitations entirely to Appendix H (stripped by the parser); a brief limitations paragraph in the main paper (covering the need for manual prompt selection and the conditional inactivity of CLIP) would improve readability.

## Nice-to-Haves

- **Ablation of prompt selection sensitivity.** The method depends on choosing positive/negative prompts for each property; an ablation testing different prompt pairs for the same task would help distinguish "the method works" from "these specific prompts work." (The prompts themselves are reported in Appendix D.)
- **Finer-grained prompt-length analysis.** The paper uses only 10 and 77 tokens as short/long thresholds; a gradual breakdown would strengthen the analysis.
- **More explicit discussion of modulation layer placement.** The paper could clarify where in the transformer block (after attention? after MLP?) the modulation (Eq. 2) is applied, as this affects how guidance propagates.

## Removed Points

These points from the input review are removed (with justification):

- **CLIP inactivity overstated (Critical Issue 2 in input):** The reviewer claimed the paper overstates CLIP inactivity, but the paper explicitly states CLIP is "partially inactive in FLUX schnell" (explaining it is impactful for short prompts) and "fully inactive in HiDream-Fast." The body clearly describes the short/long-prompt distinction. The abstract's "generally sufficient" is appropriately qualified. **Removed** — the paper already handles this nuance.

- **Prompts not reported (Critical Issue 3 in input):** The paper states "In Appendix D, we present the prompts used for each targeted aspect." The appendix was stripped by the parser and exists in the original submission. **Removed** per rule: parser-stripped content should not be flagged as missing.

- **COSMOS+CLIP reduces complexity (Missing Parts section):** The reviewer flags that adding CLIP alone to COSMOS reduces complexity and claims the paper should discuss this. The paper already does: "we observe that introducing CLIP into COSMOS does not improve performance and even reduces complexity; gains appear only when combined with modulation guidance." **Removed** — already addressed.

- **Generic framing suggestion (Section-by-Section notes):** The suggestion to reframe from "necessity" to "repurposing" is a stylistic preference, not a weakness. **Removed.**

- **Aesthetic quality drop in CausVid (Table 4):** The reviewer claims selective emphasis. The drop (57.85→57.65) is 0.2 points — negligible and within noise. Overall consistency is essentially unchanged (19.01→19.02). **Removed** — not a meaningful omission.

## Novel Insights

Beyond the paper's own contributions, the most insightful observation from the review process is that the paper's main weakness is not any flaw in the experiments or analysis, but rather a framing mismatch between the abstract's unqualified "training-free" claim and the actual procedure required for CLIP-free models. The underlying science — showing that a nearly-dormant mechanism can be repurposed as a guidance signal — is sound and well-supported.

## Suggestions

1. Qualify the "training-free" claim in the abstract (e.g., "the guidance formula itself is training-free; for models without CLIP-based modulation, a light fine-tuning step is needed to introduce the pooled embedding").
2. Add a brief statement of the statistical test used for human evaluation significance in the main paper.
3. Include a short experiment or discussion of how modulation guidance interacts with CFG.

## Score and Decision

**Round 1 bracket:** After reviewing calibration anchors, I placed the paper in the 6.0–8.0 range. The anchor distribution was:
- *Strong reject band* (avg ≤1.5): irrelevant/weak papers, not comparable.
- *1.5–3.5 band* papers avg 2.5–3.4: clearly weaker.
- *3.5–5.5 band*: "Universal Guidance for Diffusion Models" (avg 5.25, Accept) — narrower evaluation, no human eval; "Mitigating Compositional Issues" (avg 4.5, Reject) — limited to older models. Our paper is stronger than both.
- *5.5–7.5 band*: "Eliminating Oversaturation" (avg 6.0, Accept) — clean CFG fix, comparable scope; "Diffusion Feedback Helps CLIP" (avg 6.6, Accept) — solid CLIP improvement paper; "Representative Guidance" (avg 7.33, Accept) — strong guidance method with theory. Our paper is comparable to the upper end of this band (wider evaluation, human eval, but a few minor clarity issues).
- *7.5–8.5 band*: Papers avg 7.6–8.0 — more foundational contributions (architectures, theoretical analyses). Our paper is not at this level.
- *8.5+ band*: No files.

**Final score:** 7.0. The paper has a clear analysis contribution, a practically useful method, exceptionally broad evaluation, and human judgments. The weaknesses are minor and easily fixable. It is comparable to or stronger than accepted papers in the 6.0–7.3 range, but does not rise to the level of foundational contributions scoring 8.0+.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>