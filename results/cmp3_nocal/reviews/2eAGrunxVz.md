Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper proposes Spherical Watermark, a lossless watermarking framework for diffusion models. The method converts binary watermark bits into Gaussian noise via a three-module pipeline: (1) a binary embedding module that mixes repeated watermark bits with random padding using an invertible matrix T to produce 3-wise independent bits; (2) a spherical mapping module that normalizes to the unit sphere, applies an orthogonal rotation C, and scales by a chi-square radius to recover exact Gaussian noise; and (3) integration with the diffusion model's standard sampling process. The paper theoretically proves that the watermarked noise matches a Gaussian prior up to third-order moments (via spherical 3-design theory) and empirically demonstrates strong undetectability, traceability, and computational efficiency compared to prior lossless schemes (PRC Watermark, Gaussian Shading).

## Strengths

1. **Theoretically grounded embedding mechanism.** The paper connects lossless watermarking to spherical 3-design theory (Definition 3.1, Theorem 3.2), providing a principled reason why watermarked noise should be distributionally hard to distinguish from true Gaussian noise. The polar decomposition argument (Lemma 3.4) is correctly invoked: a vector r·u with r²∼χ²(n) and u uniform on S^{n-1} is exactly N(0, Iₙ).

2. **Genuine practical advantage in key management.** Eliminating per-image key+nonce storage (required by Gaussian Shading) is a real operational improvement. The fixed signature K = {T, C} means the system stores one secret rather than one per image, correctly contrasted with prior work in Section 2.

3. **Strong computational efficiency.** The ~4 orders of magnitude speedup in extraction over PRC (Figure 4) is striking and practically meaningful — the difference between a matrix-vector multiply (O(n²)) and belief-propagation decoding is a genuine algorithmic advantage.

4. **Robust capacity scaling.** Figure 6(a) shows that the method maintains high accuracy even at very large payloads (l_m > 2000) where PRC fails entirely. This is a significant practical advantage for large-scale provenance tracking.

5. **Empirical undetectability.** The classifier-based detection experiment (Figure 2) convincingly shows that Spherical Watermark and PRC achieve near-chance detection (~50%), while Tree-Ring and Gaussian Shading (with fixed keys) are trivially detectable. FID values in Table 1 are essentially identical to the unwatermarked original, which is the strongest possible fidelity result for a lossless method.

## Weaknesses

### Major

1. **The rotation matrix C dimension is underspecified when l_c < l_x (structural clarity).** The paper states "For notational convenience, we set l_c = l_x in the following descriptions" (line 113), but Footnote 1 (line 121) says "In practice, l_c is chosen as a factor of l_x (e.g. l_c = ⌊√l_x⌋) to balance rotational expressiveness with computational and storage efficiency." With l_x = 16384, l_c = ⌊√16384⌋ = 128. The equations (10, 13) show simple matrix-vector products with no block-diagonal, tiling, or reshaping mechanism described. The extraction pipeline (Eq. 13) requires an l_x-dimensional output from C^{-1}, and no construction is specified for this when l_c < l_x. The implementation details (Section 4.1) do not specify what value of l_c was actually used in experiments, nor how C was applied. This underspecification prevents full reproducibility without guesswork. *(Note: this is a clarity gap in the paper's algorithmic description — the formal theory assumes l_c = l_x, but the practical footnote introduces a mismatch that is not resolved.)*

2. **Gaussian Shading is compared in a degraded configuration without sufficient qualification.** The paper evaluates Gaussian Shading with fixed keys and acknowledges (line 193) that "with fixed keys, Gaussian Shading no longer achieves true losslessness." The resulting FID degradation (Table 1: 50.70 vs 48.13 original on COCO SD v1.5) and detectability (Figure 2: 97% accuracy) are then presented as evidence of the proposed method's superiority. Gaussian Shading was designed to use per-image keys; comparing it in a configuration it was not designed for inflates the apparent margin of advantage. The paper does partially acknowledge this, but the presentation — particularly the abstract claiming to "outperform both lossy and lossless approaches" and the undetectability comparison — does not adequately separate the regime where the comparison is informative (demonstrating the advantage of fixed-signature operation) from where it is misleading (head-to-head undetectability against a method operating outside its design regime). The meaningful lossless comparison is against PRC, where the paper's results are genuinely competitive.

### Minor

3. **Notational self-reference for l_m.** Line 84 writes "l_m = N × l_m", which redefines l_m self-referentially. This is confusing — the original l_m (watermark length) and the expanded l_m (N × original length) should use distinct notation.

4. **Marginal convergence claim in Lemma 3.3 is stated without justification.** The claim that "as l_x → ∞, the marginal law of z_i^(3) converges to N(0, 1/l_x)" is asserted without sketch or citation. While plausible via a CLT argument on the rotated coordinates, a brief justification would improve the paper's self-contained rigor.

5. **Adversarial robustness framing conflates distinct properties.** The high adversarial-accuracy results for lossless methods (Table 2, Adv. column: 88–99%) are framed as "improved robustness," but the primary reason lossless methods resist adversarial attacks is that their watermarks cause no detectable distributional shift for the adversary to exploit. This conflates "no distributional shift exists" (undetectability) with "watermark survives attacks" (robustness). These are distinct properties, and the framing should be more precise.

### Trivial

6. The classifier experiment (Figure 2) would benefit from a clearer statement of how many distinct watermark messages were used for the latent-level classifier training. Section 4.2 mentions 100 distinct users for the image-level evaluation but does not connect this clearly to the latent-level setup.

## Nice-to-Haves

- Report confidence intervals or variance across train/test splits for the classifier-based undetectability experiment (Figure 2). A single run showing ~50% accuracy with an uncalibrated classifier could be a type-II error.
- Include DDIM inversion fidelity metrics (PSNR or LPIPS between original and inverted latents) to quantify the gap between theoretical invertibility and practical pipeline.
- Ablate the padding length l_r (e.g., l_r = 128, 256, 1024) to show how much randomness is needed for undetectability. This is the most interesting ablation the paper does not run.
- Discuss forward secrecy / key rotation: if the fixed signature K is leaked, all past and future watermarks can be removed. This is a genuine limitation relative to per-image key schemes.

## Removed Points

These points from the input review are excluded with justification:

- **"The 3-wise independence proof is in the appendix and cannot be verified"** — Removed per rule: criticisms about missing appendix content should not be counted as weaknesses.
- **"The criticism of PRC's heavyweight constructs is overstated"** — Removed as subjective opinion, not a concrete weakness or error in the paper.
- **"The distribution is confined to a coset of size 2^512; higher-order moments may be exploitable"** — The paper already acknowledges this limitation explicitly (Section 5, line 332: "higher-order moments may deviate from the true prior"). Already addressed by the authors.
- **"Lemma 3.3 convergence is stated without justification"** — Already addressed above as Minor weakness 4; the "missing appendix proof" aspect of this criticism is removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the C matrix dimension issue definitively.** State explicitly what value of l_c was used in the experiments (if l_c = l_x, acknowledge the 256 MB storage cost; if l_c < l_x, describe the block-diagonal or tiled construction and specify the block size). Update the equations to reflect the actual construction, or add a remark that the formal description assumes l_c = l_x and the practical construction is detailed in the appendix.

2. **Restructure the Gaussian Shading comparison.** Either (a) move the degraded fixed-key Gaussian Shading results to a dedicated ablation showing why per-image keys matter, reserving the main comparison for PRC, or (b) keep the comparison but prominently qualify that Gaussian Shading is designed for per-image keys and the fixed-key regime demonstrates the advantage of the proposed method's fixed-signature capability, not a head-to-head undetectability advantage.

3. **Clean up the l_m notation** so the expanded dimension has a distinct symbol (e.g., l_{Nm} as used in Section 4.1, or introduce l_x early).

4. **Add confidence intervals to the classifier undetectability experiment** to rule out type-II error.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>