Good. Now I have a clear picture of the calibration landscape. Let me finalize my assessment.

**Round 1 bracket:** Between 5.0 and 6.5. ARSS is clearly above AR-1-to-3 (5.00, rejected) due to more comprehensive evaluation, stronger ablations, and better zero-shot results. It's comparable to or slightly above Zero-shot NVS via video diffusion (6.00, accepted) and Training-free Camera Control (5.80, accepted). It's well below LVSM (7.67, accepted) which had cleaner results.

**Round 2 narrowing:** The bracket narrows to 5.5–6.0. ARSS has more novelty than papers at 5.50 (CamI2V, AnyView) and stronger evaluation. The key question is whether the mixed in-domain results and presentation issues push it below the accept threshold.

Let me now write the final review with calibration anchors.

**All anchors retrieved:**
1. `/u1cQYxRI1H.md` — avg 0.50 (Round 1, <1.5) — IC-Light; unrelated illumination harmonization paper.
2. `/5lUdTogEL3.md` — avg 1.00 (Round 1, <1.5) — Lifelong ReID; unrelated.
3. `/nSDOkm0SKo.md` — avg 1.00 (Round 1, <1.5) — Financial markets; unrelated.
4. `/gwZ90hFSL2.md` — avg 1.00 (Round 1, <1.5) — Humanoid robots; unrelated.
5. `/rWIrdAo2xC.md` — avg 2.83 (Round 1, 1.5–3.5) — Monocular 3D human rendering; loosely related.
6. `/I86z54CL2y.md` — avg 3.40 (Round 1, 1.5–3.5) — GeoGS3D single-view 3D; related but weaker.
7. `/15lk4nBXYb.md` — avg 3.00 (Round 1, 1.5–3.5) — CCM-DiT camera control; related.
8. `/MI0UiWeqOl.md` — avg 2.33 (Round 1, 1.5–3.5) — Poly-AR modeling; loosely related.
9. `/pOcGFvfgjS.md` — avg 5.00 (Round 1&2, 3.5–5.5) — AR-1-to-3; **very relevant**, same AR + NVS paradigm, rejected at 5.00 with weaker evaluation.
10. `/VLuJL8cnGk.md` — avg 5.00 (Round 1, 3.5–5.5) — 3D-free meets 3D priors; NVS from single image.
11. `/OBTmkKBmQW.md` — avg 4.00 (Round 1, 3.5–5.5) — MotionFlow camera trajectory control.
12. `/j3rxIH0M9H.md` — avg 4.50 (Round 1, 3.5–5.5) — MOVIS multi-object NVS.
13. `/NuHYh4YKNe.md` — avg 6.25 (Round 1&2, 5.5–7.5) — AR spatial localization + view prediction; accepted.
14. `/zDJf7fvdid.md` — avg 6.00 (Round 1&2, 5.5–7.5) — Zero-shot NVS via video diffusion; accepted.
15. `/dTGH9vUVdf.md` — avg 5.80 (Round 1, 5.5–7.5) — FreeVS generative view synthesis.
16. `/KI1zldOFz9.md` — avg 5.80 (Round 1&2, 5.5–7.5) — Training-free camera control.
17. `/GuQeZWbaGr.md` — avg 5.50 (Round 2, 4.5–6.5) — AnyView personalized view transfer.
18. `/dIZB7jeSUv.md` — avg 5.50 (Round 2, 4.5–6.5) — CamI2V camera-controlled I2V.
19. `/QQBPWtvtcn.md` — avg 7.67 (Round 1, 7.5–8.5) — **LVSM, a baseline in the paper**; accepted.
20. `/P4o9akekdf.md` — avg 8.00 (Round 1, 7.5–8.5) — NoPoSplat; 3DGS from unposed images.
21. `/QQ6RgKYiQq.md` — avg 8.00 (Round 1, 7.5–8.5) — MovingParts dynamic NeRF.
22. `/rzF0R6GOd4.md` — avg 8.00 (Round 1, 7.5–8.5) — Neural SDF Flow.

**Calibration reasoning:** ARSS is clearly stronger than AR-1-to-3 (5.00, rejected) — it has three benchmarks, comprehensive ablations, error accumulation analysis, and a zero-shot evaluation. ARSS is comparable to Zero-shot NVS (6.00, accepted) and Training-free Camera Control (5.80, accepted) in novelty and evaluation quality. ARSS is below LVSM (7.67, accepted) due to mixed in-domain results and presentation issues. The genuine novelty (first AR for camera-controlled NVS), strong ablations, and impressive zero-shot DL3DV results push it above 5.5, but the misrepresented in-domain comparisons and omission of SEVA from error accumulation hold it below a confident accept. Score: **6.0**.

---

## Summary
ARSS proposes the first decoder-only causal autoregressive framework for camera-controlled novel view synthesis from a single image, combining a video tokenizer (VidTok with FSQ), a geometry-constrained camera autoencoder encoding Plücker raymaps, and an autoregressive transformer with a hybrid spatial-permutation strategy. The paper is evaluated on RealEstate10K, ACID, and zero-shot on DL3DV.

## Strengths
- **Genuinely novel paradigm**: ARSS is the first to apply causal AR models to camera-controlled NVS, filling a real gap in the literature. The three-component architecture (video tokenizer, camera autoencoder, permutation strategy) is coherently designed with each component addressing a clearly stated challenge.
- **Strong ablation studies**: Table 2 convincingly shows the hybrid spatial-permutation strategy outperforms both raster-scan (PSNR 16.29→19.22) and full spatio-temporal permutation (PSNR 18.76→19.22), with Figure 7 providing qualitative confirmation. Table 3 demonstrates video tokenization reduces FVD by ~62% over per-frame VQ tokenization (137.68→52.56), validating the temporal consistency motivation.
- **Impressive zero-shot DL3DV generalization**: On DL3DV (unseen during training), ARSS achieves best results across all five metrics (PSNR 16.70, SSIM 0.449, LPIPS 0.347, FID 84.96, FVD 91.25), outperforming MotionCtrl and LVSM. This is a strong evidence of generalization.
- **Principled camera autoencoder design**: The geometry-constrained loss (Eq. 5) with four Plücker coordinate regularizers (ray direction, momentum, unit-length normalization, orthogonality) goes beyond standard reconstruction losses and provides explicit 3D structural guidance.
- **Demonstrated slower error accumulation**: Figure 6 shows ARSS maintains the flattest quality degradation slopes across 16 frames among compared methods, supporting the motivation that AR models suit sequential view generation.

## Weaknesses

### Fatal
None.

### Major
- **Mixed in-domain results misrepresented through selective averaging**: On ACID, ARSS loses to SEVA on FID by ~44% (47.76 vs. 33.16) and on SSIM by ~6%. The paper (Section 4.2) averages the relative FID differences across Re10K (+1.3%) and ACID (+44%) to report "+22% FID," obscuring the massive ACID gap. FID measures distributional image quality, yet the paper labels this regression a "minor geometric inconsistency." Meanwhile, the abstract claims "comparable to SOTA" while the introduction (line 88) and discussion (line 281) claim "outperforms." This inconsistency between the actual results and how they are characterized undermines confidence in the paper's claims.
- **SEVA omitted from error accumulation analysis**: Figure 6, the paper's most distinctive evidence for the AR paradigm's advantage in long-horizon generation, compares ARSS only against LVSM, MotionCtrl, RayZer, and ViewCrafter—all substantially weaker overall (per Table 1). SEVA, the closest quantitative competitor, is absent. Without SEVA in this analysis, the claim of "consistently higher image quality and slower degradation" is unverified against the main rival.

### Minor
- **Genwarp listed as baseline but absent from Table 1**: Genwarp is introduced as a baseline in Section 4.1 (line 185) and appears in qualitative figures (Figures 3, 4), but is entirely missing from the quantitative comparison table without explanation.
- **Camera autoencoder pre-training procedure undescribed**: Section 3.2.2 describes the architecture and loss (Eq. 5), and line 72 mentions "We pre-train the camera autoencoder," but the pre-training procedure (data, loss components, optimization details) is never described.
- **AR capabilities motivated but not demonstrated**: The paper motivates AR models with the ability to "incrementally extend and reuse existing generations when the trajectory changes" (line 13) but never demonstrates this experimentally. Even a simple trajectory adaptation experiment would strongly support this motivation.
- **Training compute not controlled for SEVA comparison**: ARSS trains from scratch at 256×256 on 8 H100 GPUs for 100K iterations, while noting SEVA "benefits from large-scale, high-resolution training data." Without matched conditions, advantages on some metrics may reflect confounding factors rather than the AR paradigm itself.

### Trivial
None.

## Nice-to-Haves
- Include SEVA in Figure 6's error accumulation analysis.
- Demonstrate unique AR capabilities (trajectory adaptation, incremental extension).
- Report inference speed comparisons to strengthen the practical case for ARSS.
- Analyze why ARSS wins on pixel-aligned metrics (PSNR, LPIPS) but loses on distributional metrics (FID, SSIM) vs. SEVA.

## Removed Points
These points are flagged to be removed, treat them with caution:
- None of the harsh critic's weaknesses were removed as unreasonable — all were verified against the paper and found to be substantively correct.

## Novel Insights
The paper makes a genuine contribution by being the first to apply causal decoder-only AR models to camera-controlled novel view synthesis. The hybrid spatial-permutation strategy adapted from prior image generation work to the multi-view video setting is a well-validated design. The zero-shot DL3DV results suggest strong generalization potential. However, the most novel potential advantage of AR models—trajectory adaptation and incremental generation—remains undemonstrated, and the in-domain comparison with diffusion SOTA (SEVA) tells a more nuanced story than the paper presents.

## Suggestions
- **Highest leverage**: Include SEVA in Figure 6's error accumulation analysis. If ARSS genuinely degrades more gracefully than SEVA over long trajectories, that would be a decisive argument for the AR paradigm regardless of single-frame metrics.
- Honestly reconcile the mixed in-domain results: discuss why ARSS loses on FID/SSIM while winning on PSNR/LPIPS, rather than averaging away the gap.
- Resolve the "comparable" (abstract) vs. "outperforms" (introduction, discussion) inconsistency.
- Add Genwarp to Table 1 or explicitly explain its absence.
- Describe the camera autoencoder pre-training procedure for reproducibility.
- Consider a simple trajectory adaptation experiment to demonstrate unique AR capabilities.

## Score and Decision

**Calibration anchors (all retrieved across Rounds 1 & 2):**

| Anchor | Avg Score | Round | Relevance |
|--------|-----------|-------|-----------|
| `/pOcGFvfgjS.md` (AR-1-to-3) | 5.00 | 1&2 | Very relevant — same AR + NVS paradigm, weaker evaluation, rejected |
| `/VLuJL8cnGk.md` (3D-free meets 3D priors) | 5.00 | 1 | NVS from single image, rejected |
| `/GuQeZWbaGr.md` (AnyView) | 5.50 | 2 | Personalized view transfer, rejected |
| `/dIZB7jeSUv.md` (CamI2V) | 5.50 | 2 | Camera-controlled I2V, rejected |
| `/KI1zldOFz9.md` (Training-free Camera Control) | 5.80 | 1&2 | Camera control for video, accepted |
| `/dTGH9vUVdf.md` (FreeVS) | 5.80 | 1 | Generative view synthesis, accepted |
| `/zDJf7fvdid.md` (Zero-shot NVS) | 6.00 | 1&2 | Zero-shot NVS via video diffusion, accepted |
| `/NuHYh4YKNe.md` (Where Am I) | 6.25 | 1&2 | AR spatial localization + view prediction, accepted |
| `/QQBPWtvtcn.md` (LVSM) | 7.67 | 1 | **Baseline in this paper**, accepted |

**Bracketing:** Round 1 established a bracket of 5.0–6.5. ARSS is clearly above AR-1-to-3 (5.00) due to more comprehensive evaluation (3 benchmarks, ablations, error accumulation, zero-shot). Round 2 narrowed to 5.5–6.0, with ARSS comparable to Zero-shot NVS (6.00) and Training-free Camera Control (5.80).

**Final calibration:** ARSS's genuine novelty (first AR for camera-controlled NVS), strong ablations, and impressive zero-shot DL3DV results position it above rejected papers at 5.0–5.5. However, the misrepresented in-domain comparisons (averaging FID to hide a 44% ACID gap, labeling FID regression as "minor geometric inconsistency") and the omission of SEVA from the error accumulation analysis are substantive concerns that prevent a confident accept. The score lands at 6.0 — a borderline accept where the genuine paradigm contribution and zero-shot strength tip the balance, conditional on the authors addressing the presentation and evaluation gaps in a revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>