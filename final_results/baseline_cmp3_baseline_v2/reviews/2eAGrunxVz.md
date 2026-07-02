## Summary

This paper introduces Spherical Watermark, a lossless watermarking framework for diffusion models that embeds binary watermarks into the Gaussian noise input without modifying model weights or requiring per-image cryptographic keys. The method uses a binary embedding module to mix watermark bits with random padding, followed by a spherical mapping that projects the result onto the unit sphere, applies an orthogonal rotation, and scales by a chi-square-distributed radius to produce noise that is theoretically and empirically indistinguishable from standard Gaussian noise. Experiments on Stable Diffusion demonstrate that the method preserves visual fidelity, achieves strong traceability under various attacks, and offers substantially lower computational overhead compared to prior lossless approaches like PRC Watermark.

## Strengths

- **Theoretically grounded losslessness**: The paper provides a rigorous theoretical analysis showing that the watermarked noise distribution matches the standard Gaussian prior up to third-order moments via spherical 3-design arguments, with lemmas and theorems supporting each transformation step.
- **Elimination of per-image key storage**: Unlike Gaussian Shading (which requires unique key/nonce per image) and PRC Watermark (which uses heavy cryptographic constructs), Spherical Watermark uses a fixed secret signature, removing key management overhead while maintaining losslessness.
- **Strong empirical results**: The method achieves near-perfect undetectability (classifier accuracy near 50%, FID matching unwatermarked generation) and high tracing accuracy (99.99% ACC clean, 99.83% TPR under adversarial attacks), outperforming PRC Watermark in robustness and being ~4 orders of magnitude faster in extraction.
- **Comprehensive ablation studies**: The paper systematically ablates each module (binary embedding, spherical mapping), parameters (s, N, l_m, l_r), ODE solvers, and timestep schedules, providing clear evidence for design choices and demonstrating robustness across configurations.

## Weaknesses

### Fatal
None.

### Major
- **The claim of "encryption-free" is somewhat misleading**: While the method avoids per-image cryptographic keys, the secret signature (T, C) still functions as a secret key that must be kept confidential. The method is "encryption-free" only in the sense of not using stream ciphers or error-correcting codes, but it still relies on secret matrices. The practical distinction from prior work is reduced key management overhead rather than elimination of secrets entirely.
- **Limited evaluation of robustness under strong adaptive attacks**: The adversarial attacks tested are from WEvade, but the paper does not evaluate against an adversary who knows the watermarking scheme (including the signature) and designs targeted attacks. Since the signature is fixed and secret, a determined adversary who compromises one watermarked image could potentially infer information about the rotation matrix C or embedding matrix T. The paper does not discuss this threat model.
- **The spherical 3-design guarantee is approximate, not exact**: The paper acknowledges that higher-order moments may deviate from the true Gaussian prior. While empirical results show indistinguishability, the theoretical guarantee is limited to third-order moments. For a method claiming "losslessness," this gap between theory and the ideal standard normal distribution should be more prominently discussed.

### Minor
- **The paper uses "lossless" to mean distribution-preserving, but the extraction process involves rounding (Eq. 13) and majority voting, which introduces potential for bit errors under strong attacks.** The method is lossless in the sense of not modifying the model or degrading image quality, but extraction is not guaranteed to be error-free in all conditions.
- **The comparison with Gaussian Shading uses fixed keys for Gaussian Shading, which the paper notes "no longer achieves true losslessness."** This creates an uneven comparison, as Gaussian Shading's losslessness guarantee depends on per-image keys. The paper should more clearly separate the comparison under fair conditions.

### Trivial
- Figure 2 caption describes "True Ring" and "PRC watermark" but the text refers to "Tree-Ring" and "Gaussian Shading" — there is a mismatch between the figure caption and the main text description.

## Nice-to-Haves
- An analysis of how the method performs when the secret signature (T, C) is partially leaked or when an adversary collects multiple watermarked images from the same user to attempt signature recovery.
- A discussion of the trade-off between the dimension l_c of the rotation matrix and computational/storage efficiency, as mentioned in footnote 1 but not explored experimentally.
- Evaluation on additional diffusion architectures beyond Stable Diffusion (e.g., DALL-E, Imagen) to demonstrate generality.

## Novel Insights

The key insight is that by combining a carefully constructed binary embedding matrix (designed to produce 3-wise independent bits) with a spherical mapping that leverages the polar decomposition of Gaussian distributions, one can embed arbitrary binary watermarks into the noise input of diffusion models while preserving the exact target distribution up to third-order moments. This avoids the cryptographic overhead of prior lossless methods while achieving comparable or better robustness. The use of spherical 3-design theory to connect binary codes to approximate uniform spherical distributions is a clever theoretical contribution that bridges coding theory and generative model watermarking.

## Suggestions
- Clarify in the introduction and abstract that "encryption-free" means no per-image key management, not that the method operates without any secret parameters. Consider using "key-efficient" or "fixed-key" instead.
- Add a discussion of the threat model where an adversary has access to multiple watermarked images and attempts to recover the secret signature, including any information-theoretic bounds on what can be inferred.
- Fix the mismatch between Figure 2's caption (which mentions "True Ring" and "PRC watermark") and the text (which discusses Tree-Ring and Gaussian Shading).

## Score and Decision

The paper presents a well-motivated, theoretically grounded, and empirically strong contribution to the watermarking of diffusion model outputs. The method is novel in its combination of binary embedding with spherical mapping, achieves state-of-the-art results in undetectability and robustness, and offers substantial practical advantages in computational efficiency over prior lossless approaches. The weaknesses are relatively minor and do not invalidate the core contributions. The paper is clearly written, with thorough experimental evaluation and ablation studies.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>