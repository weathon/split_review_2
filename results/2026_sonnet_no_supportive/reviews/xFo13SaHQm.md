## Summary
WithAnyone addresses the "copy-paste artifact" in identity-consistent image generation—where models over-replicate reference faces rather than capturing identity flexibly. The paper contributes three things: (1) MultiID-2M, a large-scale 2M-image paired multi-person dataset with hundreds of diverse references per celebrity; (2) MultiID-Bench, a benchmark using Sim_GT and a Copy-Paste metric (M_CP, Eq. 2) that penalizes copying rather than rewarding it; and (3) the WithAnyone model (FLUX-based) trained with a GT-aligned ID loss and InfoNCE contrastive loss with an extended negative pool, which achieves high Sim_GT while falling substantially below baselines on the copy-paste trade-off curve (Fig. 5).

## Strengths
- **Compelling, quantified problem framing.** Fig. 2 shows natural same-person face similarity spanning 0.30–0.77, while InstantID produces a density peak near 1.0. This is not anecdotal—it is backed by distribution plots over thousands of examples and motivates the benchmark design concretely.
- **Sound Sim_GT metric design (Sec. 4).** Replacing Sim_Ref with Sim_GT as the primary metric is a genuine improvement: prior benchmarks rewarded copying because the reference and target were the same image; using a distinct GT image with natural pose/expression variation breaks that loophole. The M_CP metric (Eq. 2) operationalizes this cleanly.
- **GT-aligned ID loss is a technically clean contribution (Sec. 5.1).** Using GT landmarks rather than noisy denoised predictions enables applying the ID loss across all noise levels at negligible overhead. Fig. 7 demonstrates tighter, lower-variance ID loss gradients at all noise levels (0.2–0.8) compared to prediction-aligned landmarks.
- **Breaking the fidelity–copy-paste trade-off (Fig. 5).** All 12+ baselines lie on a single regression curve (higher Sim_GT ↔ more copy-paste); WithAnyone sits above this curve, achieving the highest Sim_GT among face-ID models while maintaining markedly lower CP. This scatter plot is unusually informative for a paper of this type.
- **Broad baseline coverage.** Evaluating 12+ systems—including GPT-4o-native, FLUX.1 Kontext, and OmniGen2—alongside ID-specific models makes the benchmark credibly comprehensive.

## Weaknesses

### Fatal
None.

### Major
- **Aesthetics deficit entirely unacknowledged.** Table 1a shows WithAnyone scoring 4.783 on aesthetics—the lowest among all evaluated methods, below InstantID (5.255), GPT-4o (5.344), InfU (5.389), and FLUX.1 Kontext (5.319). Phase 4 ("quality tuning") was explicitly designed to address this, yet the paper does not acknowledge that this phase did not succeed relative to baselines and provides no diagnostic. For a model presented as a practical step toward "controllable and ID-consistent generation," being worst on a perceptual quality metric is a real limitation that deserves at minimum one sentence of acknowledgment or diagnosis.

- **CP threshold interaction with ablation is undiscussed.** Tables 1 and 2 restrict CP ranking to cases where Sim_GT > 0.40 (single-ID). Table 3 reveals that "w/o Ext. Neg." achieves CP = 0.074 (the best score in that column) while Sim_GT = 0.368—below the threshold, which would exclude this ablation variant from CP ranking under the benchmark's own rules. The paper frames extended negatives as unambiguously beneficial, which is correct for the identity metrics, but the CP threshold interaction means the ablation's strongest-looking CP score is artificially not competing under the benchmark's own methodology. This asymmetry needs explicit discussion.

### Minor
- **OmniContext gap partially unaddressed.** Table 1b shows general customization models substantially outperform WithAnyone on the VLM-judged OmniContext benchmark (OmniGen2: 8.34, GPT-4o: 8.12 vs. WithAnyone: 6.52). The paper's explanation—that VLMs "exhibit limited ability to distinguish individual identities and instead emphasize non-identity attributes"—is plausible but not verified within the paper. A brief analysis of the conditions under which WithAnyone's identity-fidelity trade-off is preferred over general-purpose models would sharpen the practical narrative.
- **Phase 3 mixing ratio unjustified.** The 50% paired / 50% reconstruction split in Phase 3 (Sec. 5.2) is stated without ablation or sensitivity analysis. Since this ratio directly controls the copy-paste vs. identity trade-off, even a brief justification would strengthen the design claim.
- **Data contamination protocol not described in the main text.** Sec. 4 states the benchmark uses "rare, long-tail identities with no overlap to training data" but does not describe how deduplication or overlap verification was performed. Since both training and test data were sourced via celebrity search-engine pipelines over the same identity universe (~3k identities in training), the clean split assumption is non-trivial.

### Trivial
None.

## Nice-to-Haves
- Report CP scores without the Sim_GT threshold filter (e.g., a supplementary table) to make the metric fully transparent and sidestep the threshold-ablation interaction.
- Ablate the Phase 3 mixing ratio briefly to justify the 50/50 choice.
- Provide a failure analysis—when does WithAnyone exhibit residual copy-paste?—to clarify the contribution's boundaries.
- Diagnose the aesthetics deficit: does it arise from the FLUX backbone being under-trained for style fidelity, or from the contrastive loss pulling toward perceptually flat face-discriminative representations?

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **InfoNCE positive is GT, not reference (Sec. 5.1 note):** The reviewer notes that the positive in Eq. 5 is **t** (GT embedding), not the reference **r**, and suggests the paper should make this connection to Sim_GT explicit. This is a presentation enhancement suggestion, not a methodological flaw. The training objective is correctly aligned with the evaluation metric by design. Removed as a nitpick.
- **DreamID in Table 2 not introduced in baselines; InfU in Table 1 unlisted:** These are potentially minor editorial inconsistencies. Without access to the appendix (which the parser strips), we cannot confirm these are not addressed there. Removed per the rule on appendix references.
- **User study statistical significance:** 10 participants and 230 groups is noted as limited. Single-run evaluation with small user studies is standard in this community for supporting evidence. Moved to nice-to-have territory; not a weakness.

## Novel Insights
The framing of copy-paste as a measurable artifact—distinct from identity similarity—and the demonstration that all existing methods lie on a single fidelity/copy-paste regression curve while WithAnyone breaks it (Fig. 5) is a genuinely novel and empirically grounded finding. The GT-aligned ID loss insight (using GT landmarks rather than noisy denoised landmarks for ArcFace alignment) is a clean practical contribution applicable beyond this paper. The finding that extending the negative pool from ~63 in-batch samples to 4096 is critical for InfoNCE effectiveness in face generation—as demonstrated by the ablation—is an underappreciated empirical result.

## Suggestions
- Acknowledge the aesthetics deficit in the main text and provide at least a brief diagnostic or hypothesis for why Phase 4 quality tuning did not recover parity.
- Add a supplementary table showing CP scores without the Sim_GT threshold filter, or explicitly discuss how the threshold filter interacts with the ablation in Table 3.
- Describe the train/test identity deduplication procedure in the main paper (even one paragraph).
- Ablate the Phase 3 mixing ratio to justify the 50/50 choice.

---

## Calibration and Score

**Anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| IjVCcykKdr (RetriBooru) | 4.50 | R1 (3.5–5.5) | Same problem (reference leakage in subject-driven gen), anime dataset, weaker experiments—WithAnyone is substantially stronger |
| daRu82GAoZ (ID²) | 5.00 | R1 (3.5–5.5) | Different task (origin ID); rejected; less relevant |
| 4GSOESJrk6 (DreamBench++) | 6.00 | R1 (5.5–7.5) | Benchmark for personalized generation with VLM eval; accepted; comparably broad but less novel methodology |
| riieAeQBJm (UIFace) | 6.00 | R1 (5.5–7.5) | Synthetic face recognition, intra-class diversity; accepted; narrower scope |
| f8S3aLm0Vp (DIAGNOSIS) | 6.50 | R1 (5.5–7.5) | Unauthorized data detection in diffusion models; accepted |
| FoMZ4ljhVw (PnP Inversion) | 6.50 | R1 (5.5–7.5) | Diffusion image editing improvement; accepted; comparable technical clarity |
| SctfBCLmWo (Dataset bias) | 8.00 | R1 (7.5–8.5) | Dataset bias analysis; broader impact, stronger novelty |
| 84n3UwkH7b (Memorization detection) | 8.00 | R1 (7.5–8.5) | Clean contribution, strong acceptance; more fundamental finding |

**Round 1 bracket:** 6.0–7.0.

**Reasoning:** WithAnyone is substantially stronger than RetriBooru (4.5)—it operates on real celebrity photos at 2M scale, has more rigorous evaluation, a FLUX-based model with novel training objectives, and a broader baseline comparison. It is comparably strong to DreamBench++ (6.0, accepted), with more technical novelty (GT-aligned loss, InfoNCE with extended negatives, Fig. 5 trade-off analysis). The main drags are: aesthetics deficit unacknowledged (a real but bounded omission), CP threshold-ablation interaction (needs discussion, not a fatal flaw), and OmniContext gap partially unaddressed. These are real but do not undermine the core contribution. The paper sits solidly in the 6.0–6.5 range. I assign **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>