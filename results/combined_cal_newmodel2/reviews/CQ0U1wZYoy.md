Now I have enough calibration data. Let me compile the final review.

## Summary of Calibration Anchors

| Path | Score | Decision | Round | Itemized? | Comparison |
|------|-------|----------|-------|-----------|------------|
| `u1cQYxRI1H` | 0.50 | Accept | R1 | No | Very different paper (lighting editing, not restoration) |
| `kCnLHHtk1y` | 3.00 | Reject | R1 | No | Chinese architecture in diffusion - different domain |
| `b0qxhCaKIY` | 3.67 | Reject | R2 | No | Prompt + frequency for restoration - less sophisticated |
| `t3vnnLeajU` (DA-CLIP) | 5.25 | Accept | R1 | Yes | Closest anchor: CLIP-based all-in-one restoration with mixed degradation dataset. PRISM has stronger downstream evaluation and controllability analysis. |
| `vTdwuKUc5Z` | 4.25 | Reject | R1 | No | Text-prompt SR - narrower scope |
| `PacBhLzeGO` (DCPT) | 6.25 | Accept | R1, R2 | Yes | Universal restoration via degradation pre-training. PRISM's compound degradation focus and controllability are more novel. |
| `6W35Wcs077` (DASL) | 6.25 | Reject | R1, R2 | Yes | SVD-based unified restoration. Comparable scope; PRISM has stronger scientific motivation and downstream evaluation. |
| `bEDTZxwJjT` | 5.50 | Reject | R2 | No | Diffusion for inverse problems - related but not directly comparable |
| `M5t0WvjfCg` (AdaIR) | 6.00 | Accept | R2 | No | All-in-one restoration via frequency mining. PRISM's controllability and downstream evaluation are distinctive. |

**Round 1 bracket**: 5.25–6.25. Based on DA-CLIP (5.25) as the lower anchor and DCPT (6.25) as the upper anchor. PRISM has more distinctive contributions than DA-CLIP (downstream evaluation, controllability, compound-aware training) but carries a real baseline confound. In Round 2, AdaIR (6.00) and DASL (6.25) confirm the bracket.

**Final score placement**: Comparing favorability-rated items, PRISM's top strengths (downstream evaluation at 12.51, Table 4 at 12.48, controllability finding at 14.02) match or exceed DCPT's top strengths (12.62, 11.30). However, the baseline confound weakness (favorability 0.48) is a genuine drag not present in the cleaner DCPT evaluation. This places PRISM between DA-CLIP (5.25) and DCPT (6.25) — at **6.0**.

---

# Final Review

## Summary

This paper presents PRISM, a conditional diffusion framework for removing compound (multiple simultaneous) degradations from scientific images. PRISM combines compound-aware supervision over mixed degradations with a weighted contrastive disentanglement objective to organize the latent space compositionally, enabling both automated full restoration and selective, prompt-driven removal of specific distortions. The paper introduces a downstream task evaluation framework (species classification, segmentation, fluorescence measurement) that is genuinely novel for the restoration literature, and demonstrates that selective restoration outperforms full restoration on 3 of 4 scientific tasks.

## Strengths

- **Well-motivated problem framing grounded in scientific imaging needs.** The paper correctly identifies that scientific restoration faces three real challenges that existing work handles poorly: compound (not single) degradations, the need for precision over perceptual quality, and the value of selective rather than blanket correction. The motivation in Section 1 and the supporting examples in Section 2.1 are specific and grounded in the scientific imaging literature (e.g., over-denoising erasing weak biological signals in microscopy).

- **Novel downstream utility evaluation (Tables 3, 4, Figure 6).** Assessing restoration quality through downstream task accuracy (species classification, segmentation mIoU, fluorescence measurement) rather than pixel-level metrics is a distinctive and practically significant contribution. Table 4's demonstration that the same restoration choice can improve segmentation mIoU while degrading fluorescence MSE is a clean, well-executed result that convincingly supports the paper's core claim that restoration choices are task-dependent.

- **Meaningful controllability finding (Table 3).** Showing that selective distortion-specific restoration outperforms full (black-box) restoration on 3 of 4 scientific tasks, with statistically significant p-values, is a substantive finding that runs counter to the default assumption in the restoration literature. The microscopy example in Figure 6 (where denoising erases biologically meaningful structures that super-resolution preserves) is visually compelling.

## Weaknesses

### Major

- **Baseline comparison is confounded by training data asymmetry.** Line 120 states: "For fair comparison, all baselines are trained on the fixed set of primitive distortions." This means the majority of baselines in Tables 1 and 2 (AutoDIR, MPerceiver, DiffPlugin, etc.) were trained on single-distortion data while PRISM was trained on compound mixtures of up to three distortions. This confound limits the strength of the headline quantitative claim that "PRISM outperforms state-of-the-art baselines on complex compound degradations." The paper partially mitigates this: (a) OneRestore is trained on composite data like PRISM and PRISM still outperforms it; (b) the internal ablation in Figure 3 (PRISM Primitive-Aware vs. Compound-Aware) directly demonstrates the benefit of compound-aware training within the same architecture. Nevertheless, retraining at least the strongest diffusion baselines on compound data would be needed to fully support claims of architectural or methodological superiority.

- **Selective restoration protocol for Table 3 is underspecified.** The paper reports that selective restoration (removing only some distortions) outperforms full restoration, but does not disclose how the "selective" choices were made — whether by domain experts, by the authors with access to test set ground truth, or by an automated procedure. Since the selection of which distortions to remove vs. preserve is the key independent variable in this experiment, the protocol must be stated for the results to be properly interpreted. This tempers the strength of the controllability claims.

### Minor

- **The claim of a "compositional" latent space lacks quantitative evidence.** The paper repeatedly asserts that the embedding space exhibits compositional structure that enables generalization to unseen mixtures, but provides only a qualitative visualization (Appendix Fig. 13). No metric or linear-probe experiment quantifies how well the embedding decomposes into separable distortion factors, or how compositional it is for unseen mixtures. A simple probe predicting which distortions are present from the embedding, tested on both primitive and compound mixtures, would substantially strengthen this claim.

- **The contrastive loss formulation (Eq. 1) may conflate two goals without analysis.** The loss simultaneously tries to (1) pull degraded embeddings toward the clean embedding (making them distortion-invariant) and (2) structure the degraded embedding space by distortion type (preserving distortion-specific structure). The paper does not discuss potential tension between these objectives or provide evidence that they are compatible under the proposed formulation.

### Trivial

- **Use of GPT-4 for prompt generation introduces non-determinism.** The training pipeline relies on GPT-4 to generate variable natural language prompts, which is not reproducible across API versions. The paper should release the exact prompt vocabulary used for evaluation.

- **The "Rooftop Cityscapes" dataset (listed as a contribution) is Cityscapes with standard synthetic haze/low-light augmentations.** The novelty of this dataset contribution is overstated.

## Nice-to-Haves

- Retraining the strongest baselines (AutoDIR, MPerceiver) on compound training data would cleanly disentangle the architecture effect from the data effect.
- A quantitative metric for compositional structure (e.g., linear probe accuracy for distortion prediction from embeddings) would substantiate the claimed latent geometry.
- Reporting which specific statistical test was used for the p-values in Table 3, and whether multiple-comparison corrections were applied, would improve methodological rigor.

## Removed Points

- **Information asymmetry in zero-shot prompts (Critique #2, second part).** Removed because the same standardized prompt set is used for all models, so there is no between-method information asymmetry. The prompt set's quality depends on PRISM's encoder, but conditioning is symmetric across methods.
- **Missing ablations of key components (Critique #4).** Removed per the rule that parser-stripped appendix content should not be critiqued. The paper states ablations are in Appendix E.
- **Critique about baselines being "deliberately handicapped" (part of Critique #1).** Weakened from "fatal/invalid" to "major confound" because OneRestore is fairly compared and the internal ablation addresses the core question.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions to Authors

1. Retrain at least 2-3 of the strongest baselines on the same compound degradation dataset PRISM uses, and report the updated Tables 1 and 2. This is the most impactful improvement.
2. Clearly describe how the selective restoration choices in Table 3 were determined. If they were chosen by the authors using test set knowledge, acknowledge this as a limitation and ideally add a small expert study or principled selection procedure.
3. Add a linear probe experiment to quantify the compositional structure of the embedding space.
4. Release the full set of GPT-4-generated prompts used in evaluation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>