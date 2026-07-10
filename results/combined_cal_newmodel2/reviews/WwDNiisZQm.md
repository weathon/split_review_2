Now I have all the calibration data I need. Let me write the final consolidated review.

## Summary

This paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two key limitations of standard Mamba when applied to 2D images: (1) the fixed raster-scan order is content-agnostic and fails to group semantically related but spatially distant tokens, and (2) strict causality prevents tokens from accessing global context. The paper proposes Content-Adaptive Token Permutation (CTP), which uses codebook-based clustering to reorder tokens by feature similarity, and Global-Prior Prompting (GPP), which injects sample-specific global priors into the SSM state equation to relax causality. Built on a hybrid architecture combining window-attention (local) with CAM blocks (global), the CMIC model achieves SOTA BD-rate savings of 15.91%, 21.34%, and 17.58% on Kodak, Tecnick, and CLIC datasets against VTM-21.0, with competitive efficiency (69.11M params, 2.39 TFLOPs, 0.405s latency).

## Strengths

- **Well-motivated problem identification.** Section 1 clearly distinguishes Mamba's two specific failures for compression (rigid scan order, strict causality) and maps each directly to the proposed mechanisms (CTP, GPP). This is rarer and more specific than generic "Mamba doesn't work for images" critiques.

- **Clean, informative ablation study (Table 2).** The 2×2 factorial design (CTP alone / GPP alone / both) isolates each component's contribution: CTP adds ~2% BD-rate, GPP adds ~0.5–1.4%, together they add ~2.7–3.6%. The paper honestly reports these numbers without inflation.

- **Compelling ERF visualizations (Figures 7, 8, 9).** The per-layer ERF analysis in Figure 9 is the strongest evidence in the paper. The progression from narrow raster-stripe (baseline) → slightly broader (GPP alone) → semantically spread (CTP alone) → fully global (both) directly visualizes that the mechanisms work as claimed. This kind of diagnostic evidence is rare and valuable.

- **Competitive efficiency.** With 69.11M params, 2.39 TFLOPs, and 0.405s decode latency, the model achieves strong RD performance at moderate cost. The efficiency advantage over MambaIC (157M params, 5.56 TFLOPs, 0.669s) is substantial and attributable to the single-scan design.

- **Honest limitations acknowledged.** The paper notes that CAM blocks do not help in the entropy model (Appendix A.3.2), that clustering uses non-gradient EMA updates, and that throughput is measured under specific settings.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Framing overstates the isolated CAM contribution.** The abstract and introduction present the 15.91% BD-rate improvement as a headline figure without separating how much comes from the CAM innovations vs. the strong base architecture. Table 4 shows that the "Conv Block" baseline (without any CAM) already achieves −12.89% on Kodak, while CAM-only achieves −14.68% and the full hybrid (CAM + attention) achieves −15.91%. The CTP+GPP components contribute roughly 2–3 percentage points of the total gain; the remaining ~13% comes from conventional design choices (residual blocks, window attention, SCTX entropy model, channel widths). The paper should clearly state: "our base architecture (without CAM) achieves X% BD-rate savings; adding CTP and GPP yields an additional Y%." The ablation data is presented honestly in the tables, so this is a framing concern rather than a factual error, but it affects how readers interpret the contribution.

- **Baseline comparison protocol is underspecified.** Table 1 reports BD-rates for 15 competing methods without stating whether these numbers are taken from original papers or reproduced under matched conditions. Training data matters enormously in LIC — the paper trains on Flickr2W, but methods like MLIC++, FTIC, and TCM were originally trained on different datasets. This should be explicitly stated so readers can calibrate confidence.

- **Clustering is not directly optimized for compression.** The codebook centroids are updated via non-gradient EMA K-Means (Algorithm 1), not through the rate-distortion loss. The hard assignment/permutation therefore has no gradient signal from the compression objective. While the differentiable projection $\mathcal{A}$ applied to centroids (for the prompt dictionary) provides some downstream adaptation, the paper does not analyze whether the clustering objective (cosine-similarity grouping) aligns with the compression objective or whether this gap is meaningful. This is not a fatal flaw — VQ-VAE works under similar constraints — but it is a methodological gap worth analyzing.

### Trivial

- **Within-cluster token ordering not specified.** Section 3.3 states tokens are grouped by cluster membership (cluster 1, then cluster 2, etc.) but does not specify the ordering of tokens within each cluster. If it is the original raster order, the causality problem persists within each cluster (though mitigated by grouping). This minor detail affects reproducibility.

## Nice-to-Haves

- Replace attention blocks with CAM blocks to produce a pure-Mamba variant and compare BD-rate against the hybrid, to quantify how much of the SOTA result depends on the attention component.
- Compare learned (gradient-based) clustering vs. EMA-based clustering to test whether non-differentiable clustering is a meaningful bottleneck.
- Report statistical variance across multiple seeds for ablation numbers.
- Expand MS-SSIM evaluation beyond the one sentence currently provided.

## Removed Points

These points were flagged but removed for the following reasons:

- **"Hybrid nature vs. pure Mamba framing" (Harsh Critic Issue 4):** The paper transparently states in Section 3.2 that it uses "window-attention to capture fine-grained local dependencies, while our proposed CAM blocks are introduced to enhance long-range modeling." The title is about making Mamba content-aware, not building a pure-Mamba model. This is clearly scoped and not a genuine weakness.

- **"Centroids shared across all images" observation:** The paper explicitly states this in Section 3.3: "Each CAM block holds its own cluster centroids, which are shared across all images and are only updated in the training phase." This is already clearly described.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Re-center the narrative to clearly separate the base architecture's performance from the CAM-specific gains. Add a sentence in the abstract quantifying the isolated CTP+GPP improvement.
2. State how baseline numbers in Table 1 were obtained (original papers vs. reproduced).
3. Specify within-cluster token ordering in Section 3.3.
4. Add a discussion in Section 3.3 acknowledging and analyzing the misalignment between the clustering objective and the compression objective.

## Score and Decision

### Calibration Protocol

**Round 1 (Bracketing).** I retrieved anchor papers from six score bands using the query "learned image compression mamba state space model content adaptive." The most informative anchors were MambaVC (KgJwbsfN7G.md, avg 4.80, Reject), a Mamba-based LIC paper where all reviewers cited limited novelty and missing SOTA comparisons, and the Frequency-Aware Transformer (HKGQDDTuvZ.md, avg 6.00, Accept), a transformer-based LIC paper with comprehensive SOTA comparisons and solid ablations. The initial bracket was 5.5–7.5.

**Round 2 (Narrowing).** I searched within the 5.5–7.5 and 6.0–8.0 bands with more specific queries targeting Mamba-based and content-adaptive LIC papers. I itemized anchors including Spatial-Mamba (iDe1mtxqK5.md, avg 7.00, Accept) and the Idempotence paper (Cy5v64DqEF.md, avg 7.50, Accept). Comparing itemized favorability ratings: the current paper's strengths (6.37–12.58) are comparable to FAT's (5.01–13.96), while its weaknesses (3.09–4.77) are less severe than FAT's (some as low as −0.60). The paper is clearly stronger than MambaVC (4.80), which was penalized for simple VSS-block application without compression-specific design. However, the CAM contribution is more incremental (2–3% isolated BD-rate gain) than Spatial-Mamba's architecture-level improvement, placing it below Spatial-Mamba (7.00).

**All anchors retrieved:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| MambaVC | KgJwbsfN7G.md | 4.80 | R1 | Yes | Weaker: plain VSS-block application, missing SOTA comparisons |
| GroupMamba | RmmrHEH6Nx.md | 3.00 | R1 | No | Weaker: different domain (vision classification), rejected |
| Mamba-HMIL | 0yVP49SDg0.md | 3.25 | R1 | No | Weaker: different domain (WSI), rejected |
| Mamba Neural Op. | VtP7CamOR5.md | 3.00 | R1 | No | Weaker: different domain (PDEs), rejected |
| Multimodal Mamba | cagNCwQEEN.md | 3.40 | R1 | No | Weaker: different domain, rejected |
| Spatial-Mamba | iDe1mtxqK5.md | 7.00 | R1 | Yes | Stronger overall but different focus (architecture for vision, not compression) |
| Mamba (original) | AL1fq05o7H.md | 6.25 | R1 | No | Different: foundational SSM paper |
| MambaPEFT | UAKnJMIBwf.md | 6.00 | R1 | No | Different: fine-tuning Mamba, not compression |
| Autoreg. Mamba | PQpvhUrA1C.md | 5.75 | R2 | No | Different: pretraining strategy |
| FAT | HKGQDDTuvZ.md | 6.00 | R1,R2 | Yes | Comparable: LIC paper, similar strengths/weaknesses profile |
| Idempotence Comp. | Cy5v64DqEF.md | 7.50 | R2 | Yes | Different: theoretical perceptual compression, higher bar |

**Final placement.** The paper is most comparable to FAT (6.00), which also had SOTA LIC results, specific architectural innovations, and moderate weaknesses about ablation completeness and contribution attribution. The current paper surpasses FAT on ablation rigor (cleaner factorial design) and diagnostic evidence (ERF visualizations), but has a more modest isolated contribution magnitude (2–3% vs. FAT's frequency-aware modules that directly modify the attention mechanism). Below Spatial-Mamba (7.00), which introduced a more general architectural improvement validated across multiple vision tasks.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>