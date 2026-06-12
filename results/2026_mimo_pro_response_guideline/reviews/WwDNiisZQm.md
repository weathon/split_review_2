Now I have enough data to finalize. Let me compile the full review.

## Summary
This paper introduces Content-Aware Mamba (CAM) for learned image compression (LIC), proposing two mechanisms: (1) Content-Adaptive Token Permutation (CTP) that reorders tokens via codebook-based clustering so content-similar tokens are contiguous in the scan, and (2) Global-Prior Prompting (GPP) that injects sample-specific global priors into the SSM output projection. The resulting CMIC model achieves BD-rate reductions of 15.91%, 21.34%, and 17.58% over VTM-21.0 on Kodak, Tecnick, and CLIC, while being substantially more efficient than prior Mamba-based LIC models (56% fewer params, 78% less GPU memory than MambaIC).

## Strengths
- **Strong RD performance with favorable efficiency**: Table 1 shows CMIC outperforms all prior Mamba-based LIC by large margins (e.g., surpassing MambaC by 2.36–6.48% BD-rate) while using 69.11M params, 2.39 TFLOPs, and 4.44 GB peak memory — far more efficient than MambaIC (157.09M params, 5.56 TFLOPs, 20.32 GB). CMIC is competitive with the best Transformer-based methods (MLICv2, DCAE) at lower cost. Compared to TCM-L, CMIC reduces FLOPs by 36%, latency by 25%, and peak memory by 43% while delivering better BD-rate (Section 4.4).

- **Clean ablation study demonstrating component complementarity**: Table 2 isolates CTP and GPP contributions — CTP alone yields 2.0–2.4% BD-rate improvement, GPP alone 0.5–1.4%, and together 2.7–3.6% — showing additive/synergistic behavior. Table 4 validates the hybrid CAM+attention architecture against pure Conv, pure 2D-Mamba, pure attention, and pure CAM variants. Table 6 confirms K=64 is a sensible cluster count. These ablations are well-designed and convincing.

- **Compelling ERF visualizations providing direct mechanistic evidence**: Figure 9 systematically isolates each component's effect on a single Mamba layer: with neither component, the ERF stops at the scan center (confirming strict raster-scan causality); GPP alone introduces non-zero activations beyond the causal boundary in semantically meaningful regions; CTP alone replaces raster patterns with content-aligned activations. This directly validates both claimed contributions. Figures 7–8 further show CMIC has qualitatively larger, content-adaptive ERFs compared to prior methods.

- **Semantically meaningful, content-adaptive clustering**: Figure 10 shows cluster masks aligning with semantic structures (red doors, sky/clouds, feathers). Table 5 demonstrates only ~23–26 of 64 centroids are active per image with high variance (90.91 on Kodak), confirming the codebook adapts to content rather than using all clusters uniformly. Certain centroids specialize consistently (Section 4.5): Centroid #10 for high-gradient edges, #26 for red/yellow textured regions, #33 for smooth blue/green backgrounds.

- **Minimal computational overhead**: Table 3 shows training throughput decreases only ~5% (23.19 → 22.05 samples/s); Section 4.5 reports inference latency increases by just 4% (0.387s → 0.405s on 2K images). K-Means training overhead is only 5% of per-step training time.

## Weaknesses

### Fatal
None

### Major
None

### Minor

- **Imprecise framing of GPP as "relaxing causality"**: The paper repeatedly claims GPP "relaxes Mamba's strict causality" (Section 3.4, contributions list, Conclusion) and "overcomes the sequential dependency" (Abstract). However, the SSM state recurrence **h**_i = Ā**h**_{i-1} + B̄x_i remains strictly causal — each state depends only on predecessors. GPP works by augmenting the output matrix **C** with a prompt **P** derived from the full-image clustering, so **O**_i = (**C**+**P**)**h**_i + **D**x_i. This is better characterized as "conditioning a causal model on non-causal side information" than as "relaxing causality." The ERF visualizations (Fig. 9) convincingly show that GPP enables the output to respond to regions beyond the scan position, which is the real and valuable contribution — it does not need the overstatement. Precise language would strengthen the paper.

- **Unqualified "SOTA" claim on Kodak**: Table 1 shows MLICv2 achieves −16.16% BD-rate on Kodak versus CMIC's −15.91%, a 0.25% gap favoring MLICv2. The abstract claims "state-of-the-art rate-distortion performance" without qualification. CMIC does achieve best results on Tecnick (−21.34% vs. MLICv2's −20.13%) and CLIC (−17.58% vs. MLICv2's −15.79%), and has clear efficiency advantages (69M vs. 84M params). A brief acknowledgment that MLICv2 is marginally better on Kodak while CMIC leads on the other two datasets and is more efficient would make the SOTA claim more credible.

### Trivial
None

## Nice-to-Haves
- **Comparison with Zhang et al. (2024b)**: The related work discusses this CNN-based clustering-rearrangement approach for LIC (Section 2.1, 2.3) and notes that the appendix provides clustering comparisons (Appendix A.2), but it does not appear in Table 1. Since the architectural base differs (CNN vs. Mamba), this is not a critical gap, but a brief note or direct comparison would complete the picture.
- **EMA decay λ value in main text**: Algorithm 1 specifies λ as a required parameter but Section 4.1 does not state the chosen value. Including it in the experimental setup would aid reproducibility.

## Removed Points
These points are flagged to be removed, treat them with caution.
- The harsh critic's concern about missing MS-SSIM comparison with MambaVC/MambaIC — the paper explicitly addresses this (they "are only optimized for MSE"), and it is a reasonable omission, not a gap.
- Any criticism about formatting artifacts, typos, or parser issues — these are parser errors, not paper problems.
- Strengths about "the problem is important" or "the area is active" — generic, not specific to this paper's contribution.

## Novel Insights
The paper's most interesting methodological contribution is the codebook-based clustering approach for Mamba token reordering — a practical, training-stable alternative to online K-Means that borrows from VQ-VAE. The VQ-VAE-inspired EMA update avoids instability from repeated centroid re-initialization, while producing deterministic assignments at inference. The ERF analysis (Fig. 9) that systematically isolates causal vs. non-causal components provides a novel and compelling diagnostic tool for understanding how global information enters a causal SSM; this methodological contribution to SSM analysis could be highlighted more prominently.

## Suggestions
- Reframe GPP language throughout (Abstract, Section 3.4, contributions list, Conclusion) to distinguish between "relaxing causality in the scan" (not what happens) and "injecting global information into a causal model" (what happens). The ERF evidence already supports the latter characterization.
- Add one sentence acknowledging MLICv2's marginally better Kodak result while noting CMIC's overall efficiency and Tecnick/CLIC advantages.
- State the EMA decay λ value in Section 4.1 for reproducibility.

## Calibration Anchors Used

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| MambaVC | KgJwbsfN7G.md | 4.80 | 1 | Direct Mamba-LIC predecessor; rejected for low novelty and missing SOTA comparisons. CMIC is substantially more novel and better evaluated. |
| FAT (FTIC) | HKGQDDTuvZ.md | 6.00 | 1 | Transformer-based LIC with frequency-aware design; accepted with uniform 6s. CMIC has comparable or stronger novelty (two distinct mechanisms) and more comprehensive ablations/visualizations. |
| Spatial-Mamba | iDe1mtxqK5.md | 7.00 | 1/2 | Novel structure-aware state fusion for Mamba vision (8,8,6,6). CMIC is similarly innovative with domain-specific design and stronger experimental validation. |
| LTC | Tv36j85SqR.md | 7.20 | 2 | Novel lattice quantization for neural compression, approaching theoretical limits. Higher theoretical novelty; CMIC has stronger practical evaluation. |
| RECOMBINER | VkWbxFrCC8.md | 6.67 | 2 | Improved INR compression. CMIC has clearer novelty and stronger RD results. |
| UQDM | CxXGvKRDnL.md | 8.00 | 1 | Novel diffusion compression framework; stronger conceptual novelty. CMIC has more practical impact but less theoretical depth. |
| GroupMamba | RmmrHEH6Nx.md | 3.00 | 1 | Mamba vision with grouped scanning; rejected. CMIC is far more novel and better evaluated. |

**Round 1 bracket**: Between 6.0 and 7.5. CMIC clearly exceeds FAT (6.0, same domain) in novelty and experimental depth, and is comparable to Spatial-Mamba (7.0) and LTC (7.2) in the broader Mamba/compression space.

**Round 2 narrowing**: Confirmed 7.0 is appropriate — CMIC matches Spatial-Mamba's quality with stronger domain-specific contributions (ERF analysis, clustering visualization, efficiency story), while the minor causality framing issue and Kodak SOTA imprecision prevent a push to 7.5.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>