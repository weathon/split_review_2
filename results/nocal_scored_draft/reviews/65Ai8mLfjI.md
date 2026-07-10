Now let me compose the final review based on the filtered and scored items.

## Summary

This paper revisits the role of pooled CLIP text embeddings (global conditioning) in modern diffusion transformers. It first demonstrates experimentally that this embedding is surprisingly inactive—contributing little in FLUX schnell for long prompts and nothing in HiDream-Fast. The paper then proposes *modulation guidance*, a training-free method that repurposes this underutilized component by applying CFG-style extrapolation in the modulation vector space (Equation 3: ŷ = y(p,t) + w·(y(p₊,t) − y(p₋,t))). A dynamic variant that skips early layers improves the aesthetics-fidelity trade-off. Experiments across text-to-image (5 models), text-to-video (2 models), and image editing demonstrate consistent quality improvements.

## Strengths

- **Clean empirical finding (Section 4, Table 1).** The controlled analysis zeroing out the pooled CLIP embedding and measuring effects across short/long prompts with multiple metrics (CLIP Score, PickScore, ImageReward) convincingly shows the embedding is partially inactive in FLUX schnell and fully inactive in HiDream-Fast. The analysis is methodologically sound and well-documented.

- **Simple, training-free method (Equation 3).** Modulation guidance is lightweight and elegant—repurposing a dormant component into an effective steering mechanism with negligible extra computation (two CLIP encoder passes). Its simplicity and training-free nature make it practical for deployment.

- **Mechanistic insight (Figure 4).** The attention map analysis showing that modulation guidance shifts focus toward task-relevant tokens (e.g., "hands" in hands-correction prompts) provides interpretability beyond black-box metric improvements. The token-group breakdown cleanly demonstrates the mechanism.

- **Practical dynamic variant (Figure 3b).** The layer-wise step function that skips early layers improves the aesthetics-fidelity trade-off over constant guidance, backed by empirical evidence (Figure 3a).

- **Broad evaluation.** Experiments span 5 T2I models (including few-step distilled models), 2 T2V models, and image editing—strengthening the case for generalization across architectures and tasks.

## Weaknesses

### Major

- **Unaddressed video quality trade-off (Table 4).** For CausVid, modulation guidance improves dynamic degree dramatically (75.25 → 86.59) but *reduces* aesthetic quality (57.85 → 57.65) and lags far behind the Normalized Attention Guidance baseline on aesthetic quality (NAG: 62.08 vs MG: 57.65, a gap of 4.43 points) and overall consistency (NAG: 19.61 vs MG: 19.02). The paper only highlights the dynamic degree improvement and states "improvements in dynamic degree" without acknowledging this trade-off. This omission is significant because a practitioner choosing between methods would need to weigh dynamic degree gains against aesthetic quality losses. The paper should transparently discuss this trade-off and characterize when modulation guidance is preferable versus NAG.

### Minor

- **Automatic metrics lack significance tests.** The improvements in Tables 2 and 3 are often small (e.g., PickScore 22.9→23.1, CLIP Score 35.6→35.8). Without confidence intervals or significance tests, it is unclear whether these differences are reliable or within the noise range. The human evaluation partially addresses this concern (showing larger, meaningful win rates), but the gap between the two evidence sources is not discussed, and the automatic metrics remain uncalibrated.

- **"Negligible overhead" not quantified.** The paper claims negligible runtime overhead but does not report wall-clock times or FLOP comparisons. While two extra CLIP encoder passes are indeed small relative to the full diffusion trajectory, a concrete quantification (e.g., "less than X% additional inference time") would substantiate the claim.

- **Relationship to CFG under-characterized.** Equation (3) is structurally CFG-style extrapolation (y(p,t) + w·(y(p₊,t) − y(p₋,t))) applied to the modulation vector rather than the model output. The paper notes this indirectly ("Our approach also relies on guidance in feature space") and distinguishes itself from CFG ("complements CFG," "additional degree of freedom beyond CFG"). However, more precise characterization of what is and is not novel about applying guidance in modulation space versus output space would strengthen the paper's positioning.

### Trivial

None.

## Nice-to-Haves

- Compare modulation guidance against output-space CFG with identical positive/negative prompts to isolate whether the benefit comes from the modulation-space locus or from the prompt engineering itself.
- Analyze sensitivity to the exact wording of positive/negative prompts.
- Systematically characterize failure modes or prompt types where modulation guidance degrades quality (beyond the brief mention of excessive w).
- Provide visualizations or analysis of the MLP that processes y to understand why the pooled embedding is inactive in some models.

## Removed Points

These points are flagged to be removed, treat them with caution:
1. **"Baseline comparisons in appendix only"** — Removed per guidelines: the parser stripped Appendix E; criticisms about absent appendix content are not valid.
2. **"Human evaluation details in missing appendix"** — Removed per same rule (Appendix J stripped by parser).
3. **"Fine-tuning procedure underspecified"** — Removed per rule on trivial implementation details (hyperparameters like learning rate, batch size).
4. **"Positive/negative prompt confound"** — Removed because the paper already compares against NAG and Concept Sliders which also use prompt engineering, partially controlling for this. The residual concern (a "just write a better prompt" baseline) is moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a discussion section for the video results in Table 4 comparing modulation guidance to NAG across all metrics, with a characterization of when each method is preferable.
2. Add confidence intervals or bootstrapped significance ranges for the automatic metrics in Tables 2 and 3.
3. Report concrete wall-clock overhead measurements to substantiate the "negligible overhead" claim.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>