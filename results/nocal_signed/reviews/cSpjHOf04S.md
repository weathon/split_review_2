Now let me compose the final review.

## Summary

This paper proposes Gen2Seg, a method that fine-tunes pretrained generative models (Stable Diffusion and MAE) for category-agnostic instance segmentation by converting the task into image-to-image translation. Using a novel instance coloring loss (L_IC) that enforces intra-instance color consistency and inter-instance separation, the model is finetuned on only two narrow synthetic domains (indoor furnishings from Hypersim and cars from Virtual KITTI 2) comprising ~87K images. Despite this limited mask supervision, the resulting models exhibit strong zero-shot generalization to unseen object types (people, animals) and styles (art, X-rays), approaching or exceeding SAM's performance on some metrics while using orders of magnitude less labeled data. The finding that even MAE — pretrained on unlabeled ImageNet-1K — generalizes to unseen categories is the paper's most surprising result.

## Strengths

- **Clean, architecture-agnostic method.** The instance coloring loss converts instance segmentation into a regression problem in RGB pixel space, avoiding task-specific mask decoders or set-prediction heads. This design choice preserves the full generative pipeline's pretrained priors and works identically across diffusion and MAE architectures.

- **MAE zero-shot generalization is genuinely surprising.** Table 1 shows MAE-H (pretrained on unlabeled ImageNet-1K only) achieving 50.0 mIoU on COCO_exc^L, 40.3 on DRAM (art), and 34.9 on iShape (fine structures) — far above DINO-B (35.0/29.4/27.4) and SimpleClick (1.4/2.4/1.6). That a model pretrained without labels on a single-domain dataset can segment objects it has never seen a mask for is a compelling finding.

- **Controlled finetuning-data experiments (Table 2) provide strong causal evidence.** The systematic ablation of finetuning diversity — full Hypersim+VK2 → COCO → ClevrTex → 10 classes → 5 classes — isolates the effect of training data on generalization. The finding that 10-class finetuning yields results nearly identical to the full 33+ class set directly supports the claim that the behavior stems from the generative prior, not coincidental category overlap.

- **Edge detection evidence is concretely grounded.** The paper uses a Sobel filter on feature maps (a strictly worse proxy than a learned edge detector) to measure boundary quality, yet SD (COCO) — finetuned on polygonal COCO masks — still produces cleaner edges than SAM (trained on polygonal SA-1B masks). The <5 point degradation when switching from synthetic to COCO data strengthens the attribution to the generative prior.

## Weaknesses

### Major

- **Overclaiming against SAM in the abstract and introduction.** The paper states that models "outperform [SAM] when segmenting fine structures and ambiguous boundaries" without adequate qualification. While the evidence (iShape: SD 51.4 vs SAM 16.8; BSDS500 edge AP) does support this claim under the specific evaluation setup used, the framing lacks necessary context: (a) the instance segmentation results use a single-center-point prompt protocol, (b) the edge detection claim rests on a non-standard metric slice (AP at recall <20%). The paper's core contribution — zero-shot generalization from generative priors — does not depend on beating SAM, and the paper would be more credible by presenting SAM as a heavily-supervised upper bound and quantifying what fraction of its performance is recovered with orders-of-magnitude less supervision.

- **Edge detection AP is reported at a non-standard operating point.** The paper reports "AP for recall less than 20%" on BSDS500, which deviates from the standard ODS/OIS F-measure across the full precision-recall curve. Reporting only the high-precision regime mechanically favors methods that produce fewer, cleaner edges over methods that produce more abundant but potentially noisier ones. Full curves are referenced to Appendix B, but the central claim about "crisper boundaries" than SAM rests on this non-standard slice without justification in the main text. Full-curve metrics should be presented in the main paper.

### Minor

- **Loss components are not ablated.** The instance coloring loss has three terms (L_var, L_sep, L_mean) with two hyperparameters (λ_sep, λ_mean). The paper provides no experiment showing whether all three terms are necessary, what happens with only L_var, or how sensitive the method is to the hyperparameter values. For a methods paper proposing a new loss, this is a notable gap.

- **DINO is mischaracterized as "discriminatively pretrained."** Section 4.2 (line 187) describes DINO as providing "discriminative features" and groups it under "discriminative pretraining" (line 219). DINO is actually a self-supervised method trained via self-distillation, not supervised discriminative learning. This imprecision weakens the theoretical framing that contrasts generative vs. discriminative pretraining, since DINO also learns equivariant features to some degree (as shown by its success on correspondences and segmentation).

- **Resolution confound is acknowledged but not controlled.** The paper correctly notes that SAM operates at 1024×1024 while the proposed models use 224×224 (MAE) or 480×640/368×1024 (SD). This is cited to explain poor small-object performance (COCO_exc^S: SD 8.5 vs SAM 56.9), yet the paper does not control for resolution when comparing edge detection (MAE-H at 224×224 vs SAM at 1024×1024). A matched-resolution experiment or explicit characterization of resolution effects would strengthen the comparative claims.

### Trivial

- The Table 1 caption claim of "minimum 70%" performance recovery is technically accurate but tightly borderline (EgoHOS 71%, PIDRay 70%), and the wording "match or recover" overstates the consistency.

## Nice-to-Haves

- A controlled experiment pretraining the same ViT architecture from scratch with MAE vs. a contrastive objective (e.g., MoCo v3) on the same data, then applying the same instance coloring finetuning, would directly test whether the generative objective is causally responsible for the grouping behavior.
- Reporting full ODS/OIS F-measure on BSDS500 in the main paper would align with community standards and strengthen (or qualify) the boundary quality claims.
- An ablation of the three loss components and sensitivity analysis of λ_sep, λ_mean would improve the method section.

## Novel Insights

None beyond the paper's own contributions. The finding that MAE — a model pretrained on 1.2M unlabeled ImageNet images — can be adapted via a narrow finetuning on two synthetic domains to segment unseen object categories is itself the paper's most novel insight. The controlled finetuning-diversity experiments (Table 2) add causal support that goes beyond typical generalization claims in the literature.

## Suggestions

1. Reframe the SAM comparisons: present SAM as a heavily-supervised upper bound and report the fraction of recovered performance (e.g., "SD recovers 70-101% of SAM's mIoU across datasets with <0.1% of its mask supervision") rather than using "outperforms" language.
2. Report full-curve ODS/OIS F-measure on BSDS500 in the main paper alongside the recall<20% slice.
3. Add an ablation study of L_var, L_sep, and L_mean.
4. Correct the description of DINO — it is self-supervised via self-distillation, not "discriminatively pretrained."
5. Consider a matched-resolution experiment or explicitly bound how much of the performance gap on small objects and edges is attributable to resolution differences.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>