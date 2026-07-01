## Summary

This paper proposes Gen2Seg, a method to finetune generative models (MAE and Stable Diffusion) for category-agnostic instance segmentation using a novel instance coloring loss. Trained on only ~86K synthetic images of indoor furnishings and cars (Hypersim + Virtual Kitti 2), the models exhibit strong zero-shot generalization to unseen object types (humans, animals, art, x-ray luggage) and image styles. The method treats segmentation as image-to-image translation, avoiding task-specific heads, and the loss encourages intra-instance color consistency and inter-instance separation without requiring pre-assigned color labels. The paper provides extensive experiments showing that the approach approaches or matches SAM's performance on several datasets while outperforming it on fine structures (iShape, BSDS500 edges).

## Strengths

- **Genuinely novel and well-demonstrated empirical finding.** The result that a model finetuned on narrow mask supervision (~86K synthetic images of only indoor furnishings and cars) generalizes to segmenting humans, animals, art, x-ray luggage, and fine wire structures is striking. This is the paper's strongest contribution and is credibly supported by the evidence across multiple evaluation datasets.

- **Clean, principled method design.** The instance coloring loss (intra-instance variance + inter-instance separation + mean separation, Equations 3-5) is well-motivated, avoids the permutation-invariance problem of directly regressing to arbitrary color assignments, and elegantly repurposes the generative model's native image-to-image translation capability without adding task-specific heads. This is conceptually simple and architecture-agnostic.

- **Strong controlled experiments on training data diversity (Table 2).** The ablation showing that performance with only 10 Hypersim classes nearly matches the full 33+ classes, and that even 5 object types (books, chairs, lamps, tables, pillows) yield meaningful generalization, is a particularly convincing piece of evidence that the observed generalization is not simply memorization of training categories. This experiment directly supports the paper's core thesis.

- **Compelling results on fine structures and boundaries.** The iShape results (Gen2Seg SD: 51.4 vs SAM: 16.8) and the BSDS500 edge AP results (Gen2Seg SD: 93.4 vs SAM: 79.0) are large, consistent advantages. Even accounting for possible evaluation biases, these gaps are too large to dismiss and point to a genuine property of the approach.

## Weaknesses

### Fatal
None.

### Major

- **The DINO comparison does not cleanly support the "generative vs. discriminative" claim.** The paper argues that generalization is specific to *generative* pretraining and contrasts with "discriminatively pretrained models [that] fail to generalize" (abstract). The primary evidence is the DINO-B baseline (Table 1: 35.0 mIoU on COCO_exc^L vs. Gen2Seg MAE-B's 44.6 and Gen2Seg SD's 57.6). However, the DINO-B architecture is: DINO encoder → "simple up-conv" → **frozen VAE decoder from Stable Diffusion** (Section 4.2). This introduces at least two confounds relative to the MAE baseline: (1) MAE uses its own pretrained decoder, which was trained to reconstruct pixels at full resolution and thus has strong pixel-level priors, while DINO receives a decoder designed for a different latent space; (2) the MAE decoder is finetuned end-to-end, while the VAE decoder attached to DINO is frozen and may not adapt to the task. The comparison conflates "generative vs. discriminative encoder" with "has vs. lacks a compatible, finetuned decoder." A properly controlled comparison would pair DINO with a learned decoder of similar capacity and training regime as MAE's. **This does not invalidate the paper's core empirical finding** — the fact that generative models finetuned on narrow data generalize well remains valid and interesting — but it means the theoretical interpretation (that generalization is unique to generative pretraining) is not adequately supported by the presented evidence. The paper should temper claims accordingly.

### Minor

- **Edge AP metric truncation without full metrics.** The BSDS500 evaluation reports Edge AP "for recall less than 20%" (Section 4.4). This truncates the precision-recall curve to the highest-precision portion, which can favor methods that produce fewer but more precise boundary pixels over methods with more complete boundaries. The paper references full PR curves in the appendix (stripped) but should also report standard BSDS500 benchmarks (ODS/OIS F-measure) in the main text to make the edge detection claims directly comparable to the extensive prior literature and rule out metric-selection bias.

- **No variance or statistical significance estimates.** All results in Tables 1 and the edge AP table are reported as single numbers with no error bars, confidence intervals, or mention of multiple runs. Given stochastic optimization, the reader cannot assess whether reported differences (e.g., SD's 57.6 vs. SAM's 57.0 on COCO_exc^L) are meaningful or within noise. While single-run reporting is common in large-benchmark evaluations, the paper's comparative claims would benefit from basic variance information.

- **Loss hyperparameters not specified in main text.** The hyperparameters λ_sep and λ_mean are introduced in Equation 6 but their numerical values are not given in the visible portion of the paper. Training details (learning rate, optimizer, batch size) are also deferred to the appendix. These are important for reproducibility and for understanding the sensitivity of the method.

### Trivial
None.

## Nice-to-Haves

- A properly controlled discriminative baseline: train a model with the *same* instance coloring loss and a *similar-capacity learned decoder* but with a discriminatively pretrained encoder (e.g., DINOv2, supervised ViT). If such a model generalizes comparably to MAE-B, the paper's generative-specific claim is unsupported; if it fails, the claim is substantially strengthened.
- Report standard BSDS500 benchmarks (ODS/OIS F-measure) alongside the truncated Edge AP.
- Report iterative prompting results (described in Section 4.3 but absent from main tables) to complement the single-point results.

## Removed Points

These points were considered but removed with justification:

1. **"SAM comparison is not calibrated to the evaluation protocol"** — Removed because the paper explicitly evaluates SAM using a single prompt point at the ground truth center (Section 4.3: "Following Kirillov et al. (2023)"), which is the standard SAM evaluation protocol. The reviewer's concern about "SAM's automatic mask generator" conflates the instance segmentation evaluation (which uses SAM's interactive point-prompt mode) with the edge detection evaluation (which uses SAM's AutoMaskGenerator, as stated in Section 4.4). The 16.8 mIoU on iShape is not "suspiciously low" — the paper provides qualitative evidence (Figure 2 caption) that SAM fails on fine structures, and iShape is explicitly a dataset for complex fine structures where SAM is known to be weaker.

2. **"The 'inherent grouping mechanism' claim is over-interpreted"** — This is a reasonable observation but is already subsumed by the Major weakness on the DINO comparison confound. The core scientific claim that requires tempering is the generative-vs-discriminative distinction, not the "inherent" phrasing.

3. **"DINO was presumably trained on ImageNet-1K... If it is DINOv1 on ImageNet-1K"** — The paper cites DINO (Caron et al., 2021), which is a specific work. Speculating about which checkpoint variant was used is not a substantive weakness without evidence that different checkpoints would yield different results.

4. **"The toddler analogy vs. LAION-2B zero-shot framing"** — The reviewer makes an interesting observation about the framing but this is not a weakness of the paper's technical contribution; it is a presentational nuance.

5. **"The 'disabling loss for unknown objects' should be discussed more prominently"** — The paper mentions this design choice in Section 4.2 ("To ensure the model does not see the masks of unknown categories, we disable the loss for pixels within the bounding box of all unknown objects"). It is already described in context.

6. **Strengths removed as generic/delusional/superficial:** None of the four listed strengths were removed — all are specific, evidenced, and grounded in the paper's content.

7. **"SimpleClick... fails, but SAM generalizes well — claim should be qualified"** — The paper's abstract claim about "promptable segmentation architectures" is illustrated by SimpleClick's failure, not SAM's. SAM is presented as the high-water mark. This is already clear in context.

## Novel Insights

The key insight emerging from the reviews is that the paper's empirical contribution (generative models finetuned on narrow data generalize broadly) is stronger and better-supported than its theoretical interpretation (that this generalization is unique to *generative* pretraining vs. discriminative pretraining). The controlled ablation on training data diversity (Table 2) is particularly insightful and somewhat underappreciated: the finding that performance plateaus with as few as 10 object classes (and shows non-trivial generalization even with 5 classes or ClevrTex simple shapes) is strong evidence that the generalization arises from the pretrained structure rather than finetuning diversity. The large margins on fine structures (iShape, BSDS500) are genuinely novel and merit deeper investigation — they suggest that the pixel-level pretraining objective of generative models preserves boundary details that discriminative pipelines (which discard low-level information through progressive downsampling) may lose.

## Suggestions

1. **Temper the "generative vs. discriminative" claim throughout the paper.** The abstract and conclusion claim that "discriminatively pretrained models fail to generalize" and that generalization is specific to generative pretraining. Acknowledge the DINO comparison confound explicitly and qualify the claim to "generative models *in our comparison* generalize" rather than making a universal statement.

2. **Add standard BSDS500 metrics (ODS/OIS F-measure).** Supplement or replace the truncated Edge AP with full PR curves and standard benchmarks to make the edge detection claims directly comparable to prior literature.

3. **Report basic variance information.** Even a single additional run showing min/max or reporting on a subset of datasets would help calibrate the reader's confidence in comparative claims.

4. **Move key hyperparameters (λ_sep, λ_mean, learning rate, batch size) to the main text.** These are essential for reproducibility and understanding method sensitivity.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>