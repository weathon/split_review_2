## Summary

This paper establishes theoretical upper bounds on image watermarking capacity under PSNR and linear robustness constraints, then empirically demonstrates that current neural architectures fall far short of these bounds. The key experiment isolates the problem: even with a single gray image under only a PSNR constraint (no augmentations, no perceptual losses), Video Seal cannot encode 1024 bits, while a linear layer succeeds at 2048 bits and a handcrafted construction reaches 456,509 bits. The paper also introduces Chunky Seal, a scaled-up model achieving 4× capacity (1024 bits) with comparable robustness. The central finding — that the architecture itself is the bottleneck, not external complexity — is clean, novel, and significant.

## Strengths

- **Clean isolation of the architectural limitation (Section 3, Figure 5, Table 1):** The central experiment strips away all real-world complexity down to a solid gray image with only MSE loss, and tests whether Video Seal can approach the PSNR-only bound. It fails at 1024 bits while a linear layer succeeds at 2048 bits and a handcrafted encoder hits 456,509 bits. This cleanly attributes the gap to the architecture itself, not to external constraints. The tiling demonstration (32×32 → 32,768 bits) further reinforces this finding.

- **The handcrafted encoder (Equation 2) as a constructive existence proof:** Showing that a simple closed-form construction maps a hypercube of radius *d* to *q^{cwh}* distinct messages, achieving 456,509 bits at 42 dB on a 256×256 image, proves the PSNR-only bound is approachable with the right design.

- **Transparent handling of bound limitations:** The authors explicitly distinguish heuristic bounds (10–12) from the ultra-conservative Bound 13, and acknowledge that heuristic bounds can over-approximate or under-approximate true capacity.

## Weaknesses

### Major
None.

### Minor

- **The "orders of magnitude" framing lacks adequate scope distinction between settings.** The abstract states "theoretical capacities are orders of magnitude larger than what current models achieve" and the Figure 1 caption says "often by orders of magnitude" without scoping. This is well-supported for the PSNR-only setting (~1000× gap). However, the paper's own conservative Bound 13 (Table 2) yields ~0.005–0.01 bpp for aggressive augmentations like Crop&Rescale 75%, compared to current models at ~0.0013 bpp — a gap of roughly 4–10× that barely crosses one order of magnitude. Chunky Seal at 0.0052 bpp matches or exceeds this conservative bound for the most aggressive crops. The heuristic robustness bounds (Bounds 10–12) shown in Figure 1 are acknowledged as not being valid lower bounds, but this caveat is not prominent in the figure caption. The paper would benefit from clearly separating PSNR-only claims (where orders-of-magnitude gaps are well-supported) from robustness-constrained claims (where the evidence is weaker and relies on heuristic bounds).

- **Chunky Seal's LPIPS is 4.5× higher than Video Seal (0.0085 vs 0.0019, Table 3),** which the paper understates as "only slightly higher." While still low in absolute terms, LPIPS is more sensitive to structured artifacts, and this increase is meaningful. Combined with the extreme scaling cost (90× larger embedder, 23× larger extractor for only 4× capacity), Chunky Seal is a weaker demonstration of untapped potential than the framing suggests. The paper acknowledges the impracticality, but the "comparable quality" characterization is partially misleading.

- **The theoretical framework uses PSNR as the sole quality constraint**, but modern watermarking methods optimize for perceptual quality (SSIM, LPIPS). The handcrafted encoder approaches the PSNR bound by adding independent pixel noise within an ℓ₂ ball, which would likely produce visible high-frequency noise despite high PSNR. The paper's experimental strategy (Section 3.1) — testing models in the PSNR-only setup — validly establishes an architectural bottleneck, but does not validate that the PSNR bound itself is the relevant ceiling for practical perceptual-quality-constrained systems. This limits the strength of the claim that "significant opportunities" for improvement exist under real-world perceptual constraints. The VQ-VAE argument in Section 2.6 addresses cover-image distribution, not perceptual constraints on the watermark perturbation itself, so it does not bridge this gap.

### Trivial
None.

## Nice-to-Haves
- Test the handcrafted encoder's perceptual quality on natural images to clarify whether the PSNR-only bound is visually meaningful.
- Train Video Seal with an LPIPS loss in the simplified PSNR-only setup to directly test whether perceptual constraints are binding.
- Include a statistical assessment of the consistent downward trend in Chunky Seal's robustness accuracies vs Video Seal (Table 3).
- Make the caveat about Bounds 10–12 being heuristic more prominent in Figure 1's caption.

## Removed Points
These points were flagged for removal; treat with caution.
- Criticism about the 16×16 image illustrations not generalizing to 256×256: the handcrafted model (Equation 2) directly validates bounds at full resolution. Removed.
- Criticism about the linear model being rank-constrained: it succeeds (100% accuracy at 1024 and 2048 bits), so the constraint does not harm the conclusion. Removed.
- Criticism about Chunky Seal failing the paper's proposed sanity checks (handcrafted baseline): the handcrafted model has no robustness, so comparison with robust Chunky Seal is not meaningful. Removed.
- Criticism about training epochs (50 vs 600): the reviewer acknowledges this strengthens the architectural point. Removed.
- Criticism about the VQ-VAE reasoning gap: a minor gap in a peripheral argument, not central to the paper's main empirical contributions. Removed.
- Criticism about model availability: not valid per review guidelines. Removed.
- Generic "evaluation lacks rigor" sweep concerns without concrete anchors. Removed.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Revise the abstract, Figure 1 caption, and conclusion to clearly scope the "orders of magnitude" claim to the PSNR-only setting, or qualify the robustness-constrained claim with explicit reference to the heuristic nature of the bounds.
- Qualify the "comparable quality" claim for Chunky Seal by noting the LPIPS increase more prominently, rather than "only slightly higher."
- Provide visualizations of the handcrafted encoder's watermarks on natural images.
- Consider adding a simple experiment with perceptual losses (LPIPS) to the PSNR-only training setup to test whether hypothesis B (perceptual constraints) would become binding if the architecture were fixed.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>