## Summary

This paper introduces Spherical Watermark, a lossless watermarking framework for diffusion models that embeds binary watermarks into the Gaussian noise input without modifying model weights or requiring per-image key storage. The method uses a binary embedding module to mix watermark bits with random padding, followed by a spherical mapping module that projects the resulting code onto a unit sphere, applies an orthogonal rotation, and scales by a chi-square-distributed radius to recover standard Gaussian noise. The authors provide theoretical analysis showing the watermarked noise distribution preserves the target prior up to third-order moments, and demonstrate through experiments on Stable Diffusion that the method maintains visual fidelity while improving traceability, computational efficiency, and robustness compared to existing lossy and lossless approaches.

## Strengths

- **Encryption-free design eliminates key management overhead**: The method replaces per-image key storage (required by Gaussian Shading) and cryptographic error-correcting codes (required by PRC Watermark) with a fixed signature comprising an embedding matrix and rotation matrix, addressing a practical scalability concern in deployment.

- **Strong theoretical grounding for distribution preservation**: The paper provides a rigorous proof chain (Theorem 3.1, Theorem 3.2, Lemma 3.3, Lemma 3.4) showing that the watermarked noise is statistically indistinguishable from standard Gaussian noise up to third-order moments via spherical 3-design arguments, which is more thorough than typical empirical justifications in this area.

- **Competitive empirical results with significant computational advantages**: The method achieves comparable or better traceability metrics than PRC Watermark across clean and post-processing settings while being approximately four orders of magnitude faster in extraction time, a substantial practical improvement.

- **Comprehensive ablation studies**: The paper systematically ablates each module (binary embedding, spherical mapping), hyperparameters (s, N, l_m, l_p), and diffusion sampling settings (ODE solvers, timesteps), providing clear insights into which components contribute to undetectability versus robustness.

## Weaknesses

### Fatal
None.

### Major

- **The claims about the method being "encryption-free" conflate several distinct concepts**: The method still relies on secret fixed matrices T and C (the "Signature" kept secret during runtime), and the padding vector r is drawn from a Bernoulli(1/2) distribution (which could be considered a form of randomness). While the method eliminates per-image keys, it still requires a shared secret between the embedder and extractor. The paper's framing as "encryption-free" may mislead readers about the security model—the method's security relies on the secrecy of T and C, which is essentially a symmetric key. The authors should clarify what specific cryptographic overheads they avoid versus what security assumptions they inherit.

- **The theoretical guarantee is limited to third-order moments, which may not be sufficient for strong undetectability guarantees**: The spherical 3-design property ensures the distribution matches the uniform distribution on the sphere up to degree 3 polynomials. However, the chi-square scaling in Lemma 3.4 relies on the uniform distribution on the sphere. The paper does not address how deviations in higher-order moments (beyond degree 3) could be exploited by a sophisticated adversary. For a computationally bounded adversary, this may be sufficient, but the paper should discuss whether higher-order statistical tests (e.g., those used in steganalysis) could detect the watermark.

- **Missing comparison to Gaussian Shading's true lossless variant**: The paper evaluates Gaussian Shading with fixed keys, which the authors acknowledge "no longer achieves true losslessness." However, the original Gaussian Shading paper requires per-image keys for its formal guarantees. The comparison against a degraded version of Gaussian Shading weakens the claim that Spherical Watermark outperforms it—the comparison should also include the version with per-image keys (even if impractical) to show the trade-off between theoretical guarantees and practical performance.

- **The WEvade adversarial attack evaluation is insufficiently described**: The paper reports results under "Adversarial" attacks from Jiang et al. (2023) but does not specify the attack parameters, perturbation budgets, or whether the attacks are adaptive to each watermarking scheme. The claim that lossless methods are inherently more robust under adversarial attacks (Appendix E) is theoretically interesting but needs more rigorous empirical validation with properly tuned adversarial attacks per method.

### Minor

- **The FID values in Table 1 are abnormally high for all methods (including "Original")**: FID scores around 46-51 for SD v2.1 on COCO are much higher than typical reported values (~20-30). This suggests either a different evaluation protocol (e.g., comparing against a different reference set) or an issue with the FID computation. The authors should clarify what reference distribution is used and why the baseline FID is so high.

- **Figure 2 caption and labels appear garbled in the parsed text**: The figure description mentions "True Ring" when it should likely be "Tree-Ring," and the axis descriptions are confusing. This appears to be a parsing artifact, but the in-text description should be verified.

### Trivial
- The notation l_Nm and l_Nm is used but not explicitly defined in the main text (though it can be inferred as N × l_m).

## Nice-to-Haves

- A formal security definition or threat model (e.g., what capabilities the adversary has, whether they know the algorithm but not the secret signature, etc.) would strengthen the paper's positioning relative to cryptographic watermarking literature.
- Analysis of the method's robustness against adaptive adversaries who know the algorithm and can train detectors specifically targeting the spherical 3-design structure.
- Discussion of the information-theoretic trade-off between watermark capacity (l_m), undetectability, and robustness, perhaps with a rate-distortion-style analysis.

## Novel Insights

The key insight is that by leveraging spherical 3-designs—a combinatorial design concept from algebraic combinatorics—the paper shows that a carefully constructed finite set of points on the sphere can provably match the moments of the uniform spherical distribution up to degree 3. Combined with the polar decomposition of Gaussian vectors (Lemma 3.4), this provides a constructive mapping from binary strings to Gaussian noise that is both invertible and distribution-preserving up to third-order moments. This avoids the need for cryptographic primitives (stream ciphers, error-correcting codes) that prior lossless methods required, yielding significant computational savings. The practical implication is that lossless watermarking can be made efficient enough for real-time deployment without sacrificing theoretical guarantees that are meaningful against polynomial-time adversaries.

## Suggestions

1. Clarify the security model: explicitly state what is secret (T and C), what an adversary knows, and how the scheme's security reduces to the secrecy of these matrices. Distinguish between "encryption-free" (no per-image keys or cryptographic operations) and "keyless."

2. Add a comparison with Gaussian Shading using per-image keys (their original setting) to show the trade-off between key management overhead and undetectability/robustness. This would make the comparison more intellectually honest.

3. Provide more details on the WEvade adversarial attack setup: perturbation budget (epsilon), number of steps, whether the attack is white-box or black-box, and whether it is tailored to each watermarking scheme's specific weakness.

4. Explain why the FID values are so high (Table 1) or recompute them with a proper reference set. A footnote or clarification in the main text would suffice.

5. Discuss the practical implications of the third-order moment guarantee: under what threat models would an adversary need access to higher-order statistics? Is a polynomial-time adversary limited in practice?

## Score and Decision

The paper presents a novel and technically sound approach to lossless watermarking that addresses a real practical limitation (key management overhead) of prior work. The theoretical analysis is rigorous for its scope, and the empirical results convincingly demonstrate competitive or superior performance with dramatically lower computational cost. The major weaknesses—unclear security model framing and missing comparison to the non-degraded version of Gaussian Shading—are addressable through clarification rather than indicating fundamental flaws. The method's practical impact potential is high given its efficiency and compatibility with existing diffusion pipelines.

MY FINAL SCORE: 8<score></score>
MY FINAL DECISION: Accept<decision></decision>