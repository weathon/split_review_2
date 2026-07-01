## Summary

This paper proposes GenCoGS, a method that integrates two generative completion strategies — point cloud completion for Gaussian initialization (GCGI) and pseudo-view completion via an I2V diffusion model for Gaussian optimization (GCGO) — to address incomplete scene representation in 3DGS-based few-shot novel view synthesis. Experiments on LLFF, DTU, and Shiny datasets show consistent improvements over existing methods, with particularly strong gains on DTU (2.40 dB PSNR improvement over the second-best 3DGS-based method).

## Strengths

1. **Well-motivated two-pronged approach (Section 3).** The paper correctly identifies that 3DGS-based few-shot NVS suffers from incomplete scene representation in two distinct phases — initialization (sparse SfM point clouds miss unobserved regions) and optimization (pseudo views from training-view interpolation leave hollows). Addressing both with complementary strategies (GCGI for initialization, GCGO for optimization) is a coherent and well-justified design choice.

2. **Consistent quantitative improvement across all settings on LLFF (Table 1).** GenCoGS achieves higher PSNR, SSIM, LPIPS, and AVGE than all baselines at 3, 6, and 9 views. The improvements over the second-best method are modest (0.55–0.74 dB PSNR) but consistent across all four metrics and all three few-shot regimes, suggesting genuine method-level gains rather than a single favorable configuration.

3. **Strong result on DTU (Table 2).** GenCoGS achieves 23.11 PSNR on DTU 3-view, a 2.40 dB improvement over the second-best 3DGS-based method (BinoGS at 20.71) and 1.09 dB over the second-best overall (CAT3D at 22.02). This is a practically meaningful gap.

4. **Clear ablation structure (Table 4).** The ablation shows that both GCGI and GCGO individually improve over baseline (20.79 → 21.45 and 20.79 → 21.65 PSNR respectively) and their combination is additive (→ 22.13). Additional ablations (Tables 5–6) further isolate contributions of specific components, confirming the design rationale.

## Weaknesses

### Fatal
None.

### Major

1. **CPG module training regime is unspecified (methodological gap).** The CPG module (Section 3.1.1) is a learned component comprising a DGCNN backbone, Transformer encoder-decoder with dynamic queries, and a FoldingNet decoder. The paper provides zero information about: (a) what dataset(s) it was trained on, (b) what loss function was used, (c) whether it was pre-trained independently or trained jointly with the 3DGS optimization, and (d) training hyperparameters. The reference to Yu et al. 2021b (PCN) does not resolve this, because PCN is trained on synthetic 3D shape completion (ShapeNet) with ground-truth complete point clouds, whereas this task requires completing SfM point clouds of arbitrary real scenes without ground-truth 3D geometry. Since the CPG module is one of two core contributions, this omission prevents reproducibility assessment and raises questions about whether the reported GCGI gains depend on unstated favorable training conditions.

2. **Incomplete baseline comparison on Shiny dataset (evidential gap).** On LLFF and DTU (Tables 1–2), the paper compares GenCoGS against a broad set of baselines including BinoGS, CAT3D, IPSM, and ReconX. On Shiny (Table 3), the comparison is limited to RegNeRF, FreeNeRF, SparseNeRF, 3DGS, and FSGS — omitting all the stronger baselines that appear in the other tables. The paper claims "improvements of 1.47 dB in PSNR, 0.080 in SSIM, 0.125 in LPIPS" on Shiny over FSGS (19.63 PSNR). But BinoGS achieves 21.44 on LLFF 3-view and 20.71 on DTU 3-view, so it is plausible that BinoGS would score between FSGS's 19.63 and GenCoGS's 21.10 on Shiny. Without these comparisons, the claimed superiority on Shiny is not fully substantiated.

### Minor

3. **No variance or statistical significance reported.** All tables report single numbers. For improvements as small as +0.003 SSIM (LLFF 9-view) and +0.012 SSIM (LLFF 6-view), it is impossible to determine whether these differences are meaningful or within run-to-run noise. While single-run reporting is common in this field, the smallest improvements would benefit from multiple-seed variance reporting to establish reliability.

4. **I2V diffusion model integration underspecified.** Section 3.2 states that GCGO "leverages an image-to-video (I2V) diffusion model (Yu et al., 2024a)" but does not state whether this model is used off-the-shelf (frozen), fine-tuned on the target scene, or adapted in any way. The conditioning mechanism is described at a high level (CLIP embeddings + pseudo views), but the actual integration details matter for understanding computational cost and behavior. The reference to ViewCrafter provides context but does not clarify the specific choices made.

5. **Baseline value in ablation (Table 4) is unclear.** The "Baseline" in Table 4 is reported as 20.79 PSNR, while Table 1 gives FSGS as 20.31 PSNR on the same LLFF 3-view setting. If the baseline is a re-implemented version of FSGS, a different configuration, or a stripped-down version of the authors' pipeline, this should be explicitly stated to make the ablation interpretable.

### Trivial

6. **Abstract claims could contextualize which dataset each improvement comes from.** The abstract states "improvements of up to 2.40 dB, 0.08 and 0.125 in PSNR, SSIM and LPIPS" — the 2.40 dB and 0.08 SSIM are from DTU, the 0.125 LPIPS is from Shiny. On LLFF, SSIM improvements over second-best are 0.003–0.012, not 0.08. The phrasing could mislead readers about the magnitude of gains across all settings.

## Nice-to-Haves

- Report training time per scene and inference FPS, since adding an I2V diffusion model and a learned point cloud network likely increases computational cost substantially over vanilla 3DGS.
- Include a quantitative sensitivity analysis of the perturbation amplitude *A* in GCGO, rather than the single qualitative comparison in Figure 8.

## Removed Points

- **AVGE never defined** (from Harsh Critic #5): The paper states "Please refer to **Appendix for details on Datasets and Evaluation Metrics**." Since the parser strips appendices, the definition likely exists in the original submission. Removed per rule about missing appendix content.
- **Missing computation cost** (from Strengthening section): This is a nice-to-have, not a core weakness. Moved to Nice-to-Haves.
- **Missing related works**: Removed per rule — no external sources to confirm their existence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Specify the CPG module training protocol — dataset, loss function, whether it is pre-trained or jointly trained — and discuss the domain gap between synthetic shape completion and real SfM point clouds. This is the single highest-leverage improvement.
2. Add the missing baselines (BinoGS, CAT3D, IPSM) to the Shiny comparison, or explicitly state if these methods do not have published results on Shiny.
3. Report results with variance across multiple seeds, particularly for the smaller-margin improvements (e.g., LLFF SSIM).
4. Clarify whether the I2V diffusion model is used frozen or fine-tuned, and how many denoising steps are used.
5. Explain what the "Baseline" in Table 4 corresponds to relative to the methods listed in Table 1.

## Score and Decision

**Calibration anchors (all rounds):**

| Anchor | Path | Avg Human Score | Round | Comparison |
|--------|------|----------------|-------|------------|
| NoPoSplat | P4o9akekdf.md | 8.00 | R1 | Much stronger — clean, fully-specified contribution. GenCoGS not at this level. |
| LVSM | QQBPWtvtcn.md | 7.67 | R1 | Much stronger — clean transformer design, fully specified. |
| HiSplat | SBzIbJojs8.md | 6.00 | R1 | Cleaner hierarchical approach; accepted. GenCoGS has better results but a more serious methodological gap. |
| Ref-Gaussian | xPxHQHDH2u.md | 6.50 | R1 | Strong physically-based method. GenCoGS comparable in scope but weaker on specification. |
| RAIN-GS | R9lgWYE508.md | 5.75 | R1 | More incremental contribution but all components specified. GenCoGS has stronger results and more novel contribution. |
| Hi-Gaussian | L3WnnnBRdu.md | 5.75 | R1 | Rejected for pre-trained model reliance concerns. Comparable overall quality. |
| ZERO-1-to-G | nmc9ujrZ5R.md | 5.50 | R2 | Rejected for incremental combination of existing methods. GenCoGS has stronger novelty. |
| SCISplat | nkeF3iRJRo.md | 5.00 | R2 | Rejected for niche application. GenCoGS has broader significance. |

**Round 1 bracket:** 4.5–5.5. **Narrowing:** Compared to HiSplat (6.00, Accept), GenCoGS has a more significant methodological gap (unspecified CPG training). Compared to RAIN-GS (5.75, Reject) and Hi-Gaussian (5.75, Reject), GenCoGS has a more novel contribution but also a more significant reproducibility gap. The final score settles at **5.0**.

The paper proposes a well-motivated approach with encouraging results, but the unspecified training of the CPG module (one of two core contributions) and the incomplete Shiny comparison are significant weaknesses that prevent acceptance in the current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>