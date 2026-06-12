## Summary

The paper proposes "Spherical Watermark," an encryption-free and lossless watermarking framework for diffusion models that embeds binary watermarks into the Gaussian noise input through a novel spherical mapping. The method converts watermark bits into standard multivariate Gaussian noise via binary embedding (mixing with random padding), projection onto the unit sphere, orthogonal rotation, and chi-square-distributed radius scaling, requiring no per-image key storage and no modifications to pretrained models. Extensive experiments on Stable Diffusion demonstrate that the method preserves image quality (matching unwatermarked FID), achieves high tracing accuracy, and provides orders-of-magnitude speedup in extraction over the competing PRC Watermark baseline.

## Strengths

- **Novel and mathematically grounded mapping strategy.** The connection between binary sequences, spherical 3-designs, orthogonal rotations, and polar decomposition of Gaussians (Lemma 3.4) provides a clean and elegant theoretical framework for lossless watermark embedding. The progression from Theorem 3.1 (3-wise independence) through Theorem 3.3 (spherical 3-design) to Lemma 3.4 (exact Gaussian via chi-square scaling) is well-structured and the proofs (referenced in appendix) appear sound.

- **Practical efficiency gains are substantial.** The encryption-free design eliminates per-image key storage (reducing from O(num_images) to O(1) secret material) and yields extraction times roughly four orders of magnitude faster than PRC Watermark (Figure 4), which is a major practical advantage for deployment at scale.

- **Comprehensive and convincing experimental evaluation.** The paper evaluates undetectability at both latent and image levels (Figure 2, Table 1), tracing accuracy under clean, post-processing, and adversarial settings (Table 2), robustness under a wide range of attacks (Figure 5), capacity scaling (Figure 6a), sensitivity to hyperparameters (Table 3, Figure 6d), and ablations on modules (Figures 6b,c) and diffusion settings (Tables 4,5). The results consistently show the method matches or exceeds all baselines.

- **Strong adversarial robustness advantage.** Lossy watermarking methods degrade sharply under adversarial attacks from WEvade (Table 2: DwtDct drops to 49.28% ACC, RivaGAN to 52.31%), while the proposed lossless method maintains 98.12% ACC. This empirically validates the theoretical argument (Appendix E) that lossless embedding resists adversarial watermark removal because there is no distributional shift for an attacker to exploit.

## Weaknesses

### Fatal
None.

### Major

- **The gap between spherical 3-design and "statistically indistinguishable" is under-explored.** The theoretical analysis proves matching of moments up to order 3 (spherical 3-design), but the paper repeatedly claims statistical indistinguishability from N(0, I), which requires matching all moments. The abstract states "proves that the watermarked noise distribution preserves the target prior up to third-order moments" but then in the same sentence claims it is "statistically indistinguishable from a standard multivariate normal distribution." These are not equivalent. While the empirical evidence (FID, classifier experiments) strongly supports practical indistinguishability, the paper should be more precise about what the theory proves versus what the experiments demonstrate. The gap between third-order moment matching and full indistinguishability should be discussed more explicitly.

- **Comparison fairness with Gaussian Shading.** The paper notes that "with fixed keys, Gaussian Shading no longer achieves true losslessness" (Section 4.1), yet this degraded version is the one used in all comparisons. The original Gaussian Shading achieves losslessness precisely through per-image key management, which is the mechanism the proposed method replaces. A fairer comparison would acknowledge that the storage overhead of per-image keys is the *cost* of exact losslessness in Gaussian Shading, and the proposed method trades third-order-moment indistinguishability (rather than exact losslessness) for eliminating this cost. The framing as a strict improvement is slightly misleading.

- **The "encryption-free" terminology is imprecise.** The method still requires a secret signature K = {T, C} that must be kept confidential to prevent unauthorized watermark removal. The distinction from prior work is that this secret is fixed (not per-image), which is a legitimate practical advantage in storage and management. However, labeling this "encryption-free" may confuse readers into thinking no secret is involved at all, when in fact the security model still relies on the secrecy of T and C.

### Minor

- **Extraction relies on approximate DDIM inversion.** The "lossless" guarantee pertains to the embedding (the watermarked noise is approximately Gaussian), but extraction requires inverting the diffusion process (Eq. 12), which is inherently approximate. The paper acknowledges this implicitly (empty prompts for inversion, 50-step DDIM) but doesn't formally characterize how inversion error affects the bitwise extraction accuracy. The majority-vote mechanism with N=31 provides a practical buffer, but the robustness margin relative to inversion error should be analyzed.

- **Limited capacity analysis.** The default configuration uses l_m = 512 bits. While Figure 6(a) shows performance up to l_m = 4000+, the FID and undetectability results are only reported at the default capacity. It would strengthen the paper to show whether the lossless property degrades at higher capacities.

### Trivial
None.

## Nice-to-Haves

- A formal proof or bound on how the finite-sample (spherical 3-design) approximation to the uniform sphere distribution affects total variation distance or KL divergence from N(0, I), rather than relying solely on moment matching.
- A comparison of the actual key/signature storage requirements between Gaussian Shading (with per-image keys) and the proposed method (with fixed signature), quantifying the practical savings.
- Discussion of how the method would extend to video diffusion models or other modalities with temporal structure.

## Novel Insights

The paper's core novel insight is that binary sequences with 3-wise independence, when projected onto the unit sphere and combined with chi-square scaling, yield samples that are practically indistinguishable from standard Gaussian noise. This connects the combinatorial design of binary mixing matrices (Algorithm 1) to the geometric theory of spherical t-designs in a way that is both theoretically elegant and practically useful. The observation that this construction eliminates the need for heavyweight cryptographic primitives (stream ciphers, error-correcting codes) while maintaining comparable or superior robustness is a genuinely useful contribution to the watermarking literature.

## Suggestions

- Clarify the distinction between the theoretical guarantee (third-order moment matching) and the empirical claim (full indistinguishability) more carefully throughout the paper, including in the abstract.
- Add a brief discussion of the security model: what happens if an adversary knows the method but not the secret signature T, C? Can they detect the watermark's presence even without extracting it?
- Report FID and undetectability metrics at multiple watermark capacities to strengthen the scalability analysis.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>