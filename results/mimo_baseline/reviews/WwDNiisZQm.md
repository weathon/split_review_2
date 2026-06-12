## Summary

This paper introduces Content-Aware Mamba (CAM), a state-space model variant for learned image compression that addresses two fundamental limitations of standard Mamba in the image domain: content-agnostic raster scanning and strict causality. The authors propose Content-Adaptive Token Permutation (codebook-based clustering to reorder tokens by feature similarity) and Global-Prior Prompting (injecting cluster-derived global priors into the SSM output). Built into the CMIC model, these techniques achieve state-of-the-art rate-distortion performance, surpassing VTM-21.0 by 15.91%, 21.34%, and 17.58% in BD-rate on Kodak, Tecnick, and CLIC datasets while maintaining moderate computational cost.

## Strengths

- **Well-motivated and clearly articulated problem.** The paper convincingly identifies two distinct limitations of applying Mamba to image compression—rigid content-agnostic scanning and strict causality—and proposes targeted solutions for each. The motivations are grounded in the specific structure of image redundancy rather than generic model improvements.
- **Strong and comprehensive experimental evaluation.** CMIC outperforms all compared methods across three standard benchmarks (Kodak, Tecnick, CLIC) and achieves BD-rate improvements over the nearest Mamba-based competitor (MambaIC/MambaC) of 2.17%–6.48% while reducing parameters by 56% and GPU memory by 78% (Table 1). The ablation studies (Table 2) cleanly isolate contributions: CTP alone gives 1.8%–2.4% BD-rate reduction, GPP adds 0.5%–1.4%, and they are complementary.
- **Excellent analytical visualizations.** The paper provides unusually thorough visual evidence: global ERF comparisons across nine models (Fig. 7–8), per-image content-adaptivity demonstrations (Fig. 8), single-layer non-causality analysis (Fig. 9) isolating CTP and GPP effects, and cluster visualization (Fig. 10) showing semantically meaningful groupings. These go well beyond typical ablation tables and provide genuine mechanistic insight.
- **Practical efficiency.** The codebook-based clustering uses EMA updates during training and deterministic assignment at inference, adding only ~5% training overhead and ~4% decoding latency increase (Table 3). The throughput is 22.05 samples/s on 256×256 patches, faster than all compared Mamba-based models (Table 3).

## Weaknesses

### Fatal
None.

### Major

- **The prompt conditioning mechanism is adapted from MambaIRv2 (Guo et al., 2024a).** The key equation $\mathbf{O}_i = (\mathbf{C} + \mathbf{P})\mathbf{h}_i + \mathbf{D}\mathbf{x}_i$ is directly borrowed from the Attentive State-Space equation. While the novelty lies in constructing P from clustering-derived centroids rather than a standalone learnable matrix (which is a meaningful difference tying the prompt to redundancy structure), the paper could more explicitly discuss the incremental nature of this adaptation and what specifically changes when prompts are semantically grounded vs. free-form.

- **No evaluation on perceptual/learned distortion metrics.** The model is optimized and evaluated only with PSNR and MS-SSIM. Given that modern LIC research increasingly evaluates with LPIPS, FID, or other perceptual metrics (and some competing methods may be optimized for these), this limits the completeness of the RD performance claims.

### Minor

- **Fixed K=64 across all blocks and stages.** The paper reports that only 16–32 centroids are typically activated per image (Table 5), suggesting the codebook is over-parameterized. While the paper shows K=64 works well (Table 6), a per-stage or adaptive K mechanism could be more efficient and may further improve performance. The current design choice is not deeply justified beyond "it works."

- **The entropy model contribution is minimal.** The paper honestly reports (Appendix, referenced in Section 4.5) that adding CAM to the entropy model yields "negligible performance gains while increasing latency." This is fine as honest reporting, but it slightly limits the claim that CAM is a general-purpose improvement for LIC—it appears most effective in the transform networks.

- **Comparison fairness with MambaIC/MambaC.** There is a naming inconsistency (MambaIC in text vs. MambaC in Table 1, likely "MambaIC" by Zeng et al. 2025). The BD-rate advantage over MambaIC is smaller (2.17%–6.48%) than over other methods, and the paper does not discuss whether architectural differences beyond the scanning mechanism account for some of the gap.

### Trivial
None.

## Nice-to-Haves
- Evaluation with perceptual distortion metrics (LPIPS, etc.) to complement PSNR/MS-SSIM analysis
- Analysis of how the clustering quality degrades or changes across training stages (early vs. late training)
- Discussion of sensitivity to the EMA decay parameter λ in the codebook update

## Novel Insights

The paper's most genuinely novel insight is that content-aware token reordering and semantically-grounded prompting are complementary mechanisms for adapting Mamba to 2D image compression—one addresses the scan path while the other addresses the causal information bottleneck. The single-layer ERF analysis in Figure 9 provides compelling visual evidence that GPP enables non-causal information flow (activations appear beyond the scan position) while CTP reshapes the receptive field toward semantically correlated regions. This decomposition of the two failure modes (wrong order, wrong direction) and their independent solutions is a clean conceptual contribution. The observation that each block's codebook naturally learns semantically consistent centroids shared across images (e.g., Centroid #10 for high-gradient edges, #26 for red/yellow textures) suggests the clustering captures meaningful visual primitives rather than arbitrary groupings.

## Suggestions
- Add LPIPS evaluation to provide a more complete picture of perceptual quality, which is increasingly standard in LIC benchmarks.
- Provide a clearer comparison table specifically isolating the scanning mechanism from other architectural differences when comparing against MambaIC, to better quantify the contribution of content-aware scanning alone.

## Score and Decision

This is a well-executed paper with clear problem motivation, two technically sound and complementary contributions, thorough ablations, and exceptionally strong visual analyses. The results are state-of-the-art across three benchmarks with meaningful efficiency improvements. The main limitation is that the prompting mechanism is adapted from prior work (MambaIRv2), and the clustering approach, while well-suited, draws from established VQ-VAE ideas. However, the specific combination and instantiation for Mamba-based compression is novel, and the experimental evidence strongly supports the claims.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>