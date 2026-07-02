Now I have enough data to calibrate. Let me compile the final review.

## Summary
This paper establishes theoretical upper bounds on image watermarking capacity under PSNR and robustness constraints, showing that theoretical capacities are orders of magnitude larger than what current methods achieve (~2 bpp at 40 dB vs. ~0.001 bpp in practice for PSNR-only). Through progressive controlled experiments — retraining Video Seal on a single gray image, a linear model, tiling, and a handcrafted embedder — the authors systematically eliminate alternative explanations and demonstrate the gap stems from architectural limitations. Chunky Seal, a scaled-up Video Seal, achieves 1024 bits at 45 dB with 99.15% bit accuracy — a 4× improvement over Video Seal's 256 bits.

## Strengths
- **Systematic elimination of alternative explanations through controlled experiments (Section 3.1, Table 1, Figure 5):** Video Seal is retrained on a single gray image with only MSE loss and no augmentations — the simplest possible setup matching the theoretical framework. Video Seal fails at 1024 bits (89.63% bit accuracy at 40 dB), while the theoretical bound at that PSNR is ~600,000 bits (Figure 3). This directly rules out hypotheses A, B, and C (that real-world complexity explains the gap), forming the paper's strongest experimental contribution.

- **Progressive chain of simple baselines approaching theoretical bounds (Section 3.2, Table 1):** A linear embedder achieves 2048 bits at 40 dB, tiling 32×32 Video Seal yields 32,768 bits, and the handcrafted hypercube model achieves 456,509 bits at 42 dB — each progressively closer to the ~600,000-bit bound. This rules out hypothesis D (bounds are unachievable) and provides strong evidence that the bounds are practically reachable.

- **Principled geometric framework for capacity analysis (Sections 2.2–2.5):** By modeling images as integer lattice points and PSNR as an ℓ₂-ball constraint (Eq. 1), the paper develops a family of 13 bounds covering cube-in-ball, ball-in-cube, and partial overlap regimes. The extension to robustness via singular value analysis of linear transformations (Section 2.5) demonstrates the framework's generality beyond prior information-theoretic approaches relying on Gaussian assumptions.

- **Resolution-insensitivity finding (Section 3.1, Table 1):** Video Seal at 256×256px achieves essentially the same capacity as at 32×32px (512 bits at ~41–52 dB), meaning the architecture effectively wastes 64× of available pixels. This is a striking diagnosis of architectural failure.

- **Actionable sanity checks for the community (Section 5):** The paper proposes concrete tests a new watermarking method should pass: linear scaling of capacity with image size, linear decrease with PSNR, outperforming simple baselines, and predictable capacity drops under stronger augmentations. These are grounded in the theoretical framework and practically useful.

- **Quantification of data distribution effect (Section 2.6):** Using VQ-VAE/VQGAN compression to upper-bound perceptually distinct images shows data distribution reduces capacity by only ~0.05 bpp, addressing a natural concern with a concrete estimation.

## Weaknesses

### Fatal
None.

### Major
- **Mismatch between theoretical and empirical evaluation regimes (Section 2.5 vs. Section 4):** The theoretical robustness analysis examines specific individual augmentations — crop at 50%/75%, rotation at 15°/30°/45°, LinJPEG at q=8/10/15 (Figure 4, Table 2) — while Chunky Seal is evaluated under a different mixture of transforms at different severity ranges: rotation ≤10°, crop 77–95%, JPEG Q50–80 (Table 3). This makes it impossible to directly compare Chunky Seal against the paper's own theoretical bounds for any single augmentation. The most dramatic gap findings (orders of magnitude) apply to the PSNR-only setting, while the practically relevant robustness-aware gap is likely much narrower. The paper would be substantially stronger if Chunky Seal were evaluated under the exact augmentation regimes analyzed theoretically.

- **Heuristic robustness bounds with uncertain tightness (Section 2.5):** Bounds 10–12 are explicitly heuristic with acknowledged over- and under-approximation, while Bound 13 is provable but described as "extremely conservative and unrealistic." The most practically relevant bounds — governing capacity under robustness — are of uncertain tightness. The paper states it "believes" Bounds 10–12 are closer to truth, but this relies on intuition rather than formal evidence. Since the practically relevant gap (under robustness) is smaller than the PSNR-only gap, the uncertainty in these bounds weakens the narrative about how much room for improvement exists in realistic settings. However, even the conservative Bound 13 shows meaningful remaining capacity (e.g., 904 bits for Crop&Rescale 75%, 26,757 for LinJPEG q=10 at 256×256px), so the core claim survives.

### Minor
- **Chunky Seal's LPIPS regression understated (Section 4, Table 3):** The paper claims Chunky Seal "maintains nearly identical image quality across all metrics, and only slightly higher LPIPS." However, LPIPS increases 4.5× from 0.0019 to 0.0085. While both values are small in absolute terms (LPIPS ranges 0–1), a 4.5× increase should be explicitly noted and discussed rather than characterized as "slightly higher."

- **No explicit connection between theoretical and empirical metrics (Sections 2–3):** The theoretical bounds assume exact PSNR constraints and perfect bit recovery. The empirical results use soft MSE loss and report bit accuracy. While 100% bit accuracy corresponds to perfect recovery, the paper does not discuss what happens at intermediate bit accuracies (e.g., is Chunky Seal's 99.15% "achieving" capacity?). This is relevant for interpreting empirical results against theoretical bounds.

### Trivial
None.

## Nice-to-Haves
- Evaluate Chunky Seal under the exact augmentation regimes analyzed theoretically (crop at 50%/75%, rotation at 15°/30°/45°, LinJPEG at q=8/10/15) to enable direct comparison.
- Analyze where the handcrafted model's advantage comes from (e.g., continuous residuals wasting capacity in learned models vs. loss landscape difficulty).
- Include error bars or significance tests for Chunky Seal robustness comparisons against Video Seal.
- Multiple codebook sizes or different compression models for the data distribution estimation (currently based on a single VQ-VAE/VQGAN estimation of ~0.05 bpp).

## Removed Points
These points are flagged to be removed, treat them with caution.

- **"Orders of magnitude" claim is only for PSNR-only setting:** While the gap narrows under robustness, the paper is transparent about this throughout. Figure 1 clearly shows both PSNR-only and robustness-aware bounds. The paper explicitly states robustness "significantly reduces the capacity but cannot fully explain the low watermarking capacity of current models." This is a framing nuance, not a weakness.

- **Costa's result differs from blind watermarking setup:** The paper cites Costa correctly for the specific claim that "decoder knowledge of the cover does not affect capacity" (Section 2.6), not for the broader Gaussian channel framework. The use is appropriate.

- **Bounds assume uniform distributions over feasible set:** This is standard for capacity analysis and consistent with how capacity bounds work in information theory.

- **Rate-distortion optimal coding vs. practical capacity:** The paper's bounds count feasible image points, which is the standard capacity definition. The handcrafted model uses a near-optimal codebook by construction (Eq. 2).

## Novel Insights
The paper's most novel insight is the progressive experimental methodology: by systematically stripping away real-world complexity (data distribution, augmentations, perceptual constraints) and bringing models to the simplest theoretical setup, the paper conclusively demonstrates that architectural limitations — not fundamental capacity limits — explain the gap between theoretical and empirical performance. The resolution-insensitivity finding (Video Seal wastes 64× pixels) is particularly striking and provides a concrete diagnostic for the architectural failure. The handcrafted model achieving 456,509 bits at 42 dB — nearly matching the theoretical bound — demonstrates that the bounds are not merely theoretical but practically achievable with the right design, making this one of the clearest demonstrations of architectural suboptimality in the watermarking literature.

## Suggestions
- Evaluate Chunky Seal under the exact augmentation regimes analyzed theoretically (crop at 50%/75%, rotation at 15°/30°/45°, LinJPEG at q=8/10/15) to enable direct comparison with Bounds 10–12 and Bound 13.
- Report and discuss the LPIPS regression explicitly rather than characterizing a 4.5× increase as "slightly higher."
- Add a brief discussion connecting the theoretical perfect-recovery setup with the empirical bit-accuracy metric.

## Calibration Report

**Round 1 anchors retrieved (12 papers across 6 bands):**

| Band | Paper | Avg Score | Comparison |
|------|-------|-----------|------------|
| <1.5 | Scaling In-the-Wild Training (IC-Light) | 0.50 | Completely different topic |
| <1.5 | Balancing Differential Discriminative Knowledge | 1.00 | Unrelated |
| <1.5 | Cross-Lingual Capabilities for Humanoid Robots | 1.00 | Unrelated |
| <1.5 | NEMESIS Jailbreaking LLMs | 1.40 | Unrelated |
| 1.5–3.5 | Limits to Reservoir Learning | 3.33 | Theoretical capacity analysis but different domain |
| 1.5–3.5 | GNN as Noisy Communication Channels | 3.00 | Capacity analysis but different domain |
| 1.5–3.5 | Learned Image Compression | 3.40 | Image compression, related but different |
| 1.5–3.5 | Sparse Watermarking in LLMs | 3.00 | LLM watermarking, less rigorous |
| 3.5–5.5 | Watermark-based Detection and Attribution | 4.50 | Theoretical + empirical watermarking, narrower scope |
| 3.5–5.5 | SuperMark | 3.75 | Practical watermarking method |
| 3.5–5.5 | A Recipe for Watermarking DMs | 5.33 | Empirical recipe, less theoretical novelty |
| 3.5–5.5 | Interpretable Boundary-based Watermark | 4.00 | Watermarking for model protection |
| 5.5–7.5 | An undetectable watermark | 6.50 | Theoretical guarantees + experiments, accepted |
| 5.5–7.5 | Shallow Diffuse | 6.00 | Practical watermarking method, rejected |
| 5.5–7.5 | Hidden in the Noise | 5.83 | Two-stage watermarking, accepted |
| 5.5–7.5 | Robust Watermarking (VINE/W-Bench) | 6.40 | Benchmark + method, accepted |
| 7.5–8.5 | Towards Lightweight Deep Watermarking | 7.60 | Loss analysis + framework, rejected |
| 7.5–8.5 | Progressive Compression with Quantized Diffusion | 8.00 | Compression, different |
| 7.5–8.5 | Scaling Laws for Associative Memories | 7.60 | Different topic |
| 7.5–8.5 | Understanding FixMatch | 8.00 | Different topic |
| >8.5 | (None) | — | — |

**Round 1 bracket:** The paper under review provides both theoretical bounds and controlled experiments — more fundamental than "Recipe" (5.33) or "Detection and Attribution" (4.50), and more rigorous than "Shallow Diffuse" (6.0). It's comparable to "An undetectable watermark" (6.50, accepted) in having theoretical + practical contributions, but the reviewed paper's theoretical contribution is more fundamental (capacity bounds vs. undetectability guarantees). It's comparable to "Towards Lightweight Deep Watermarking" (7.60, rejected) in identifying fundamental issues in the field, but the reviewed paper has a stronger theoretical framework. Initial bracket: **6.5–7.5**.

**Round 2 narrowing:** After reading "An undetectable watermark" (6.50) and "Towards Lightweight" (7.60) in full, I note that: (1) the "undetectable watermark" paper had weaker robustness than existing methods but scored 6.50 (accepted), suggesting novelty in theoretical framing is valued; (2) the "Towards Lightweight" paper at 7.60 (rejected) had very practical contributions but lacked the theoretical depth of the reviewed paper. The reviewed paper's theoretical contribution (bounds on watermarking capacity) is more fundamental than either of these. However, the mismatch between theoretical and empirical evaluation regimes for robustness is a genuine weakness that neither anchor has. Final: **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>