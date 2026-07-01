## Summary

This paper presents EmbodiedMAE, a multi-modal masked autoencoder that simultaneously learns representations across RGB, depth, and point cloud modalities for robot manipulation. The authors introduce DROID-3D, a processed version of the DROID dataset with temporally consistent metric depth and point clouds from ZED SDK temporal fusion. They evaluate across 70 simulation tasks (LIBERO + MetaWorld) and 20 real-world tasks on two robot platforms (SO100 and xArm), comparing against several vision foundation models including DINOv2, SigLIP, SPA, R3M, and VC-1.

## Strengths

1. **DROID-3D dataset (Section 2.1).** Processing the full 76K trajectories of DROID with ZED SDK temporal fusion (~500 hours of processing) to obtain temporally consistent metric depth and point clouds is a substantial engineering effort. This fills a genuine gap: existing large-scale robot datasets either lack 3D information or use low-quality estimated depth. The resource has standalone value for the community.

2. **Comprehensive evaluation scope (Sections 3.3–3.4).** The evaluation spans 70 simulation tasks (LIBERO + MetaWorld) and 20 real-world tasks on two distinct robot platforms (SO100 and xArm), with multiple input modalities (RGB, RGBD, PC). This breadth substantially exceeds most VFM-for-robotics papers, and the inclusion of both a low-cost open-source platform and a high-performance arm is well-motivated.

3. **Cross-modal prediction diagnostics (Figure 3, Section 3.2).** The re-coloring experiment — where an altered RGB patch during depth-to-RGB prediction propagates only to the semantically correct object — provides compelling qualitative evidence that the model has learned object-level understanding beyond pixel-level reconstruction.

## Weaknesses

### Fatal
None.

### Major

1. **Claim-evidence mismatch in the RGB-only setting.** The abstract and Finding 1 (Section 3.3) state that EmbodiedMAE "consistently outperforms all baseline VFMs." However, on MetaWorld (Table 1), the RGB-only EmbodiedMAE (73.0) ties with SPA RGB (73.0) on the average success rate, and on Medium-difficulty tasks SPA RGB (62.8) exceeds EmbodiedMAE RGB (60.4). The paper defaults to the RGB-only variant ("Unless otherwise specified, 'EmbodiedMAE' refers to the Large-scale, RGB-only variant," Section 3.3). The claiming of "consistent outperformance" is not supported by the paper's own data in this setting. The multi-modal variants show clear advantages, but the RGB-only claim needs qualification.

### Minor

2. **LIBERO main results are presented only as learning curves, not as a final numerical table.** MetaWorld has a full success rate table (Table 1), but LIBERO — where the strongest comparative claims are made (Figure 6 caption: "Our model surpasses all baselines") — is presented exclusively through learning curves. Precise numerical comparison requires extracting values from the plots. A tabular summary of final convergence values would bring LIBERO evidence to the same standard as MetaWorld.

3. **No variance or statistical significance information.** No standard deviations, confidence intervals, or multi-seed results are reported. For the real-world experiments evaluated on only 10 trials per task, a single trial shifts the success rate by 10 percentage points. In the MetaWorld results, where EmbodiedMAE RGB and SPA RGB differ by fractions of a percent on average, variance estimates would clarify which differences are reliable. While single-run evaluation is common in large-scale robot learning benchmarks, the absence of any variance information weakens evidential strength, particularly for the real-world 10-trial experiments.

4. **Novelty relative to MultiMAE is not clearly articulated.** The Dirichlet-based stochastic masking and the multi-modal MAE architecture are adopted from MultiMAE (Bachmann et al., 2022), as cited in Section 2.2. The paper's extensions — point clouds as a third modality with a learned tokenizer, cross-attention in the decoder, pre-training on robot interaction data, and model distillation — are described but not explicitly framed as departures from MultiMAE. A direct comparison against a MultiMAE baseline retrained on DROID-3D is absent, making it difficult to attribute which design choices drive the reported gains.

5. **Key hyperparameters underspecified.** The Dirichlet concentration parameter α (Section 2.2), which controls the masking strategy the paper identifies as important, is never given a concrete numerical value. The point cloud tokenizer parameters N (number of groups) and K (nearest neighbors) are not specified. These are consequential for reproducibility, though they may appear in the (stripped) appendix.

### Trivial
None.

## Nice-to-Haves
- Reporting the Dirichlet α value and point cloud tokenization parameters (N, K) explicitly in the main text would aid reproducibility.
- Adding a brief discussion framing the architectural differences from MultiMAE (without necessarily retraining it) would clarify the technical contribution.
- Adding binomial confidence intervals for the 10-trial real-world experiments would strengthen the real-world evidence.

## Removed Points

These points were raised in the input review but are removed with justification:

- **"DINOv2 depth comparison is potentially unfair"**: The suggested comparison — a DINOv2 variant trained with the same multi-modal MAE objective — would essentially be re-implementing EmbodiedMAE with DINOv2 initialization. The paper's chosen baseline (DINOv2-RGBD with a trainable depth branch, Appendix A.3) is a reasonable and standard way to incorporate depth.
- **"Section 2.2 does not specify handling of heterogeneous patch counts"**: The paper clearly describes that tokens from different modalities are "masked, concatenated, and passed to the ViT encoder" with per-modality positional embeddings. The ViT handles variable-length sequences natively.
- **"ZED SDK proprietary nature should be acknowledged as a limitation"**: Using commercial SDKs for data processing is common practice. The paper transparently describes its data processing pipeline.
- **"EmbodiedMAE does not support language instruction"** (Section 5 criticism): The paper openly acknowledges this as a limitation and future direction. Criticizing an acknowledged limitation is redundant.
- **"Section 2.3 description of h_I, h_D, h_P vs h is confusing"**: After concatenation and encoding, per-modality representations can be extracted by their original positions in the sequence — this is standard for transformer architectures.
- **Formatting/style nitpicks and speculative criticisms** that could not be verified against the paper text.

## Novel Insights

The most informative observation from the cross-review analysis is that the paper's "consistent outperformance" claim rests on an asymmetry in evidence presentation: the MetaWorld results (where the claim is weakest, showing a tie with SPA in RGB) are presented in a clean numerical table, while the LIBERO results (where the advantage appears clearer) are presented only as learning curves without final numbers. This means a reader cannot verify the strongest claim as rigorously as the weaker one. The cross-modal re-coloring experiment (Figure 3, column 12) is a genuinely insightful diagnostic that goes beyond standard reconstruction visualizations and deserves emphasis.

## Suggestions

1. Qualify the comparative claims to reflect benchmark-dependent results: the RGB-only advantage is clearer on LIBERO than on MetaWorld (where it ties with SPA on average).
2. Add a numerical table of final LIBERO success rates (with task-level breakdown) to match the MetaWorld presentation standard.
3. Report the Dirichlet α value, N, and K explicitly.
4. Explicitly list the architectural differences from MultiMAE in a short paragraph or table to clarify the technical contribution.
5. Add confidence intervals or individual trial results for the 10-trial real-world experiments.

## Score and Decision

**Calibration Anchors (Round 1):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md | 1.00 | R1 | Unrelated topic (cross-lingual robotics), not comparable |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5lUdTogEL3.md | 1.00 | R1 | Unrelated topic (person re-ID), not comparable |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wl1Kup6oES.md | 3.00 | R1 | "From Appearance to Motion" — simple contrastive learning for manipulation, 3 sim environments only. Our paper has much broader evaluation, real-world validation, and dataset contribution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9GKMCecZ7c.md | 3.40 | R1 | "Building Generalist Robot Policy" — investigates PTMs for manipulation, simulation-only. Our paper adds real-world validation and DROID-3D. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FMsmo01TaI.md | 4.33 | R1 | "The Power of the Senses (M3L)" — closest methodological parallel (masked multimodal learning for manipulation), but limited to 3 simulation tasks with no real-world. Our paper's evaluation breadth and dataset contribution are significantly stronger. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XYdstv3ySl.md | 6.50 | R1 | "3D-Spatial Multimodal Memory (M3)" — multimodal memory for static scenes. Different focus, similar score band. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NtQqIcSbqv.md | 6.00 | R1 | "Learning to Jointly Understand Visual and Tactile" — multimodal learning, similar score band. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/yAzN4tz7oI.md | 7.00 | R1 | "RDT-1B" — large diffusion foundation model for bimanual manipulation. Stronger in scale but also has claim precision concerns. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7gUrYE50Rb.md | 8.00 | R1 | "EQA-MX" — embodied QA, higher quality but different sub-area. |

**Round 1 Bracket:** 5.5–7.0. The paper is substantially stronger than the 3.0–4.33 anchors (broader evaluation, real-world validation, dataset contribution) but less impactful than RDT-1B at 7.0.

**Final Score:** 6.0 — The paper makes solid contributions (DROID-3D dataset, broad evaluation, sound multi-modal MAE methodology) but the claim-evidence calibration gap (overclaiming "consistent outperformance" in the RGB-only setting) and presentation gaps (no variance information, LIBERO curves-only) prevent a higher score. None of the weaknesses are fatal; all are addressable in revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>