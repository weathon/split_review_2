## Summary
# Final Review Report

## Summary

This paper introduces Content-Aware Mamba (CAM), a state-space model (SSM) designed for learned image compression that addresses two key limitations of standard Mamba: (1) content-agnostic raster scanning that fails to prioritize feature-similar tokens, and (2) strict causal recurrence misaligned with the non-causal nature of images. The authors propose two complementary mechanisms: **Content-Adaptive Token Permutation (CTP)**, which uses codebook-based cosine K-means clustering to reorder tokens by feature similarity before SSM processing, and **Global-Prior Prompting (GPP)**, which injects sample-specific global priors into the SSM output projection to relax strict causality. The resulting CMIC model achieves competitive rate-distortion performance, surpassing VTM-21.0 by 15.91%–21.34% BD-rate on standard benchmarks and outperforming prior Mamba-based LIC models (MambaVC, MambaIC) by clear margins.

**Overall assessment:** The paper presents a well-motivated technical approach that effectively identifies and addresses genuine limitations of Mamba for image compression. The codebook-based clustering with EMA updates is thoughtfully designed for training stability and inference efficiency. The ERF visualizations provide compelling qualitative evidence of improved global context modeling. However, several concerns limit the strength of the claims: (1) the reported BD-rate advantage over the strongest baselines (MLICv2, DCAE) is marginal and lacks statistical significance reporting, (2) the linear complexity claim needs more careful qualification given the clustering overhead, and (3) the conclusion omits limitations and failure-mode analysis. Novelty assessment is deferred to manual literature verification due to retrieval constraints in this run.

## Strengths
1. **Well-motivated problem identification.** The paper correctly identifies two genuine limitations of standard Mamba for 2D image compression: content-agnostic scanning and strict causality. This problem framing is clear, technically sound, and practically relevant, providing a strong foundation for the proposed solutions.

2. **Elegant technical design for clustering.** The codebook-based token clustering with EMA update (Section 3.3) is a practical improvement over naive online K-Means. By sharing centroids across images and updating via EMA, the approach achieves training stability, avoids per-sample iterative clustering at inference, and produces semantically meaningful groupings as evidenced by the cluster visualizations (Fig. 10). The design is well-adapted to the LIC setting.

3. **Complementary mechanism design.** CTP and GPP address different aspects of the Mamba limitation (scan rigidity vs. causal recurrence) and the ablation study (Table 2) confirms their complementary contributions, with combined gains (2.7%-3.6% BD-rate) exceeding the sum of individual gains in some settings.

4. **Strong qualitative evidence.** The ERF visualizations (Fig. 7-9) are among the most compelling aspects of the paper. The layer-wise ERF analysis (Fig. 9) cleanly isolates the effects of CTP and GPP, providing intuitive understanding of how each component extends the receptive field. The content-adaptive ERF patterns (Fig. 8) that align with semantic structures (hair, shoreline, aircraft) are visually convincing.

5. **Efficiency-conscious architecture.** The model achieves competitive BD-rate with 69.11M parameters and 2.39 TFLOPs, which is favorable compared to MambaIC (157.09M, 5.56 TFLOPs). The 5% throughput overhead from CTP/GPP (Table 3) is modest. The explicit inclusion of complexity metrics (params, FLOPs, latency, peak memory) in the main comparison table is a good practice.

6. **Comprehensive ablation study.** The paper systematically ablates CTP and GPP (Table 2), compares against alternative architectural choices (Conv, 2D Mamba, Attention-only, CAM-only in Table 4), and analyzes cluster number sensitivity (Table 6). This makes the contribution of each component transparent.

## Weaknesses
### W1. Insufficient statistical reliability evidence for SOTA claim (Major)
**Evidence:** Table 1 shows CMIC BD-rate of -15.91% on Kodak, while MLICv2 achieves -16.16% and DCAE achieves -15.40%. On Kodak (24 images), CMIC is effectively second-best with a margin of 0.25 percentage points behind MLICv2. On CLIC, the advantage over DCAE (-17.58% vs -16.46%) is 1.12 percentage points, and over MLICv2 (-15.79%) is 1.79 points. No variance, confidence intervals, or significance tests are reported.

**Impact:** BD-rate is a summary statistic computed from a rate-distortion curve fitted over multiple rate points. For small test sets (Kodak has 24 images), a few outlier images can shift BD-rate by 1-2 percentage points. Without bootstrap confidence intervals or multi-seed variance, the claimed "state-of-the-art" ranking is not statistically grounded, especially given the mixed ranking across datasets.

**Repair path (Must):** Report mean±std BD-rate over at least 3 training seeds for CMIC and top-3 baselines. Add 95% bootstrap confidence intervals for Kodak (24 images). Revise SOTA claim to acknowledge the mixed ranking: "CMIC achieves highly competitive RD performance, matching or surpassing prior methods across three datasets."

### W2. Missing clustering quality validation in high-dimensional space (Major)
**Evidence:** Section 3.3 uses cosine similarity for clustering in learned latent spaces with dimension d ≥ 128 (up to d=320 in later stages). The paper acknowledges only qualitative cluster visualization (Fig. 10, 3 images) but provides no quantitative clustering quality metrics (silhouette score, average cosine similarity to assigned centroid, cluster purity, assignment confidence distribution).

**Impact:** In high-dimensional spaces, cosine similarity distributions can become uniform, making hard argmax assignments noisy. If clustering is unreliable, the claimed benefit of content-adaptive token permutation is compromised. The paper's core contribution (C1) partially rests on the assumption that clustering produces semantically meaningful groupings.

**Repair path (Must):** Add quantitative clustering diagnostics: average cosine similarity between tokens and centroid, percentage of low-confidence assignments, and cluster size distribution, reported per network stage. Discuss whether dimension reduction or soft assignments would improve robustness.

### W3. Complexity analysis needs precision regarding clustering overhead (Moderate)
**Evidence:** The paper repeatedly claims "linear complexity" and "maintaining its linear complexity" (Abstract, Section 3.3). However, the clustering step adds O(N·K·d) operations per CAM block (N = tokens, K = 64 clusters, d = feature dimension). While O(N·K·d) is linear in N, the constant factor K·d = 64 × 128+ is non-trivial. The throughput drop from removing CTP/GPP (23.19 to 22.05 samples/s, ~5%) is modest, suggesting overhead is acceptable, but the analytical claim should be refined.

**Impact:** Readers expecting "linear complexity" in the SSM sense may be misled about the clustering cost, which is separate from the SSM's O(N·d_h) scan. This distinction matters for practitioners considering scaling to higher-resolution images.

**Repair path (Must):** Add a complexity breakdown: "The CAM block has two components: SSM scan with O(N·d_h) and clustering with O(N·K·d). In our configuration, clustering accounts for approximately 5% of total inference cost."

### W4. GPP novelty relative to MambaIRv2 needs clearer differentiation (Moderate)
**Evidence:** Section 3.4's prompt conditioning equation O_i = (C + P)h_i + Dx_i is nearly identical to the "Attentive State-Space" mechanism in MambaIRv2 (Guo et al., 2024a), which the paper cites. The claimed difference is that the prompt dictionary is "explicitly tied to redundancy-aware clustering centroids" rather than a standalone learnable matrix. However, the functional form of conditioning (additive modulation of C matrix) is the same, and the practical benefit of tying U to centroids (vs. learning it directly) is not empirically demonstrated.

**Impact:** The paper's contribution claim for GPP (C2) as a "novel" mechanism is weakened if the core operation reuses an existing mechanism with only a different input source. A control experiment comparing centroid-tied prompts vs. directly learned prompts would clarify the value of this design choice.

**Repair path (Must):** Add an ablation comparing (a) GPP with centroid-tied prompts vs. (b) GPP with a learnable prompt pool (as in MambaIRv2). Report BD-rate and prompt convergence speed.

### W5. No variance reporting in main experiments (Moderate)
**Evidence:** Section 4.1 reports training details (Flickr2W dataset, Adam, initial LR 10^{-4}) but provides no information about training seed variation, validation split, early stopping criteria, or training convergence diagnostics. Table 1 reports only point estimates.

**Impact:** Without multi-seed experiments, the community cannot assess the stability of the reported BD-rate numbers. LIC models can be sensitive to initialization and training dynamics, especially with clustering components that involve discrete assignments.

**Repair path (Must):** Add multi-seed results (3 seeds) for all main experiments. Report mean and standard deviation for BD-rate. State the random seed used for the primary results.

### W6. Conclusion lacks limitations discussion (Moderate)
**Evidence:** The conclusion (Section 5) only recaps contributions and re-asserts SOTA performance. It does not mention: (a) the entropy model limitation noted in Section 4.5 ("adding CAM yields negligible performance gains while increasing latency"), (b) scenarios where clustering may produce poor assignments, (c) the small-margin advantage over MLICv2/DCAE on Kodak, or (d) the lack of validation on video or medical/remote-sensing data.

**Impact:** An unbalanced conclusion reduces scientific transparency and can mislead readers about the method's maturity and remaining challenges.

**Repair path (Must):** Add a limitations paragraph covering: CAM's ineffectiveness in entropy models, potential clustering failures on OOD images, and the scoped nature of the performance claims.

### W7. Minor writing and consistency issues (Minor)
- Inconsistent naming: "MambaIC" vs "MambaC" used interchangeably in text and Table 1.
- The SSM discretization equations (Eq. 1) do not specify that A is diagonal or structured, which is essential for numerical stability.
- The context variable φ in the rate equation is not formally defined before its first use.
- The "state-of-the-art" claim in the abstract is too strong given mixed ranking on Kodak.
- The causal challenge framing (Challenge 2) conflates scan-direction causality with fundamental SSM recurrence.
- Training dataset Flickr2W is cited as Liu et al. (2020) but many readers may be unfamiliar with this dataset; brief description of size and diversity would help.

## Score
**Final Score: 6.5/10**

**Rationale:** The paper addresses a well-motivated problem with an elegant technical design (codebook-based clustering + global prompting for Mamba-based LIC). The qualitative evidence (ERF visualization, cluster inspection) is compelling, and the ablation study is thorough. The core ideas (CTP, GPP) are clearly presented and show measurable improvement over the vanilla Mamba baseline (2.7-3.6% BD-rate gain).

However, the score is constrained by the following factors:
- **Research value/novelty (primary dimension):** The CTP mechanism is a practical engineering contribution rather than a fundamentally new modeling paradigm. The GPP mechanism closely follows MambaIRv2's attentive state-space formulation with a different prompt source. Novelty assessment is deferred for manual verification due to retrieval constraints.
- **Validity concerns:** The lack of statistical significance reporting (no variance, no confidence intervals) weakens the core performance claim. The claimed "state-of-the-art" is not consistently supported across datasets (CMIC ranks second on Kodak behind MLICv2).
- **Evidence gaps:** Clustering quality is only qualitatively validated; the complexity analysis needs refinement; the conclusion omits limitations.

The paper has clear strengths and the technical approach is publishable after addressing the identified weaknesses, particularly W1 (statistical evidence), W2 (clustering validation), and W4 (GPP novelty differentiation). The architectural insights about content-adaptive scanning for Mamba are valuable for the LIC community.

**Novelty & Retrieval Note:** External literature verification could not be conducted in this run due to API token unavailability. The novelty verdicts for C1 (CTP), C2 (GPP), and C3 (CMIC model) are marked as **deferred manual verification**. The paper's own comparison against MambaVC and MambaIC suggests meaningful improvement over prior Mamba-based LIC, but how the proposed method compares against the full spectrum of efficient transformer and SSM-based approaches requires comprehensive literature review.