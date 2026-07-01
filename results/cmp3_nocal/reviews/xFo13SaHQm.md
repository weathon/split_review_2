## Summary

This paper makes three contributions to identity-consistent image generation: (1) **MultiID-2M**, a large-scale dataset of ~500k paired group photos with 25k+ identities plus 1.5M unpaired images; (2) **MultiID-Bench**, a benchmark that replaces the conventional Sim(Ref) metric with Sim(GT) (similarity to a ground-truth image of the same identity in a different pose/expression) and introduces a Copy-Paste metric (M_CP) to quantify reference bias; and (3) **WithAnyone**, a diffusion model built on FLUX that uses paired training data, a GT-aligned ID loss, and an ID contrastive loss with extended negatives to reduce copy-paste artifacts while maintaining identity fidelity. The central thesis is that paired training data enables breaking the trade-off between identity similarity and copy-paste.

## Strengths

1. **The copy-paste problem is real and well-motivated.** Section 1 (Fig. 2) concretely demonstrates that natural face similarity between different photos of the same person varies substantially (scores 0.77, 0.46, 0.46, 0.30), yet models like InstantID and PuLID cluster near 1.0 similarity to the reference. This identifies a genuine failure mode that existing evaluation metrics obscure.

2. **MultiID-Bench's use of Sim_GT as the primary metric (Eq. 1, lines 71–75).** Prior work reports Sim(Ref), which mechanically rewards copying. Replacing it with similarity to a ground-truth image of the same identity (different pose/expression) is the right way to measure whether a model has actually learned the identity rather than memorized the specific reference.

3. **The copy-paste metric M_CP (Eq. 2, lines 85–89).** Formalizing the relative bias toward reference vs. ground truth as a normalized angular distance is well designed. The [-1, 1] range is intuitive, and normalizing by the reference–ground-truth distance prevents trivial inflation.

4. **The GT-aligned ID loss (lines 105–109).** Using ground-truth landmarks to align generated images for ArcFace embedding extraction—rather than detecting landmarks on noisy generated images or applying the loss only at low noise levels—is a practical insight that cleanly sidesteps a known engineering problem.

5. **MultiID-2M scale and construction pipeline.** 500k paired group photos + 1.5M unpaired, ~25k identities, with a systematic four-stage construction pipeline, is a substantial community resource. The ethics and anonymization measures (lines 63–65, 307–313) are appropriately detailed.

## Weaknesses

### Fatal

None.

### Major

1. **Ablation study reveals a contradictory pattern that the paper does not discuss.** Table 3 shows that removing extended negatives (leaving only 63 in-batch negatives) *improves* the Copy-Paste metric (CP = 0.074) relative to the full model (CP = 0.161). The paper (line 285) states only that "the effectiveness of ID contrastive loss is greatly reduced," referring to the drop in Sim(G) from 0.405 to 0.368, but never acknowledges that CP improves. This matters because the extended negatives are presented as providing "stronger discrimination signals" (line 33), and the ablation suggests these signals come at the cost of increased reference-bias. The paper needs to explain why removing negatives reduces copy-paste, or revise its claims about what the contrastive loss contributes. This does not invalidate the method, but it undercuts the internal logic of the loss design narrative.

### Minor

2. **The "breaking the trade-off" claim exceeds what the evidence supports.** The paper states WithAnyone "breaks the long-observed trade-off between fidelity and artifacts" (lines 23–24, 303). Table 1 shows WithAnyone achieves Sim(GT)=0.460 (slightly *below* InstantID's 0.464) with CP=0.144 (substantially below InstantID's 0.337). This is a clear improvement on the Pareto frontier, but it does not constitute a categorical structural break — WithAnyone cannot simultaneously match InstantID's 0.464 Sim(GT) while keeping its own 0.144 CP. The claim should be recalibrated to "substantially improving the Pareto frontier" or "deviating from the existing trade-off curve," which is already well supported by Figure 5.

3. **WithAnyone has the lowest aesthetics score among all methods in Table 1 (Aes = 4.783), contradicting claims of visual quality.** The abstract claims WithAnyone "maintains strong perceptual quality" (line 9) and the contributions state "enhancing visual quality" (line 39), yet the reported Aes score is the lowest in the table (vs. GPT-4o's 5.344, InfU's 5.389, InstantID's 5.255). The user study (Fig. 8) shows higher aesthetics rankings, but with only 10 participants and no reported confidence intervals or inter-annotator agreement, this tension remains unresolved. The paper should either acknowledge this gap, provide evidence that Aes is not appropriate for this setting, or temper its quality claims.

4. **The evaluation construct favors the proposed method without acknowledging the asymmetry.** WithAnyone was trained on paired data for the exact task evaluated (given reference images and a ground-truth prompt, generate the scene). Baselines like InstantID and PuLID were trained for a different task (single-reference, reconstruction-based generation) and not on paired data. The paper frames results as "state-of-the-art performance" (line 39) rather than as evidence for the value of paired training on a specific task formulation. The gap between claimed generality and actual evaluation scope is material — it remains unclear how much of the improvement comes from the paired data versus the architectural design. Training a baseline on the same data (e.g., a paired-data variant of PuLID) would substantially strengthen the paper.

5. **The user study is too small and thinly described to support strong conclusions.** Ten participants ranking 230 groups across 4 criteria is described in two sentences (line 295). Figure 8 has garbled label names ("Cure" for WithAnyone — though this is a parser artifact), and no confidence intervals, inter-annotator agreement, or statistical testing is reported. The paper defers details to Appendix H (stripped), but as presented in the main text, the study does not provide meaningful quantitative support.

6. **No limitations section.** The conclusion (lines 297–303) restates contributions without acknowledging: (a) the dataset covers only celebrities from professional photo shoots; (b) the CP metric requires ground-truth images, limiting use to benchmark settings; (c) the method was not tested on non-celebrity, in-the-wild images where copy-paste artifacts would be most practically harmful.

### Trivial

7. **DreamID appears in Table 2 (multi-person subset) but is not introduced in the main-text baselines description (lines 198–199).** The baseline listing covers OmniGen, OmniGen2, Qwen-Image-Edit, FLUX.1 Kontext, UNO, USO, UMO, GPT-4o, UniPortrait, ID-Patch, PuLID, and InstantID, but DreamID is absent.

## Nice-to-Haves

- **Train a baseline on the same paired data.** The single most informative experiment would be training a baseline architecture (e.g., PuLID or InstantID) on MultiID-2M with the same four-phase pipeline, holding everything except architectural choices fixed. This would isolate whether the gains come from the data+training recipe or from WithAnyone's specific design.
- **Report inference speed, parameter count, and memory usage.** WithAnyone builds on FLUX (compute-heavy), and practical utility depends on efficiency.
- **Test on non-celebrity faces.** The entire evaluation uses celebrity faces; testing on non-public figures would better demonstrate general-purpose applicability.

## Removed Points

These points are flagged to be removed; treat them with caution.

- The critic's argument that "the trade-off is partly a mathematical artifact of the CP metric" (because high Sim(Ref) mechanically yields high CP) is removed. CP is *designed* to measure reference-bias; this criticism misunderstands the metric's purpose.
- "OmniContext evaluation feels like padding" — removed as speculative. The paper includes it as complementary evidence with appropriate caveats.
- "Abstract overstates 'Extensive experiments'" — removed as a subjective nitpick; the paper does present substantial experiments.
- "Table 2 is difficult to parse" — this is a parser artifact from PDF extraction, not an original-submission issue.
- Missing related works — removed per instruction (cannot verify external completeness).
- Formatting/style nitpicks — removed per instructions.

## Novel Insights

The most notable insight from the review process is the tension in the ablation study (Weakness 1): the contrastive loss with extended negatives improves identity similarity (Sim(G) from 0.368→0.405) but simultaneously increases copy-paste (CP from 0.074→0.161). This suggests that "pulling the generated image toward reference images of the same identity" (line 115) has a side effect of also pulling it toward the specific reference image, re-introducing a mild form of the very copy-paste the method aims to eliminate. The paper's framing of the contrastive loss as unambiguously beneficial is incomplete — there is a genuine trade-off within the method itself that warrants analysis.

## Suggestions

1. Recalibrate "breaking the trade-off" to "substantially improving the Pareto frontier" or "deviating from the existing trade-off curve."
2. Add a frank discussion of the ablation result: why does removing extended negatives improve CP? Is the contrastive loss trading identity fidelity for reference-bias in a way worth characterizing?
3. Acknowledge the aesthetics gap and either explain why Aes may not capture the relevant notion of perceptual quality in this setting, or temper the visual quality claims.
4. Add a limitations section to the conclusion.
5. If possible, include a baseline trained on the same paired data (or acknowledge this as a remaining open question).

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>