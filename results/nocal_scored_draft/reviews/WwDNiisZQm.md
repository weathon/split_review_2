Now I'll write the consolidated final review.

## Summary
This paper introduces Content-Aware Mamba (CAM) for learned image compression. It addresses two fundamental limitations of Mamba-style SSMs in this setting: (1) the content-agnostic fixed raster scan, which is replaced by a **Content-Adaptive Token Permutation** mechanism using codebook-based clustering to group semantically similar tokens regardless of spatial distance; and (2) the strict causality of SSM recurrence, which is mitigated by **Global-Prior Prompting** — injecting sample-specific global priors (derived from cluster centroids via a learned projection) into the SSM output equation. Built on these innovations, the CMiC model achieves state-of-the-art BD-rate savings of -15.91%, -21.34%, and -17.58% against VTM-21.0 on Kodak, Tecnick, and CLIC, surpassing prior Mamba-based and Transformer-based LIC models while maintaining favorable complexity.

## Strengths
- **Well-motivated technical problem with precise diagnosis.** The paper identifies two specific, distinct shortcomings of Mamba for image compression — content-agnostic fixed scan order and strict causality — and ties both directly to the compression objective of eliminating semantic redundancy (Section 1). This is not a generic "Mamba is limited" critique but a targeted analysis of why its design is misaligned with compression requirements.
- **Clean and complementary technical solutions with ablated evidence.** Content-Adaptive Token Permutation (codebook-based clustering, Section 3.3) and Global-Prior Prompting (centroid-tied prompt dictionary, Section 3.4) address distinct limitations and are naturally complementary. The ablation study (Table 2) cleanly quantifies their individual contributions (~2% BD-rate from CTP, ~0.7–1.2% from GPP) and combined effect (2.7–3.6%), confirming the design hypothesis.
- **Strong empirical results across multiple benchmarks.** CMiC achieves BD-rate savings of -15.91%, -21.34%, and -17.58% against VTM-21.0 on Kodak, Tecnick, and CLIC respectively (Table 1), surpassing prior Mamba-based models (MambaVC, MambaIC) and a broad set of Transformer/CNN-based SOTA methods. RD curves (Figs. 4–6) show consistent dominance across the full bitrate range. Complexity metrics (params, FLOPs, latency, peak memory) are competitive.
- **ERF analysis that visually validates the claimed mechanism.** Per-layer ERF visualizations (Fig. 9) convincingly show that removing both CTP and GPP yields the narrow raster-scan band predicted by strict causality, and that each component progressively broadens and semantically aligns the receptive field. The per-image ERF visualizations (Fig. 8) further demonstrate content-adaptivity — high-influence regions align with semantic structures.
- **Honest reporting of limitations.** The paper explicitly notes that adding CAM to the entropy model yields negligible gains (Section 4.5) and that MS-SSIM comparison is omitted for MambaVC/MambaIC because they were optimized only for MSE (Section 4.3). This transparency strengthens credibility.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Training dataset under-specified.** The paper trains on "Flickr2W (Liu et al., 2020)" (Section 4.1) but does not state the dataset size (number of images/resolutions) or compare training data scale with that used by competing methods. Since training data size directly affects RD performance, this missing detail makes the SOTA claims harder to interpret and compare against. The authors should specify the exact dataset composition and acknowledge how it compares to competitors' training sets.
- **MS-SSIM BD-rate results under-documented.** The paper states "CMIC also delivers significant MS-SSIM improvements... It outperforms TCM-L and FTIC by -7.34% and -3.87% respectively" (Section 4.3), but these numbers are given as a single sentence without specifying the dataset, without a dedicated table comparable to Table 1, and the cited Fig. 6 is labeled as PSNR curves on Kodak. For a second primary evaluation metric, this level of documentation is insufficient.

### Trivial
- **Inconsistent model naming.** Table 1 (line 209) uses "MambaC" while the cited work is MambaIC (Zeng et al., 2025). Both "CMiC" and "CMIC" are used interchangeably throughout the paper (e.g., the abstract and Table 1 use "CMIC", while Section 1 contributions and some figures use "CMiC").

## Nice-to-Haves
- **Clarify what GPP can and cannot provide.** The SSM state update $h_i = \bar{A}h_{i-1} + \bar{B}x_i$ remains strictly causal; the prompt $P$ only modifies the output equation $O_i = (C+P)h_i + Dx_i$. While the ERF evidence (Fig. 9) convincingly shows GPP broadens the receptive field, a precise characterization of what information the prompt can and cannot convey would strengthen the paper. The paper's current language is appropriately qualified ("mitigates," "relaxes") but a reader might over-interpret "overcomes the sequential dependency" in the abstract.
- **Analysis of why CAM does not help the entropy model.** The paper notes this limitation (Section 4.5) without analysis of *why*. Understanding this could guide future improvements.
- **Confidence intervals for BD-rate results.** BD-rate is computed from 4–6 RD points; without variance estimates, small differences between methods may not be statistically meaningful. This is a standard concern across virtually all LIC papers and is not specific to this work.
- **Per-image RD breakdown on Tecnick.** The gap between Tecnick (-21.34%) and Kodak (-15.91%) is attributed to high-resolution benefits; a breakdown by content type would strengthen this narrative.

## Removed Points
These points are flagged to be removed, treat them with caution:
- "Mitigating strict causality" clarification: The reviewer questioned precision of language. However, the paper provides strong ERF evidence (Fig. 9) that GPP broadens the receptive field beyond the causal boundary — the functional claim is well-supported. The paper's language ("mitigates," "relaxes") is appropriately qualified.
- MambaVC peak memory question (14.73 GB in Table 1): This concerns another method's implementation details, not the paper's own numbers.
- Confidence intervals request: Demoted to nice-to-have; not standard practice in LIC literature.
- Centroid initialization fragility (first batch representativeness): Speculative concern; no evidence this is a practical issue.
- Per-image RD analysis on Tecnick: Demoted to nice-to-have; beyond the paper's demonstrated scope.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Include the Flickr2W dataset size and compare training data scales with competitor methods.
- Add a dedicated MS-SSIM BD-rate table comparable to Table 1, specifying the dataset(s) and covering all competing methods.
- Standardize model naming to either CMiC or CMIC throughout; correct "MambaC" to "MambaIC" in Table 1.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>