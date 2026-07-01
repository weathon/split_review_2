Now I have sufficient calibration. Let me produce the final review.

## Summary

This paper develops a geometric framework for bounding the message-carrying capacity of images under PSNR and linear robustness constraints, using lattice-point counting in high-dimensional intersections. It derives theoretical bounds suggesting capacities orders of magnitude larger than current watermarking models achieve, and validates through controlled experiments that even in a maximally simplified setting (single gray image, PSNR-only constraint), Video Seal fails to approach these bounds while simple linear or handcrafted models succeed. The paper also presents Chunky Seal, a scaled-up model achieving 4× higher capacity (1024 bits) with comparable quality and robustness, demonstrating that architectural limitations—not fundamental capacity ceilings—constrain current methods.

## Strengths

- **Novel geometric framework for watermarking capacity.** Modeling capacity as counting integer lattice points in the intersection of a PSNR ball and the image hypercube (Section 2.2–2.4) is a genuinely creative approach that yields concrete numeric bounds for realistic image sizes. This moves beyond prior information-theoretic approaches that relied on Gaussian noise assumptions (Costa 1983, Moulin & O'Sullivan 2003) and provides a practical upper bound the community can build on.

- **Well-designed controlled experiments isolating architectural limitations.** The multi-stage ladder of evidence (Section 3) systematically rules out competing hypotheses: Video Seal fails at 1024 bits on a single gray image with only MSE loss (Table 1), a linear layer succeeds at 2048 bits (Section 3.2), tiling achieves 32,768 bits, and a handcrafted construction achieves 456,509 bits at 42 dB (Eq. 2). This cleanly demonstrates that the gap is not due to data distribution, resolution, or the bounds being unachievable—it is architectural.

- **Constructive proof that PSNR-only bounds are not loose.** The handcrafted embedder (Eq. 2) is a mathematical construction that saturates near-bound capacity, ruling out hypothesis D (bounds are unachievable) convincingly for the PSNR-only case. Many theoretical capacity papers lack any such constructive demonstration.

- **Conservative lower bound (Bound 13) for robustness.** Despite the heuristic nature of Bounds 10–12, Bound 13 provides an extremely conservative lower bound showing even 75% crop leaves at least 904 bits at 42 dB for 256×256px images (Table 2), still above the ~256-bit capacity of current methods.

- **Honest limitations section.** The paper explicitly acknowledges that its bounds are PSNR-only, that the robustness bounds are heuristic rather than formal, that numerical integration becomes impractical at high resolutions, and that Chunky Seal is too large for deployment (Section 5).

## Weaknesses

### Fatal

None.

### Major

- **Theoretical bounds use PSNR as the sole quality constraint, limiting the practical interpretation of the "orders of magnitude" headline claim.** The geometric bounds (Section 2.3) count all integer lattice points inside a PSNR ball, but many of these points differ from the cover by high-frequency pixel perturbations that may be perceptible despite high PSNR. The handcrafted model achieving 456,509 bits at 42 dB independently modulates each pixel by up to ±2 (Eq. 2), producing a noise pattern whose imperceptibility under perceptual metrics (LPIPS, SSIM) is not demonstrated. The paper acknowledges this as hypothesis B (Section 3) but dismisses it by noting the controlled experiments strip out perceptual losses—this addresses whether models *can be trained* under PSNR-only, but does not address whether the *bounds themselves* would shift downward substantially under a perceptual metric. The "orders of magnitude" gap shown in Figure 1 is established only under PSNR; its magnitude under realistic perceptual constraints is unknown. This does not invalidate the geometric framework (which could be adapted), but it weakens the central claim that current methods are as far from fundamental perceptual limits as Figure 1 suggests.

- **Heuristic robustness bounds (Bounds 10–12) are unvalidated and diverge from the conservative bound (Bound 13) by orders of magnitude.** The heuristic bounds predict ~100,000 bits under 75% crop at 256×256px (Section 2.5), while Bound 13 gives only 904 bits (Table 2)—over two orders of magnitude less. The paper asserts that Bounds 10–12 "are much closer to the true capacity" but provides no empirical validation against any ground-truth capacity measurement. This wide gap makes the robustness analysis inconclusive for quantitative claims derived from the heuristic bounds (Figure 4). However, the paper's broader argument that "robustness cannot fully explain the gap" is still supported by the conservative Bound 13 (904 bits > current ~256-bit capacities), so this weakness does not invalidate the main conclusion but does weaken the precision of the robustness analysis.

### Minor

- **Only Video Seal is tested in the controlled experiments.** The conclusion that "our models have severe structural limitations" (Section 5) is drawn from one architecture. While the complementary experiments (linear model, tiling, handcrafted) collectively show that PSNR-only capacity is achievable with non-deep-learning approaches, the generalization to "current deep learning architectures" would be stronger with at least one additional architecture (e.g., HiDDeN) tested in the same simplified setup.

- **Chunky Seal's parameter scaling shows diminishing returns.** Scaling the embedder by 90× and extractor by 23× yields only 4× capacity increase (Table 3), with slightly worse LPIPS (0.0085 vs. 0.0019) and marginally lower per-transformation robustness on several augmentations. The paper frames this as "simple scaling" (Section 4) but the cost-benefit ratio is steep.

- **The linear model performs far below the handcrafted construction (2048 bits at 40.4 dB vs. 456,509 bits at 42 dB).** The paper does not discuss why gradient-based learning fails to discover the near-optimal strategy—whether this is a local minima issue, a gradient signal issue, or an inductive bias problem—which limits the insight from the linear model experiment.

- **Tiled embeddings are independent per-tile, not a unified message.** The paper reports 32,768 bits by tiling 512-bit models at 32×32px (Section 3.2, Table 1) but this produces 64 independent 512-bit messages. Under global transformations (rotation, rescaling), each tile is transformed differently, making this an optimistic capacity estimate rather than a directly usable watermark under robustness constraints.

- **No analysis of what Video Seal's encoder/decoder actually learns.** The paper attributes failure to "structural limitations" but provides no analysis of embedding patterns (e.g., effective rank, spatial localization of the learned residual) that could inform architectural improvements.

### Trivial

None.

## Nice-to-Haves

- Test Chunky Seal on the controlled gray-image PSNR-only setup from Section 3 to directly compare its architectural capacity exploitation against Video Seal.
- Provide qualitative examples and LPIPS/SSIM measurements for the handcrafted model's outputs at stated PSNR values to demonstrate imperceptibility under perceptual metrics.
- Validate heuristic robustness bounds against a simple trainable system (e.g., linear model) under at least one transformation to increase confidence in Bounds 10–12.
- Discuss why the linear model fails to reach the handcrafted model's capacity via gradient descent.

## Removed Points

These points from the input review were removed or merged with justification:

- **"456,509-bit handcrafted model operates at an unstated PSNR"** — REMOVED as factually incorrect. Table 1 clearly states 42.00 dB for this entry. The reviewer later acknowledges this, but the initial framing is inaccurate.
- **"Apples-to-oranges comparison between handcrafted model and current models"** — REMOVED. The handcrafted model is explicitly for the PSNR-only case (Section 2.3), and the paper separates this from the robustness analysis (Section 2.5). The comparison in Figure 6 is apples-to-apples within the PSNR-only setup.
- **"Could be strong with revisions" framing** — REMOVED. The overall assessment should reflect the paper's actual contribution level without hedging.
- **Missing related works** — REMOVED per constraint (no external sources to verify existence/completeness).
- **Missing appendix content** — REMOVED per constraint (appendix stripped by parser, not absent from original submission).
- **Formatting and typo nitpicks** — REMOVED per constraints (parser artifacts, not author errors).

## Novel Insights

Beyond the paper's own contributions, the most striking pattern from combining the review and the paper is that the controlled experiments establish a crisp diagnostic problem: if a linear layer can learn 2048 bits from scratch in 50 epochs, while Video Seal's full U-Net+ConvNeXt architecture cannot learn 1024 bits in 600 epochs, then the architecture is not merely underparameterized—it is actively *anti-inductive* for the PSNR-only watermarking task. The handcrafted construction (Eq. 2) is essentially a lookup table mapping messages to independent per-pixel perturbations, which a linear layer should converge to given the right optimization landscape. The fact that Video Seal cannot learn this suggests its inductive biases (convolutions, downsampling, skip connections) are misaligned with the task in a way that goes beyond simple capacity constraints. This creates an interesting research question: what architectural priors are needed for watermarking, and can we design architectures that are provably at least as good as a linear layer on the PSNR-only task?

## Suggestions

1. Address the PSNR-perceptual gap by either (a) providing LPIPS/SSIM measurements for the handcrafted model's outputs at stated PSNR values, or (b) showing qualitative examples demonstrating imperceptibility.
2. Validate the heuristic robustness bounds against a simple trainable system (e.g., linear model) under at least one transformation to increase confidence.
3. Test at least one additional architecture (e.g., HiDDeN) in the simplified gray-image setup to support generalization beyond Video Seal.
4. Discuss why the linear model fails to reach the handcrafted model's capacity via gradient descent, as this may guide understanding of optimization challenges.
5. Report Chunky Seal's performance on the gray-image PSNR-only task to directly compare architectures in the simplified setting.

## Score and Decision

**Calibration anchor papers (retrieved across all rounds):**

| Path | Avg Human Score | Round | Comparison |
|------|---------------|-------|------------|
| jlhBFm7T2J (Undetectable watermark) | 6.50 | R1, R2 | Stronger theoretical guarantee (undetectability) and comparable empirical work. Current paper has a different but comparably novel theoretical contribution. |
| ll2nz6qwRG (Hidden in the Noise) | 5.83 | R1, R2 | New watermarking method with less novel theory. Current paper is stronger theoretically. |
| 1IwoEFyErz (Shallow Diffuse) | 6.00 | R1 | Similar theoretical contribution level but had presentation/ablation issues. Current paper is better presented. |
| 16O8GCm8Wn (Robust Watermarking W-Bench) | 6.40 | R1 | Benchmark+method paper with strong experiments. Current paper has stronger theoretical component. |
| LdIlnsePNt (SEAL watermarking theory) | 6.00 | R2 | Theory+method paper; rejected due to proof rigor issues. Current paper has no identified proof issues. |
| O08nfMzc93 (Watermark detection/attribution) | 4.50 | R1 | Theoretical analysis with limited experiments. Current paper is significantly stronger. |
| T0ebbDO60R (SuperMark) | 3.75 | R1 | Training-free watermarking method. Current paper has a different, more fundamental contribution. |
| j7b4mm7Ec9 (Lightweight Watermarking) | 7.60 | R1 | Very clean method paper with minimal weaknesses. Current paper has more notable limitations. |

**Round 1 bracket:** 5.5 – 7.0

**Narrowing:** The current paper has a genuinely novel theoretical framework and well-designed controlled experiments, placing it well above papers in the 3–5 range. It is comparable to accepted papers at 5.83–6.50 in quality, with a stronger theoretical component than most. However, the PSNR-only bound limitation and unvalidated heuristic robustness bounds are substantive concerns that prevent it from reaching the 7+ range of papers with cleaner, more comprehensively validated contributions.

**Final score: 6.5 — Accept**

This paper contributes a novel geometric framework for watermarking capacity that is broadly useful, supported by well-designed controlled experiments. The major weaknesses (PSNR-only bounds and unvalidated heuristic robustness bounds) are real limitations on the headline claims but do not invalidate the core contribution, which is adaptable to other quality metrics and provides a framework the community can build on. The honest limitations section and the constructive handcrafted model strengthen the paper's credibility.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>