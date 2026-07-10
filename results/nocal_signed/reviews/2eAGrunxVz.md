Now let me compile the final review based on my thorough analysis of both the paper and the per-item impact scores.

---

## Summary

This paper proposes Spherical Watermark, a lossless watermarking framework for diffusion models. The key idea is to map binary watermark bits to Gaussian noise inputs through a pipeline of binary embedding (using 3-wise independent codes) and spherical mapping (using spherical 3-designs, orthogonal rotation, and chi-square scaling). The method eliminates per-image key management required by prior lossless schemes and achieves strong undetectability and robustness. Experiments on Stable Diffusion v1.5 and v2.1 with COCO and SDP prompts demonstrate that the watermarked outputs are statistically indistinguishable from unwatermarked ones, while maintaining high extraction accuracy under various attacks.

## Strengths

- **Elegant theoretical construction.** The chain connecting 3-wise independence of the binary code → spherical 3-design on the unit sphere → orthogonal rotation → chi-square scaling to approximate Gaussian noise is clean and well-motivated. The paper connects these concepts in a logically sound way. (Section 3.2–3.3)

- **Eliminating per-image key management is a genuine practical advantage.** Prior lossless methods (Gaussian Shading, PRC) require per-image keys or heavy cryptographic decoding. Using a fixed secret signature (T, C) with per-image random padding is a simple and effective alternative that reduces infrastructure overhead. (Section 3.2)

- **Strong undetectability evidence.** FID values in Table 1 show the proposed method's output matches the unwatermarked original within sampling noise (48.1224 vs 48.1256 on COCO SD v1.5). Binary classifiers at both latent and image levels achieve near-chance accuracy (~50%), confirming empirical indistinguishability. (Section 4.2, Table 1, Figure 2)

- **Comprehensive robustness evaluation.** The evaluation covers clean, post-processing, and adversarial settings (Table 2), with systematic ablations isolating the contributions of binary embedding and spherical mapping (Figure 6b–c). The method achieves strong extraction accuracy across diverse distortion types. (Section 4.2–4.3, Table 2, Figure 6)

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Theoretical overclaim in the abstract.** The abstract states the method recovers "exact multivariate Gaussian noise," and Section 3.3 opens by saying z_w "is distributed as N(0, I)." However, the actual guarantee is indistinguishability up to degree-3 moments via a spherical 3-design — the construction does not achieve exact uniformity on the sphere, only a degree-3 approximation. The limitation is honestly discussed in Section 5 ("higher-order moments may deviate"), but the abstract-level framing is inconsistent with what is actually proved. The paper would benefit from aligning the claim language throughout. (Abstract, Section 3.3, Section 5)

- **PRC computational efficiency comparison lacks precision.** The claimed ~10,000× speed advantage over PRC (extraction: ~10⁻³·⁵ s vs ~10¹ s, Figure 4) is reported at only one significant figure on a log scale, without released code or detailed hardware/implementation specifications for the baseline. While the direction of the advantage is plausible (matrix operations vs. belief propagation), the magnitude cannot be independently verified from the information provided. (Section 4.2, Figure 4)

- **FID reference distribution is ambiguous.** The paper reports FID "measured against the unwatermarked output distribution" (line 229), yielding absolute values of ~48 for the "Original" condition. It is unclear whether the reference is real images or another set of generated images, making the absolute values difficult to interpret. The relative comparison (proposed ≈ Original) remains informative. (Section 4.1, Table 1)

- **Incomplete treatment of rotation matrix size l_c.** The theory assumes l_c = l_x, but footnote 1 states that in practice l_c is chosen as a factor of l_x (e.g., ⌊√l_x⌋). The paper does not explain how the rotation is applied to the full 16384-dimensional latent when l_c < l_x. If applied in blocks, the spherical 3-design guarantee holds per block rather than for the full vector, which should be explicitly discussed. (Section 3.2, footnote 1)

### Trivial

None.

## Nice-to-Haves

- Discuss the trade-off between l_m (watermark length), l_r (padding length), and N (repetition count) in terms of effective watermark capacity.
- Consider an experiment where the prompt or seed changes between embedding and extraction, as this is a natural attack scenario for API-based generation.
- Statistical significance tests for the near-50% classifier accuracies would further strengthen the undetectability claim.

## Removed Points

These points were flagged in the input review but removed after verification:

1. **Gaussian Shading "deliberately degraded" criticism (REMOVED):** The reviewer claimed the paper evaluates Gaussian Shading in a "deliberately degraded configuration" that inflates the paper's relative undetectability. However, the paper explicitly states "Note that with fixed keys, Gaussian Shading no longer achieves true losslessness" (Section 4.1) and consistently qualifies "Gaussian Shading (with fixed keys)" in results (Section 4.2). The comparison is transparent and fairly scoped to the fixed-key regime where both methods operate.

2. **Several generic/speculative concerns (REMOVED):** The input review contained section-by-section notes that were descriptive or lacked specific evidentiary anchors (e.g., notes about related work coverage, problem formulation adequacy). These did not identify concrete problems with the paper's content.

## Novel Insights

None beyond the paper's own contributions. The paper's central insight — using spherical 3-designs and polar decomposition for encryption-free lossless watermarking — is well-articulated in the manuscript itself.

## Suggestions

- Reconcile the "exact Gaussian" language in the abstract and Section 3.3 with the degree-3 guarantee that is actually proven.
- Provide precise timing measurements (means with standard deviations, not just log-scale approximations) for the PRC comparison, or clearly state that values are approximate.
- Clarify the FID reference distribution (real images vs. generated images) and explain why the absolute values are in the ~48 range.
- Explain how the rotation matrix C is applied when l_c < l_x in practice (e.g., whether the latent is reshaped and rotated in blocks).

## Score and Decision

The paper presents a novel, well-motivated, and theoretically grounded watermarking method with strong empirical validation. All identified weaknesses are minor and addressable — they concern presentation precision and reporting detail rather than any fundamental flaw in the method or its evaluation. The contributions (elimination of per-image key management, theoretical connection of spherical designs to lossless watermarking, strong empirical results) are solid and valuable to the community.

**MY FINAL SCORE:** <score>8</score>
**MY FINAL DECISION:** <decision>Accept</decision>