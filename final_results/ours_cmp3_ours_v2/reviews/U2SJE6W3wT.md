## Summary

This paper proposes AdcVSR, a compressed diffusion model for real-world video super-resolution (Real-VSR). The approach combines (1) a "2D + 1D" architecture — a pruned 2D Stable Diffusion backbone augmented with lightweight 1D temporal convolutions — and (2) a dual-head, dual-discriminator adversarial distillation scheme that disentangles detail richness and temporal consistency into separate optimization objectives. The student model is distilled from the large 3D DiT teacher DOVE, achieving a 95% parameter reduction (10.55B → 0.57B) and an 8× speedup on inference while maintaining competitive video quality across multiple benchmarks.

## Strengths

1. **Novel dual-head adversarial distillation scheme.** The idea of decoupling detail and consistency discrimination into separate heads, each trained with carefully curated data types (temporally shuffled videos, static pseudo-videos from images, etc.; Eq. 4–5), is a genuine technical contribution that goes beyond standard adversarial training or the original ADC method. The five data types provide systematic, disentangled supervision signals for competing objectives.

2. **Substantial and well-verified efficiency gains.** The 95% parameter reduction (10.55B → 0.57B) and 8× speedup (4.42s → 0.55s) relative to the DOVE teacher are practically significant. Inference-time measurements are reported on the same hardware (H20 GPU), which is good practice.

3. **Well-motivated problem framing.** Section 3.1 clearly articulates the detail-consistency conflict in Real-VSR, citing prior empirical evidence, providing a coherent design rationale for the dual-head discriminator scheme.

4. **Ablations isolate each contribution.** Tables 2, 3, and 4 separately ablate the network architecture, the discriminator design, and the distillation setup, each testing a component the paper claims is novel, with results directionally supporting the design choices.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Quality-efficiency framing needs more precise calibration.** The paper claims AdcVSR "maintains competitive video quality" (abstract, Sec. 1), but on several no-reference perceptual metrics (MANIQA, CLIPIQA, MUSIQ, DOVER), Real-ISR methods PiSA-SR and HYPIR — which lack any temporal modeling — outperform AdcVSR on both UDM10 and VideoLQ (Table 1). On VideoLQ, for example, PiSA-SR achieves CLIPIQA 0.6199 vs. AdcVSR's 0.6024 and MUSIQ 67.31 vs. 64.55. The paper acknowledges this (line 187: "Real-ISR diffusion networks PiSA-SR, AdeSR, and HYPIR... are highly effective at removing degradations... result[ing] in high-quality outputs with strong scores on no-reference perceptual metrics"), but the overall framing ("competitive video quality") elides that adding temporal modeling incurs a measurable cost on per-frame perceptual quality. The claim would be more accurate if phrased as: "AdcVSR achieves the best temporal consistency among all compared methods while approaching the best per-frame quality on most metrics, with dramatically lower complexity."

2. **Main comparison table covers only 2 of 6 test datasets.** The paper lists six test datasets (Section 4.1): UDM10, SPMCS, YouHQ40 (synthetic) and RealVSR, MVSR4x, VideoLQ (real-world). Table 1 reports results only for UDM10 and VideoLQ; results on SPMCS, YouHQ40, RealVSR, and MVSR4x are deferred to the appendix (line 239), which is unavailable. Since the ablation studies use YouHQ40 (Table 3) and MVSR4x (Table 4), these results exist but are absent from the main comparison, limiting the reader's ability to assess consistency across all datasets.

3. **Limited sensitivity analysis for the "2D + 1D" architecture.** The paper's central architectural claim — that "a 2D diffusion backbone is capable of synthesizing details, and consistency can be maintained with several 1D temporal convolutions" (Section 3.2) — is supported by only one comparison (Table 2) on one dataset (UDM10) using two metrics (DISTS, E_warp*). There is no sensitivity analysis on the number of 1D conv layers (only kernel size 3 is mentioned), nor a comparison against alternative lightweight temporal mechanisms (e.g., small 3D convolutions, temporal attention with limited window). While the design choice is reasonable, the evidence that this specific configuration is optimal or sufficient is thin.

4. **Dual-head discriminator ablation uses only two metrics.** Table 3 compares discriminator variants on YouHQ40 using only CLIP-IQA and E_warp*. These are precisely the two aspects the discriminator targets, making the result somewhat self-confirming. A broader evaluation (including LPIPS, DISTS, or additional no-reference metrics) would confirm that the dual-head design does not introduce unexpected degradation on other quality axes.

5. **Naming inconsistency.** "AdeVSR" appears instead of "AdcVSR" in the Figure 3 caption and surrounding text (lines 185, 187, 189).

### Trivial
- Metrics are reported as point estimates without variance or confidence intervals. This is standard practice for this type of evaluation but worth noting.
- No discussion of limitations or failure cases (e.g., performance under large motion with kernel-3 1D convs).

## Nice-to-Haves
- A deeper analysis of E_warp*: since AdcVSR wins on this metric by a large margin but lags on some perceptual metrics, the paper could analyze whether low E_warp* might partially reflect temporal over-smoothing (e.g., by reporting E_warp* alongside a measure of temporal detail variance).
- Comparison against other lightweight temporal mechanisms (small 3D convs, temporal attention, recurrent propagation) at similar parameter counts.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- The critic's claim that AdcVSR ranks 4th on LPIPS (it ranks 3rd; the critic miscounted). The broader point about trailing the leaders on perceptual metrics stands, but the specific rank was wrong.
- Criticisms about missing appendix content: removed per hard rules (appendix stripped by parser, not absent from submission).
- Concerns about the DOVE teacher creating an asymmetric baseline comparison: inherent to distillation papers and not a meaningful weakness.
- Concerns about training data availability and model release: removed per hard rules (cited entities are assumed to exist).

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis largely recapitulates what the paper reports, with useful framing suggestions.

## Suggestions

1. Add a supplementary table in the main text with a subset of metrics across all six datasets (addresses Weakness 2).
2. Calibrate the quality claim to precisely describe where AdcVSR excels (temporal consistency) and where it trails (per-frame perceptual quality on no-reference metrics) (addresses Weakness 1).
3. Add sensitivity analysis for the 1D temporal convolutions (number of layers, kernel size alternatives) (addresses Weakness 3).
4. Expand the dual-head discriminator ablation (Table 3) to include additional metrics beyond the two targets (addresses Weakness 4).
5. Fix the "AdeVSR" → "AdcVSR" naming inconsistency (addresses Weakness 5).

## Score and Decision

**Calibration anchors used (all rounds):**

| Anchor | Avg Score | Decision | Comparison to current paper |
|--------|-----------|----------|---------------------------|
| AddSR | 5.00 | Reject | Adversarial distillation for blind SR. Current paper is stronger: more novel contribution (dual-head discriminator), harder problem (video), better-calibrated claims. |
| DFOSD | 4.75 | Reject | Distillation-free one-step diffusion ISR. Current paper is clearly stronger in novelty and scope. |
| Does Diffusion Beat GAN | 5.75 | Reject | Analysis paper with limited novelty. Current paper has stronger technical contribution. |
| Solving Diffusion ODEs | 6.67 | Accept | Theoretical contribution with limited practical gains. Current paper has stronger empirical contribution. |
| AugKD | 6.00 | Accept | Knowledge distillation for image SR. Comparable quality and contribution level. |
| Self-distillation for diffusion | 3.00 | Reject | Much weaker than current paper. |

**Round-1 bracket:** 4.5–7.0. The paper is substantially stronger than reject-range anchors (AddSR 5.0, DFOSD 4.75) due to clearer novelty and more thorough evaluation. It aligns with mid-range anchors (AugKD 6.0). It is weaker than top anchors (Shortcut Models 8.0) which present major architectural breakthroughs.

**Final calibrated score:** 6.0. The paper presents a genuine technical contribution (dual-head adversarial distillation with disentangled supervision), achieves impressive efficiency gains (95% parameter reduction, 8× speedup), and evaluates reasonably across multiple benchmarks. The weaknesses are real but addressable — primarily presentation issues (missing datasets in main table, quality claim calibration, limited ablation depth) rather than fundamental flaws. This is a borderline-accept paper that would be strengthened by addressing the concerns above.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>