## Summary
# Final Review Report

## Summary

This paper presents Stylos, a feed-forward framework for multi-view 3D style transfer built on 3D Gaussian Splatting. The key idea is to combine a pretrained VGGT geometric backbone (kept unchanged) with a Style Aggregator module that injects style information via cross-attention, and a voxel-level 3D style loss that enforces multi-view consistency. The method operates on unposed image collections (single to hundreds of views) and produces stylized 3D Gaussians in a single forward pass without per-scene optimization.

The paper demonstrates competitive results on CO3D and Tanks & Temples benchmarks, achieving best consistency metrics (short/long-range LPIPS and RMSE) against StyleGaussian, G-Style, SGSST, and Styl3R, with the fastest inference speed (0.05s per scene). The strongest empirical contribution is the cross-view stylization consistency, which improves over the closest feed-forward baseline Styl3R by a substantial margin (e.g., Truck short-range LPIPS: 0.028 vs 0.061).

However, the manuscript has a critical textual error where the Quantitative Evaluation paragraph describes Styl3R's results as best while the tables clearly show Stylos as best, suggesting a copy-paste error. Additionally, the novelty contribution is partially inherited from VGGT/AnySplat, key implementation details are missing, and no variance/statistical significance is reported. These issues must be addressed before publication.

## Strengths
1. **Novel formulation of feed-forward 3D stylization.** Stylos is among the first methods to demonstrate that 3D style transfer can be performed in a single forward pass from unposed multi-view images, without per-scene optimization or precomputed camera parameters. This is a meaningful step toward real-time 3D stylization.

2. **Effective style-content separation design.** The two-pathway architecture — self-attention for geometry, cross-attention for style — is well-motivated and ablations confirm that the Global CrossBlock variant outperforms other configurations. Keeping the geometric backbone frozen during style fine-tuning is a practical design choice that preserves reconstruction quality.

3. **Competitive empirical results.** On both CO3D and Tanks & Temples datasets, Stylos achieves the best consistency metrics (short/long-range LPIPS and RMSE) among compared baselines, including the feed-forward baseline Styl3R. The qualitative results (Fig. 5) show noticeably more coherent stylization — e.g., the truck scene is rendered in consistent yellow without color artifacts that affect other methods.

4. **Fast inference speed.** At 0.05s per scene, Stylos is an order of magnitude faster than Styl3R (0.16s) and orders of magnitude faster than per-scene optimization methods (minutes to hours). This practical efficiency is a genuine strength for potential deployment.

5. **Controllable stylization.** The interpolation experiments (Fig. 6) demonstrating multi-style blending and content-style trade-off control without additional optimization are a nice addition that showcases flexibility beyond single-style transfer.

## Weaknesses
### W1. Critical text-table contradiction (Severity: Critical — Must fix)

**Location:** Page 7 — Section 4.2, "Quantitative Evaluation" paragraph.

The text states: "As shown in Table 3, Styl3R achieves strong and stable consistency scores, ranking the first across all consistency metrics and all four scenes." However, Table 3 clearly shows Stylos (the authors' own method) as the best across ALL metrics and scenes, with Styl3R consistently performing worse (e.g., Truck short-range LPIPS: Stylos = 0.028, Styl3R = 0.061). The same error propagates to the description of Table 4, where the text attributes best/second-best results to Styl3R, but the table shows Stylos achieving those rankings.

This appears to be a systematic find-replace error where "Stylos" was incorrectly replaced with "Styl3R" in this paragraph. It is a critical factual error because it completely misrepresents the paper's own experimental outcomes. Readers relying on the text without cross-checking tables will be misled.

**Required fix:** Rewrite the entire "Quantitative Evaluation" paragraph to accurately describe Stylos's performance. A corrected version is provided in Annotation #2.

### W2. Novelty boundaries are not clearly delineated from prior work (Severity: Major — Must fix)

**Location:** Page 3 — Sec 3.2.1; Page 2 — Related Work 2.1.

The paper honestly states that the geometric backbone "follows the alternating-attention design of VGGT" and is "kept unchanged." The voxelization and Gaussian adapter follow AnySplat. However, the contribution claims (C1 and C3) describe the overall pipeline as if it were a novel end-to-end system, without explicit acknowledgment of what is inherited versus new. The technical novelty resides specifically in: (a) the CrossBlock-based Style Aggregator that inserts cross-attention between self-attention and MLP, and (b) the voxel-level 3D style loss. The feed-forward pose-free reconstruction capability is entirely inherited from VGGT/AnySplat.

**Required fix:** Add explicit sentences in Sec 2.1 and Sec 3.2.1 acknowledging the inherited components and clearly stating the novelty boundary. The contribution claims should be scoped to the style injection mechanism and loss, not the overall pipeline.

### W3. Missing implementation details reduce reproducibility (Severity: Major — Must fix)

**Location:** Page 3 — Sec 3.2.2 Style Aggregator.

Several critical details are absent: (1) style token extraction — the text never specifies that DINOv2 processes the style image; this is only visible in the figure caption. (2) Feature projection — how style tokens and content tokens are projected to the same dimension is unspecified. (3) Token counts $L_q$ and $L_{kv}$ are not given, making computational complexity opaque. (4) The Hybrid CrossBlock variant is described only by reference to "released codes."

**Required fix:** Specify style token extraction via DINOv2 + learned projection, state token counts, and provide Hybrid CrossBlock equations in the main text.

### W4. Missing variance and statistical significance in experimental results (Severity: Major — Must fix)

**Location:** Page 5-8 — Section 4, Tables 1-4.

All tables report point estimates without standard deviation, confidence intervals, or significance tests. Key comparisons involve very small differences (e.g., Table 2: short-range LPIPS 0.048 vs 0.047, long-range RMSE 0.142 for both image loss and 3D loss). Without variance estimates across seeds or scenes, readers cannot assess whether reported improvements are statistically reliable. The ablation study (Table 2) uses "15 held-out scenes randomly selected" but reports only aggregate means.

**Required fix:** Report mean $\pm$ std over at least 3 training seeds for all main results. For CO3D ablation, report per-scene variance within each category. Add explicit discussion of effect sizes and statistical significance for key comparisons.

### W5. Architecture-training ambiguity (Severity: Major — Must fix)

**Location:** Page 4 — Sec 3.3 vs Sec 3.2.2.

The paper states that the geometric backbone is "kept unchanged" from VGGT, but the Style Aggregator "replaces standard block with CrossBlock" — implying modification of the backbone itself. Stage 2 freezes "all geometry-related modules" but updates the Style Aggregator. It is unclear how CrossBlocks (inserted into the backbone) can be trained separately from the frozen backbone layers. The architectural boundary between "backbone" and "aggregator" is not defined.

**Required fix:** Clarify whether CrossBlocks are inserted into the backbone or attached as an external module. Specify gradient flow: how do gradients reach the CrossBlocks without flowing through frozen layers? Provide a diagram or pseudocode showing the trainable/frozen boundary.

### W6. Missing limitations section (Severity: Minor — Should fix)

**Location:** Page 9 — Section 5 Conclusion.

The conclusion does not discuss any limitations of the approach. Known limitations include: (a) quality degradation when views/batch > 32, (b) the 3D voxelization resolution trade-off, (c) dependence on VGGT's failure modes (textureless surfaces). Adding a limitations paragraph would strengthen scientific rigor.

### W7. Introduction could be restructured for clarity (Severity: Minor — Should fix)

**Location:** Page 1 — Section 1 Introduction.

The introduction combines method description, 2D loss critique, and contributions in a dense single flow. The transition from pipeline description to a discussion of 2D style transfer losses is jarring. Splitting into two paragraphs (method overview; loss motivation + contributions) would improve readability. Additionally, the first paragraph should state the core technical challenge more concretely rather than saying "remains challenging."

### W8. Minor typo in Eq. (3) (Severity: Minor — Should fix)

**Location:** Page 5 — Eq. (3).

The second term uses $\mathcal{R}_{b,s}^l$ where the subscript $s$ should be $v$ to match the view summation index. This is a typesetting error.

### W9. Related Work lacks critical differentiation (Severity: Minor — Should fix)

**Location:** Page 2 — Sec 2.1.

The pose-free reconstruction section reads as a chronological list without explaining how Stylos differs from each cited method. Explicit differentiation would strengthen positioning.

### W10. Evaluation time comparison may be slightly unfair (Severity: Minor — Consider)

**Location:** Page 8 — Table 4 footnotes.

Stylos's inference time (0.05s) is compared against methods that require per-scene training (165m, 14.7m, 35.2m). This is a valid comparison for deployment use cases, but the table should also report Stylos's total training time since the feed-forward methods require upfront training. Including training GPU-hours would provide a complete picture of computational cost.

## Score
**Final Score: 6/10**

**Scoring rationale.** This score prioritizes research value and novelty as primary dimensions, while considering validity, soundness, and reproducibility.

The core contribution — combining a feed-forward pose-free 3D reconstruction backbone with cross-attention-based style conditioning and a voxel-level style loss — has clear research value as one of the first demonstrations of single-forward 3D stylization from unposed inputs. The empirical results are competitive and the speed advantage (0.05s) is practically meaningful.

However, the score is constrained by: (1) a critical textual error that undermines trust in the manuscript's internal consistency (W1); (2) the fact that major components (VGGT backbone, AnySplat voxelization/adapter) are inherited from prior work without explicit novelty boundary delineation (W2); (3) missing variance/statistical evidence that prevents assessment of result reliability (W4); and (4) insufficient implementation details for reproducibility (W3). These issues are fixable but current as-is.

**Post-revision target:** If W1-W4 are satisfactorily addressed and limitations are honestly discussed (W6), the paper could reach a score of 7/10. The critical text error (W1) must be corrected before any positive reconsideration.

**External literature verification deferred.** Due to Retrieval-Disabled Mode (external paper search unavailable), novelty/comparison conclusions regarding overlap with specific prior works (e.g., Styl3R, StyleGaussian, G-Style) are based solely on the manuscript's own reported comparisons. Independent literature verification is recommended before final acceptance decisions.