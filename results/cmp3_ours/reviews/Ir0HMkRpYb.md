## Summary

This paper presents Stylos, a feed-forward pipeline for 3D style transfer that takes unposed multi-view images and a single style reference, and outputs a stylized 3D Gaussian scene in a single forward pass (~0.05s). The method builds on the VGGT/AnySplat backbones, inserting cross-attention between self-attention and MLP in the transformer blocks for style conditioning, and adds a voxel-level 3D style loss that aligns aggregated 3D features with style statistics. Experiments on CO3D (cross-category) and Tanks & Temples (cross-scene zero-shot) show that Stylos achieves better cross-view consistency than all baselines including the only other feed-forward competitor, Styl3R, while being 3× faster.

## Strengths

- **Consistent and convincing quantitative results.** Stylos wins *every* single consistency metric (short-range and long-range LPIPS, RMSE) across *all four* Tanks & Temples scenes (Table 3), and achieves best or second-best artistic metrics (ArtScore, ArtFID) across all scenes (Table 4). This is a clean, unambiguous result.
- **Practical design eliminates key bottlenecks.** By jointly predicting poses, depth, and Gaussian primitives from the VGGT backbone, Stylos removes the need for precomputed camera parameters — a real advantage for real-world multi-view captures where calibrated poses are unavailable.
- **Very fast inference.** 0.05s per scene vs. 0.16s for Styl3R and minutes/hours for per-scene optimization methods (Table 4). The feed-forward nature makes it deployment-ready.
- **Qualitative results are genuinely impressive.** Figure 5 shows that Stylos produces coherent, geometry-respecting stylization (e.g., the truck scene with *desert-town* style) where competing methods fail or produce artifacts.
- **Multi-style blending and controllable stylization** (Section 4.3, Figure 6) demonstrate a smooth, interpretable embedding space — a capability not available in per-scene optimization methods.

## Weaknesses

### Major

- **Section 4.2 text erroneously attributes Stylos' results to the baseline Styl3R.** Lines 232–233 read: *"As shown in Table 3, Styl3R achieves strong and stable consistency scores, ranking the first across all consistency metrics and all four scenes… Furthermore, Table 4 shows that Styl3R attains either the best or second-best artistic metric values"* — but Tables 3 and 4 clearly show **Stylos (ours)** achieves these results (bolded entries), while Styl3R has significantly worse numbers (e.g., Truck short-range LPIPS: Styl3R=0.061 vs Stylos=0.028) and missing entries for the Train scene. The paragraph describes the proposed method's performance while calling it a baseline. This makes the quantitative evaluation section factually wrong and confusing. **The results themselves are recoverable from the correctly labeled tables**, but this error undermines confidence and must be corrected before publication.

### Minor

- **Technical novelty over the backbone is modest.** The geometric backbone is "kept unchanged" from VGGT (line 74), the Gaussian adapter and voxelization follow AnySplat (line 108), and the CrossBlock design is cited from Deng et al. (2022). The paper's novel contributions — inserting cross-attention into VGGT blocks for style conditioning, a separate color head, and a voxel-level 3D style loss — are architecturally straightforward. The contribution is real (nobody has applied this specific combination to feed-forward 3D stylization) but the paper frames it more ambitiously than the technical delta warrants. The system-level result (it works well) is the strongest argument, not the architectural novelty.

- **The voxel-level 3D style loss provides only marginal quantitative improvement over the simpler scene-level loss.** Table 2 shows that ArtScore jumps from 4.78 (image loss) → 9.12 (scene loss), then to only 9.15 (3D loss) — a 0.3% relative improvement. Long-range LPIPS improves from 0.156→0.153 (−2%), and long-range RMSE ties with the image-level baseline at 0.142. The paper claims the 3D loss "produces sharper boundaries and a stronger sense of 3D geometry" (line 201), which is supported primarily by qualitative examples. Either the advantage is genuinely small, or the metrics do not capture what the loss improves; either way, the claim is overstated relative to the evidence.

- **The CrossBlock ablation (Table 1) evaluates only reconstruction metrics (PSNR/SSIM/LPIPS) on scenes where the first frame is used as a pseudo-style.** This tells us which design best preserves geometry, but says nothing about which produces the best *stylization*. Since stylization quality is the paper's main contribution, the ablation should also report stylization metrics (ArtScore, consistency metrics) under actual style-transfer conditions.

- **Several architecture details are underspecified.** The paper does not state the number of transformer blocks, feature dimensions, number of predicted Gaussians, or training resolution. The style image encoding pathway is labeled "Patch Embedding DiNOv2" in Figure 1 but not described in the text beyond this. These details are needed for reproducibility.

- **Styl3R results are missing for the "Train" scene** (dashes in Tables 3–4) with no explanation. If Styl3R failed or could not be run, this should be stated explicitly.

### Trivial

- **Naming inconsistency throughout the paper.** Title and abstract use "Stylos," but the conclusion (Section 5), Figure 5–6 captions, and parts of Section 4 use "Stylus." This creates confusion about the method's actual name.

## Nice-to-Haves

- **Clarify what Stage 1 training adds.** Stage 1 initializes the backbone from VGGT and distills from a frozen VGGT teacher. If the backbone is already VGGT, what does Stage 1 actually learn? An ablation comparing with/without Stage 1 would clarify this.
- **Report StylizedGS quantitative results in the main tables** rather than only in the appendix with a brief dismissal ("due to its multiple failure cases"). Even if it fails systematically, reporting the numbers would improve transparency.
- **Acknowledge the asymmetry of comparing feed-forward vs. per-scene optimization methods** more explicitly. The timing footnote (Table 4) is helpful, but the main text presents all methods as comparable alternatives. Since Stylos convincingly beats the only other feed-forward method (Styl3R), the paper's position is strong enough that it does not need to conflate the comparison categories.

## Removed Points

- *"The comparison against per-scene optimization methods is asymmetrical"* — The paper already acknowledges this in the timing footnote (Table 4). The critic overstated the severity; this is a nice-to-have framing suggestion, not a weakness.
- *"Limited novelty" framed as a critical issue* — Downgraded to Minor because the paper honestly reports which components are inherited. The system-level contribution (a working feed-forward 3D stylization pipeline from unposed inputs) is real and validated by the results. The critic's framing as "critical" is disproportionate.
- *Stage 1 training clarification needed* — This is a reasonable question but the paper does describe the purpose (line 114: "learn geometry and photometric appearance" to avoid trivial identity mapping). Moved to Nice-to-Haves.
- *"Missing code URL"* — The paper states "Our codes are available at" (line 9) with a blank; this is a last-minute formatting issue, not a substantive weakness.
- *Generic speculation about confounders or fairness* — The harsh critic raised several category-driven concerns that had no specific anchor in the paper; these have been removed per the filtering rules.

## Novel Insights

The most interesting observation emerging from this review is the gap between what the quantitative metrics measure and what the 3D style loss actually improves. The scene-level loss does almost all the work (ArtScore 4.78→9.12), while the 3D voxel loss adds only a marginal bump (9.12→9.15). Yet the qualitative examples (Figure 3) do show visible differences in boundary sharpness and geometric coherence. This suggests that standard stylization metrics (ArtScore, LPIPS, RMSE) may not adequately capture 3D geometric consistency gains. The paper would benefit from either developing a metric that measures what the 3D loss improves, or tempering the claim about its quantitative significance.

## Suggestions

1. **Fix the Section 4.2 text immediately.** Replace every instance of "Styl3R" in lines 232–233 with "Stylos (ours)" so the text matches the tables. This is the single highest-impact revision.
2. **Re-run the CrossBlock ablation (Table 1) on stylization metrics** (ArtScore, consistency LPIPS/RMSE) under real style transfer conditions, not just reconstruction with pseudo-style.
3. **Add a brief explanation for the missing Styl3R results on the Train scene** in Tables 3–4.
4. **Tone down the claim about the 3D style loss** or provide per-pixel error maps / geometric consistency measures that better capture what it improves.
5. **Resolve the naming inconsistency** (Stylos vs. Stylus) throughout the paper.

## Score and Decision

**Round 1 (Bracketing):** Based on the paper's content and comparison to calibration anchors, I initially identified a plausible score range of 5.5–7.5. The paper is not as cleanly novel as NoPoSplat (8.0), which presented a clear technical insight (canonical-space prediction) with strong results. It is closer in profile to the 4D Human Video Stylization paper (5.67, rejected) and StyleShot (5.50, rejected) — both of which were seen as incremental combinations of existing components with solid empirical results. However, Stylos has stronger quantitative results than either of those papers (winning all metrics across all scenes vs. baselines), which pushes it slightly higher. It does not reach the level of STORM (6.50, accepted), which had a clearer novel architecture. The Section 4.2 presentation error is a significant mark against it.

**Calibration anchors used:**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| NoPoSplat (P4o9akekdf) | 8.00 | 1 | Cleaner technical novelty, accepted; Stylos is not at this level |
| STORM (M2NFWRPMUd) | 6.50 | 1 | More architectural novelty, accepted; Stylos is slightly weaker |
| 4D Human Video Stylization (LH2JNpfwdH) | 5.67 | 2 | Similar incremental combination critique, rejected; Stylos has stronger results |
| StyleShot (Qy3UwW4OJ9) | 5.50 | 2 | Similar modest novelty, rejected; Stylos has comparable contribution level |
| Geo-3DGS (c4Nh4A8Xn5) | 5.00 | 1 | Incremental 3DGS contribution, rejected; Stylos has a more distinctive end-task and stronger results |

**Final score: 5.5.** The paper demonstrates a practically useful system with strong empirical results that convincingly outperform the only comparable feed-forward method. However, the technical novelty over inherited backbones is modest, the headline 3D style loss provides marginal quantitative improvement, and a significant presentation error in the core experimental section (attributing the method's own results to a baseline) undermines confidence. The paper is on the borderline and would benefit from thorough revision.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>