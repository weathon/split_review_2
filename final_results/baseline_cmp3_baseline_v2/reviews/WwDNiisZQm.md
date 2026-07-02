## Summary

This paper introduces Content-Aware Mamba (CAM), a state-space model (SSM) designed for learned image compression that overcomes two key limitations of the standard Mamba: (1) its rigid, content-agnostic scanning order and (2) its strict causal processing. CAM addresses these via a content-adaptive token permutation mechanism that groups feature-similar tokens together in the scan sequence, and a global-prior prompting mechanism that injects sample-specific priors into the SSM to relax causality. Built on these components, the CMIC model achieves state-of-the-art rate-distortion performance, surpassing VTM-21.0 by 15.91%–21.34% BD-rate on standard benchmarks, while maintaining linear complexity and moderate computational overhead.

## Strengths

- **Novel and well-motivated approach to adapting Mamba for image compression.** The paper clearly identifies two fundamental misalignments between standard Mamba and the structure of images: content-agnostic scanning and strict causality. The proposed solutions—content-adaptive token permutation via codebook-based clustering and global-prior prompting—are both principled and directly address these issues.
- **Strong empirical results across multiple datasets.** CMIC consistently outperforms a wide range of competing methods, including both Transformer-based (FTIC, TCM-L) and Mamba-based (MambaVC, MambaIC) models, achieving BD-rate savings of 15.91% (Kodak), 21.34% (Tecnick), and 17.58% (CLIC) over VTM-21.0. The improvements are substantial and consistent across bitrates.
- **Comprehensive ablations and analysis.** The paper includes thorough ablation studies isolating the contributions of Content-Adaptive Token Permutation and Global-Prior Prompting, throughput analysis, comparisons with alternative architectural choices, and insightful ERF visualizations that clearly demonstrate how each component affects the receptive field and causality. The clustering visualization (Fig. 10) convincingly shows that the method groups semantically related tokens.
- **Favorable complexity-performance trade-off.** Compared to prior Mamba-based models (e.g., MambaIC), CMIC achieves better RD performance while using 56% fewer parameters, 57% fewer FLOPs, and 78% lower peak memory, largely because it avoids multi-directional scans. The overhead from the clustering and prompting modules is minimal (≈5% training time, ≈4% inference time), making the method practical.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- The paper does not explore the sensitivity of the codebook update (EMA decay λ, number of K-Means iterations T) in ablations. While the clustering stability is mentioned, a brief analysis of these hyperparameters would strengthen the reproducibility claim.
- The comparison of activation counts (Table 5) is interesting but the variance is high (90–121), suggesting that some images may activate very few clusters. The paper acknowledges content-adaptive behavior, but the impact of very sparse cluster assignment on the permutation and subsequent SSM modelling is not discussed.

### Trivial
- The paper uses both "CMiC" and "CMIC" inconsistently (e.g., Figure 1 caption vs. Table 1); this is purely a typesetting issue.
- The number of clusters K=64 is chosen without a clear justification for why it is the same across all blocks and all resolutions; a brief note on this design choice would be helpful.

## Nice-to-Haves
- An analysis of how the clustering behaviour changes across network stages (early vs. late layers) could further illustrate the hierarchical nature of the learned representations.
- A comparison with an alternative non-causal strategy such as bidirectional scanning (e.g., two-directional Mamba without extra computational blow-up) would help isolate the benefit of prompting over a simpler baseline.
- The code release will be valuable; ensuring it includes the entropy model details and clustering update logic will aid reproducibility.

## Novel Insights

Beyond the paper’s own contributions, the ERF visualizations (Figures 7–9) offer a compelling demonstration that content-adaptive token permutation and global-prior prompting jointly reshape the receptive field from a narrow, raster-constrained band into a broad, semantically aligned field. The observation that the number of activated clusters varies per image (Table 5) and that centroids learn semantically consistent patterns (e.g., one centroid responds to edges, another to red-textured regions) provides a qualitative understanding of how the model encodes content-specific redundancy structure—a perspective that goes beyond standard rate-distortion metrics.

## Suggestions
- Include a small ablation on the EMA decay λ and the number of K-Means iterations T to show robustness and guide practitioners.
- Discuss the scenario where an image activates very few clusters (e.g., ≤8 out of 64) and whether the permutation still provides benefit or the baseline Mamba-like scanning would suffice.
- Clarify the implementation of the prompt conditioning: is the prompt matrix P added to C element-wise before the matrix-vector product with h_i, or is it concatenated? The equation O_i = (C+P)h_i + D x_i should be accompanied by a note on the dimensionality alignment.

## Score and Decision
The paper presents a well-motivated, novel method with strong empirical results, thorough ablations, and clear visualizations. The contributions are significant and advance the state of the art in Mamba-based learned image compression. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>