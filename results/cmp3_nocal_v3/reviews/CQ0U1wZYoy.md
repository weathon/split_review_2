## Summary

PRISM introduces a conditional diffusion framework for compound degradation restoration in scientific images. It combines compound-aware supervision on mixed distortions with a weighted contrastive disentanglement loss that organizes the latent space so compound distortions are represented as structured combinations of primitives. This enables both joint removal of overlapping distortions and selective, prompt-driven correction. The paper evaluates across microscopy, wildlife monitoring, remote sensing, and urban domains, including a downstream task analysis.

## Strengths

1. **The problem framing is genuinely well-motivated.** The observation that scientific images suffer from compound degradations, that sequential removal cascades errors, and that "more restoration is not always better" (Section 4.2.1) is an important and underexplored thesis. The paper connects these observations to concrete scientific failure modes (over-denoising erasing faint bacteria in microscopy, generic denoisers oversmoothing marine features) rather than hand-waving.

2. **The weighted contrastive disentanglement loss (Section 3.2) is a clean technical idea.** Using Jaccard distance between distortion sets to weight contrastive pairs — so that haze+rain embeddings are pulled toward haze-only and rain-only embeddings more than toward unrelated distortions — directly targets the compositional structure the method needs. This is the paper's most novel component.

3. **The downstream task evaluation (Table 3, Section 4.2.1) is the paper's strongest empirical contribution.** Demonstrating that selective restoration outperforms full restoration on 3 of 4 scientific tasks, and that the optimal restoration strategy differs across tasks (e.g., super-resolution helps segmentation but hurts fluorescence in microscopy), directly supports the paper's central thesis. This kind of task-dependent analysis is rare in the restoration literature and genuinely informative.

## Weaknesses

### Fatal

None.

### Major

1. **No variance estimates on the main quantitative results (Tables 1 and 2).** Only Table 3 reports standard deviations and p-values; Tables 1 and 2 present single-point estimates. Given the modest gaps in Table 2 (e.g., ThapaSet: PRISM 22.36 PSNR vs. AutoDIR 21.53, UIEB: 22.18 vs. 21.02), it is not possible to assess whether the reported advantages exceed run-to-run variability. The paper's core quantitative claims about outperforming baselines would be substantially stronger with multi-run statistics or bootstrapped confidence intervals.

2. **The automated distortion predictor (MLP) is not evaluated.** The paper describes (Section 3.3, line 129) a lightweight MLP that predicts multi-label distortion sets from the image embedding, which feeds into the automated restoration pipeline and the zero-shot evaluation. However, the paper never reports precision, recall, or any accuracy metric for this classifier. Its failure modes (misclassifying distortions → wrong prompt → wrong restoration) are not analyzed or ablated. Since both the automated pipeline and the interpretation of zero-shot results depend on its quality, this is a significant gap.

3. **The selective restoration policies in Table 3 are not explained.** The paper states what was done (e.g., "restoring only contrast" for camera traps, "removing haze" for urban scenes) but does not specify how these policies were chosen — whether by domain expert intuition, by exhaustive search over combinations, or by some other procedure. Without this information, it is unclear whether the results reflect what a practitioner could achieve without access to ground-truth labels, or whether they represent an oracle upper bound. This limits the practical force of the claim that "controllability significantly improves downstream performance."

### Minor

1. **Tension between stated principles and main evaluation.** The paper argues (Section 4.2.1) that "restoration quality cannot be judged by appearance alone" and that PSNR/SSIM are insufficient for scientific evaluation. Yet the headline results (Tables 1, 2) rely entirely on these metrics, with the downstream evaluation (Table 3) positioned as secondary. The paper would be stronger if it front-loaded the task-based evaluation or acknowledged this tension more directly.

2. **Table 1 does not isolate the contrastive loss contribution.** The paper states that "all baselines are trained on the fixed set of primitive distortions" (line 120), meaning most baselines see only single-distortion examples while PRISM trains on compound mixtures. The one controlled baseline, OneRestore (trained on composites), trails PRISM by ~2.7 PSNR. This gap is informative, but the comparison against other baselines conflates the benefit of compound-aware training with the specific contrastive loss innovation. The paper's own within-model ablation (Figure 3, Primitive-Aware vs. Compound-Aware PRISM) provides cleaner evidence and should be foregrounded over the cross-model comparison.

3. **Zero-shot framing slightly overstates what is demonstrated.** The zero-shot evaluation (Table 2) maps real-world distortions onto pre-defined synthetic primitives via CLIP-based categorization, then applies manual prompts for those categories. This is a sensible approach, and the performance gaps (0.8–1.2 PSNR) are meaningful. However, framing this as "compositional generalization to unseen mixtures" overstates the evidence: the model is categorizing novel distortions into known buckets rather than decompositionally handling truly novel primitives. The modest gap magnitudes and lack of variance estimates also temper the strength of the claim.

### Trivial

None that survive filtering.

## Nice-to-Haves

- Re-center the paper around the downstream evaluation (Tables 3 and 4), which is the most novel and convincing evidence, rather than treating it as secondary.
- Report precision/recall of the automated distortion predictor to clarify how the pipeline behaves.
- Clarify how selective policies were determined for Table 3 — even a brief description (e.g., "policies were chosen by consulting a domain expert who inspected example images") would strengthen the presentation.
- The SCPM module (Section 3.2, line 118) and the automated prompting pipeline (Section 3.3) receive only 1–2 sentences each in the main paper with appendix deferrals; slightly more main-paper discussion would improve readability.

## Removed Points

These points from the input review are removed (with justification):

- **"Table 1 is structurally unfair and uninterpretable"** — REMOVED. The paper is transparent about the baseline training setup. The comparison against baselines trained on primitive distortions is standard practice in this literature. The paper explicitly identifies OneRestore as the controlled comparison (trained on composites like PRISM), and includes within-model ablations (Figure 3) that provide cleaner evidence. The criticism overstates the severity. The legitimate concern about not isolating the contrastive loss is retained as Minor #2.

- **"Zero-shot claims are overstated" as a critical issue** — REMOVED. The paper's zero-shot approach is reasonable for this setting; the performance gaps are meaningful. The remaining concerns (modest gap sizes, no variance, framing) are captured in Minor #3.

- **SCPM description too brief** — REMOVED as a minor presentational concern; the paper references the original work and the appendix for details.

- **"Missing distortion library details"** — REMOVED; these details are in Appendix B (stripped by the parser).

- **"Rooftop Cityscapes receives no evaluation"** — REMOVED; it appears in Table 3 (Urban scenes row). The paper also references Appendix C for details.

- **Section-by-section notes about speculatively missing content** — REMOVED as they either concern appendix-stripped content or reflect presentational preferences rather than substantive flaws.

## Novel Insights

The harsh review correctly identifies that the paper's strongest and most distinctive evidence lies in the downstream task evaluation (Table 3), which shows that different scientific analyses on the same data require different restoration strategies (e.g., super-resolution improves segmentation but hurts fluorescence in microscopy). This insight — that restoration is task-dependent and that controllability is a necessity rather than a convenience — is the paper's most novel empirical finding. The main quantitative comparisons (Tables 1, 2) are standard for the field but do not carry the same weight, and the paper would benefit from positioning this task-dependency analysis as its central contribution.

## Suggestions

- Report multi-run statistics or confidence intervals for Tables 1 and 2 to establish that the reported gaps exceed noise.
- Evaluate the automated distortion predictor (precision/recall by distortion type) so readers can assess the reliability of the automated pipeline.
- Clarify how selective restoration policies were chosen for Table 3 — even a brief description of the protocol would resolve the ambiguity.
- Consider re-ordering the results so the downstream task analysis (Section 4.2.1) appears before the metric-based comparisons (Section 4.1), which would align the paper's structure with its stated principles.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>