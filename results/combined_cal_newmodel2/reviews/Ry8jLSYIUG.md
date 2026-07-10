Now I have enough information to calibrate. Let me finalize the review.

## Summary
This paper introduces a geometric framework for bounding the message-carrying capacity of images under PSNR (ℓ₂) constraints and linear robustness constraints. The framework models images as points on a high-dimensional integer grid and counts lattice points in the intersection of a cube (the set of valid images) and a ball (the PSNR constraint). The theoretical bounds suggest capacities orders of magnitude larger than current models achieve. Controlled experiments on solid gray images show that Video Seal fails to approach even the PSNR-only bounds while simpler models succeed, pointing to architectural limitations. Chunky Seal, a scaled-up version of Video Seal, achieves 4× capacity (1024 bits) at the cost of 90× more embedder parameters.

## Strengths
- **Novel geometric framework for capacity bounds.** Modeling images as points on a high-dimensional integer grid, PSNR constraints as ℓ₂-balls, and counting lattice points in their intersection (Sections 2.2-2.3) is a genuinely different approach from prior information-theoretic work. It handles discrete pixel levels and produces concrete numerical capacity estimates for specific resolutions and PSNR thresholds. This is the paper's most original theoretical contribution.
- **Clean experimental paradigm for isolating architectural limitations.** The controlled experiment in Section 3 — training Video Seal on a single solid gray image with only a PSNR constraint and no augmentations — is well-designed. The finding that Video Seal cannot embed 1024 bits into a uniform gray field while a linear model can (Table 1, Figure 5) is a genuinely surprising result that points to real architectural issues in Video Seal. This is the strongest empirical evidence in the paper.
- **Elegant handcrafted embedder.** Equation (2) — fitting the largest axis-aligned cube inside the PSNR ball and using it to encode messages — is a clean construction that nearly matches the theoretical bound on solid gray images, demonstrating the bounds are approachable in principle under the paper's assumptions.
- **Honest about limitations of robustness bounds.** The paper explicitly acknowledges that Bounds 10-12 are heuristic (p. 5: "these heuristic bounds under-approximate and cases where they over-approximate the true capacity") and that Bound 13 is "extremely conservative and unrealistic." This transparency about the limits of the theoretical analysis is commendable.

## Weaknesses

### Fatal
None.

### Major
- **The theoretical bounds equate PSNR (ℓ₂ distance) with imperceptibility, which is a weaker constraint than true perceptual similarity for natural images.** The entire theoretical framework (Sections 2.2-2.4) counts images within an ℓ₂-ball, but for a natural image with edges, textures, and objects, many images within the PSNR ball would be visibly distorted. The paper frames these as bounds on "imperceptible" watermarking capacity (line 37: "capacity is determined by the number of unique points that satisfy imperceptibility and robustness constraints"), but they are strictly bounds on PSNR-constrained capacity. The data distribution argument in Section 2.6 attempts to bridge this gap but is not fully convincing. The headline claim that theoretical capacities are "orders of magnitude larger" applies to a less restrictive constraint than actual watermarking requires for natural images. The paper acknowledges this gap only briefly in limitations (Section 5) rather than addressing it substantively. This is the most significant limitation: it means the gap between the bounds and practical performance may be substantially smaller for natural images under realistic perceptual constraints than the "orders of magnitude" language suggests.

### Minor
- **The controlled experiments (Section 3) use only solid gray images.** While this is a valid minimal setup for isolating architectural limitations, a solid gray image is the best possible case for the ℓ₂ bounds — any image within the PSNR ball is perceptually acceptable. The paper claims to rule out explanations A-C (real-world complexity) based on these experiments, which is logically valid for the PSNR-only setting. However, the broader conclusion that current models are far from achievable capacity on *natural images* with *realistic robustness constraints* extrapolates beyond what the gray-image evidence directly supports. Section 4's Chunky Seal results, which do involve natural images and robustness, show only a modest 4× improvement with massive scaling.

- **The Section 2.6 argument about data distribution's negligible effect is not rigorous.** The VQ-VAE's codebook size (2^10240) bounds the total number of distinct natural images overall, not the number that could fall within a single cover's PSNR ball. The "conservative" assumption that all 2^10240 images could lie in one PSNR ball is physically unrealistic (they would not all fit in the ball's volume). And the invocation of Costa (1983) at the end of the paragraph is about Gaussian channels, not this geometric counting problem. This argument therefore does not convincingly dismiss the data distribution concern, though the paper's main empirical evidence (Section 3) does not depend on it.

- **Chunky Seal's demonstration shows diminishing returns.** 4× capacity (1024 vs. 256 bits) requires a 90× larger embedder and 23× larger extractor (Table 3), with slightly worse robustness and quality metrics (LPIPS 0.0085 vs. 0.0019, overall bit accuracy 99.15% vs. 99.31%). The paper acknowledges this is not a practical path forward, and the modest scaling returns are as consistent with the bounds being loose for realistic settings as with the paper's thesis that substantially higher capacities are within reach.

### Trivial
- Table 1 reports single values from best-performing runs across hyperparameter sweeps without variance or confidence intervals. Figures 5 and 6 partially address this with scatter plots, but the headline numerical comparisons would benefit from statistical characterization.

## Nice-to-Haves
- Running controlled experiments on at least one natural image (even a single test image with only the PSNR constraint and no augmentations) would substantially strengthen the generalization claim.
- Tightening the robustness bounds (Bounds 10-12) from heuristic to provable for specific transformation families would add rigor.
- Showing qualitative examples of watermarked images at the highest bit counts (linear model at 2048 bits, handcrafted at 456,509 bits) would help readers calibrate what these capacity numbers mean in perceptual terms.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Criticism that the PSNR-perceptual gap is "fatal/structural":** Downgraded to Major. The paper is explicit about working under PSNR constraints, and PSNR is the standard metric in the watermarking community. The gap is a real limitation but not a fatal invalidation.
- **Criticism about missing statistical reporting (from Harsh Critic's "Missing Parts"):** Kept as Trivial above rather than elevated to Minor or Major.
- **Criticism that controlled experiments "do not support the conclusion that current models are far from achievable capacity on natural images":** Downgraded to Minor from the harsh critic's framing as a critical issue. The paper's logic (if the gap exists in the simplest case, complexity cannot be its primary cause) is sound for the specific purpose of ruling out hypotheses A-C. The paper does separate its PSNR-only claims from real-world claims.
- **The Costa (1983) reference criticism:** Folded into the existing Minor weakness about Section 2.6 rather than treated as a separate issue.
- **Missing qualitative examples / perceptual metrics suggestions:** Moved to Nice-to-Haves.
- **Strengthening the Paper on Its Own Terms items:** Moved to Nice-to-Haves.

## Novel Insights
The reviews surface a key tension that the paper itself does not fully resolve: the geometric bounds are clean and intuitive for ℓ₂-constrained capacity, but the leap to claiming these bound "imperceptible" watermarking capacity for natural images is where the argument strains. The paper's most convincing evidence is the failure of Video Seal on minimal gray-image PSNR-only setups — this genuinely reveals architectural limitations — but the size of that architectural gap for natural images under realistic perceptual+robustness constraints remains an open question that the paper's evidence does not directly address. The reviewers converge on the judgment that the theoretical framework is valuable and the experimental paradigm is clean, but the headline claims outrun the evidence.

## Suggestions
- Acknowledge more directly that the bounds are for PSNR-constrained capacity, not perceptual capacity, and clarify what this implies for the headline "orders of magnitude" claims about natural images.
- Add at least one controlled experiment on a natural image (same stripped-down setup: PSNR-only, no augmentations) to test whether the architectural limitations identified on gray images also manifest on structured images.
- Report variance across runs for the simplified experiments in Table 1.
- Either tighten the Section 2.6 argument with a more principled estimate of data distribution effects, or remove it and acknowledge the gap more directly.

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| u1cQYxRI1H.md | 0.50 | R1, <1.5 | No | Strong reject; unrelated topic (illumination harmonization) |
| 5lUdTogEL3.md | 1.00 | R1, <1.5 | No | Strong reject; unrelated topic (person re-id) |
| gwZ90hFSL2.md | 1.00 | R1, <1.5 | No | Strong reject; unrelated (NLP for robots) |
| 5kMwiMnUip.md | 1.40 | R1, <1.5 | No | Strong reject; unrelated (LLM jailbreaking) |
| Uj0h13lVrR.md | 1.00 | R1, <1.5 | No | Strong reject; unrelated (GFlowNets) |
| bEgDEyy2Yk.md | 1.00 | R1, <1.5 | No | Strong reject; unrelated (minimax paths) |
| S3zKrEQpRr.md | 3.00 | R1, 1.5-3.5 | No | Weak paper on GNNs as communication channels |
| Z1E0EahS5w.md | 3.33 | R1, 1.5-3.5 | No | Reservoir learning limits paper |
| 6j0GH40mFt.md | 3.40 | R1, 1.5-3.5 | No | Learned image compression; somewhat related but weaker |
| hYEV8QmaOt.md | 3.40 | R1, 1.5-3.5 | No | Image anti-forensics; different sub-area |
| Hh0Cg4epYY.md | 2.33 | R1, 1.5-3.5 | No | Bayes error bounds; different topic |
| f47c05mcOj.md | 3.00 | R1, 1.5-3.5 | No | Adversarial perturbations for compression |
| O08nfMzc93.md | 4.50 | R1, 3.5-5.5 | **Yes** | Watermark detection/attribution theory. Weak experiments, sloppy writing. Our paper is stronger in novelty and experimental design. |
| T0ebbDO60R.md | 3.75 | R1, 3.5-5.5 | No | Training-free watermarking. Lower quality. |
| HexshmBu0P.md | 5.33 | R1, 3.5-5.5 | **Yes** | Watermarking diffusion models recipe. Strong experiments but limited novelty. Our paper has more novel theory. |
| 9XEBFywIW7.md | 4.40 | R1, 3.5-5.5 | No | Content watermarking; different setting |
| HAD6iZxKuh.md | 5.20 | R1, 3.5-5.5 | No | WMAdapter; applied method paper |
| jlhBFm7T2J.md | 6.50 | R1, 5.5-7.5 | **Yes** | Undetectable watermark. Strong theory+experiments. Our paper's strengths are comparably high but our main weakness is more consequential. |
| ll2nz6qwRG.md | 5.83 | R1, 5.5-7.5 | **Yes** | Two-stage watermarking. Solid accepted paper. Our paper compares favorably in novelty but has a more fundamental assumption gap. |
| 1IwoEFyErz.md | 6.00 | R1, 5.5-7.5 | No | Shallow Diffuse; subspace watermarking |
| UchRjcf4z7.md | 6.50 | R1, 5.5-7.5 | No | Transfer attack on watermarks |
| 16O8GCm8Wn.md | 6.40 | R1, 5.5-7.5 | No | W-Bench/VINE; watermark evaluation benchmark |
| hzxvMqYYMA.md | 5.75 | R1, 5.5-7.5 | No | Image quality assessment theory |
| j7b4mm7Ec9.md | 7.60 | R1, 7.5-8.5 | **Yes** | Lightweight watermarking. Very strong experiments but rejected on novelty/relevance concerns. Our paper is different in nature (theory vs methods). |
| CxXGvKRDnL.md | 8.00 | R1, 7.5-8.5 | No | Diffusion-based compression; different area |
| Tzh6xAJSll.md | 7.60 | R1, 7.5-8.5 | No | Associative memory scaling laws |
| 25kAzqzTrz.md | 8.00 | R1, 7.5-8.5 | No | FixMatch theory |
| EUSkm2sVJ6.md | 7.60 | R1, 7.5-8.5 | No | Data usage inference |
| 6O3Q6AFUTu.md | 8.00 | R1, 7.5-8.5 | No | Image interpolation with diffusion |

Round-1 bracket: 4.5–6.0.

Round 2 narrowed via the 4.5–5.5 and 5.5–6.5 bands. The favorability comparison shows our paper's strengths (12-15 on the geometric framework and experimental paradigm) exceed those of the 4.50 anchor (max ~11) and are comparable to or higher than the 5.33 and 5.83 anchors. However, our paper's core weakness (PSNR-perceptual gap, favorability -1.16) is more damaging than the weakness profiles of the 5.83 and 6.50 anchors (which have no single weakness below -1.0 in a similar way). This weakness prevents the paper from reaching the 6+ range where the accepted anchors sit.

The paper sits above the 4.50 anchor (which had weak experiments and poor writing) and the 5.33 anchor (limited novelty), but below the 5.83 accepted paper and the 6.50 accepted paper, both of which have cleaner claims-to-evidence mappings. Final score: **5.5**.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>