Now let me write the final review.

## Summary

The paper studies how much information can theoretically be hidden in an image under imperceptibility (PSNR) and robustness constraints, establishing upper bounds via geometric counting of lattice points. It then compares these bounds to the capacities achieved by current deep watermarking models and finds a large gap. Through carefully controlled experiments that progressively simplify the setup (single gray image, no augmentations, only MSE loss), the paper shows that Video Seal cannot learn to embed 1024 bits while simple linear or handcrafted models easily achieve 2048–456,509 bits — directly demonstrating that the architecture, not fundamental constraints, is the bottleneck. A proof-of-concept scaled model (Chunky Seal) further shows 4× capacity gains are possible while maintaining comparable robustness and quality, though at large model-size cost.

## Strengths

1. **Controlled isolation of architecture as the bottleneck (Section 3, Table 1, Figure 5):** The paper systematically tests five hypotheses for the theory-practice gap by progressively simplifying the watermarking setup. In the simplest case — a single gray image with only an MSE loss — Video Seal fails to embed 1024 bits while a linear embedder/extractor succeeds at 2048 bits and a handcrafted model achieves 456,509 bits at 42 dB. This chain of controlled experiments cleanly eliminates robustness, perceptual constraints, and data distribution as explanations, leaving only architectural limitations.

2. **Conservative lower bounds under robustness (Section 2.5, Table 2, Bound 13):** Bound 13 provides a provably conservative (i.e., unrealistically low) lower bound on capacity under linear robustness transformations. Even under aggressive Crop&Rescale 75% at 42 dB, it guarantees at least 904 bits for 256×256px images; under LinJPEG q=10 it guarantees 26,757 bits. Since current methods achieve ≈100–200 bits, this proves that robustness constraints alone cannot explain the gap, even with the most pessimistic assumptions.

3. **Geometric counting framework (Sections 2.2–2.4, Figure 3):** The paper models images as integer lattice points in a high-dimensional cube and uses exact lattice-point counting (Mitchell's algorithm) and volume approximations to derive capacity under PSNR constraints across three regimes (cube-in-ball, ball-in-cube, non-trivial intersection). This is more general than prior information-theoretic approaches that relied on Gaussian-noise or small-perturbation assumptions.

4. **Tiling demonstration (Section 3.2, Table 1):** Because Video Seal achieves nearly identical capacity at 32×32px and 256×256px, the authors tile the 32×32px model to obtain 32,768 bits on a 256×256px image. This elegantly proves the architecture fails to use the available pixel budget while simultaneously showing that capacities far beyond current practice are achievable without any new training.

5. **Self-aware limitations discussion (Section 5):** The paper explicitly acknowledges that the heuristic robustness bounds (Bounds 10–12) could over- or under-approximate true capacity, that Bound 13 is "extremely conservative and unrealistic," that Chunky Seal is not a practical path forward, and that sharper theoretical advances are needed. This transparency is commendable.

## Weaknesses

### Major

1. **"Orders of magnitude" claim is not uniformly supported across all settings.** The paper's headline claim is well-supported for the PSNR-only (no robustness) case, where the gap is ≈2500×. However, for the with-robustness case that matters in practice, the only rigorous bound (Bound 13, Table 2) gives a gap ranging from ≈3.5× (Crop&Rescale 75%) to ≈100× (LinJPEG q=10) — not uniformly "orders of magnitude." The heuristic bounds (Bounds 10–12, Figure 4) that visually anchor the "orders of magnitude" framing are acknowledged by the paper itself as potentially over-approximating true capacity (Section 2.5: "the true capacity under linear transformation could be much lower than these bounds predict"). Yet the abstract and introduction use the phrase without qualification: "theoretical capacities are orders of magnitude larger than what current models achieve" (Abstract, line 11). The paper would be stronger if it clearly distinguished between settings rather than bundling them under a single umbrella.

2. **The framework does not formally bound the gap between distinct-image capacity and decodable-message capacity under robustness.** The theoretical bounds count distinct watermarked images that satisfy constraints. The handcrafted model (Eq. 2) shows this gap is small for the PSNR-only (no robustness) case. But for the robustness setting, the paper does not establish how many of the distinct surviving images are actually distinguishable by a learned blind decoder after transformation. Bound 13 is already very conservative (it is a lower bound), but the paper's argument that the entire observed gap in the full robustness setting is due to architectural limitations (extrapolated from the PSNR-only setting) relies on analogy rather than direct evidence. A stronger test would be to evaluate whether Chunky Seal or another model can approach Bound 13's values.

### Minor

3. **Chunky Seal's trade-offs are under-emphasized in the abstract and results.** The abstract states Chunky Seal "increases capacity 4× to 1024 bits, all while preserving image quality and robustness" without mentioning the 90× larger embedder (1022.7M vs. 11.0M parameters) and 23× larger extractor (773.7M vs. 33.0M). The paper does acknowledge this is not a practical path forward in the discussion (Section 5), and the table (Table 3) reports model sizes, so the information is available. However, the presentation of results emphasizes the capacity gain without proportional emphasis on the cost. Additionally, Chunky Seal shows small but consistent degradations on several augmentations (rotation: 98.27% vs. 98.84%; JPEG: 98.79% vs. 99.74%) and 4× higher LPIPS (0.0085 vs. 0.0019), which is partially masked by the "overall" accuracy aggregation.

4. **Statistical comparison between Chunky Seal and Video Seal is informal.** Table 3 reports standard deviations, which is good, but some robustness differences (e.g., JPEG accuracy gap of ~1%) appear meaningful given the tight standard deviations. A significance test or discussion of whether these differences are systematic would strengthen the comparison, especially since Chunky Seal is 90× larger.

### Trivial

5. Bound 1 (absolute capacity = *cwhk* bits) is stated as a formal numbered bound. It is simply the observation that an uncompressed image contains *cwhk* bits of information. Including it alongside substantive bounds inflates the apparent number of distinct contributions.

## Nice-to-Haves

- A direct evaluation of whether Chunky Seal (or another model) can approach the conservative Bound 13 values under the corresponding augmentations, to test whether the gap in the robustness setting is also architectural.
- Statistical significance tests for the small robustness accuracy differences between Chunky Seal and Video Seal in Table 3.

## Removed Points

The following points from the harsh critic were reviewed and removed after verification against the paper:

- **PSNR-only bounds are "apples-to-oranges":** The critic claimed the PSNR-only bound (no robustness) cannot be compared to empirical methods that include robustness. However, the paper's controlled experiments (Section 3) explicitly strip away robustness and *still* show a gap, making this a valid comparison in that setting. The paper is clear about when it discusses the no-robustness case vs. the with-robustness case.

- **Data distribution argument is "unvalidated" and "misleadingly framed":** The critic claimed the VQ-VAE-based estimate is "the opposite of conservative." In fact, assuming *all* possible natural images could fall in the same PSNR ball *maximizes* estimated collisions, which is the conservative (worst-case) direction for computing a lower bound on capacity. The paper's use of VQ-VAE codebook size is an approximation, but the conclusion (data distribution has negligible effect) is robust because even a 1000× larger codebook would add only ~10 bits to the log₂ count.

- **Criticism that Bound 1 inflates contributions:** This was kept as Trivial weakness 5 above but was rephrased; the original harsh critic version was more dismissive ("inflates the apparent number of contributions").

- **Criticisms about missing appendix content, proofs, or references:** The parser strips these sections from all papers; they exist in the original submission.

- **Criticisms about "not yet released" code/checkpoints:** The paper states "Chunky Seal code and checkpoints will be released" (footnote 1). Per guidelines, do not question existence/release status of cited entities.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Restructure claims by setting.** Present the PSNR-only (no robustness) analysis and experiments as a clean, independent contribution establishing architecture as the bottleneck in a simplified setting. Then present the with-robustness case with more circumspect language, explicitly stating the gap varies from ~3.5× to ~100× across augmentations under the conservative bound.

2. **Add a qualifier in the abstract.** Instead of "orders of magnitude larger than what current models achieve," add a brief qualification such as "in simplified settings and under heuristic robustness bounds."

3. **Visually distinguish heuristic bounds from validated bounds in figures.** In Figure 4 (and Figure 1), clearly mark the heuristic robustness bounds (Bounds 10–12) as unvalidated estimates, not as established facts. A dashed line or a note in the caption would suffice.

4. **Add a baseline for Bound 13 achievability.** Test whether Chunky Seal (or a simpler architecture) can approach the conservative Bound 13 values for the corresponding augmentations, even if computationally expensive. This would directly test whether the robustness-case gap is also architectural.

5. **Explicitly report cost alongside capacity for Chunky Seal.** In a single place (e.g., the results paragraph), state: "Chunky Seal achieves 4× capacity at the cost of a 90× larger embedder and 23× larger extractor." This is already implicit from Table 3 but should be explicit.

## Score and Decision

The calibration tool was unavailable; I have therefore calibrated manually against known ICLR quality standards.

The paper makes a genuine contribution: it provides a clean theoretical framework for reasoning about watermarking capacity, designs informative controlled experiments that convincingly identify architecture as a bottleneck in simplified settings, and demonstrates that higher capacities are achievable. The paper is transparent about its limitations. However, the headline "orders of magnitude" claim overreaches for the with-robustness case, and the paper would benefit from sharper separation of claims by setting. These are framing issues that are addressable in revision, not fatal methodological flaws.

On balance, this is a solid paper with a real contribution and addressable weaknesses. I recommend accept with revisions.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>