## Summary

This paper investigates global text conditioning (specifically the pooled CLIP embedding) in diffusion transformers. It makes two contributions: (1) an empirical analysis showing that the pooled CLIP embedding has little to no effect on output quality in current models (especially for long prompts), and (2) a training-free "modulation guidance" method that amplifies the pooled embedding's effect by extrapolating in modulation space using positive/negative prompt pairs, showing improvements across text-to-image, text-to-video, and image editing tasks.

---

## Strengths

**1. A clean, practically useful empirical finding (Section 4, Table 1).** The controlled ablation (zeroing out the CLIP pooled embedding) cleanly demonstrates that CLIP's contribution through modulation is negligible—zero for HiDream-Fast across all prompt lengths, and very small for FLUX schnell on long prompts. This is a concrete finding that informs architectural decisions about whether to include modulation-based text conditioning.

**2. Simple, training-free method with broad applicability.** Modulation guidance (Equation 3) requires no training, no LoRA, and no complex loss functions. The overhead is one additional CLIP forward pass per guidance direction. The paper demonstrates consistent improvements across five text-to-image models, two video models, and an image editing task—suggesting genuine generality rather than cherry-picking.

**3. Thoughtful extension to CLIP-free models (Section 5).** Adding a small MLP on top of the pooled embedding with distillation training (keeping the original model frozen, training on synthetic data) is a clean retrofit strategy. The paper shows this enables modulation guidance for models like COSMOS and CausVid that discarded the pooled embedding entirely.

**4. Interpretability analysis for the hands case (Figure 4).** The paper shows that for hands correction, modulation guidance shifts attention toward relevant tokens ("hands," hand-related tokens), providing some evidence that the guidance operates through the intended semantic mechanism rather than being a generic perturbation.

---

## Weaknesses

### Fatal
None.

### Major

**1. Unresolved tension between the analysis and the method.** The paper's first contribution is that the pooled CLIP embedding is "inactive" (HiDream-Fast: literally zero effect across all metrics; FLUX schnell: negligible for long prompts). The second contribution is to amplify this signal via modulation guidance and obtain clear improvements. The paper never explains how amplifying a near-zero signal produces visible effects.

There are two distinct possibilities the paper does not disentangle: **(A)** the effect is small but directionally meaningful, and amplification makes it useful (the paper's implicit narrative); **(B)** the guidance operation perturbs the modulation space in a way that happens to improve outputs regardless of the semantic content of the guidance direction (e.g., any sufficiently large perturbation at the right scale improves aesthetics). Distinguishing these matters because only (A) supports the paper's claim that the pooled embedding has untapped semantic utility.

The tension is sharpest for HiDream-Fast: Table 1 shows CLIP has *zero* effect on CLIP Score (30.3→30.3), PickScore (21.8→21.8), and ImageReward (7.9→8.1) even for short prompts, yet Table 2 shows modulation guidance on HiDream achieves 60% SbS win rate for aesthetics and 80% for complexity. If the pooled embedding has literally no effect in the default regime, how can amplifying it work? The paper's "What does modulation guidance actually do?" section only analyzes the hands correction case and does not address this question for the general aesthetics/complexity guidance that constitutes most of the results.

### Minor

**2. Missing stratification by prompt length in the main evaluation.** Section 4 establishes that CLIP's effect is prompt-length-dependent for FLUX schnell (short prompts: measurable; long prompts: negligible). However, the main evaluation (Tables 2–4) aggregates over COCO 2014 (5K prompts of varied lengths) and PartiPrompts (128 diverse prompts). Without stratification, the reader cannot tell whether the reported improvements are driven primarily by short-prompt cases (where CLIP has some signal to amplify) or hold uniformly across all prompt lengths. This is especially relevant since the paper's own Figure 1 shows the CLIP effect vanishing around 30–40 tokens.

**3. Potential model-variant discrepancy between analysis and evaluation.** The analysis in Section 4 uses HiDream-Fast (a 4-step distilled variant), finding CLIP has zero effect. The evaluation in Section 6 uses "HiDream" (the standard variant). If these are different model variants with different behaviors, the analysis and evaluation are not directly comparable. The paper should clarify whether the same model variant is used across both sections, and if not, whether the zero-effect finding generalizes to the standard variant used in the main experiments.

**4. Undiscussed trade-off in video results (Table 4).** For CausVid, dynamic degree improves substantially (75.25→86.59) while aesthetic quality slightly drops (57.85→57.65). The paper reports the dynamic degree improvement but does not discuss the aesthetic quality degredation. A similar pattern appears for Hunyuan (dynamic degree 50.51→53.61, motion smoothness 99.23→99.03). These trade-offs are worth acknowledging, especially since the guidance is applied using the same "aesthetics" prompts.

**5. Automatic metric improvements are small.** Across Tables 2–4, automatic metric gains are often 0.1–0.3 points (e.g., CLIP Score 35.6→35.8 for FLUX schnell aesthetics). Many entries are not bolded (meaning no improvement over original). The paper explicitly notes human-preference gains as the headline result, but the gap between large human-evaluation wins (~72% SbS) and tiny automatic-metric changes could benefit from discussion about what these metrics capture or fail to capture.

### Trivial

None.

---

## Nice-to-Haves

- **Control experiment with random guidance vectors.** Replacing the semantic direction (y(p₊,t) − y(p₋,t)) with random vectors of the same norm would directly test whether the semantic content of the pooled embedding matters or whether any perturbation of the modulation space suffices. This would help resolve the Major weakness above.

- **Confidence intervals for SbS win rates and GenEval scores.** The 128-prompt (general) and 70-prompt (object counting) evaluations have non-trivial uncertainty. Reporting standard errors or 95% confidence intervals would help assess whether the 4–8 point drops in "Relevance" for some conditions are real or noise.

---

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Baseline comparisons absent from main paper."** The paper references Appendix E (Tables 8, 9) for comparisons against Normalized Attention Guidance and Concept Sliders, and states the headline numbers (34%, 16% improvements). The appendix was stripped by the parser. Having detailed comparison tables in the appendix is standard practice.

- **"Human evaluation methodology underspecified."** The paper states "details in Appendix J" for the annotation protocol. The appendix was stripped by the parser; these details exist in the original submission.

- **"Training details are sparse."** Per standard practice, hyperparameter details (batch size, learning rate, MLP architecture) would reside in the appendix, which was stripped.

- **General section-by-section notes** (e.g., "Section 3 — Fine," requests for mechanistic analysis of *why* CLIP is inactive). These are either confirmations of the paper's adequacy or suggestions beyond the paper's scope.

---

## Novel Insights

The one genuinely novel insight from the review process is the possibility that the discrepancy between the analysis (HiDream-Fast: zero CLIP effect) and the evaluation (HiDream: clear modulation guidance improvements) could be explained by the two being different model variants. This goes beyond what the paper discusses and points to a specific, actionable clarification the authors should provide. Beyond this, the paper's own findings (CLIP is largely inactive; extrapolation in modulation space improves quality) are the main novel contributions—the review primarily reveals that the paper's explanatory framework for *why* the method works is incomplete.

---

## Suggestions

1. Resolve the central tension by adding a control experiment: replace the semantic guidance direction with random vectors of matched norm. If random vectors produce comparable improvements, the claimed mechanism (semantic steering via the pooled embedding) is not supported.
2. Stratify the main results by prompt length (short vs. long), especially given the paper's own finding that CLIP's effect is length-dependent.
3. Clarify whether HiDream and HiDream-Fast are the same model variant, and if not, confirm that the Section 4 analysis applies to the models evaluated in Section 6.
4. Acknowledge the aesthetic-quality trade-off in the video results and discuss it openly.

---

## Score and Decision

**Score: 6**

**Decision: Borderline Accept**

**Rationale:** The paper has a genuinely useful empirical finding and a simple method that produces consistent improvements across many settings. However, the unresolved tension between the "CLIP is inactive" analysis and the "amplifying CLIP works" method is a significant gap that weakens the paper's explanatory narrative. This is fixable—it requires additional analysis, not a fundamentally new method. As submitted, the paper's story is incomplete, but the empirical contributions are solid enough to warrant borderline acceptance with the expectation that the authors address the mechanism question.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>