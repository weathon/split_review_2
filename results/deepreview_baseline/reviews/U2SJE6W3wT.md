## Summary
This paper proposes AdcVSR, an improved adversarial diffusion compression method for real-world video super-resolution. The method distills a large 3D diffusion Transformer teacher (DOVE) into a compact 2D Stable Diffusion backbone augmented with lightweight 1D temporal convolutions, achieving 95% parameter reduction and 8× speedup. A key contribution is a dual-head, dual-discriminator adversarial distillation scheme that disentangles the optimization of spatial details and temporal consistency, addressing the fundamental conflict between these two objectives.

## Strengths
- **Novel and well-motivated architecture design**: The insight that a 2D SD backbone with lightweight 1D temporal convolutions can effectively learn from heavy 3D DiT teachers is both intuitive and empirically validated. This "2D + 1D" approach is principled, grounded in the observation that LR videos already provide much spatio-temporal structure, and achieves dramatic efficiency gains (95% parameter reduction, 8× speedup vs. DOVE).
- **Well-designed adversarial distillation scheme**: The dual-head, dual-domain discriminator design that explicitly decouples detail and consistency evaluation is a clever solution to a known fundamental conflict in video generation. The five curated data types with head-specific labels provide a clean and comprehensive training signal that demonstrably balances both objectives (Table 3 shows both CLIPIQA and warp error improve jointly).
- **Strong empirical results**: The method achieves competitive or best performance on temporal consistency (lowest warp error on both synthetic and real-world datasets) while maintaining strong perceptual quality. The efficiency gains are substantial and well-documented across multiple dimensions (parameter count, inference time, step number).

## Weaknesses

### Fatal
None.

### Major
- **Limited novelty relative to AdcSR**: The core compression pipeline (pruning SD2.1 UNet and VAE decoder, adversarial distillation) is directly adopted from AdcSR (Chen et al., 2025a). The main novelties are (1) adding 1D temporal convolutions, (2) dual-head discriminators, and (3) dual-domain supervision. While these are useful extensions, the paper reads more as an engineering adaptation of an existing method to video rather than a fundamentally new approach. The technical contributions are incremental.
- **Comparison fairness concerns**: The paper compares against one-step Real-VSR methods (SeedVR2, DOVE, DLoRAL) that operate at different parameter scales and architectural regimes. However, the teacher DOVE (10.55B params) is itself a much larger model than the one-step competitors. Since AdcVSR directly distills from DOVE, its performance advantage in temporal consistency may partially reflect teacher quality rather than the student architecture or distillation method. A fairer comparison would include a baseline that applies standard ADC (single-head, 2D-only) to DOVE for a direct ablation of the proposed components.

### Minor
- **The 1D temporal convolution design is underexplored**: The paper uses a simple 1D conv with kernel size 3 and ReLU. No ablation studies explore alternative temporal modeling choices (e.g., 3D conv, temporal attention, more complex 1D designs). Given that this is a core architectural contribution, the lack of such analysis weakens the claim that "lightweight 1D temporal convolutions" are optimal.
- **Limited analysis of the detail-consistency conflict**: The paper states this conflict as a known problem (citing Sun et al., 2025) but provides no quantitative analysis of the gradient conflict or how the dual-head design resolves it. The claim that "neither aspect can be disregarded or down-weighted" is intuitive but not formally demonstrated.

### Trivial
- Figure 3 caption has a typo ("AdeVSR" instead of "AdcVSR").
- Tables use inconsistent number of decimal places for some metrics (e.g., some have 2 decimal places, others 4).

## Nice-to-Haves
- An analysis of the gradient norms from the detail vs. consistency heads during training would strengthen the claim about "balanced optimization."
- Ablation on the number of 1D temporal conv layers (currently just one per UNet block) would help understand the trade-off between temporal modeling capacity and efficiency.
- A user study evaluating perceptual quality and temporal consistency would complement the automatic metrics, especially for the real-world datasets where ground truth is unavailable.

## Novel Insights
The key insight—that a 2D image diffusion backbone with simple 1D temporal convolutions can match the video super-resolution performance of heavy 3D DiT models—is genuinely useful and transferable. The paper provides compelling evidence that expensive 3D spatio-temporal attention may be overkill when the LR input already encodes temporal structure, and that adversarial distillation with disentangled objectives (detail vs. consistency) can resolve a fundamental conflict in video generation. This has practical implications for building efficient video restoration systems.

## Suggestions
1. Provide an ablation study comparing 1D temporal convs against other lightweight temporal modeling approaches (e.g., temporal attention with reduced heads, 3D conv with small kernel, simple frame concatenation with 2D conv).
2. Include a baseline that applies standard ADC (single-head, single-domain) to compress DOVE into the same "2D + 1D" architecture, to isolate the effect of the proposed distillation scheme from the architecture design.
3. Add a quantitative analysis (e.g., gradient cosine similarity between detail and consistency heads during training) to demonstrate that the dual-head design resolves gradient conflicts.

## Score and Decision

The paper presents a well-executed engineering contribution with clear practical value: compressing large diffusion models for video super-resolution into efficient, compact models. The dual-head adversarial distillation is a thoughtful solution to a real problem. However, the technical novelty relative to the prior AdcSR work is incremental, and the paper would benefit from stronger ablations to isolate the contributions of its individual components. The empirical results are solid but not transformative—the method does not achieve state-of-the-art on most perceptual metrics, and the comparison fairness is slightly compromised by the teacher leakage concern. Overall, this is a competent paper that makes a useful but bounded contribution to the field.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>