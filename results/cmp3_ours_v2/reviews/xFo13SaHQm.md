Here is the final consolidated review.

---

## Summary

This paper identifies and formalizes a "copy-paste" artifact in identity-conditional image generation, where models replicate the reference face rather than generating the identity with natural variation. The authors contribute: (1) **MultiID-2M**, a large-scale paired dataset of ~500k group photos with reference images for ~25k identities; (2) **MultiID-Bench**, a benchmark with a Copy-Paste metric (M_CP) that quantifies how much a generated image biases toward the reference versus the ground truth; and (3) **WithAnyone**, a FLUX-based diffusion model with a paired-training strategy and ID contrastive loss that reduces copy-paste while maintaining identity fidelity.

## Strengths

1. **The copy-paste problem is well-motivated and convincingly demonstrated (Section 1, Figure 2).** The paper shows that natural face similarity for the same person varies between 0.30–0.77, while models like InstantID produce near-1.0 similarity, indicating over-copying. This is a genuine and underappreciated failure mode.

2. **The Copy-Paste metric M_CP (Eq. 2) is principled.** By computing the angular bias of the generated embedding toward the reference versus ground truth, normalized by reference–GT distance, the metric directly measures what the paper claims. Using Sim(GT) as the primary fidelity metric (rather than the commonly reported Sim(Ref)) is a real improvement over existing evaluation protocols.

3. **The GT-aligned landmark trick for ID loss (Section 5.1) is simple and effective.** Extracting landmarks from noisy diffusion outputs is unreliable; using ground-truth landmarks avoids this issue and works across all noise levels (Figure 7). This is a practical, reproducible insight.

4. **The paired-training design (Phase 3, Section 5.2) directly addresses the problem.** Using a different image of the same identity as target (rather than reconstruction where reference=target) breaks the shortcut that incentivizes copying. The ablation (Table 3) confirms its positive effect (CP=0.239 without Phase 3 → 0.161 with it).

5. **Quantitative results show a genuine improvement in the fidelity–diversity trade-off (Tables 1-2, Figure 5).** On the single-person subset, WithAnyone achieves Sim(GT)=0.460 (comparable to InstantID's 0.464) with CP=0.144 (versus InstantID's 0.337). Figure 5 shows WithAnyone sitting clearly off the regression curve that all other methods lie on — this is the paper's most compelling piece of evidence.

6. **Dataset scale and construction are well-documented (Section 3).** The four-stage pipeline is clearly described, and the corpus of ~500k paired images + ~1.5M unpaired images is a substantial resource released under responsible licensing.

## Weaknesses

### Major

- **The evaluation task is scene-reconstruction-conditional, not fully open-ended generation (Section 4).** MultiID-Bench provides a ground-truth image and a prompt *describing that GT*. The model is asked to reconstruct the scene described by the prompt. This differs from the real use case where a user provides a novel prompt specifying an entirely unseen scene. The availability of a GT image aligned with every test prompt means Sim(GT) measures how well the generated face matches a known target — a convenient proxy, but one that does not directly test generalization to novel pose/expression/lighting combinations without any matching GT. The paper does not discuss this proxy gap.

- **The extended-negatives ablation reveals a trade-off the paper does not fully explain (Table 3).** Removing extended negatives (dropping from 4096 to 63) *improves* CP (0.074 vs 0.161) while reducing Sim(G) (0.368 vs 0.405). The paper states the ID contrastive loss is "less effective" without extended negatives, but the actual numbers show a more complex pattern: extended negatives primarily help identity fidelity at the cost of increased copying. Since the paper's central claim is about breaking the fidelity–copying trade-off, this pattern warrants a more detailed explanation instead of the brief treatment it receives.

### Minor

- **The "breaking the trade-off" framing is stronger than the evidence supports (Abstract, Sections 1, 7; Tables 1-2).** WithAnyone achieves a *more favorable point* on the fidelity–diversity trade-off (comparable Sim(GT) to InstantID with much lower CP), not a bypass. For instance, on the single-person subset WithAnyone has Sim(GT)=0.460 — numerically slightly *below* InstantID (0.464). The paper would be more credible with measured language such as "achieving a substantially more favorable point on the trade-off."

- **The dataset is exclusively celebrities (Section 3), and generalization to non-celebrity faces is untested.** MultiID-2M is built from publicly known figures with hundreds of images each. The conditioning pathway — trained on identities with ~400 reference images on average — may not transfer to cases with 1–2 reference photos of non-public individuals. The paper does not acknowledge this limitation.

- **The user study (Section 6.3, Figure 8) has methodological weaknesses.** (a) Only 10 participants were recruited for ranking 230 groups of images across 4 criteria. (b) No inter-rater reliability metric is reported. (c) The bubble chart labels methods with names ("Cure", "UNO", "iDetch", "Uniformal", "OmniGen") that do not match the main tables — "Cure" is presumably WithAnyone but this is not stated. Given the strong quantitative evidence elsewhere, this study does not materially strengthen the paper.

- **The "FFHQ only" ablation (Table 3) is not informative as presented.** Training on FFHQ yields Sim(G)=0.224 and CP=0.027. The paper interprets this as showing the dataset's importance, but the CP score is artificially low because the model fails at identity fidelity. This confound means the row does not cleanly support the dataset's value — it only shows that training on too little data gives poor overall performance.

- **Critical hyperparameters for the ID contrastive loss are not reported in the main paper** (temperature τ; negative pool size M = 4096 is mentioned only in the ablation description). The contrastive loss is a claimed contribution but cannot be reproduced without these values.

### Trivial

- The OmniContext table formatting (Table 1b) is difficult to parse; the bold/ranking indicators appear inconsistent with the numerical values. This should be cleaned up in the camera-ready version.

## Nice-to-Haves

- A controlled experiment that isolates the paired-data benefit: same architecture, same training budget, same data volume, but one version uses paired targets and the other uses reconstruction targets throughout. This would directly measure whether the paired signal itself (rather than additional data or training) drives the CP reduction.
- A dedicated limitations section discussing the celebrity-domain constraint and GT-conditioned evaluation paradigm.
- Sensitivity analysis on the ArcFace clustering threshold (currently 0.4) and the CP score filtering threshold (Sim(GT) > 0.40).
- Justification or ablation of the 50% paired / 50% reconstruction mix used in Phase 3.

## Removed Points

These points from the input review were removed after verification against the paper:

- **Criticism about the OmniContext table being "confusing" with PuLID marked as best despite lower absolute scores** — The paper explicitly states "best among face customization models" (line 252), not best overall. General models like OmniGen2 are separate baselines, so the bold indicators are consistent with the paper's claim. The criticism misreads the scope of the claim.
- **Criticism that M_CP near -1 requires knowing GT scene structure** — This is by design; the metric measures relative bias toward reference vs. GT, and the paper clearly defines its range and meaning. This is not a flaw in the metric.
- **Generic concerns about missing appendix content, missing related work, or formatting/typos** — These are parser artifacts, not author errors.
- **Claim that the paired-data insight is "fairly straightforward once stated"** — This is subjective opinion, not a substantive weakness.
- **Criticism about the clustering threshold of 0.4 without evidence of downstream impact** — Speculative; no experiment was run to demonstrate harm.
- **Criticism that missing training details in main text is a major issue** — The paper references the appendix for full details; this is standard practice.

## Novel Insights

The most interesting observation emerging from the review is that the extended-negatives ablation (Table 3) shows a pattern where more negatives improve Sim(G) but worsen CP — suggesting the contrastive loss itself operates on the trade-off the paper claims to break. The paper acknowledges this implicitly but does not analyze it, which is a missed opportunity to deepen the contribution. Understanding why extended negatives increase copy-paste behavior (e.g., do they push the generated embedding toward a "mean face" that happens to be closer to the reference?) could yield further insight.

## Suggestions

1. Tone down the "breaking the trade-off" language throughout (abstract, introduction, conclusion) to something like "achieving a substantially more favorable point on the fidelity–diversity trade-off."
2. Add a limitations paragraph discussing the celebrity-domain scope and the GT-conditioned evaluation paradigm.
3. Report temperature τ and negative pool size M explicitly in the main paper.
4. Analyze the extended-negatives trade-off pattern more thoroughly — the fact that more negatives reduce CP is interesting and deserves explanation.
5. Clean up the user study reporting: clarify method naming, report inter-rater reliability, or consider removing the study if it adds limited value given the strong quantitative evidence.
6. Fix the OmniContext table formatting so bold/ranking indicators are unambiguous.

**Calibration Summary:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|-----------|
| ID-Booth (NWvsm2VxAM) | 3.00 | R1 | Much weaker — limited novelty, poor results, minor extension of prior work |
| DiffDeID (Bz9wjvToCS) | 4.40 | R1 | Different task (de-identification), weaker methodology, fewer ablations |
| MS-Diffusion (PJqP0wyQek) | 6.00 | R2 | Comparable area (multi-subject generation). Our paper has stronger problem motivation and more substantial contributions |
| UIFace (riieAeQBJm) | 6.00 | R1 | Related area (face generation for recognition). Comparable rigor |
| InstantPortrait (ZkFMe3OPfw) | 6.67 | R1 | Portrait editing with ID preservation. Our paper has broader contributions |
| Multi-Task Gen (cbv0sBIZh9) | 5.75 | R2 | Different task (multi-task generation). Not directly comparable |
| DiffusionGuard (9OfKxKoYNw) | 6.00 | R1 | Different task (defense against editing). Not directly comparable |

**Round 1 bracket:** 6.0–7.0. **Final score:** 6.5 — The paper is stronger than MS-Diffusion (6.0) in breadth of contributions and clarity of problem framing, and comparable to InstantPortrait (6.67) in overall quality.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>