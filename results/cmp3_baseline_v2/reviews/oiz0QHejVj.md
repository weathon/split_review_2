## Summary
This paper proposes CLIP-Map, a mapping-based compression framework for CLIP models that replaces traditional select-based pruning with learnable transformation matrices. The method uses Kronecker factorization to map large weight matrices to smaller ones (width compression) and linear combinations of layers for depth compression, combined with a diagonal inheritance initialization strategy to stabilize training. Experiments on zero-shot retrieval and classification benchmarks show that CLIP-Map outperforms select-based methods like TinyCLIP, especially under high compression ratios.

## Strengths
- **Novel approach to CLIP compression**: The paper introduces a mapping-based paradigm that avoids hard parameter removal, which is a conceptually clean departure from standard pruning. This is a genuinely different perspective on model compression that could inspire future work.
- **Strong empirical results at high compression ratios**: At 1.0% and 10.0% compression ratios, CLIP-Map substantially outperforms TinyCLIP across nearly all retrieval and classification metrics (e.g., +5.3 TR@1 on MSCOCO at 1.0% ratio, +4.6 TR@1 at 10.0% ratio). The gains are particularly pronounced under extreme compression, which is the most challenging regime.
- **Well-motivated technical design**: The Kronecker factorization for efficient mapping and the diagonal inheritance initialization are both clearly motivated by the specific challenges of mapping-based compression (parameter explosion, distribution shifting). The analysis of variance scaling in Eq. 6-8 provides a concrete justification for the initialization scheme.
- **Comprehensive evaluation**: The paper evaluates on multiple benchmarks (MSCOCO, Flickr30K, ImageNet-1K, 21 downstream classification datasets) and compares against several baselines (TinyCLIP, MoPE-CLIP, CLIP-KD, MobileCLIP). The ablation studies on initialization methods and mapping duration are informative.

## Weaknesses
### Fatal
None.

### Major
- **Insufficient comparison with select-based methods at the same training budget**: The paper compares CLIP-Map against TinyCLIP with progressive compression (†TinyCLIP, 2×25ep or 3×25ep), but CLIP-Map uses 5 mapping epochs + 20 retraining epochs = 25 total epochs. The progressive TinyCLIP uses 50 or 75 epochs. This is an unfair comparison—CLIP-Map uses fewer total epochs yet claims superiority. The paper should compare against TinyCLIP with the same total training budget (25 epochs) without progressive compression, or acknowledge that the advantage partly comes from the mapping stage being more sample-efficient. The non-progressive TinyCLIP results (without †) use 25 epochs, and CLIP-Map still outperforms them, which is a fairer comparison, but the paper's narrative emphasizes the progressive results.

- **Missing details on the mapping stage optimization**: The paper does not specify what loss function is used during the mapping stage (Stage 1). Is it the standard CLIP contrastive loss? Is it a reconstruction loss between the original and mapped model outputs? This is a critical omission—the mapping stage is the core novelty, yet the objective being optimized is never stated. Without this, the method is incompletely specified.

- **No analysis of the computational overhead of the mapping stage**: The mapping stage introduces additional parameters (F_in, F_out) and requires training them. The paper does not report the FLOPs, memory, or time overhead of the mapping stage itself, nor does it compare the total training cost (mapping + retraining) against the baseline's training cost. The claim of "fewer training epochs" is misleading if the mapping stage is computationally expensive per epoch.

- **Limited architectural exploration**: The method is only evaluated on ViT-B/16 as the teacher, with compressed variants of ViT. The paper claims generalization to ResNet vision encoders but only shows a single result (ResNet-50, w/o retraining, 25.5 TR@1 on MSCOCO) without any comparison baseline. The claim of generalization is not well supported.

### Minor
- **The paper overclaims on "unified and simplified pipeline"**: The mapping stage and retraining stage are still two separate stages, similar to the pruning-retraining pipeline. The claim of "end-to-end optimization" is not accurate since the mapping parameters are trained first, then the student is retrained separately.
- **The comparison with MobileCLIP in Table 3 is not meaningful**: MobileCLIP uses a different training dataset (DataCompDR-12M) with higher quality, so the performance difference cannot be attributed to the compression method. The paper acknowledges this but still includes the comparison, which is potentially misleading.
- **The paper does not report standard deviations or statistical significance**: Given the stochastic nature of training, it would be helpful to know whether the reported improvements are statistically significant.

### Trivial
- The paper has some redundancy in figure captions (Figure 1, 2, 3 captions are repeated).
- The abstract mentions "text-to-image generation" as an application but the paper only evaluates on retrieval and classification.

## Nice-to-Haves
- An analysis of what the learned mapping matrices look like after training (e.g., visualization of F_in and F_out) would provide insight into what the mapping is actually doing.
- A comparison against a simple baseline of training a small model from scratch (without any initialization from the large model) would help isolate the benefit of the mapping-based initialization.
- The paper could discuss the relationship between the mapping approach and low-rank factorization or matrix product operator compression methods.

## Novel Insights
The key insight is that model compression can be reframed as a learnable mapping problem rather than a selection problem. The paper shows that by using Kronecker-factorized transformations with a carefully designed diagonal initialization, one can preserve more information from the original weights than pruning-based approaches. This is a genuinely different perspective that could influence future work on model compression, particularly for multimodal models where cross-modal alignment is sensitive to information loss. The finding that the mapping stage benefits from a moderate duration (5 epochs) before degrading is also practically useful.

## Suggestions
1. **Specify the loss function used in the mapping stage (Stage 1)**. This is essential for reproducibility. If it is the standard CLIP contrastive loss, state that explicitly. If it is a reconstruction loss between original and mapped model outputs, describe it.
2. **Add a fair comparison against TinyCLIP with the same total training budget (25 epochs) without progressive compression**. The non-progressive TinyCLIP results in Table 1 already serve this purpose, but the paper should explicitly highlight this comparison and discuss the results.
3. **Report the computational cost of the mapping stage** (FLOPs, GPU-hours, memory) and compare the total training cost (mapping + retraining) against the baseline's training cost.
4. **Add standard deviations or confidence intervals** for the main results, or at least acknowledge the lack of statistical significance testing.
5. **Remove or clearly separate the MobileCLIP comparison** from the main comparison table, as the training data is different and the comparison is not informative.

## Score and Decision
The paper presents a novel and well-motivated approach to CLIP compression with strong empirical results, particularly at high compression ratios. The technical design (Kronecker factorization + diagonal inheritance initialization) is sound and clearly explained. However, the paper has several significant issues: the missing specification of the mapping stage loss function, unfair comparisons against baselines with larger training budgets, and lack of analysis of the mapping stage's computational overhead. These issues are major but not fatal—they can be addressed with clarifications and additional experiments. The core idea is valuable and the results are promising.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>