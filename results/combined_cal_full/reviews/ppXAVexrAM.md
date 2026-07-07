## Summary

ARSS proposes the first decoder-only autoregressive (GPT-style) framework for novel view synthesis from a single image. The method uses three modules — a video tokenizer (VidTok with FSQ), a camera autoencoder that encodes Plücker ray maps into positional tokens, and an autoregressive transformer with a hybrid token permutation strategy (spatial shuffle, temporal fixed). The core thesis is that the causal AR formulation provides advantages over diffusion-based NVS for long camera trajectories, and this is supported by an informative error accumulation analysis (Figure 6).

## Strengths

- **First application of decoder-only AR models to NVS with camera control.** The paper correctly identifies that existing diffusion-based NVS methods generate views jointly, making causal/extensible generation awkward. Applying GPT-style causal transformers to this problem is a conceptually clean framing that the paper follows through on. (Section 1, Figure 2)
- **Error accumulation analysis (Figure 6) is a genuine strength.** Per-frame metrics show ARSS degrades more gracefully than all baselines along long trajectories, directly supporting the causal formulation's advantage. This is the paper's strongest piece of evidence.
- **Hybrid token permutation strategy is sensible and well-ablated.** Shuffling spatial tokens while maintaining temporal order is a principled solution to the mismatch between uni-directional causal transformers and bi-directional visual data. Table 2 shows clear improvements over both "raster" and "full perm." alternatives.
- **Clean, well-motivated three-module architecture.** Each module (video tokenizer, camera autoencoder, AR transformer) directly addresses a specific problem with naive AR generation for NVS, and each connects to a corresponding ablation.

## Weaknesses

### Major

- **Internal inconsistency between main results and ablations.** The "Ours" row in Tables 2 and 3 differs substantially from the Re10K "Ours" row in Table 1: SSIM 0.565 vs 0.624 (−9.4%), LPIPS 0.294 vs 0.269 (+9.3%), FID 60.11 vs 47.60 (+26%). The paper does not specify which dataset or split the ablations use. Without clarification, readers cannot determine whether ablation effects reflect genuine design improvements or data-split artifacts. This is the most concerning issue — it undermines confidence in the internal consistency of the reported numbers.

- **Overstated claims contradict the evidence.** The abstract accurately says "comparable," but the Introduction (line 88) and Discussion (line 281) claim the method "outperforms state-of-the-art methods." Table 1 shows a mixed picture: on Re10K, ARSS leads on PSNR (+0.29) and LPIPS (−0.080) but trails on SSIM (−0.046) and FID (−0.62). On ACID, SEVA's FID (33.16) is 31% better than ARSS's (47.76) — a large distributional-quality gap. The "outperforms" claim is not supported by the full set of results.

### Minor

- **No measures of variance.** No standard deviations, confidence intervals, or run-to-run variability are reported for any metric. Several key comparisons involve small margins (e.g., PSNR 19.02 vs 18.73 on Re10K) that could be within noise. This is especially problematic for FID and FVD, which have known high variance at moderate sample sizes. Without error bars, the paper's quantitative comparisons are not adequately supported.

- **Camera autoencoder pre-training lacks critical details.** The paper states the camera autoencoder is "pre-trained" (Section 3.2.2) but provides no information on the training data, number of iterations, batch size, or learning rate. Since the camera encoder is a claimed contribution, this gap hinders reproducibility.

- **Several baselines perform unusually poorly without explanation.** ViewCrafter (PSNR 12.67) and RayZer (PSNR 12.97) on Re10K are far below typical reported performance for these methods. The paper does not clarify whether numbers come from public checkpoints with recommended settings or from reimplementation, raising the question of whether these baselines were evaluated suboptimally.

- **Tokenizer ablation conflates two factors.** Table 3 compares VidTok (FSQ + video-level encoding) against a VQ image tokenizer (VQ + per-frame encoding), making it unclear whether the 62% FVD improvement comes from the FSQ quantization mechanism, the temporal encoding, or both. A controlled ablation separating these factors would be needed to attribute the gain.

### Trivial

- **Equation (5) definition error.** Both the ray direction and the momentum term are labeled "d" in the text — the second should be "m" (the paper defines m = o × d but then writes "**d** is the momentum term").

## Nice-to-Haves

- Evaluate 3D consistency with geometry-aware metrics (depth-map consistency, reprojection error) rather than only 2D metrics, to substantiate the claimed 3D awareness.
- Report inference wall-clock time or FLOPs vs. diffusion baselines to substantiate the practical advantage of incremental AR generation.
- Run a controlled tokenizer ablation that separates FSQ vs. VQ from video-level vs. per-frame encoding.

## Removed Points

These points were considered but removed for the reasons stated:

- "Camera token mechanism is unclear" — removed: Section 3.2.3 and Eq. 6/8 explain that camera tokens are interleaved as input conditioning (not predicted), and Figure 2 illustrates this.
- "Typo 'perpetual loss'" — removed per hard rule on typo/formatting criticisms.
- "No comparison against adapted AR image methods (LlamaGen, MAR, VAR)" — removed: the paper compares against relevant NVS baselines; adapting unrelated AR methods is beyond the paper's stated scope and standard practice.
- "Related work is thin" — removed: too generic to be actionable without a concrete anchor.
- Various generic area-of-concern sweep speculations from the harsh critic that lacked specific paper anchors.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's core strengths (first AR model for NVS, informative error accumulation analysis) and surface specific evidentiary issues (internal data inconsistency, overclaimed results) that the authors should address in revision.

## Suggestions

1. **Reconcile the ablation numbers with the main table.** Clearly state which dataset and split each table uses. If ablations use a validation split, provide the corresponding main-model performance on that same split so readers can perform a fair comparison.
2. **Calibrate the claims.** Replace "outperforms state-of-the-art" with phrasing that matches the evidence (e.g., "competitive with SEVA on pixel accuracy and perceptual quality, though trailing on structural similarity and distributional metrics").
3. **Add variance estimates.** Report standard deviations or confidence intervals for all metrics, especially FID and FVD.
4. **Provide camera autoencoder training details** (data, iterations, batch size, learning rate) in an appendix.
5. **Clarify baseline evaluation protocol** for ViewCrafter and RayZer — whether public checkpoints with recommended settings were used.
6. **Run a controlled tokenizer ablation** that separates FSQ vs. VQ from video-level vs. per-frame encoding.

## Score and Decision

**Calibration summary.** All anchors retrieved across rounds (R = round, I = itemized):

| Path | Avg Score | Round | Itemized? | Comparison to This Paper |
|------|-----------|-------|-----------|--------------------------|
| `u1cQYxRI1H.md` (IC-Light) | 0.50 | R1 | No | Unrelated topic; score is an outlier. |
| `Uj0h13lVrR.md` (GFN) | 1.00 | R1 | No | Unrelated topic. |
| `5lUdTogEL3.md` (L-ReID) | 1.00 | R1 | No | Unrelated topic. |
| `hrXt6Fdl2P.md` (FV-NeRV) | 2.60 | R1 | No | Different task (video compression). |
| `rWIrdAo2xC.md` (Human Gaussian) | 2.83 | R1 | No | Different task (3D human rendering). |
| `hWlCc7Iksi.md` (ARVideo) | 3.40 | R1 | Yes | AR for video SSL, but contribution judged incremental. My paper has clearer novelty but worse evidence quality (internal inconsistency). Slightly above this anchor. |
| `I86z54CL2y.md` (GeoGS3D) | 3.40 | R1 | No | Different task (3D reconstruction from single image). |
| `CFOQd4tqn1.md` (Ctrl123) | 4.00 | R1 | No | Similar NVS topic but diffusion-based. |
| **`pOcGFvfgjS.md` (AR-1-to-3)** | **5.00** | **R1** | **Yes** | **Closest anchor: AR for consistent multi-view generation. AR-1-to-3 had fair comparison concerns but internal consistency. My paper adds an internal data inconsistency that pushes it below this anchor.** |
| `VLuJL8cnGk.md` (3D-free NVS) | 5.00 | R1 | No | Diffusion-based NVS, different family. |
| `w6YS9A78fq.md` (Diff Transformer) | 5.00 | R1 | No | Broader topic (unified generation). |
| `zDJf7fvdid.md` (Zero-shot NVS) | 6.00 | R1 | No | Diffusion-based NVS, better execution. |
| **`NuHYh4YKNe.md` (Where Am I)** | **6.25** | **R1** | **Yes** | **AR for joint pose/view prediction. Better motivated, more thorough evaluation. My paper is notably weaker.** |
| **`BWuBDdXVnH.md` (ControlAR)** | **6.25** | **R1** | **Yes** | **Controllable AR image generation. Clean execution, good ablations. My paper is notably weaker.** |
| `dTGH9vUVdf.md` (FreeVS) | 5.80 | R1 | No | Driving-scene NVS, different domain. |
| **`QQBPWtvtcn.md` (LVSM)** | **7.67** | **R1** | **Yes** | **Strong NVS paper with minimal inductive bias. My paper is substantially weaker in execution depth.** |
| `P4o9akekdf.md` (NoPoSplat) | 8.00 | R1 | No | Strong 3D reconstruction paper. |
| `QQ6RgKYiQq.md` (MovingParts) | 8.00 | R1 | No | Dynamic scene reconstruction. |

**Round-1 bracket:** The weighted-item comparison places this paper between ARVideo (3.40) and AR-1-to-3 (5.00). Like AR-1-to-3 (5.00), my paper proposes an AR approach for multi-view generation with a similar novelty level. However, AR-1-to-3 had clean internal consistency; my paper's ablation-vs-main-table discrepancy (FID differs by 26%) is an additional credibility issue that AR-1-to-3 did not have. The shared heavy negative weight between my paper's "internal inconsistency" (−1.56) and AR-1-to-3's "unfair comparison" (−3.37) and "insufficient evaluation" (−3.96) are in similar territory, but the inconsistency issue is more fundamental because it undermines trust in all reported numbers. Meanwhile, my paper's strengths (+3.75 to +4.68) are comparable to AR-1-to-3's strongest strengths (+4.54 to +4.84). This anchors the final score below 5.00 but above 3.40, settling at **4.0**.

The final score reflects that the paper has a real and well-motivated contribution (first AR model for NVS) supported by an informative error accumulation analysis and clean ablation trends, but is held back by an unexplained internal data inconsistency that undermines trust in the quantitative results, coupled with overstated claims that exceed what the evidence supports.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>