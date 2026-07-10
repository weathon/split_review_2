## Summary

This paper asks whether current deep learning-based image watermarking models have saturated the fundamental capacity limits of images. The authors derive theoretical capacity bounds under PSNR constraints (plus heuristic extensions for robustness), finding that capacities should be orders of magnitude larger than current practice (~0.001 bpp). Controlled experiments strip away real-world complexity to show that Video Seal fails to reach even 1024 bits on a single gray image with only an MSE loss, while linear and handcrafted models succeed at much higher capacities. The authors then train Chunky Seal, a scaled-up Video Seal, achieving 4× higher capacity (1024 bits) while maintaining comparable quality and robustness.

## Strengths

- **The PSNR-only capacity bounds (Section 2.2–2.4) are clean and mathematically principled.** The geometric framing—counting integer lattice points inside the intersection of a cube (image space) and a sphere (PSNR constraint)—is well-conceived. The three regimes (cube-in-ball, ball-in-cube, partial overlap) are handled carefully with volume approximations where exact counting is intractable, and the extension to arbitrary cover images with a rigorous ≤1 bpp penalty (Section 2.4) is sound.

- **The controlled experiments (Section 3) are the paper's strongest contribution.** By stripping away all real-world complexity (single solid gray image, no augmentations, only MSE loss) and comparing Video Seal against a linear model and a handcrafted model, the paper convincingly attributes the capacity gap to architectural limitations rather than data complexity. Table 1 and Figure 5 cleanly show Video Seal cannot reach 1024 bits in this trivial setup while a single linear layer succeeds at 2048 bits and tiling of 32×32 models yields 32,768 bits.

- **The paper is honest about its limitations.** Section 2.5 explicitly states that the robustness bounds (Bounds 10–12) are heuristic and can over-approximate the true capacity, and provides a deliberately conservative lower bound (Bound 13) alongside them. Section 5 reiterates this. This is responsible treatment of a difficult theoretical problem.

## Weaknesses

### Fatal
None.

### Major

- **Framing mismatch between abstract/intro/Figure 1 and the actual status of the robustness bounds.** The abstract states the paper "establishes upper bounds on the message-carrying capacity of images under PSNR and linear robustness constraints" indicating capacities "orders of magnitude larger." The introduction (item i) and Figure 1 present the heuristic robustness bounds (Bounds 10–12) as "theoretical bounds" without caveats. However, Section 2.5 explicitly states these bounds "can over-approximate the true capacity" (line 158) — meaning they are not valid upper bounds. The only formal bound under robustness (Bound 13) gives at most ~3.5× improvement over current models for aggressive crops (904 vs 256 bits at Crop&Rescale 75%). While the PSNR-only bounds (showing ~2500× gap) are rigorous, the paper does not clearly separate this well-supported claim from the heuristic robustness estimates. The reader deserves this distinction upfront.

### Minor

- **The data distribution argument (Section 2.6) is not rigorous.** The claim that all 2^{10240} distinct VQ-VAE reconstructions "could fall in the PSNR ball" of a single image is a heuristic upper bound on the number of potential covers. Real image manifolds are highly structured and local density in pixel space varies enormously; the VQ-VAE codebook counting does not directly address how many *actual natural images* lie within a given PSNR ball. The conclusion is likely correct and the estimate is conservative, but the argument as presented is too thin to fully support it.

- **Chunky Seal's scaling gains lack analysis.** The paper reports which architectural dimensions were scaled (embedding dimension, U-Net channel multipliers, ConvNeXt depth/channels) but does not ablate which specific changes drive the capacity improvement. Understanding whether the gain comes from the larger embedding dimension, deeper decoder, or simply more parameters would be more informative for future architectural design. Additionally, Chunky Seal shows notably higher LPIPS (0.0085 vs 0.0019) than Video Seal, a non-trivial quality cost at the higher capacity that the paper reports but does not analyze.

### Trivial
None.

## Nice-to-Haves

- An ablation study for Chunky Seal isolating which architectural change (embedding dimension, channel multipliers, ConvNeXt depth, full-channel watermarking) contributes most to the capacity gain.
- A deeper diagnosis of why Video Seal specifically fails at 1024 bits (e.g., vanishing gradients, a bottleneck in the U-Net, or optimization difficulty with the message embedding layer) rather than the generic attribution to "architectural limitations."

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Criticism that the handcrafted model demonstration does not carry weight / conflates simplified and realistic settings** — REMOVED because the paper explicitly qualifies it with "at least in the solid gray image case with PSNR constraint and no robustness requirements" (line 287) and uses it only to rule out case D (bounds being unachievable) for the PSNR-only setup, not for robustness. The reviewer misread the paper.

2. **Criticism that Chunky Seal does not demonstrate meaningful narrowing of the gap** — REMOVED because the paper never claims it does; it explicitly states "Chunky Seal still remains far from the theoretical bounds" (line 301) and frames it as a feasibility demonstration. 

3. **Complaints about missing appendix content / reproducibility details / formatting artifacts** — REMOVED per filtering rules (parser artifacts and standard practice, not author errors).

4. **Generic speculation about confounders, metrics measuring proxies, whether confounders are controlled** — REMOVED as not anchored to specific paper content.

5. **Demand for analysis of why Video Seal fails at higher capacity** — Weakened to Nice-to-Have; the paper already provides evidence (linear model succeeds, architecture is the bottleneck) and deeper failure-mode diagnosis is aspirational, not a flaw.

## Novel Insights

None beyond the paper's own contributions. The paper's central insight — that watermarking capacity is far from saturated and the primary bottleneck is architectural rather than fundamental — is well-supported by the PSNR-only bounds and controlled experiments.

## Suggestions

- In the abstract and introduction, explicitly separate the two regimes: (a) PSNR-only bounds (rigorous, showing ~2500× gap) and (b) robustness bounds (heuristic estimates suggesting a large gap, with a conservative formal lower bound of ~10×). Figure 1 should distinguish the heuristic robustness curves from the proven PSNR-only curve.
- Add an ablation study for Chunky Seal that isolates which architectural change contributes most to the capacity gain.
- Strengthen the data distribution argument (Section 2.6) with a more concrete estimate, or explicitly mark it as a heuristic.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Reject</decision>