Now I'll write the final review.

## Summary

ARSS is the first decoder-only autoregressive model for novel view synthesis (NVS) from a single image with camera trajectory control. It combines a video tokenizer (VidTok) for temporally consistent visual tokens, a camera autoencoder that maps Plücker raymaps to 3D positional tokens, and a spatial-only token permutation strategy that preserves temporal causality while enabling bi-directional spatial context. On RealEstate10K and ACID, ARSS achieves best PSNR and LPIPS among compared methods, and shows slower error accumulation over long camera trajectories.

## Strengths

1. **First AR model for NVS with camera control.** The paper correctly identifies that the causal structure of AR models maps naturally onto sequential view generation, which diffusion models handle less directly. The architecture in Figure 2 cleanly communicates the three-module design (video tokenizer, camera encoder, spatial permutation). This is a genuine and clearly stated novel contribution.

2. **Strong LPIPS gains on both in-domain datasets.** On Re10K, ARSS achieves LPIPS 0.269 vs. LVSM's 0.314 (~14% relative improvement) and SEVA's 0.349 (~23% improvement). On ACID, LPIPS 0.265 vs. SEVA's 0.326 (~19% improvement). These perceptual quality gains are meaningful and consistent across both datasets.

3. **Convincing ablations that support design choices.** Table 2 (token order) shows spatial-only permutation outperforms both raster and full-permutation strategies. Table 3 (tokenizer) shows a dramatic 62% FVD improvement over VQ image tokenization, convincingly motivating the video tokenizer choice. The ablations are self-consistent and the visual results in Figure 7 corroborate the quantitative findings.

4. **Error accumulation analysis (Figure 6).** Per-frame metrics along the trajectory show ARSS degrades more slowly than baselines, directly supporting the paper's core motivation about causal generation being advantageous for long camera sweeps. This is a clean experiment that goes beyond aggregate metrics.

## Weaknesses

### Major

1. **Unexplained metric discrepancy between main results and ablations.** The ablation "ours" numbers in Tables 2 and 3 (PSNR 19.22, SSIM 0.565, LPIPS 0.294, FID 60.11) differ substantially from the main results in Table 1 (PSNR 19.02, SSIM 0.624, LPIPS 0.269, FID 47.60). SSIM is ~9% worse, LPIPS ~9% worse, and FID ~26% worse in the ablation tables. Notably, PSNR moves in the *opposite* direction (higher in ablations), so this is not simply a matter of one run being better or worse overall. The paper provides no explanation — whether this reflects a different evaluation subset, a different model snapshot, different decoding parameters, or some other factor. Without this explanation, the ablation results cannot be reliably interpreted relative to the main results, which undermines quantitative trust in the paper's claims.

2. **Results are systematically overstated relative to actual metrics.** The introduction (line 88) and discussion (line 281) claim the method "out-performs" / "outperforms state-of-the-art methods," but the actual results are mixed. On Re10K: ARSS wins PSNR (+1.5% vs SEVA) and LPIPS (−23% vs SEVA) but loses on SSIM (−6.9% vs SEVA) and FID (+1.3% vs SEVA). On ACID: ARSS wins PSNR (+0.7%) and LPIPS (−18.7%) but loses notably on SSIM (−6.2%) and substantially on FID (+44% — 47.76 vs. 33.16). Section 4.2 partially acknowledges the trade-off ("minor geometric inconsistencies" for the Re10K case) but the broader narrative frames the results as an across-the-board win. The claims should be recalibrated to honestly characterize where ARSS wins (PSNR, LPIPS) and where it loses (SSIM, FID).

### Minor

3. **Parallel decoding is claimed but never evaluated.** Section 3.2.3 states spatial permutation "allows parallel decoding" and the system can "predict multiple tokens at one time," but no experiments report whether parallel decoding was used, how many tokens are decoded in parallel, or any speed/memory trade-offs. If this capability is not demonstrated, the claim should be removed or caveated.

4. **Unsubstantiated comparative claims about SEVA's resources.** The paper states (line 241) SEVA "benefits from large-scale, high-resolution training data and heavy computational resources, whereas our approach attains competitive performance without such requirements" and (line 281) that ARSS is "trained from scratch." No evidence is provided for SEVA's compute or data budget. Moreover, ARSS uses a pre-trained VidTok video tokenizer and a LlamaGen backbone, so "trained from scratch" overstates the extent of independent training.

5. **Inference decoding hyperparameters unspecified.** Section 4.1 describes inference only as "iteratively sample the target tokens" without specifying whether sampling is greedy, top-k, top-p, or the temperature — details needed for reproducibility of the reported results.

6. **Equation (7) notation is imprecise.** The cross-entropy loss in Eq. (7) does not clearly separate predictions from targets, unlike the well-formed Eq. (3). The intended objective is understandable from context but the formulation as written is incomplete.

### Trivial

7. **Typo in Eq. (5) description.** Line 153: "where $\mathbf{d}$ is the normalized camera ray direction, $\mathbf{d}$ is the momentum term" — the second $\mathbf{d}$ should be $\mathbf{m}$.

## Nice-to-Haves

- **Statistical significance or variance reporting.** Error bars would strengthen confidence in close comparisons (e.g., Re10K PSNR: 19.02 vs. 18.73). This is not standard practice in this field's NVS benchmarks, so its absence is not a weakness, but its inclusion would strengthen the paper.
- **Human evaluation.** Given the mixed quantitative trade-offs, a perceptual study could further establish whether the LPIPS advantage is borne out by human judgment.
- **Camera autoencoder loss weights** ($\lambda_1$–$\lambda_4$) and training details are not reported, hindering full reproducibility.

## Removed Points

- **"No comparison to Zero-1-to-3, MVDream, Consistent-1-to-3":** Removed per guidelines — I cannot verify the existence or relevance of these as missing baselines without external sources. The paper's baseline selection (SEVA, LVSM, Genwarp, MotionCtrl, ViewCrafter, RayZer) covers the relevant NVS comparison space.
- **"No discussion of temporal dimension during inference":** The paper specifies temporal compression (17 frames → 5 temporal tokens) and describes inference in Section 4.1. This is a clarification question, not a weakness.
- **"Qualitative images not visible":** Parser artifact; removed.
- **"44% worse FID on ACID is a significant distributional mismatch":** The FID gap on ACID is real but is already captured under Weakness 2 (overstated results). Keeping it as a separate point would be redundant.
- **"Strength about well-structured ablations":** Kept as Strength 3; the harsh critic correctly identified this.
- **"Strength about first AR model for NVS":** Kept as Strength 1.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the Table 1 / Table 2 metric discrepancy.** State explicitly whether the ablations use a different evaluation subset, model snapshot, or generation parameters. If the numbers come from the same evaluation protocol, explain why they differ.
2. **Recalibrate claims.** Replace "outperforms state-of-the-art" with a precise characterization of where ARSS wins (PSNR, LPIPS, slower error accumulation) and where it loses (SSIM, FID). Presenting the results as a trade-off would be more honest and scientifically interesting.
3. **Either evaluate parallel decoding** with speed/memory benchmarks, or remove the claim.
4. **Remove or substantiate** the data/compute comparison with SEVA by citing published resource usage.
5. **Specify decoding hyperparameters** (sampling strategy, temperature, top-k/top-p values) in the implementation details.

## Score and Decision

**Calibration anchors used:**

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| AR-1-to-3 | pOcGFvfgjS.md | 5.00 (Reject) | R1, R2 | Closest match: autoregressive NVS from single image. ARSS is stronger (real-world datasets, more thorough evaluation) but weaker on claim accuracy and has the metric discrepancy. |
| Ctrl123 | CFOQd4tqn1.md | 4.00 (Reject) | R1 | Diffusion-based NVS, rejected. ARSS has more novel contribution. |
| SAR (Set AR) | b9dBNNeDd3.md | 4.60 (Reject) | R1 | Visual AR modeling paper. ARSS has more applied contribution but less theoretical depth. |
| FreeVS | dTGH9vUVdf.md | 5.80 (Accept) | R1 | Generative NVS, accepted. Similar-level contribution to ARSS but cleaner evaluation (no metric discrepancy). |
| Zero-shot NVS via Video Diffusion | zDJf7fvdid.md | 6.00 (Accept) | R2 | Training-free NVS, accepted. Stronger evaluation than ARSS. |
| 3D-free meets 3D priors | VLuJL8cnGk.md | 5.00 (Reject) | R2 | NVS from single image, rejected. Similar mixed results but less novelty. |
| GST (Where Am I) | NuHYh4YKNe.md | 6.25 (Accept) | R2 | AR model for spatial tasks. More comprehensive evaluation and clear contributions. |
| LVSM | QQBPWtvtcn.md | 7.67 (Accept) | R1 | Transformer NVS baseline cited in paper. Significantly stronger results and cleaner evaluation. |

**Bracket (Round 1):** Between 4.5 and 6.0 — above AR-1-to-3 and 3D-free NVS (both 5.00, rejected) but below FreeVS (5.80, accepted) and clean NVS papers.

**Narrowing (Round 2):** The most similar accepted paper (FreeVS, 5.80) has no metric discrepancy, suggesting the discrepancy is a real differentiator. AR-1-to-3 (5.00, rejected) is the closest rejected work but ARSS is stronger in evaluation breadth and novelty. 

**Final score:** 5.0 — The paper has genuine novelty as the first decoder-only AR model for NVS with camera control and demonstrates meaningful LPIPS gains. However, the unexplained metric discrepancy between main results and ablations undermines quantitative credibility, and the claims are systematically overstated relative to the mixed results. These issues are addressable in revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>