## Summary

The paper investigates the theoretical capacity limits of image watermarking under PSNR and linear robustness constraints. It derives upper bounds on capacity and shows that current deep learning-based methods operate orders of magnitude below these limits. Through controlled experiments (gray image, PSNR-only) and a scaled-up model (Chunky Seal, 1024 bits), the paper demonstrates that the gap is not due to fundamental constraints but to architectural limitations, suggesting substantial room for future innovation.

## Strengths

- **Novel theoretical framework:** The paper introduces a geometric approach (counting integer points in the intersection of a high-dimensional cube and a PSNR ball) to derive upper bounds on watermarking capacity, accounting for PSNR constraints and linear robustness transformations. This provides a clearer target for the community.
- **Careful isolation of the performance gap:** By training Video Seal on a single gray image with only a PSNR constraint (removing data distribution, augmentations, and perceptual losses), the authors convincingly show that real-world complexity does not explain the gap between theory and practice.
- **Validation that bounds are achievable:** Simple baselines (linear embedder/extractor, tiling a 32×32 model, and a handcrafted embedding) approach or get much closer to the theoretical bounds, demonstrating that the bounds are not overly optimistic.
- **Chunky Seal as a practical proof-of-concept:** Scaling Video Seal produces a 1024-bit watermark with comparable quality and robustness to the 256-bit Video Seal, confirming that higher capacity is achievable in practice and that current architectures are not saturated.

## Weaknesses

### Fatal

None.

### Major

- **Robustness bounds are heuristic, not formal:** The capacity bounds under linear transformations (Bounds 10–12) are derived heuristically using singular values of the transformation matrix. The paper acknowledges they may over- or under-approximate true capacity, and the conservative Bound 13 is extremely loose. The claim of "orders of magnitude gap" under robustness therefore rests on uncertain theoretical ground.
- **The handcrafted model validates the PSNR-only bound but is not robust:** The handcrafted embedder (Equation 2) operates on a solid gray image and only under a PSNR constraint. It does not generalise to natural images or to common distortions, limiting its relevance to practical watermarking. The paper could more clearly separate the two regimes (no-robustness vs. with robustness).

### Minor

- **PSNR-only focus ignores perceptual constraints:** The theoretical analysis uses only PSNR as the imperceptibility metric, while practical watermarking also considers SSIM, LPIPS, etc. The paper acknowledges this but does not extend the bounds to incorporate other distortion measures.
- **Tiling experiment assumes independent patches:** The tiling strategy (training at 32×32 and tiling to 256×256) effectively boosts capacity but assumes each patch can be decoded independently; this may not be robust to cropping or other transformations that break patch boundaries.
- **Number of bounds is overwhelming:** The paper introduces 13 bounds (1–13) plus additional variants (3,4,5,6,7,8,9, etc.). While the main takeaways are clear, the presentation could be streamlined for readability.

### Trivial

- None beyond the above.

## Nice-to-Haves

- Extend the theoretical analysis to non-linear transformations (e.g., actual JPEG compression) or to perceptual metrics like LPIPS.
- Provide an ablation study isolating which architectural components of Video Seal limit capacity (e.g., U-Net depth, channel multipliers, skip connections).
- Discuss how the insights could directly inform future architecture design (e.g., promoting high-rank or identity-preserving mappings).

## Novel Insights

The paper’s key insight is that the observed plateau in watermarking capacity is not a fundamental limit but a consequence of architectural underperformance. Even in the simplest possible setting (single gray image, no robustness), a state-of-the-art architecture (Video Seal) fails to embed 1024 bits, while a trivial linear model succeeds at 2048 bits and a handcrafted model reaches ~456k bits. This reveals that current learned watermarking methods do not effectively utilize the available degrees of freedom in pixel space, and that simple, non-data-driven strategies can dramatically outperform them. The finding that architectural inductive biases—not data distribution, resolution, or augmentations—are the bottleneck points the community toward a largely unexplored direction for improving watermarking.

## Suggestions

1. Strengthen the theoretical contribution by providing a formal bound on the approximation error of the heuristic robustness bounds (Bounds 10–12), or prove that they are lower/upper bounds under stated conditions.
2. Include a simple experiment that trains a model with a perceptual loss (e.g., LPIPS) in the simplified gray-image setup to see if the gap persists under perceptual constraints.
3. Streamline the presentation of bounds: move less central bounds (e.g., numerical integration variants) to the appendix and keep only the most informative ones in the main text.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>