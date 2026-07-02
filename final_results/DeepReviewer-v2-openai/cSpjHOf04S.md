## Summary
# Final Review Report

## Summary

This paper investigates whether generative models (Stable Diffusion v2 and Masked Autoencoder) can be repurposed for category-agnostic instance segmentation when finetuned on a deliberately narrow set of object types (indoor furnishings and cars). The authors propose an instance coloring loss that treats segmentation as image-to-image translation (RGB to per-instance distinct colors), avoiding task-specific decoder heads. The key empirical finding is that models finetuned with this approach generalize zero-shot to unseen object types and image styles, approaching or exceeding SAM's performance on fine-structure benchmarks (iShape, BSDS500) despite being trained on far less diverse mask supervision (3.7M masks vs SAM's 1.1B). The paper further shows that MAE (pretrained only on ImageNet-1K) also generalizes, and that reducing finetuning category diversity to as few as 5 classes still preserves much of the generalization ability. These results provide compelling evidence that generative pretraining produces representations that transfer well to perceptual grouping tasks with minimal supervision.

However, the manuscript exhibits several important weaknesses: (1) the central causal claim that generalization is due to a "generative prior" is presented as proven when alternative explanations (loss design, synthetic data quality, resolution differences) are not ruled out; (2) the quantitative results are overstated in the abstract and introduction—SAM outperforms the proposed method on 3 of 7 evaluation datasets by considerable margins, but the narrative emphasizes the 4 where the method is competitive or ahead; (3) the small-object failure is attributed to pretraining biases without controlling for the dominant confound of low finetuning resolution; (4) the hypothesized mechanism (equivariant vs invariant representations) is empirically unmeasured. Due to Retrieval-Disabled Mode in this review run, novelty and related-work comparison conclusions are deferred for manual verification.

## Strengths
1. **Compelling research question and setting.** The paper investigates a genuinely interesting question: can models learn instance segmentation from a very narrow category set and still generalize to unseen types? This "category-restricted generalization" setting is well-motivated and differs from the standard zero-shot or open-vocabulary segmentation paradigms. The toddler-at-zoo analogy effectively communicates the motivation.

2. **Clean, elegant methodological design.** The instance coloring loss (L_var + L_sep + L_mean) formulates segmentation as an image-to-image translation problem, avoiding task-specific decoders, mask heads, or feature pyramids. This design choice is principled—it keeps the entire generative model (encoder+decoder) intact, preserving pretrained representations rather than discarding the decoder as is common practice. The loss functions are mathematically well-defined and the training procedure is conceptually simple.

3. **Strong empirical results on fine-structure segmentation.** The method achieves 51.4 mIoU on iShape (vs SAM's 16.8) and 93.4 Edge AP on BSDS500 (vs SAM's 79.0), demonstrating a clear and significant advantage on fine-detail and boundary-quality tasks. These results are not incremental improvements but substantial qualitative leaps, suggesting generative priors are particularly beneficial for pixel-accurate boundary understanding.

4. **Comprehensive ablation on data diversity.** Table 2 systematically varies training data (COCO, ClevrTex, 10-class, 5-class) and shows that generalization persists even with only 5 object types or synthetic shape datasets. This ablation strengthens the paper's core argument that the observed generalization is not simply due to dataset size or diversity.

5. **Inclusion of MAE (ImageNet-1K only) demonstrates the effect is not solely due to internet-scale pretraining.** While the best results use Stable Diffusion (LAION-2B), the fact that MAE-B/MAE-H (pretrained only on ImageNet-1K) significantly outperform DINO-B (also ImageNet-1K) under the same finetuning protocol provides strong evidence that generative pretraining matters beyond data scale.

6. **Transparent compute and data reporting.** The paper clearly states training hardware, hours, dataset sizes, and mask counts, making it possible to assess the resource requirements. The comparison with SAM's compute budget is instructive even though hardware is not directly comparable.

## Weaknesses
### W1. Overly strong causal claims about the generative prior mechanism (Major)

The paper repeatedly states that generalization is due to the "generative prior" or "inherent grouping mechanism" as if this is a directly measured causal explanation rather than a hypothesis. The evidence is consistent with this interpretation but does not rule out alternatives: (1) the instance coloring loss itself may act as a strong regularizer that encourages boundary-detection regardless of the backbone; (2) the synthetic training data (Hypersim + VK2) may have sufficient low-level visual diversity to teach general boundary understanding even from a narrow category set; (3) the finetuning resolution gap with SAM's 1024x1024 may explain small-object failures more than pretraining biases. A controlled experiment that ablates the backbone (same loss, same data, same resolution) while measuring generalization would strengthen the causal claim.

**Impact:** Weakens confidence in the paper's main theoretical conclusion. The empirical results are strong, but the attribution to a specific mechanism remains correlational.

**Required revision:** Add a matched experiment: finetune a non-generative ViT (same architecture as MAE, but without generative pretraining) using the identical loss and data to isolate the effect of generative pretraining. More carefully separate empirical findings from mechanistic interpretations throughout the text.

### W2. Inconsistent quantitative narrative (Major)

The abstract and introduction claim that the method "approaches SAM" and "outperforms it when segmenting fine structures and ambiguous boundaries," but Table 1 tells a more nuanced story. On EgoHOS, SAM achieves 56.4 vs the method's 40.0 (a 29% relative gap). On PIDRay, SAM achieves 44.2 vs 30.9 (30% relative gap). On DRAM, SAM leads 50.2 vs 48.2. The method only clearly outperforms SAM on iShape (51.4 vs 16.8) and is competitive on COCO_exc^L (57.6 vs 57.0). The edge detection results (BSDS500) are impressive but use a non-standard truncated metric (AP at recall < 20%) that may favor high-precision edges at the expense of recall.

**Impact:** Creates a mismatch between the paper's promotional framing and the actual evidence, which may reduce reviewer trust.

**Required revision:** Rewrite the abstract and introduction to present the results more precisely: "Our model approaches SAM on some benchmarks, clearly outperforms it on fine-structure segmentation (iShape) and boundary quality (BSDS500), but underperforms on egocentric (EgoHOS) and X-ray (PIDRay) datasets." Report full BSDS500 F-ODS/F-OIS scores rather than only the truncated metric.

### W3. Small-object limitation confounded with resolution (Major)

The paper attributes small-object failures to pretraining biases (SD emphasizing large objects, MAE preferring central objects) but fails to adequately discuss the confound of finetuning resolution. SD models finetune at 480x640 (Hypersim) and 368x1024 (VK2), while MAE models use 224x224. SAM finetunes at 1024x1024. The resolution gap alone can explain much of the small-object performance difference without invoking pretraining biases. The suggestion that "stronger generative models like FLUX.1" would help is only a partial solution.

**Impact:** Undermines the pretraining-bias explanation and suggests a simpler alternative explanation (resolution) that should be controlled before publication.

**Required revision:** Either (a) add a controlled experiment finetuning SD at 1024x1024 resolution to measure the resolution effect, or (b) explicitly acknowledge the resolution confound and adjust the narrative accordingly, stating that the resolution gap is a primary cause.

### W4. Equivariant-vs-invariant hypothesis is empirically unsupported (Major)

The paper argues that DINO-B (discriminative) fails because it learns invariant representations while generative models learn equivariant ones needed for segmentation. This is a compelling hypothesis but no evidence is provided: no equivariance metric is computed, no correlation with performance is shown, and no ablation isolates this factor. Without empirical support, this remains speculation that could be wrong—the failure could equally be due to DINO's architectural design (lack of decoder, lower-resolution features) or optimization differences.

**Impact:** A central explanatory claim in the paper's narrative is unsupported. Readers are asked to accept a specific mechanistic explanation that has not been tested.

**Required revision:** Either add an equivariance quantification experiment (e.g., measure feature consistency under translation/scaling for each model and correlate with segmentation performance) or downgrade the claim from explanation to hypothesis, explicitly stating it as speculation to be tested in future work.

### W5. Incomplete evaluation protocol (Moderate)

Several evaluation elements are missing or underreported: (1) no variance or significance statistics—all results appear to be single-run with no standard deviations or confidence intervals, making it impossible to assess reliability; (2) the BSDS500 edge evaluation uses a non-standard truncated metric without presenting full precision-recall curves or standard F-measures in the main text (cited to Appendix B which is not available in the extracted text); (3) the "golden standard" iterative prompting protocol for multi-point evaluation is described but multi-point results are not shown in Table 1 (only single-prompt results are reported); (4) no failure-case analysis or qualitative limitations are discussed beyond small objects.

**Impact:** Reduces reproducibility and makes it harder to assess whether observed advantages are statistically reliable.

**Required revision:** Report mean±std over at least 3 seeds for key results. Add standard BSDS500 metrics (F-ODS, F-OIS, full AP) to the main text. Include multi-prompt results. Add a failure-case figure with representative examples where the method clearly fails.

### W6. No controlled comparison with generative vs non-generative backbones at matching capacity (Moderate)

The comparison with DINO-B is informative but DINO-B and MAE-B have different training objectives (self-distillation vs reconstruction) and different architectural details (DINO uses [CLS] token, MAE uses decoder). The comparison does not fully control for architecture or training data scale. A cleaner baseline would be to train MAE's encoder-only (discarding the decoder) with a randomly initialized lightweight decoder, isolating the effect of keeping vs discarding the generative decoder.

**Impact:** The claimed "generative vs discriminative" advantage is confounded with architectural choices beyond the objective function.

**Required revision:** Add an MAE-encoder-only baseline (discard decoder, add lightweight decoder head) finetuned with the same loss and data to measure the importance of keeping the generative decoder.

### W7. Moving average vs timestamp in SD forward pass not fully justified (Minor)

Using t=999 (maximum timestep) in Stable Diffusion without noise addition is based on Garcia et al. (2024) but the rationale is not explained. At t=999, the diffusion model is conditioned on near-pure noise in standard inference, but the paper forwards a clean image. The mismatch between training-time distribution (noisy inputs at high t) and inference-time distribution (clean inputs at high t) could affect feature quality. An analysis of sensitivity to the timestep choice would strengthen the method.

**Impact:** Minor methodological concern. The approach works empirically, but the theoretical justification is incomplete.

**Required revision:** Add a sensitivity analysis of timestep t in the appendix, or explain why feeding clean images at high-t conditioning is theoretically sound.

### W8. Conclusion introduces unsupported claims (Minor)

The conclusion states that generative pretraining "inherently teaches a detailed understanding of its constituent parts" and that "the ability to perceive the visual world will only grow" with model scaling. These claims go beyond what the paper's experiments demonstrate (improved segmentation and edge detection on specific benchmarks) and venture into speculative territory without empirical support.

**Impact:** Minor writing issue that can be corrected with better claim-bounding.

**Required revision:** Rewrite the conclusion to summarize only what has been empirically validated: improved zero-shot generalization from generative pretraining under restricted supervision, with specific performance characteristics on different dataset types. Move speculative claims about "understanding" and "perception" to a future work paragraph.

## Score
**Final Score: 7/10**

**Rationale.** This score reflects the paper's genuine research value—addressing a well-motivated question with a clean method and strong results on fine-structure benchmarks—while accounting for the gap between its emphatic narrative and the actual quantitative evidence. The paper identifies an interesting phenomenon (generative models generalize instance segmentation from narrow category supervision) and provides compelling empirical documentation. However, the score is moderated by several concerns: (1) the central causal claim (that a "generative prior" is responsible for generalization) is presented with more certainty than the evidence supports, as alternative explanations are not adequately ruled out; (2) the quantitative narrative in the abstract and introduction overstates the method's competitiveness with SAM, which leads on most evaluated datasets; (3) a key explanatory hypothesis (equivariant vs invariant representations) is presented without empirical measurement; (4) the small-object analysis confounds resolution with pretraining bias. None of these issues individually invalidate the paper's contributions, but together they suggest that the manuscript would benefit from more restrained claims and additional controlled experiments before reaching its full potential impact. The novelty assessment against related work is deferred due to Retrieval-Disabled Mode in this review run; if the method's generalization properties are indeed unique among existing works, the score could reasonably increase to 8/10 after addressing the above concerns.