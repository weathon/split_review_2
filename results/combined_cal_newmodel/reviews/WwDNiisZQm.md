Now let me organize everything into the final review.

## Summary

This paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two specific limitations of standard Mamba: (1) its content-agnostic, fixed raster-scan token ordering is misaligned with feature-space redundancy patterns, and (2) its strict causal recurrence mismatches the non-causal structure of images. The authors propose Content-Adaptive Token Permutation (CTP), which uses codebook-based clustering to reorder tokens by feature similarity, and Global-Prior Prompting (GPP), which injects sample-specific global priors into the SSM output projection. Their CMiC model achieves SOTA BD-rate savings (−15.91%, −21.34%, −17.58% vs. VTM-21.0 on Kodak, Tecnick, CLIC) while maintaining lower complexity than prior Mamba-based LIC models.

## Strengths

- **Well-motivated problem diagnosis (Section 1, lines 15–28).** The paper identifies two specific, distinct limitations of standard Mamba for image compression — the content-agnostic fixed scan order and the strict causal recurrence — with clear reasoning linking each to suboptimal redundancy removal. This is not a generic "Mamba is bad" claim but a targeted analysis that directly motivates the two proposed components.

- **Two clean, complementary innovations (Sections 3.3–3.4).** CTP addresses the scan-order problem via codebook-based clustering and sequence reordering; GPP addresses the causality problem by injecting sample-specific global priors into the SSM output projection. The ablation study (Table 2) confirms they contribute independently and additively: CTP alone gives 1.8–2.4% BD-rate improvement, GPP alone gives 0.5–1.4%, and together they give 2.7–3.6%.

- **Strong, consistent empirical results (Table 1, Figures 4–6).** CMiC achieves BD-rate savings of −15.91%, −21.34%, and −17.58% relative to VTM-21.0 on Kodak, Tecnick, and CLIC, respectively. It outperforms the strongest prior Mamba-based LIC model by 2.17–6.48% and surpasses strong Transformer-based models like FTIC and TCM-L. Results are reported across three standard datasets with clean RD curves showing consistent advantage across the full bitrate range.

- **Informative mechanistic evidence via ERF visualizations (Figures 7–9).** These go beyond "our model is better" to show *why* the method works. Figure 9 elegantly isolates the effects of CTP and GPP: without both, the ERF exhibits a strict raster-scan causal boundary; with GPP alone, the boundary is relaxed; with CTP alone, the ERF reorganizes along semantic boundaries; with both, it becomes global and content-adaptive.

- **Computational efficiency well-documented (Tables 1, 3).** Despite adding clustering and prompting modules, CMiC (69.11M params, 2.39 TFLOPs) is substantially lighter than MambaIC (157.09M params, 5.56 TFLOPs) with only modest throughput overhead (23.19 → 22.05 samples/s).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Causality claim is slightly overstated.** The abstract states that GPP "overcomes the sequential dependency" and the introduction frames it as "non-causal long-range modeling." However, GPP modifies only the output projection (O_i = (C+P)h_i + Dx_i), while the hidden state recurrence (h_i = Āh_{i-1} + B̄x_i) remains strictly causal. The ERF evidence clearly shows that GPP broadens the effective receptive field — this is a genuine and well-supported contribution — but the framing should be more precise about what is being relaxed (output conditioning via global priors) versus what remains unchanged (the causal state update). The paper's own description in Section 3.4 ("relaxing the strict causal constraint") is more accurate than the abstract's "overcomes."

2. **Baseline comparisons not controlled for training data.** The paper trains CMiC on Flickr2W and reports baseline results from their original papers without retraining on the same data. While this is common practice in the LIC literature, it is not acknowledged as a limitation. The large gap to some baselines (e.g., 7.51% vs. MambaVC on Kodak) could in part reflect training-set differences rather than purely architectural superiority. This does not invalidate the results, but the paper would be strengthened by acknowledging this or retraining the most competitive baselines.

### Trivial

1. **Naming inconsistency.** Table 1 and line 222 use "MambaC" while the text (lines 26, 240) and Figure 7 caption refer to the same model (Zeng et al., 2025) as "MambaIC." The paper should use a consistent name throughout.

## Nice-to-Haves

1. Add a dedicated MS-SSIM BD-rate table in the main paper. The MS-SSIM improvements are mentioned in prose (line 224: −7.34% vs. TCM-L, −3.87% vs. FTIC) but not tabulated, even though models are trained with MS-SSIM loss.
2. Report confidence intervals or standard deviations for BD-rate results, especially for comparisons where the gap is small (e.g., 2.36% over MambaIC on Kodak).
3. Show clustering visualizations from deeper CAM block stages (beyond Stage 2 of the analysis network) to strengthen the claim that centroids capture semantically meaningful patterns across the full architecture.
4. Discuss whether any training instability was observed from the non-gradient K-Means centroid updates (the paper references Appendix A.8–A.10 on stability, which is good) and note training-time overhead beyond the per-step 5% figure.

## Removed Points

- The harsh critic's "Critical Issue 2" about Table 2 formatting being garbled: this is a parser artifact, not a paper flaw. Removed per rule: pure formatting/parser issues.
- The harsh critic's "Section-by-section note" about checking K-means iterations on 2K images: the paper already states that inference requires no iterative updates (deterministic assignment), so this concern is addressed. Removed per rule: paper already addresses the concern.
- Harsh critic's speculation about the K-means non-gradient update creating a train-test mismatch: the paper references stability analysis in Appendix A.8–A.10, and the ERF/performance evidence confirms the mechanism works. Removed per rule: speculation without evidence of actual harm.
- Harsh critic's "Strengthening the Paper on Its Own Terms" points about cluster visualizations in deeper stages: moved to Nice-to-Haves above (minor suggestions, not core weaknesses).

## Novel Insights

The contrast between the paper's genuine contribution and its framing is instructive: GPP's real impact — broadening the effective receptive field via global output conditioning — is well-supported by the ERF evidence, and the mechanism is clearly described in Section 3.4. The framing imprecision in the abstract and introduction does not undermine the technical contribution; it simply calls for more precise language. The paper's primary novel insight is that content-adaptive token permutation (via clustering) and output-side global prompting are complementary and sufficient to overcome Mamba's structural limitations for image compression without multi-directional scans, which quadruple complexity.

## Suggestions

1. **Sharpen the causality claim.** Replace "overcomes the sequential dependency" and "non-causal long-range modeling" with more precise phrasing, e.g., "GPP relaxes the strict causality of the SSM output by conditioning each step on global priors, broadening the effective receptive field without modifying the causal state update."
2. **Fix naming inconsistency.** Use "MambaIC" consistently throughout the paper (or whichever name the authors intend for the model from Zeng et al., 2025).
3. **Acknowledge training-data limitation.** Add a sentence noting that baseline results are from original papers and may reflect different training setups.
4. **Add MS-SSIM table.** Tabulate MS-SSIM BD-rate results for completeness.

## Score and Decision

**Calibration Summary (all anchors retrieved):**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| MambaVC | KgJwbsfN7G | 4.80 | R1 | Yes | MambaVC applies VSS blocks to LIC with limited novelty; CMiC introduces architectural modifications (CTP, GPP) with stronger results and mechanistic analysis |
| Neural Cellular Automata Comp. | gIrVoQEDQv | 3.40 | R1 | No | Different approach (NCA-based lightweight compression); much lower performance bar |
| GroupMamba | RmmrHEH6Nx | 3.00 | R1 | No | General vision SSM with group scanning; not compression-specific |
| Spatial-Mamba | iDe1mtxqK5 | 7.00 | R1/R2 | Yes | Modifies Mamba with structure-aware state fusion for general vision; CMiC has comparable novelty with more task-specific validation |
| Frequency-Aware Transformer | HKGQDDTuvZ | 6.00 | R2 | Yes | LIC with frequency decomposition; CMiC has comparable results with stronger ablation and mechanistic evidence |
| Idempotence & Perceptual Comp. | Cy5v64DqEF | 7.50 | R2 | No | Theoretical contribution on perceptual compression; different contribution type |
| Mamba (original) | AL1fq05o7H | 6.25 | R1 | No | Foundational SSM method; not directly comparable |

**Round 1 bracket:** 5.5–7.5 (above MambaVC's 4.80, within range of Spatial-Mamba's 7.00 and below Idempotence's 7.50)

**Round 2 narrowing:** Direct comparison with Frequency-Aware Transformer (6.00) and Spatial-Mamba (7.00). CMiC's strongest weaknesses (favorability -1.54, -0.58) are substantially milder than MambaVC's (−2.77, −3.89, −3.43, −1.57) and comparable to Spatial-Mamba's (−1.73, 2.64). CMiC's strengths (11.08–12.89) are in the same range as Spatial-Mamba's (10.25–13.18) and Frequency-Aware Transformer's (10.66–12.70). The framing imprecision is the only real weakness, and it does not threaten any result. This places CMiC clearly above 6.00 and in the 6.5–7.0 range.

**Final score: 7.0** — The paper presents genuinely novel architectural innovations (CTP and GPP) for Mamba-based LIC, supported by strong empirical results, thorough ablation, and unusually informative mechanistic analysis (ERF visualizations). The weaknesses are minor and addressable.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>