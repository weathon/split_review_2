Now I have a clear picture. Let me finalize the review.

**Anchors from all rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| T0ebbDO60R.md (SuperMark) | 3.75 | R1 | Much weaker; limited novelty, straightforward approach |
| kRJNV8RCE3.md (Hiding Images in DMs) | 4.75 | R1 | Different approach; rejected |
| zqo2eKjSWH.md (Stable Signature Unstable) | 4.50 | R1 | Attack paper; rejected |
| HexshmBu0P.md (Recipe for Watermarking DMs) | 5.33 | R1 | Broader but less deep; rejected |
| ll2nz6qwRG.md (WIND/Hidden in the Noise) | 5.83 | R1 | Similar domain but less theoretical depth; accepted |
| 1IwoEFyErz.md (Shallow Diffuse) | 6.00 | R1 | Different technique; rejected |
| jlhBFm7T2J.md (PRC Watermark) | 6.50 | R1+R2 | Closest baseline; Spherical WM improves on this in every metric |
| mDKxlfraAn.md (Image Watermarks Removable) | 6.40 | R2 | Attack paper; accepted |
| f8S3aLm0Vp.md (DIAGNOSIS) | 6.50 | R2 | Related area; accepted |
| 71pur4y8gs.md (TabWak) | 7.20 | R1+R2 | Different domain but comparable theoretical rigor |

**Round 1 bracket: 6.5–7.5.** The paper is clearly stronger than PRC Watermark (6.50) — the closest comparable work — because it improves on PRC in robustness (+4.45% TPR under adversarial attacks), extraction speed (~4 orders of magnitude faster), capacity scalability (PRC fails beyond l_m=2000), and has a cleaner theoretical framework (spherical 3-designs). The two genuine weaknesses (theory-practice gap on l_c, overclaiming on indistinguishability) are non-fatal but prevent the paper from reaching the TabWak (7.20) level.

**Final score: 7.0.**

---

## Summary
This paper introduces Spherical Watermark, an encryption-free lossless watermarking framework for diffusion models that embeds binary watermark bits into Gaussian noise through three invertible stages: binary embedding via a structured mixing matrix, spherical mapping (projection to unit sphere, orthogonal rotation, chi-square scaling), and diffusion integration. The method eliminates per-image key storage and achieves strong empirical results on Stable Diffusion v1.5/v2.1: matching unwatermarked FID, chance-level classifier detection, superior robustness under adversarial attacks, and ~4 orders of magnitude faster extraction than the closest lossless competitor (PRC Watermark).

## Strengths
- **Novel and mathematically elegant framework**: The core insight — using 3-wise independent Bernoulli bits projected onto the unit sphere to form a spherical 3-design, then applying orthogonal rotation and chi-square scaling to approximate Gaussian noise — is genuinely novel. The chain of proofs (Theorems 3.1–3.2, Lemmas 3.3–3.4) connecting combinatorial properties (spherical t-designs) to distributional guarantees is clean and well-grounded.
- **Empirical validation of losslessness**: Table 1 shows FID virtually identical to unwatermarked originals (e.g., 48.1224 vs 48.1256 on COCO/SD v1.5). Figure 2 shows both latent-level MLP and image-level ResNet-18 achieve ~50% (chance) accuracy at distinguishing watermarked from unwatermarked samples, while Tree-Ring reaches 100% and Gaussian Shading 97%.
- **Dramatic computational speedup**: Figure 4 shows extraction time ~10⁻³·⁵ seconds vs ~10¹·⁰ for PRC Watermark (~4 orders of magnitude faster), reflecting the elimination of belief-propagation decoding.
- **Superior adversarial robustness**: Table 2 shows 98.12% ACC and 99.83% TPR under adversarial attacks, compared to PRC Watermark (97.69% ACC, 95.38% TPR). Lossy methods collapse entirely (DwtDct: 49.28% ACC).
- **High-capacity scalability**: Figure 6(a) shows PRC Watermark fails entirely beyond l_m=2000 bits under JPEG-70, while Spherical Watermark sustains high detection rates across the full range tested.
- **Comprehensive ablations**: Module ablation (Figure 6b–c), parameter sensitivity (Table 3, Figure 6d), ODE solver and timestep ablations (Tables 4–5) all thoroughly demonstrate the design's soundness.

## Weaknesses

### Fatal
None

### Major
- **Theory-practice gap on rotation dimension l_c**: All theoretical analysis in Section 3.3 assumes l_c = l_x = 16384 (full rotation matrix). However, the footnote on line 121 states: "In practice, l_c is chosen as a factor of l_x (e.g. l_c = ⌊√(l_x)⌋) to balance rotational expressiveness with computational and storage efficiency." With l_c = 128 and l_x = 16384, C is 128×128 but z^(2) ∈ ℝ^{16384}. The paper never explains how C actually operates on z^(2) in this setting — the most natural interpretation is blockwise independent rotation over 128 blocks of 128 dimensions, but this is never stated. Blockwise rotation preserves the 3-design property within blocks but does not mix coordinates across blocks, potentially leaving cross-block higher-order structure detectable. The paper does not re-derive or even state the distributional guarantees under this practical setting, leaving a significant gap between theory and implementation.

- **Overclaiming on indistinguishability**: The theoretical proofs establish moment matching up to degree 3 (through spherical 3-designs), and the formal definition (Eq. 2) requires computational indistinguishability with negligible advantage. However, the introduction (line 26) claims to "prove that the final noise is statistically indistinguishable from standard Gaussian noise," the conclusion (line 336) states inputs are "provably and empirically indistinguishable from a standard Gaussian prior," and contribution 2 (line 28) claims to "provide both theoretical analysis and empirical evidence that the watermarked noise distribution is statistically indistinguishable." While the abstract partially hedges (separating the theoretical "up to third-order moments" from the empirical "statistically indistinguishable"), the introduction and conclusion conflate these claims. The formal Eq. 2 guarantee is never established by the theoretical analysis.

### Minor
- **Missing explanation of extraction inversion**: The extraction procedure (Eq. 13) skips the chi-square radius normalization and relies on rounding to recover binary bits. This works because C⁻¹ẑ_T = r·z^(2) where z^(2) has entries ±1/√(l_x), and since r > 0, rounding recovers the correct binary value. A brief justification of *why* this works (r > 0 preserves sign) would improve clarity.
- **Simple detector architectures for undetectability evaluation**: The classifier-based detection uses only a 2-layer MLP and ResNet-18. Stronger detectors or statistical tests specifically targeting higher-order moments (e.g., Mardia's test) would further strengthen the undetectability claims.

### Trivial
None

## Nice-to-Haves
- Storage cost analysis for the fixed signature K = {T, C}. T is a 16384×16384 sparse binary matrix; stating actual storage requirements would strengthen practical claims.
- Evaluation against model extraction or fine-tuning attacks that alter the inversion mapping G⁻¹.
- Testing on generative models beyond Stable Diffusion to validate the claimed generality.

## Removed Points
These points are flagged to be removed, treat them with caution.
- Missing related works — cannot verify external claims about missing literature without access to external sources.
- Typos/formatting — parser artifacts, not author errors.

## Novel Insights
The paper's core insight — using spherical t-designs and polar decomposition to construct an approximately-Gaussian noise distribution from binary bits — is genuinely novel and mathematically elegant. The realization that 3-wise independent Bernoulli bits, when projected onto the unit sphere, form a spherical 3-design that can then be rotated and chi-square-scaled to approximate Gaussian noise provides a clean alternative to the cryptographic constructions (stream ciphers, error-correcting codes) that previous lossless watermarking methods relied upon. This is a substantive contribution to the watermarking literature.

## Suggestions
1. Clarify the practical rotation implementation: either re-derive guarantees for blockwise rotation (if that is indeed what is implemented) or explicitly state it as an approximation whose adequacy is demonstrated empirically.
2. Carefully distinguish theoretical guarantees (third-order moment matching) from empirical claims (indistinguishable from Gaussian) throughout the paper, particularly in the introduction and conclusion.
3. Add a brief explanation of why chi-square scaling is implicitly inverted by rounding during extraction (r > 0 preserves sign, enabling correct bit recovery).

## Score and Decision

**Score: 7.0**

**Reporting:**
- **Round 1 bracket: 6.5–7.5.** The paper is clearly above PRC Watermark (jlhBFm7T2J.md, avg 6.50) — the closest comparable baseline — since it improves on PRC in robustness, speed, capacity, and theoretical elegance. It is slightly below TabWak (71pur4y8gs.md, avg 7.20) due to the theory-practice gap on l_c and overclaiming.
- **Round 2** narrowed the search to 6.0–8.0 for lossless watermarking with provable guarantees, confirming the same anchor papers and supporting the 7.0 placement.
- The paper's two major weaknesses (theory-practice gap, overclaiming) are genuine but non-fatal — they concern the framing rather than the methodological or empirical contributions. The empirical results are strong, the mathematical framework is novel, and the method demonstrably improves upon the state of the art.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>