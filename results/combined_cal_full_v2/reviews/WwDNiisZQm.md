Now I have enough calibration data. Let me write the final consolidated review.

## Summary

This paper introduces Content-Aware Mamba (CAM), a state-space model that addresses two key limitations of standard Mamba for learned image compression: (1) the content-agnostic raster scan order, and (2) the strict causal chain. CAM overcomes these via content-adaptive token permutation (clustering tokens by feature similarity and reordering the scan sequence) and global-prior prompting (injecting sample-specific priors into the SSM output matrix to relax causality). The full model CMIC achieves competitive rate-distortion performance (best on 2 of 3 standard benchmarks) with substantial efficiency gains over prior Mamba-based LIC models — 56% fewer parameters, 57% fewer FLOPs, and 78% less peak memory versus MambaIC.

## Strengths

- **Well-motivated problem identification (Section 1).** The paper correctly identifies two genuine limitations of applying Mamba-style SSMs to image compression: the content-agnostic raster scan order and the strict causal chain. Both are fundamental to Mamba's 1D sequence design and misaligned with 2D image structure. The motivation is crisp and specific — not a generic "Mamba is imperfect" argument.

- **Clean, decisive ablation design (Table 2, Section 4.5).** The two proposed components (CTP and GPP) are ablated independently and in combination, bidirectionally (add to baseline and remove from full model). The numbers are clear: CTP contributes ~2.0–2.4% BD-rate reduction on its own, GPP contributes ~0.5–1.4%, and together they achieve 2.7–3.6%. This is more rigorous than most LIC ablation studies.

- **Informative ERF analysis (Figures 7–9).** The effective receptive field visualizations go beyond what is typically shown in LIC papers. Figure 9 is especially valuable: it isolates the per-layer ERF of a single SSM layer under four configurations, directly demonstrating how GPP breaks strict raster-scan causality (non-zero activations after the center token) and how CTP reshapes the ERF toward semantically meaningful regions. This provides mechanistic evidence that the proposed components actually do what the paper claims.

- **Strong complexity–performance trade-off (Table 1).** CMIC achieves competitive BD-rate with 69.11M parameters, 2.39 TFLOPs, and 0.405s decoding latency on 2K images. Compared to MambaIC (157.09M params, 5.56 TFLOPs, 20.32 GB peak memory), the efficiency gains are substantial — 56% fewer parameters, 57% fewer FLOPs, 78% less peak memory — while achieving better RD on 2 of 3 datasets.

## Weaknesses

### Fatal
None.

### Major

- **Overclaimed state-of-the-art results (Abstract, Section 4.3).** The abstract (line 9) and Section 4.3 (line 224) state that CMIC "achieves state-of-the-art rate-distortion performance" and "consistently outperforms leading methods across all evaluated datasets." However, Table 1 shows that MLICv2 achieves **−16.16%** BD-rate on Kodak versus CMIC's **−15.91%**, meaning CMIC is not the best on this dataset. The claim is factually inaccurate as written. While CMIC is best on 2 of 3 datasets (Tecnick, CLIC) and offers superior efficiency, the text should qualify this precisely — e.g., "CMIC achieves competitive or best-on-two-of-three SOTA results with significantly better efficiency" — rather than claiming uniform superiority. This is a framing issue, not a methodological flaw, but it must be corrected for publication.

### Minor

- **Undiscussed gradient barrier in clustering mechanism (Section 3.3).** The content-adaptive token permutation relies on hard clustering via arg max over cosine similarities, which is non-differentiable. The centroids are updated via EMA (a non-gradient update, acknowledged at line 120). The paper notes at line 177 that "the mapping A(·) is differentiable" but never discusses the core implication: the network must learn features that happen to cluster well without direct gradient feedback from the rate-distortion objective. While this is a known pattern from VQ-VAE (which the paper cites) and the method clearly works empirically, a brief discussion of why this works in practice (or what limitations it imposes) would be valuable in the main text rather than deferred to the appendix (A.8–A.10).

- **Encoder-decoder clustering consistency under quantization (Section 3).** CAM blocks appear in both the analysis transform (encoding unquantized latents y) and the synthesis transform (decoding quantized latents ŷ). Since quantization noise can shift features, cluster assignments could differ between encoder and decoder for the same spatial position. If assignments diverge, the decoder's content-adaptive scan may not match the encoder's, potentially affecting reconstruction quality. The paper does not discuss this at all. While the centroids are fixed (learned and shared), the assignment of individual tokens depends on feature values altered by quantization. An empirical analysis of assignment agreement across test images would strengthen confidence. The method works empirically, so this is unlikely to be a fatal concern, but it merits discussion.

- **Throughput ablation only at 256×256 resolution (Table 3).** Since the method's claimed advantage is most pronounced on high-resolution images (Tecnick, CLIC), reporting throughput and overhead at higher resolutions (e.g., 2K, where latency is already reported in Table 1) would be more informative for understanding the method's practical footprint.

### Trivial

- **Codebook initialization strategy (line 116).** Dividing the first batch into K consecutive segments to initialize centroids is somewhat ad hoc and lacks justification. A brief explanation of why this initialization works would be helpful.

- **Dimensions of C, P, h_i in prompt conditioning equation (line 181).** The equation O_i = (C + P)h_i + Dx_i does not specify the dimensions involved. If C is d_out × d_h and P is N × d_s, the addition requires broadcasting or reshaping that is not explained, creating unnecessary ambiguity.

## Nice-to-Haves

- Report the total number of centroids across all CAM blocks (K × number of CAM blocks) to make storage overhead transparent.
- Include a brief note on how the non-differentiable clustering interacts with end-to-end training (related to the Minor weakness on gradient barrier above), even just pointing to the VQ-VAE parallel.
- Specify training data used by cited baselines (where known) to contextualize the comparisons in Table 1. CMIC trains on Flickr2W; stating whether key competitors (e.g., MLICv2) used different training sets would clarify whether the Kodak comparison is apples-to-apples.

## Removed Points

- **"Multi-directional scanning quadruples computational complexity" is misleading:** Removed — the paper is clearly referring to the SSM scanning component, not the whole model. In context this is not misleading.
- **Training data for baselines not specified:** Removed — this is a scope-creep critique. Reporting training data for all cited baselines is not a standard expectation in LIC comparison tables; authors cite the original papers.
- **Per-block centroid overhead not reported:** Removed — a minor reporting detail that does not affect the paper's conclusions.
- **Clustering overhead breakdown (permutation index storage):** Removed — too granular for a main-review weakness.
- Generic strengths (e.g., "the paper addressed an important problem"): Removed — lacking specific evidence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the SOTA claim.** Qualify precisely: "CMIC achieves competitive SOTA results, outperforming leading methods on Tecnick and CLIC while offering substantially higher efficiency than prior Mamba-based approaches." Acknowledge MLICv2's Kodak result.
2. **Add a short discussion of the non-differentiable clustering** in Section 3.3, noting the VQ-VAE parallel and explaining why the method works despite the gradient barrier.
3. **Empirically analyze encoder-decoder clustering agreement.** For a set of test images, compute the percentage of tokens assigned to the same cluster in the encoder (unquantized) and decoder (quantized). If agreement is high (>95%), add a sentence confirming the concern is empirically resolved.
4. **Report throughput at higher resolutions** to complement the 256×256 measurements in Table 3.
5. **Clarify dimensions** for the C + P addition in the prompt conditioning equation.

---

## Score and Decision

Let me now report all calibration anchors and the final score.

**Round 1 Bracketing**: The paper falls between 5.5 and 7.0. It is clearly stronger than MambaVC (4.80, sim 0.83, directly comparable topic) which was criticized for limited novelty, while its evaluation depth (bidirectional ablations, ERF analysis) and genuine methodological contributions place it below but comparable to Spatial-Mamba (7.00, sim 0.78).

**Round 2 Narrowing**: Comparing weighted item profiles: CMIC's strongest items (ablation weight=10.88, ERF weight=10.51, efficiency weight=9.15) exceed or match those of Spatial-Mamba (ablation weight=10.18, results weight=9.54). CMIC's weakest item (SOTA overclaim, weight=3.46) is less negative than Spatial-Mamba's novelty concern (weight=-3.45) or the Autoregressive Pretraining paper's novelty concern (weight=-5.19). However, the SOTA overclaim is a verifiable factual inaccuracy that human reviewers would penalize explicitly. The paper's application specificity (compression only) versus Spatial-Mamba's general-purpose backbone also justifies a slightly lower score.

**Final Score**: 6.5

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>