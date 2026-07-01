## Summary

This paper introduces ARSS, a decoder-only autoregressive transformer framework for novel view synthesis from a single image. The method uses a video tokenizer to discretize multi-view image sequences, a camera autoencoder to encode Plücker ray maps into 3D positional tokens, and a spatial-permutation training strategy that preserves temporal causality while allowing bi-directional spatial context. Experiments on RealEstate10K, ACID, and zero-shot on DL3DV show that ARSS achieves results competitive with diffusion-based NVS methods while offering the advantages of causal sequential generation.

## Strengths

- **Novel application of causal AR models to NVS**: The paper is the first to apply a decoder-only GPT-style autoregressive transformer to novel view synthesis with explicit camera control, opening a new direction for sequential visual generation with causal structure.
- **Comprehensive evaluation**: The method is evaluated on multiple datasets (RealEstate10K, ACID, DL3DV) against a diverse set of baselines, including both diffusion-based and feed-forward methods, with pixel-aligned, perceptual, and distributional metrics.
- **Effective error accumulation analysis**: The per-frame metric plots (Figure 6) convincingly demonstrate that ARSS maintains higher quality and slower degradation along long camera trajectories compared to all baselines, which is a key advantage for sequential generation.
- **Ablation studies on token ordering and tokenizer**: The paper provides clear ablation experiments showing that the proposed hybrid spatial-only permutation with temporal preservation outperforms both raster and full spatiotemporal permutation, and that the video tokenizer substantially improves temporal consistency over VQ image tokenizers.

## Weaknesses

### Fatal
None.

### Major
- **Overstated claims vs. actual results**: The paper claims to "outperform current state-of-the-art methods" in the introduction and discussion, but the quantitative results show mixed performance. For example, on RealEstate10K, SEVA achieves higher SSIM (0.670 vs. 0.624) and similar FID, and on ACID, SEVA also has higher SSIM (0.664 vs. 0.623). The paper acknowledges this only briefly and attributes it to "large-scale, high-resolution training data and heavy computational resources" without evidence or controlled comparison. This weakens the central claim.
- **Missing critical ablations**: There is no ablation on the camera autoencoder itself (e.g., replacing it with a simpler conditioning method like concatenating camera parameters directly, or removing camera tokens entirely). Without this, it is unclear how much the proposed 3D positional tokens contribute relative to the video tokenizer and spatial permutation. Similarly, there is no comparison against training an image-tokenizer-based AR model with the same camera conditioning to isolate the benefit of the video tokenizer.
- **Low evaluation resolution and limited practical scope**: All experiments are conducted at 256×256 resolution, which is notably lower than many diffusion-based NVS methods (e.g., SEVA at 512×512). This limits the practical applicability and makes comparisons less direct. The paper does not discuss scalability to higher resolutions.
- **Unclear training and inference details for comparisons**: The paper does not specify whether all baselines are evaluated under identical settings (e.g., same number of input views, same trajectory length). Given that ARSS uses single-image input and generates 16 target views, but some baselines (e.g., SEVA, ViewCrafter) may have been designed for different settings, the fairness of the comparison is not fully transparent.

### Minor
- The ablation study (Table 2) reports a PSNR of 19.22 for "ours" while the main results (Table 1) report 19.02. This discrepancy is not explained and may indicate different experimental setups or training budgets between the ablation and main results.
- The paper claims that SEVA "benefits from large-scale, high-resolution training data and heavy computational resources" but provides no quantitative comparison of training data size, resolution, or compute budget. This weakens the argument that ARSS is more efficient.
- Some sentences are verbose or unclear (e.g., "the temporal order is still maintained to make sure that the tokens from later frames are always generated based on tokens of former frames" could be stated more concisely).

### Trivial
- The reference "Better et al., 2023" appears to be a formatting error (should be Betker et al.).

## Nice-to-Haves
- An ablation comparing the camera autoencoder against a simpler conditioning method (e.g., directly embedding camera parameters) would strengthen the paper's claims.
- Reporting inference speed and model parameter counts would help readers understand practical trade-offs between ARSS and diffusion-based methods.
- Visualizing failure cases (e.g., large viewpoint changes, occluded regions) would provide a more complete picture of the method's limitations.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
- Conduct an ablation that removes the camera autoencoder and instead conditions the AR model on camera parameters via a simple embedding, to isolate the benefit of the proposed 3D positional tokens.
- Include a controlled comparison where SEVA or another diffusion baseline is evaluated at 256×256 resolution under the same trajectory length, to enable a fairer assessment.
- Clarify the discrepancy between the ablation and main result PSNR values, or report all experiments under the same setting.
- Tone down the "outperform SOTA" claim, as the results are more accurately described as competitive, with some metrics better and some worse than leading diffusion methods.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>