Now I have all the information needed. Let me write the final consolidated review.

## Summary
2-3 sentence summary of the paper's contribution.

The paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending existing STVG benchmarks from ~20 seconds to 1–5 minutes, and proposes ART-STVG — an autoregressive transformer that processes frames sequentially with selective spatial/temporal memory banks and a cascaded decoder design. The method outperforms existing all-at-once STVG methods on the extended long-video benchmarks by large margins while remaining competitive on short-form STVG.

## Strengths
- **Well-motivated problem formulation.** Existing STVG datasets (HCSTVG-v2: ~20s, VidSTG: ~35s) are far shorter than real-world video durations. The paper correctly identifies that the dominant all-at-once processing paradigm creates both a computational bottleneck and a modeling challenge for longer videos. This is a timely and underexplored direction.
- **Principled architectural response.** Processing frames sequentially avoids the O(T) memory growth of existing methods, and the streaming framing is naturally suited to long-video localization. The ablations confirm the value of this design: the autoregressive baseline without memory already outperforms existing methods at 3–5 minutes (Tab. 1c–e).
- **Thorough ablation study.** Tables 2–5 cleanly isolate the contributions of temporal memory selection (16.7→23.0 m.tIoU, a 6.3-point gain), spatial memory selection (21.3→23.0), the cascaded decoder (21.5→23.0), and the hyperparameter N_s. The temporal memory ablation is especially informative: using all memories *hurts* performance (16.7→9.6), while selective memory recovers and surpasses the baseline.
- **Clear results on long videos.** The method shows consistent and increasing gains over existing methods as video length grows (e.g., on 5-min videos: 15.0 m.tIoU vs. ≤8.1 for all baselines), making a compelling case for the autoregressive approach in this setting.

## Weaknesses

### Fatal
None.

### Major
- **The extended benchmark datasets are critically underspecified.** The paper creates five LF-STVG datasets (1–5 min) by extending HCSTVG-v2 validation videos from their original 20-second duration. However, it never explains how ground-truth spatio-temporal tube annotations were obtained for the extended portions. The paper states: "we manually review the extended videos to ensure their quality" — but manual review is not a description of annotation creation. Were new spatio-temporal tube annotations created for the full 1–5 minute duration? If so, what was the annotation protocol and inter-annotator agreement? If annotations exist only for the original 20-second window embedded within each longer video, how are metrics computed for frames outside that window? Every quantitative result in Table 1 depends on the answer, and the paper provides none. This is not a minor documentation gap — it affects whether the empirical claims are verifiable. The authors must clarify the annotation protocol and metric computation before the results can be properly evaluated.

### Minor
- **Loss formulation and some method details deferred to supplementary.** The loss function is entirely absent from the main paper (Sec. 3.5: "Due to limited space, please see our loss function in supplementary material"). The main paper should at minimum specify which losses are used for spatial (L1? GIoU?) and temporal (cross-entropy? focal?) predictions.
- **Inconsistent notations and metrics.** Table 2 and Table 3 column headers read "m.vIoT" instead of "m.vIoU" (a typo). Figure 2 caption references "m_Ap@1" and "m_Ap@5" metrics that do not appear in any table — this is either a figure caption inconsistency or an artifact, but it creates confusion.
- **Framing overstates novelty of memory mechanisms relative to the autoregressive architecture.** The paper positions memory banks and selection as the central contributions, but the baseline (autoregressive without memory) already outperforms existing methods on videos ≥3 minutes (Tab. 1c–e: 16.7 vs. TA-STVG's 13.9 m.tIoU). The memory components add meaningful gains on top, but the framing could more honestly attribute the largest single source of improvement to the autoregressive sequential processing itself.
- **No discussion of limitations or failure cases.** The conclusion (Sec. 5) is a standard summary with no reflection on limitations — e.g., the trade-off of being slower than parallel methods on short videos, falling behind TA-STVG on the original HCSTVG-v2 benchmark (59.2 vs. 60.4 m.tIoU, Tab. 7), or the simplicity of the cosine-similarity temporal boundary detection.

### Trivial
None.

## Nice-to-Haves
- **Fairer long-video baseline comparisons.** The main comparison (Tab. 1) evaluates existing methods on 1–5 min videos despite them being trained only on 20-second clips and designed for all-at-once processing. While Table 6 partially addresses this (training on 40-second videos), adapting existing methods via frame subsampling or sliding windows would strengthen the comparison.
- **Statistical significance.** No confidence intervals or error bars are reported. Given the near-zero vIoU@0.7 scores for existing methods at 4–5 minutes, some measure of variance would be valuable.
- **Qualitative prediction examples** beyond attention maps (Figs. 5, 6) would help build intuition for when the method works and fails on long videos.
- **Dataset release plan.** The paper promises code and model release but does not state whether the extended LF-STVG datasets and their annotation protocol will be released.

## Removed Points
- **Criticism about unfair comparison being "systematically unfair."** This is removed: the paper trains all methods on the *same* 20-second training data (stated explicitly in Sec. 4.1). The fact that existing methods fail on longer videos is the point the paper is making, not an artifact of unfair comparison. Table 6 further validates the advantage with matched 40-second training. The comparison is informative about the limitations of existing approaches when applied out-of-domain.
- **"Short-form results undercut general superiority claim."** The paper does not claim general superiority — it claims superiority on LF-STVG while being "competitive" on SF-STVG. The authors accurately describe the trade-off. This criticism misunderstands the paper's scope.
- **Criticism about missing related work / first-to-explore claim.** The paper's claim about being "first to explore LF-STVG" is a factual assertion about the problem formulation. As per instructions, I cannot verify or refute the existence of related work I don't have access to.
- **Formatting/style nitpicks and reproducibility complaints about missing appendix content.** These are parser artifacts or standard field practice.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Document the annotation protocol for the extended benchmarks** — this is the single most important improvement. Explain how ground-truth tubes were obtained for the full 1–5 minute duration, and how metrics are computed for frames outside the original 20-second window. Without this, the empirical core of the paper is unverifiable.
2. **Move the loss formulation into the main paper** (at least a brief specification).
3. **Fix the "m.vIoT" typo** in Tables 2 and 3, and resolve the discrepancy between Figure 2's caption metrics and those reported in tables.
4. **Add a limitations section** acknowledging the trade-offs of the autoregressive design (e.g., inference speed on short videos, the short-form performance gap with TA-STVG).

## Score and Decision

**Bracket (Round 1):** Based on calibration against similar papers — LVM-Net (avg 3.00, rejected, long-form video memory), AMViT (avg 4.60, rejected, memory for long-form video), Grounded Video Caption (avg 3.83, rejected, new task+dataset for grounded video), Motion-Grounded Video Reasoning (avg 5.00, rejected, new spatiotemporal grounding task), Language Repository (avg 5.50, rejected, long video understanding), TRACE (avg 6.75, accepted, temporal grounding with causal autoregressive modeling) — the reviewed paper sits between 3.5 and 5.5. It has a stronger architecture story and more thorough ablations than AMViT or LVM-Net, but its benchmark documentation gap is more severe than any single issue in those papers.

**Narrowing:** Comparing directly against the most structurally similar anchors: Motion-Grounded Video Reasoning (5.00, rejected) introduced a new task and dataset with proper annotation documentation, and the reviewed paper's work is comparable in scope but weaker on benchmark transparency. Grounded Video Caption (3.83, rejected) introduced a new task with a manual annotation protocol and was still rejected. The reviewed paper falls between these, closer to 4–4.5 given the strength of its architecture ablations but the seriousness of the documentation gap.

**Final calibrated score: 4.5**
**Decision: Reject**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>