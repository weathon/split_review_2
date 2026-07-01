## Summary

This paper asks whether current deep-learning image watermarking models are near saturation or have substantial headroom. It develops geometric upper bounds on watermarking capacity under PSNR and linear-robustness constraints, finding that theoretical capacities are much larger than what current models achieve. Controlled diagnostic experiments show that Video Seal's architecture fails to exploit capacity even in a trivial setting (single gray image, no augmentations) where simpler models succeed — pointing to architectural bottlenecks. The paper then demonstrates Chunky Seal, a scaled Video Seal that achieves 4× capacity (1024 vs 256 bits) with comparable robustness and quality as a feasibility proof-of-concept.

## Strengths

- The controlled diagnostic experiments (Section 3.1–3.2) are well-designed and produce an informative finding. Showing that Video Seal fails to embed 1024 bits into a single gray image (where a linear model succeeds at 2048 bits) cleanly isolates an architectural limitation. The resolution-invariance result — similar capacity at 32×32 and 256×256 — is a genuinely useful diagnostic insight that the architecture does not exploit available spatial degrees of freedom. The tiling experiment achieving 32,768 bits further strengthens this diagnosis.

- Chunky Seal (Section 4) serves as a legitimate proof-of-concept: scaling a modern architecture increases capacity 4× while maintaining comparable robustness and quality on natural images across a broad set of transformations. The paper is transparent about the enormous parameter cost (~1.8B, 23–93× Video Seal), which limits practical applicability but does not undermine the feasibility demonstration.

## Weaknesses

### Fatal
None.

### Major

1. **The "orders of magnitude" framing in the abstract and introduction overstates what the paper's bounds support, given caveats the paper itself provides.** The abstract (line 11) presents this as a settled finding, but:
   - The PSNR-only bounds (Bounds 2–4), which generate the largest apparent gaps, count integer lattice points inside an ℓ₂ ball. These are valid upper bounds, but they do not account for the decoder's need to partition this space into distinguishable message regions under blind decoding — achieving them would require distinguishing images differing by single gray-level shifts in single pixels, which no practical robust decoder can do. The paper does not discuss this granularity limitation.
   - The heuristic robustness bounds (Bounds 10–12), which produce the "0.5 bpp" figure (line 156), are explicitly described as "not valid lower bounds" whose "true capacity…could be much lower" (line 158). The paper is candid in Section 2.5 but the abstract and introduction do not communicate this significant uncertainty.
   - The paper's own deliberately conservative Bound 13 shows a more modest gap (10–20× for most augmentations, as low as ~5× for aggressive cropping). This does not contradict "orders of magnitude" against current models, but it narrows the gap considerably.
   
   The paper has a real tension: transparent about bound limitations in Section 2.5, but presenting the headline narrative without caveats.

2. **The claim "even under the very conservative Bound 13 we still would expect capacities of at least 0.01 bpp" (line 176) is inconsistent with the paper's own Table 2.** The most aggressive transformation (Crop&Rescale 75%) shows a conservative capacity of 904 bits for a 256×256 image — only 0.005 bpp, half the stated lower bound. Most entries exceed 0.01 bpp, but the blanket claim is imprecise.

3. **Chunky Seal's comparison is framed as "all while preserving image quality and robustness" (Abstract, line 11) but shows meaningful trade-offs.** From Table 3: LPIPS is 4.5× worse (0.0085 vs 0.0019), the embedder is 93× larger, and the extractor 23× larger. Bit accuracy is slightly lower on most individual transformations and overall (99.15% vs 99.31%). The paper partially acknowledges this (lines 293, 305), but the abstract's framing is optimistic — it is more accurately described as trading some quality and substantial parameter efficiency for capacity.

### Minor

4. **Figure 1 plots the PSNR-only bound, heuristic robustness bounds, and empirical results on the same axes without distinguishing rigorous bounds from heuristic estimates.** The caption (line 17) says "theoretical bounds…under a PSNR constraint alone (thick line) and in combination with robustness requirements (thin lines)" without signaling that the thin lines are heuristic. Given that Section 2.5 acknowledges these "could be much lower" (line 158), readers could over-interpret the certainty of the robustness bounds.

5. **The controlled experiments (Section 3) demonstrate architectural limitations of Video Seal specifically, but the paper extrapolates to broad claims about all models.** The conclusion "Our models are likely significantly underperforming" (line 287) follows from experiments on one architecture in a memorization task (single gray image, no robustness). While the hypothesis-testing logic is sound for this architecture, the scope of the resulting claim exceeds the scope of the evidence.

### Trivial
- The "at least 0.01 bpp" imprecision (Weakness 2) should be corrected to match the paper's own data.

## Nice-to-Haves

- Test the linear embedder/decoder on natural images with blind decoding under a PSNR constraint. This would directly test whether the "architecture is the bottleneck" diagnosis holds outside the gray-image memorization setting.
- Provide an ablation isolating which architectural feature limits capacity (receptive field? decoder expressiveness? optimization difficulty?). The paper attributes the gap to "architectural limitations" broadly without isolating the mechanism.
- Visually distinguish bound families in Figure 1 (e.g., dashed for heuristic, solid for rigorous).

## Removed Points

These points were raised by the harsh reviewer but are not included as weaknesses in the final review:

- **"The paper's own conservative bounds contradict the 'orders of magnitude' narrative" (reviewer Issue 2):** This conflates Chunky Seal (the paper's own feasibility demonstration) with "current models," misreading the paper's claim. The "orders of magnitude" claim is about current models (Video Seal at 256 bits, others at ~100 bits = ≤0.0013 bpp), not about Chunky Seal. The gap between current models and even the most aggressive conservative bound (0.005 bpp) is ~4–5×, and most other conservative bounds show a 10–20× gap. The criticism focuses on only one data point (crop 75%) while ignoring the broader bound landscape.

- **"The handcrafted model is not a watermarking method" / "the linear model only works on known cover":** The paper explicitly frames these as diagnostic experiments in a simplified setting (Section 3.2) to test whether the PSNR-only bounds are achievable in principle. The paper does not claim these are practical watermarking schemes. The criticism demands the paper solve a different problem than the one it set out to diagnose.

- **"Paper never evaluates its linear embedder/decoder on natural images":** The linear model experiment is scoped as a diagnostic test; evaluating on natural images with blind decoding is a different experiment for a different question. This is a nice-to-have, not a missing requirement.

- **Various presentation/style nitpicks and formatting criticisms** traceable to PDF parsing artifacts, not author errors.

## Novel Insights

The controlled tiling experiment (Section 3.2) provides a concrete demonstration that Video Seal's architecture does not exploit available spatial degrees of freedom — identical capacity at 32×32 and 256×256 resolution. This diagnostic methodology (isolating one dimension of the capacity-quality-robustness trade-off to attribute the gap) is a useful template for the watermarking community. Beyond this, the geometric bounding framework is mathematically sound, though its practical informativeness is limited by the gap between counting lattice points and guaranteeing decodable message partitions under blind decoding with robustness.

## Suggestions

- Revise the abstract and introduction to accurately reflect the uncertainty in the robustness bounds. Distinguish between the rigorous PSNR-only upper bounds (which are provably loose because they do not model decodability) and the heuristic robustness bounds (which the paper itself flags as potentially unreliable).
- Correct the "at least 0.01 bpp" claim to match the actual conservative bound data in Table 2.
- Add a visual distinction in Figure 1 between rigorous bounds, heuristic bounds, and conservative bounds.
- Quality the "preserving quality and robustness" claim about Chunky Seal to acknowledge the LPIPS and parameter-efficiency trade-offs.
- Discuss the decoding granularity problem explicitly — i.e., that achieving the PSNR-only bound would require distinguishing images at the single-pixel level, which is incompatible with robustness requirements.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>