## Summary

The paper introduces Spherical Watermark, an encryption-free watermarking framework for diffusion models. It converts binary watermark bits into a latent code that is provably a spherical 3-design (matching standard Gaussian noise up to third-order moments) and empirically indistinguishable from a true Gaussian prior. The method replaces the cryptographic overhead of prior lossless schemes (PRC) with simple binary matrix operations, achieving ~4 orders of magnitude faster extraction, while eliminating per-image key storage needed by Gaussian Shading.

## Strengths

- **Practical speed advantage over PRC watermarking:** The paper demonstrates ~4 orders of magnitude faster extraction (Figure 4), replacing heavy belief-propagation decoding with simple binary matrix multiplication and orthogonal rotation. The comparison correctly isolates the watermark transformation from diffusion sampling.

- **The spherical 3-design analysis is well-matched to the method.** Rather than claiming exact Gaussian equivalence (which would be false for any finite construction), the paper proves moment matching up to degree 3 (Theorem 3.1, Theorem 3.2, Lemma 3.3) and relies on Lemma 3.4 (polar decomposition) plus empirical validation to argue closeness to Gaussian. The theory and method are coherent.

- **Clean, fully reversible modular design** (ℬ, 𝒮, 𝒢) with explicit forward and inverse operations (Eqs. 9–13). The embedding matrix T is self-inverse over 𝔽₂ and C is orthogonal, so extraction is a simple sequence of linear operations plus rounding and majority vote — no iterative decoding, no belief propagation, no per-image key derivation.

## Weaknesses

### Fatal
None.

### Major

- **The framing of "losslessness" overstates what the theory proves.** The abstract claims the method recovers "exact multivariate Gaussian noise" (line 9) and the title uses "Lossless" without qualification. However, the theoretical analysis establishes only a spherical 3-design (moment matching up to degree 3), not exact Gaussianity. The paper acknowledges this gap in the limitations (line 332: "higher-order moments may deviate"), but the central framing — title, abstract, contribution list — uses stronger language than the theory supports. The method is empirically near-perfect and the conclusion is likely correct, but the theoretical claim is pitched above what the analysis delivers. This is a presentational overreach, not a methodological flaw.

- **The Gaussian Shading comparison is conducted in a knowingly weakened regime.** The paper evaluates Gaussian Shading with "fixed keys" and notes (line 193) that "with fixed keys, Gaussian Shading no longer achieves true losslessness" — yet the degraded FID (50.70 vs. 48.13 on COCO SD v1.5) and detectability (97% accuracy in Figure 2) are then used to argue that the proposed method has superior undetectability. Gaussian Shading with per-image keys achieves exact losslessness (proven in Yang et al., 2024) at a storage cost. A fairer framing would present this as a trade-off (exact losslessness + key storage vs. approximate losslessness + no per-image storage) rather than as a unidirectional improvement. The disclosure is present, but the comparison framing is unbalanced.

### Minor

- **Inversion reconstruction error is unreported.** The pipeline relies on DDIM inversion (Eq. 12) to recover the latent from the generated image, but no measure of inversion accuracy (e.g., MSE between original and inverted latent for non-watermarked images) is provided. This makes it difficult to bound the noise introduced by this step and to separate inversion errors from watermark extraction errors.

### Trivial

- **Notation reuse in Equation 6:** l_m = N × l_m uses the symbol l_m for both the original watermark length and the total repeated length, which is confusing on first reading.

## Nice-to-Haves

- Including a precision-recall analysis beyond TPR@1%FPR would further strengthen the evaluation, though the current metric is standard.
- Specifying the source of per-image randomness (e.g., PRNG seeded per request) would aid reproducibility.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Adversarial attack details absent from main text (Issue 6):** The paper references Appendix F.4 for adversarial attack configuration. Per the hard rules (parser-stripped appendix content exists in the original submission), this is not a valid weakness against the paper as submitted.
- **False positive rate analysis request:** Already reported as TPR@1%FPR, which is the standard metric in watermarking evaluations. A full precision-recall analysis would be additive but is not required.
- **Per-image randomness source question and various Strengthening-the-Paper suggestions:** These are either trivial implementation details or are already subsumed by the Major weaknesses above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Recalibrate the losslessness terminology** consistently throughout the paper. Replace "exact multivariate Gaussian noise" in the abstract with wording that accurately reflects the 3-design guarantee (e.g., "noise whose distribution matches the standard Gaussian up to third-order moments and is empirically indistinguishable in practice"). Similarly, qualify or contextualize "Lossless" in the title or body.

2. **Reframe the Gaussian Shading comparison** as a trade-off analysis: Gaussian Shading with per-image keys achieves exact losslessness at a storage cost; the proposed method achieves approximate losslessness with no per-image storage. Both designs are valid for different deployment constraints. This would replace the current framing, which pits the proposed method against a knowingly degraded version of the baseline.

3. **Report inversion reconstruction error** (e.g., latent-space MSE between original DDIM-inverted latents and those recovered through the full inversion pipeline for clean, non-watermarked images) to quantify the noise introduced before watermark extraction.

## Score and Decision

The core method is sound, the practical speed improvement over PRC is substantial and well-demonstrated, and the spherical 3-design theory is intellectually honest. The two major weaknesses — overstated losslessness framing and an unbalanced Gaussian Shading comparison — are presentational issues rather than methodological failures. Both are fixable in revision. The contributions are real and the evidence supports the central claims.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>