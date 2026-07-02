Now I will produce the final consolidated review.

## Summary

This paper takes a geometric approach to upper-bound the message-carrying capacity of images under PSNR constraints. The authors derive capacity bounds for three regimes (cube-in-ball, ball-in-cube, non-trivial intersection) and extend these with heuristic bounds under robustness to linear transformations (crop, rotation, JPEG). Controlled experiments demonstrate that even in a minimal setup (single gray image, PSNR-only constraint), Video Seal fails to reach the theoretical capacity while simple linear and handcrafted models succeed, pointing to architectural limitations. The authors then train Chunky Seal, a scaled-up model achieving 1024 bits (4× over Video Seal) with comparable robustness.

## Strengths

1. **Clean geometric framework for PSNR-only capacity (Section 2.3).** The box-ball intersection model (Figure 2) provides a precise, interpretable way to upper-bound watermarking capacity under a PSNR constraint. The three regimes are correctly enumerated with clean transitions. The computed bound of ~600,000 bits for a 256×256×3 image at 42 dB serves as a useful reference point.

2. **Well-designed controlled experiments isolating architectural failure (Section 3).** Reducing to a single gray image with only a PSNR constraint and demonstrating that Video Seal cannot embed 1024 bits while a trivial linear embedder/extractor can is a convincing diagnostic. The tiling experiment (embedding at 32×32px and tiling to 256×256px) elegantly shows that the architecture, not the problem, is the bottleneck. The handcrafted model (Equation 2) achieving 456,509 bits at 42 dB confirms the PSNR-only bounds are not vacuous.

3. **Chunky Seal is a real, non-trivial improvement.** Scaling Video Seal to 1024 bits (4× improvement) while maintaining comparable quality and robustness across a wide battery of transformations (Table 3) is a substantive result. The fact that this was done without hyperparameter tuning strengthens the case that further gains are possible.

## Weaknesses

### Fatal
None.

### Major

**1. The central "orders of magnitude" claim rests on robustness bounds the paper itself cannot fully defend.** The paper acknowledges that Bounds 10–12 are "heuristic," "not valid lower bounds," and that "the true capacity under linear transformation could be much lower than these bounds predict" (lines 156–158). Bound 13 (the only provable lower bound) is described as "extremely conservative and unrealistic" (line 158). Yet Figure 4 — the paper's primary visual evidence for a large remaining gap under realistic conditions — plots only the heuristic bounds (10–12), not Bound 13. The abstract and introduction state that "theoretical capacities are orders of magnitude larger than what current models achieve" without distinguishing between the well-supported PSNR-only bounds and the contested robustness bounds. The paper is transparent about the caveats in Section 2.5, but the headline claims outrun what the provable numbers support. Concretely: Bound 13 gives 904 bits for Crop&Rescale 75% at 42 dB (Table 2), while Chunky Seal already operates at 1024 bits — a gap that is not "orders of magnitude." For other augmentations in Table 2, Bound 13 gives values (14K–602K bits) that are indeed much larger than current methods, but the paper does not directly test whether these numbers are achievable, leaving the "orders of magnitude" claim in a precarious middle ground where the only rigorous bound is close to current practice for the hardest transformation.

**2. No direct comparison between Chunky Seal and the robustness bounds under matched conditions.** Chunky Seal is tested under transformation ranges (e.g., "Crop 77–95%") that do not exactly match the conditions used for Bounds 10–13 (e.g., "Crop&Rescale 75%" at a specific 42 dB PSNR). Table 3 reports bit accuracy under ranges, not the maximum reliable capacity under the specific conditions of the bounds. This makes it impossible to determine whether Chunky Seal is near the heuristic bounds, near the conservative bounds, or somewhere in between. The paper's most direct empirical test of the bounds is missing.

### Minor

**3. Robustness bounds deferred to appendix and not fully assessable from the main text.** The derivation of Bounds 10–13 is described only at a high level in Section 2.5 with details deferred to Appendix G. The reader cannot assess the soundness of these bounds from the main paper. The paper would benefit from a brief sketch of the derivation approach (even one paragraph per bound type) to make the main text self-contained for most readers.

**4. Chunky Seal's results are more consistent with a modest gap than with "orders of magnitude" under the most aggressive robustness.** For Crop&Rescale 75%, Chunky Seal (1024 bits) is near Bound 13 (904 bits). While Bound 13 is acknowledged as "extremely conservative" and the comparison is not apples-to-apples, the fact remains that the paper's own largest model operates close to the only provable lower bound for this common transformation. The paper's preferred interpretation is that the heuristic bounds (~0.5 bpp) are the relevant ones, but it does not provide evidence that the gap between Bound 13 and the heuristic bounds can be closed by better architectures.

**5. The logical chain from PSNR-only experiments to robustness conclusions has a gap.** The handcrafted model (456,509 bits) shows the PSNR-only bounds are achievable, and Video Seal's failure shows architectural limitations in that setting. The paper then concludes that models are "significantly underperforming" overall, including under robustness. But the PSNR-only achievements of the handcrafted model say nothing about whether the *robustness-inclusive* bounds are achievable — the handcrafted model provides zero robustness. The robustness conclusion relies on Chunky Seal's 4× improvement, which is real but modest, leaving a disconnect between the strong PSNR-only evidence and the weaker robustness evidence.

### Trivial

None.

## Nice-to-Haves

- **Plot Bound 13 in Figure 4 alongside the heuristic bounds.** Showing the conservative bound would give readers an honest visual range of plausible capacities under robustness, rather than only the upper end.
- **Test Chunky Seal's maximum reliable capacity under the exact conditions used for Bound 13.** For example, evaluate at Crop&Rescale 75% at exactly PSNR 42 dB and report the maximum bit count with >99% accuracy. This would directly verify whether Bound 13 is indeed "too conservative."
- **Explore the capacity–robustness Pareto frontier.** If the paper's thesis is correct, reducing capacity should yield higher robustness (or higher quality). A simple ablation (e.g., 256-bit Chunky Seal) showing improved robustness over 1024-bit Chunky Seal would strengthen the argument.

## Removed Points (flagged for removal — treat with caution)

1. **Criticism that the data distribution analysis (Section 2.6) conflates codebook capacity with natural image density.** The paper makes a maximally conservative assumption: that ALL 2^10240 distinct VQGAN-representable images could fall within a single PSNR ball, yielding a collision penalty of at most 10,240 bits (~0.05 bpp). The critic's concern about higher density of natural images in pixel space would imply MORE images in the ball, but the paper already assumes the maximum possible (all distinct images). The critic's argument misunderstands the paper's conservative bounding approach. This criticism is removed as factually incorrect.

2. **Criticism that the handcrafted and linear baselines "do not support the conclusion they are invoked to support" regarding robustness bounds.** The paper explicitly limits the handcrafted model to "the solid gray image case with PSNR constraint and no robustness requirements" (line 287). The paper does not claim the handcrafted model validates the robustness-inclusive bounds. The broader argument about architectural limitations is supported by multiple lines of evidence (Video Seal failure, linear model success, tiling, Chunky Seal scaling), not solely by the handcrafted model. The critic's characterization overstates what the paper claims. This criticism is removed as a misreading of the paper's logical structure.

3. **"No attempt to trade capacity for robustness"** — this demands an exploration outside the paper's stated scope (demonstrating that higher capacity is possible, not mapping the full Pareto frontier).

## Novel Insights

None beyond the paper's own contributions. The reviews surface a tension between the paper's headline claims and its own acknowledged limitations — the heuristic robustness bounds are used prominently while the only provable lower bound (Bound 13) is minimized — but this is a critique of presentation, not a novel insight about the subject matter.

## Suggestions

1. **Re-calibrate the central claim.** Distinguish clearly between the well-supported PSNR-only bounds (which genuinely show orders-of-magnitude gaps) and the robustness-inclusive bounds (which are heuristic and less validated). Consider framing the robustness bounds as conjectures or plausibility arguments rather than as established theoretical limits.

2. **Add a direct comparison experiment.** Measure Chunky Seal's maximum reliable capacity under the exact conditions of Bound 13 (e.g., Crop&Rescale 75% at 42 dB) and report whether it exceeds 904 bits. This single experiment would significantly clarify whether Bound 13 is truly "too conservative."

3. **Include Bound 13 in Figure 4.** Showing the conservative bound on the same axes as the heuristic bounds would allow readers to see the full range of plausible capacities rather than only the optimistic end.

## Score and Decision

The paper has genuine contributions — the PSNR-only capacity analysis is novel and technically sound, the diagnostic experiments are well-executed and insightful, and Chunky Seal demonstrates that practical improvement is possible. However, the paper's headline claims about "orders of magnitude" of untapped capacity under realistic robustness constraints are not adequately supported, as the only provable lower bound (Bound 13, 904 bits for aggressive crops) is close to what Chunky Seal already achieves. The paper would benefit from more measured framing and direct empirical validation of its robustness bounds.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>