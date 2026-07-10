Now I have all the information needed. Let me produce the final consolidated review.

---

## Summary

The paper tackles a well-motivated problem in identity-consistent image generation: the "copy-paste artifact" where models replicate reference faces verbatim rather than generating natural variations of an identity. It contributes (1) **MultiID-2M**, a large-scale paired multi-ID dataset (~500k paired images, ~25k identities) that enables training with multiple references per identity; (2) **MultiID-Bench**, a benchmark with a novel Copy-Paste metric (M_CP) that quantifies the relative bias toward reference vs. ground-truth; and (3) **WithAnyone**, a FLUX-based model trained via a four-phase pipeline with GT-aligned ID loss and ID contrastive loss. The method demonstrably reduces copy-paste artifacts while maintaining competitive identity similarity.

## Strengths

- **The paper identifies and formalizes the "copy-paste artifact" problem convincingly (Fig. 2, Section 1):** Real photos of the same person vary in similarity (0.30–0.77 in their example), while current models peak sharply at 1.0. This is a grounded, actionable diagnosis of a failure mode that prior work tolerated or inadvertently rewarded. The problem framing is the paper's strongest contribution.

- **The Copy-Paste metric (M_CP, Eq. 2) is a conceptually clean contribution:** By measuring the relative bias of the generated embedding toward the reference versus the ground truth, normalized by reference-GT angular distance, the metric separates "good identity preservation" from "copying the reference." It is simple, interpretable (range [-1, 1]), and captures something prior metrics missed — this is likely to be useful to the community beyond this specific method.

- **MultiID-2M fills a genuine data gap:** The lack of paired multi-ID data has constrained the field to reconstruction-based training. A dataset with ~500k identified multi-ID images, ~25k identities, and matched references at this scale — released under permissive licenses with thoughtful privacy measures (anonymized internal IDs, no personal names in training) — is a substantial resource for the community.

- **The GT-aligned ID loss (Eq. 4) is a practical architectural improvement:** Using GT landmarks rather than predicted ones to enable ID supervision across all noise levels is well-motivated by the noisy-landmark problem and cleanly solves a limitation of prior work (PortraitBooth's low-noise-only restriction, PuLID's full-denoisal cost). The four-phase training pipeline is internally consistent and follows from the paper's diagnosis.

## Weaknesses

### Major

- **The "breaking the trade-off" claim is inflated relative to the evidence.** The headline claim — "breaking the long-observed trade-off between fidelity and artifacts" (abstract, conclusion) — rests on the observation that WithAnyone occupies a different region of the Sim(GT)-vs-CP scatter plot than baselines (Fig. 5). However, WithAnyone is explicitly trained on paired data with objectives L_ID (Eq. 4) and L_CL (Eq. 5) that directly optimize closeness to GT and separation from negatives — i.e., the very quantities measured by the benchmark. Baselines were trained with reconstruction objectives where reference = target. The results show meaningful improvement consistent with the method's design, but the most parsimonious explanation is that paired training with aligned objectives yields expected outcomes, not that the method has escaped a fundamental constraint. This does not invalidate the contribution — the method genuinely addresses a real problem — but the framing should be recalibrated to "successfully addressing copy-paste via paired training" rather than "breaking a trade-off." A cross-evaluation experiment (e.g., fine-tuning baselines on paired data) would strengthen the causal claim.

### Minor

- **Sim(GT) as the primary identity metric has inherent limitations.** Identity is a latent variable, not a specific photograph. A model that generates a different natural image of the same person (different expression, pose, lighting) would score lower on Sim(GT) despite perfect identity preservation, while a model that memorizes the exact GT image would score 1.0 (the CP metric flags this, but Sim(GT) remains the primary identity metric in every table). The paper partially addresses this through the companion CP metric and the Sim(GT) > 0.40 filtering criterion, but the strongest claims ("state-of-the-art identity similarity") rest on Sim(GT) without acknowledging this limitation.

- **The user study is too thin to carry the claims placed on it.** Ten participants is a small sample for a ranking study with 230 groups × 4 criteria. The strong statement that results "indicate that our method consistently achieves the highest average ranking across all dimensions" (Section 6.3) is weakly supported at this sample size, and key details are deferred to the appendix. The naming inconsistency in Fig. 8 (the method is called "Cure" in the caption, not "WithAnyone") also suggests possible figure-preparation issues. The user study should be expanded or the claims hedged.

- **The ablation results contain subtleties the paper glosses over.** Removing extended negatives (w/o Ext. Neg.) improves CP from 0.161 to 0.074 while dropping Sim(G) from 0.405 to 0.368. The paper states this "greatly reduced" the loss's effectiveness, but the CP improvement is not discussed. The relationship is explainable (weaker identity preservation → fewer copy-paste artifacts), but this nuance should be addressed transparently rather than presented as an unambiguous ablation success.

- **WithAnyone's aesthetics scores are consistently at the lower end** (4.783 in Table 1 vs. 5.344 for GPT-4o, 5.389 for InfU), yet the paper does not acknowledge or explain this pattern, despite Phase 4 being described as "quality tuning" to "enhance perceptual fidelity."

### Trivial

- None that survive filtering.

## Nice-to-Haves

- Report training cost (GPU-hours, dataset throughput) to aid reproducibility assessment.
- Add a cross-evaluation experiment: fine-tune baselines on a subset of MultiID-2M's paired data to test whether the paired data or the specific architecture drives the improvement.
- Clarify the "Cure" naming in Fig. 8 and ensure figure-baseline names match the paper.

## Removed Points

- *Abstract's "hundreds of individual images" vs. actual distribution:* The reference bank has ~3k identities at ~400 each, so "hundreds" applies there, not to the 25k multi-ID identities. The abstract is slightly imprecise but not incorrect.
- *OmniGen2 and GPT-4o achieving competitive/lower CP:* These are general models, not face customization models. The paper's claim about being best among face customization methods is accurate.
- *Computational cost not reported:* Moved to Nice-to-Haves.
- *Speculation about missing appendix content:* The parser strips these sections; they exist in the original submission.

## Novel Insights

None beyond the paper's own contributions. The reviewer's primary insight — that the evaluation alignment between training objectives and metrics inflates the "breaking" narrative — is a framing observation, not a novel finding about the method or problem.

## Suggestions

1. Reframe the contribution: replace "breaking the trade-off" with language emphasizing that paired training directly addresses the root cause of copy-paste artifacts, and that the observed improvement is the expected outcome.
2. Discuss the Sim(GT) limitation more explicitly — a sentence in Section 4 or a Limitations paragraph would suffice.
3. Expand the user study or hedge claims about it proportionally.
4. Address the w/o Ext. Neg. CP improvement in the ablation discussion.
5. Comment on the aesthetics score pattern.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>