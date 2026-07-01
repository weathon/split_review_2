Now I'll write the final review.

## Summary

This paper establishes theoretical upper bounds on image watermarking capacity under PSNR constraints (and heuristically under linear robustness constraints), showing theoretical capacity is orders of magnitude larger than current models achieve. Through controlled experiments that strip away real-world complexity (a single gray image, no augmentations), it demonstrates that Video Seal cannot reach even 1024 bits, while a linear model reaches 2048 bits and a handcrafted construction reaches 456,509 bits. Chunky Seal, a scaled-up architecture, achieves 4× the capacity of Video Seal (1024 bits) with comparable quality and robustness, confirming the bottleneck is architectural rather than fundamental.

## Strengths

- **Clean theoretical framework for PSNR-only capacity (Section 2.2–2.4).** The geometric approach — modeling images as lattice points in a hypercube and counting intersection with an ℓ₂ ball — is sound and well-executed. The three regimes (ball-in-cube, cube-in-ball, non-trivial intersection) are handled transparently, and cross-checks between volume approximations and exact lattice counts (Mitchell method) build confidence. The bound of ~2000 bits at 45 dB for a 16×16×3 image is well-scoped and falsifiable.

- **Controlled failure experiment (Section 3.1, Table 1, Figure 5).** Stripping Video Seal to a single gray image with only MSE loss and showing it cannot reach 1024 bits is the paper's strongest empirical result. This cleanly eliminates hypotheses A (robustness constraints), B (perceptual constraints), and C (data distribution) as explanations for the capacity gap. The fact that performance is nearly identical at 256×256 and 32×32 resolution (Figure 5 left vs. center) starkly demonstrates the architecture does not use the available pixel budget.

- **Linear and handcrafted baselines (Section 3.2, Table 1).** A single linear layer reaching 100% accuracy for 2048 bits at 40.4 dB, and a handcrafted grid-based construction reaching 456,509 bits at 42 dB, definitively rule out hypothesis D (bounds are unachievable). These turn a potentially purely negative result into a positive demonstration that the theory is not vacuous.

- **Transparent treatment of robustness bounds (Section 2.5).** The paper is candid about its limitations: Bound 13 is described as "extremely conservative and unrealistic," and the heuristic bounds (10–12) are openly acknowledged as not being formal lower bounds. This honesty is commendable.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Imprecise framing of the robustness-case gap.** The abstract and introduction state that "theoretical capacities are orders of magnitude larger than what current models achieve" without distinguishing the well-supported PSNR-only case (~2,300× gap) from the robustness-constrained case. Under the paper's own conservative Bound 13 (which it describes as "extremely conservative and unrealistic"), the gap for Crop&Rescale 75% is only ~3.5× (904 vs. 256 bits), ranging up to ~105× for LinJPEG q=10. The heuristic bounds (which the paper argues are more realistic) show larger gaps (~400× for aggressive cropping), but the high-level framing conflates these. While the body is transparent about the limits (Section 2.5 clearly discusses Bound 13's conservatism), the abstract and Figure 1 caption could give readers an inflated impression of the robustness-case gap. A sharper distinction at the abstract level would better serve the paper.

- **Chunky Seal lacks a controlled ablation isolating its design choices.** The embedder is increased by 90× and extractor by 23× to get a 4× capacity gain (256→1024 bits). Because Video Seal was never trained at 1024 bits with a comparable parameter budget, it is unclear whether the improvement comes from the specific changes (3-channel watermarking, stride reduction, wider layers) or simply from more parameters. The paper candidly describes this as "a scaling exercise" and notes it was trained "without hyperparameter tuning, whereas Video Seal was extensively optimized," but a controlled comparison (e.g., a wider/deeper Video Seal at 1024 bits) would clarify whether architectural innovation beyond scaling is needed.

- **No variance or repeated-run statistics for the simplified experiments (Table 1).** Table 1 reports only the best-performing runs. Without standard deviations or multiple-seed results, it is unclear which results are robust and which may be the best from a noisy hyperparameter sweep. Given the modest sweep coverage (3 learning rates × 3 λ_i values), this is a limitation.

### Trivial

- **Bound plots are shown only for small resolutions.** Figure 3 uses 16×16 images and Figure 4 uses 40×6 images. The paper extrapolates to 256×256 in text, which is analytically straightforward (bounds scale with dimension), but including direct plots at the standard resolution would improve readability.

- **The sanity check "outperform simple linear or handcrafted baselines" (Section 5) is oddly worded.** The handcrafted model achieves near-bound performance (~456,509 bits), so no practical method would "outperform" it — the paper presents the handcrafted model as an achievability result, not a baseline to surpass. This wording needs clarification.

## Nice-to-Haves

- Training a scaled-up Video Seal (same architecture, wider/deeper) at 1024 bits would clarify whether Chunky Seal's specific design changes matter.
- Adding variance/error bars to Table 1 would strengthen the empirical claims.
- For the heuristic robustness bounds (Bounds 10–12), a more precise characterization of when they over- vs. under-estimate true capacity would be useful.

## Removed Points

These points were flagged during the review process but are removed after cross-checking against the paper. Treat them with caution.

- **"Handcrafted model does not operate blind and assumes the cover is at the center."** The paper explicitly scopes this to "the solid gray image case with PSNR constraint and no robustness requirements" (line 287). The model is presented as an existence proof against hypothesis D (bounds are unachievable), not as a practical blind watermark. This is already properly scoped.

- **"The handcrafted model's 456,509-bit number should not be compared directly to what a blind system could achieve."** The paper does not compare it to blind systems misleadingly — it is presented alongside the linear and tiling models as evidence against hypothesis D, all in the same single-gray-image setup. The paper explicitly notes this is "at least in the solid gray image case."

- **Various generic speculations about confounders, metric proxying, and scope-creep demands** that were not grounded in specific paper content.

## Novel Insights

None beyond the paper's own contributions. The observation that the robustness-case gap under Bound 13 is as small as ~3.5× is already surfaced in the paper's own Section 2.5 (Bound 13 discussion) and is not a new discovery from the review.

## Suggestions

1. Sharpen the abstract to explicitly distinguish the PSNR-only gap (~2,300×, well-supported by exact counting) from the robustness-constrained gap (uncertain magnitude, bounded between ~3× and ~400× depending on the bound used).
2. Add a controlled comparison: train Video Seal at 1024 bits with a comparable parameter count to isolate the effect of Chunky Seal's architectural changes.
3. Report repeated-run statistics (mean ± std) for the simplified experiments in Table 1.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>