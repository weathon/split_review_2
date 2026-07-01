## Summary

The paper introduces Spherical Watermark, a lossless watermarking framework for diffusion models that embeds binary watermarks into the latent Gaussian noise without per-image key storage or cryptographic operations. It uses a binary embedding module (mixing repeated watermark bits with random padding via an invertible matrix) and a spherical mapping module (projecting onto the unit sphere, applying an orthogonal rotation, and scaling by a chi‑square radius) to produce noise that is statistically close to standard Gaussian. Experiments on Stable Diffusion show that the method preserves visual fidelity, is computationally efficient (extraction ~4 orders of magnitude faster than PRC), and achieves strong tracing accuracy under various attacks.

## Strengths

- **Novel and well‑motivated framework.** The paper identifies a real limitation of existing lossless watermarking schemes (per‑image key storage or heavy cryptographic overhead) and proposes an elegant alternative that embeds fresh randomness directly into the noise, eliminating the need for external key management.
- **Solid theoretical analysis.** The authors prove that the watermarked noise is a spherical 3‑design, matching the first three moments of the uniform distribution on the sphere, and provide lemmas showing how orthogonal rotation and chi‑square scaling yield a distribution that empirically and asymptotically approaches standard Gaussian. This provides a principled foundation for the method.
- **Strong empirical validation.** Extensive experiments compare against six baselines (traditional, latent‑based, lossy, lossless) across two datasets and two model versions. The method matches the original FID, achieves near‑chance classification detection (≤50%), and maintains high extraction accuracy under clean, post‑processed, and adversarial conditions. Ablation studies clearly isolate the contribution of each module.
- **Computational efficiency.** The spherical mapping and binary embedding/ extraction involve only simple matrix operations and rounding, making embedding and extraction orders of magnitude faster than PRC while avoiding the belief‑propagation decoding overhead.

## Weaknesses

### Fatal
None.

### Major
- **Overclaimed “losslessness” guarantee.** The watermarked noise is only proven to match the Gaussian up to third‑order moments (spherical 3‑design), not exact statistical indistinguishability. Higher‑order moments may deviate, and the paper acknowledges this only in the limitations (Section 5) but continues to use “lossless” as a central claim throughout. This is a mismatch between the theoretical result and the language used.
- **Unclear implementation of the orthogonal rotation matrix.** The paper states that a single orthogonal matrix `C` of size `l_c × l_c` is used, with `l_c` chosen as a factor of `l_x` (e.g., `⌊√l_x⌋`). It is not explained how a smaller matrix is applied to a vector of dimension `l_x`. If block‑diagonal or other structured rotations are used, the theoretical guarantees of Lemma 3.3 (full orthogonal rotation preserving spherical 3‑design) may not hold. This implementation detail is critical for reproducibility and theoretical soundness.
- **Unfair comparison with Gaussian Shading.** Gaussian Shading is evaluated with fixed keys, which the paper notes “no longer achieves true losslessness”. However, the original scheme was designed for per‑image keys; the fixed‑key variant is a misapplication that predictably introduces detectability. A fair comparison would either compare with per‑image key Gaussian Shading (and discuss the storage trade‑off) or restrict the claim to the fixed‑key setting more explicitly. The current presentation gives the impression that Gaussian Shading is inherently weaker.

### Minor
- **No false‑positive rate (FPR) analysis for extraction.** The paper reports TPR at 1% FPR but does not provide the actual achieved FPR of the detector or discuss how the decision threshold is set. For forensic applications, controlling the FPR is essential.
- **Security parameter ρ is left undefined.** The definitions of undetectability and traceability (Section 3.1) use a security parameter `ρ` and `negl(ρ)`, but ρ is never specified (e.g., number of bits, latent dimension). This makes the formal claims somewhat ambiguous.

### Trivial
- Minor phrasing: “encryption‑free” could be misinterpreted as “no secrecy required”; the method still relies on secret matrices `T` and `C`.

## Nice‑to‑Haves

- Provide a concrete bound on the statistical distance (e.g., total variation or KL divergence) between the watermarked noise distribution and a true standard Gaussian, even if only for the asymptotic regime.
- Release an official implementation and pre‑computed signature matrices to aid reproducibility.
- Discuss how the method could be extended to other generative models beyond diffusion (e.g., GANs, VAEs) that also use Gaussian priors.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the fresh randomness needed for each watermarked sample need not be stored as an external key: it can be generated on‑the‑fly as part of the binary embedding (the random padding vector `r`) and recovered during extraction, because the invertible transformation ensures that `r` is encoded into the noise and can be inverted out. This turns the usual “key per sample” problem into a signal‑recovery problem, enabling an encryption‑free protocol. The use of a spherical 3‑design to bridge discrete binary codes and the continuous Gaussian prior is also a creative simplification of the more complex cryptographic constructions in prior work.

## Suggestions

- Clarify the exact form of the rotation matrix `C` when `l_c < l_x`. Provide the block‑diagonal or partitioned scheme and verify that the spherical 3‑design property is preserved after such a rotation.
- Rephrase the “losslessness” claim to “approximate losslessness” or “statistically indistinguishable in practice (moments up to third order match)”, and clearly differentiate the guarantee from exact distribution‑preserving methods like Gaussian Shading with per‑image keys.
- Include a comparison with Gaussian Shading using per‑image keys (even if only in the appendix) to quantitatively show the storage overhead that their method avoids.
- Report the actual FPR achieved on negative samples (no watermark) for the extraction procedure, and describe how the threshold is chosen.

## Score and Decision

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>