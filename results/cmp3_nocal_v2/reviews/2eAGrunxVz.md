Now let me write the final, consolidated review in the required format.

## Summary
This paper proposes Spherical Watermark, a method for embedding multi-bit watermarks into diffusion model-generated images by encoding them directly into the initial Gaussian noise input. The approach uses a binary embedding module (mixing watermark bits with random padding via an invertible binary matrix) followed by a spherical mapping module (normalization to the unit sphere, orthogonal rotation, and chi-square scaling) to produce noise that is distributed as standard Gaussian. The method eliminates per-image key storage required by Gaussian Shading and avoids the heavy cryptographic operations of PRC Watermark. Empirical results show near-perfect undetectability (classifiers at chance), strong extraction accuracy, and orders-of-magnitude faster decoding than PRC.

## Strengths

1. **The core geometric idea is clever and well-motivated.** Mapping binary codes to Gaussian noise via the polar decomposition of a multivariate normal (uniform-on-sphere × chi-scale) is a natural approach, and framing the intermediate binary vector as a spherical $t$-design is a mathematically principled way to argue about distributional indistinguishability. This is genuinely different from the stream-cipher and error-correcting-code approaches of prior lossless methods (Gaussian Shading, PRC).

2. **The random-padding mechanism elegantly avoids per-image key storage.** By mixing the watermark with fresh random padding via the invertible matrix $\mathbf{T}$ (which is its own inverse), the embedding becomes randomized per invocation without requiring any state to be stored for extraction — the padding is recovered as part of $\mathbf{x}$ and simply discarded. This is a practically meaningful improvement over Gaussian Shading's per-image key requirement.

3. **Computational efficiency is convincingly demonstrated.** The extraction time is roughly four orders of magnitude faster than PRC Watermark (Figure 4), which is expected given that PRC relies on iterative belief-propagation decoding while the proposed method uses only matrix-vector multiplication and rounding.

4. **The ablation study is well-structured.** Isolating the binary embedding module (showing it is necessary for undetectability) and the spherical mapping module (showing it is necessary for robustness under brightness attacks) cleanly validates the design's two-stage architecture.

## Weaknesses

### Fatal
None.

### Major

1. **The rotation mechanism is incompletely specified when $l_c \neq l_x$, leaving the theoretical guarantees unverifiable.** The paper defines $\mathbf{C} \in \mathbb{R}^{l_c \times l_c}$ and states "For notational convenience, we set $l_c = l_x$ in the following descriptions" (line 113). Footnote 1 (line 121) acknowledges that in practice $l_c$ is a factor of $l_x$ (e.g., $l_c = \lfloor \sqrt{l_x} \rfloor$). With the experimental setting $l_x = 16384$, this gives $l_c = 128$. Equation (10) defines $\mathbf{z}^{(3)} = \mathbf{C} \mathbf{z}^{(2)}$, but $\mathbf{C} \in \mathbb{R}^{128 \times 128}$ and $\mathbf{z}^{(2)} \in \mathbb{R}^{16384}$ — these dimensions do not match. The paper never explains how the rotation is actually applied: whether $\mathbf{C}$ acts blockwise on disjoint chunks of $\mathbf{z}^{(2)}$, whether only a subspace is rotated, or whether some other mechanism is used. The theoretical analysis (Lemma 3.3) proves that the rotated vector remains a spherical 3-design *under the assumption that the full vector is rotated by an orthogonal matrix*. If $l_c \neq l_x$, this proof does not directly apply to whatever mechanism is actually used. Until the actual rotation procedure is specified and its distributional consequences are analyzed, the paper's central claim (that the watermarked noise is indistinguishable from standard Gaussian) rests on an incomplete method specification. **This is the paper's most significant weakness and must be addressed.**

### Minor

2. **Formal security definitions are invoked but not matched by evidence.** The paper sets up cryptographic-style definitions (Equations 2-4) requiring computational indistinguishability with security parameter $\rho$ and negligible function $\text{negl}(\rho)$. However, $\rho$ is never instantiated, and the theoretical analysis only proves moment matching up to 3rd order. The empirical evidence (classifier accuracy near 50%) is suggestive but does not constitute a cryptographic security proof. The formalism promises more than the analysis delivers. The definitions should be aligned with what is actually shown (e.g., "statistically indistinguishable up to 3rd-order moments").

3. **The "encryption-free" framing downplays a meaningful security trade-off.** The method still relies on a fixed secret signature $\mathcal{K} = \{\mathbf{T}, \mathbf{C}\}$ that is "kept fixed and secret during runtime" (line 82). If $\mathcal{K}$ is compromised, all watermarks in the system become forgeable. In contrast, compromising a per-image key in Gaussian Shading only breaks one image's watermark. The paper presents the elimination of per-image key storage as an unalloyed advantage, but this trades key-management overhead for a different (and in some threat models weaker) security posture. A brief acknowledgment of this trade-off would improve the characterization.

4. **The "lossless" claim is slightly overstated.** Table 2 reports ACC = 99.99% (std 0.01%) under clean (PNG) conditions, not 100%. The formal traceability definition (Equation 4) requires success with probability $1 - \text{negl}(\rho)$. The empirical accuracy is extremely high but not strictly equal to 1, and the error rate's dependence on any parameter is not characterized. This is a minor mismatch between the formalism and the numbers, not a practical concern.

### Trivial

5. **FID is computed against unwatermarked *generated* images, not real images** (line 229). The high absolute values (~48-50 in Table 1) will confuse readers who expect FID against real COCO images (~15-20). The table caption should clarify this.

6. **Algorithm 1 constructs a 3-tensor $\mathbf{R} \in \{0,1\}^{N \times l_m \times l_r}$ that is reshaped to $\{0,1\}^{l_m \times l_r}$.** The indexing $\mathbf{R}[i, j, G]$ (with $G$ a set of indices) and the reshape operation are not dimensionally obvious.

7. **TPR@1%FPR is reported for multi-bit extraction** (Table 2), but the paper does not explain how a false positive is defined when extracting 512-bit messages.

## Nice-to-Haves
- A complementary comparison with Gaussian Shading in its intended per-image-key mode (reporting storage requirements separately) would provide a complete picture, alongside the fixed-key comparison already included. (The paper already notes the limitation of fixed keys for Gaussian Shading, so this is about completeness, not fairness.)
- A more detailed discussion of the single-key vs. per-image-key security model trade-off (see Weakness 3) would strengthen the framing.

## Removed Points
These points are flagged to be removed; treat them with caution.
- **Gaussian Shading evaluation asymmetry**: The critic argued the evaluation was "unfair" because Gaussian Shading was used with fixed keys. However, the paper explicitly acknowledges this limitation (line 193: "with fixed keys, Gaussian Shading no longer achieves true losslessness"). Comparing both methods under the same condition (fixed keys) is a valid experimental design — it demonstrates that the proposed method handles fixed keys without degradation while Gaussian Shading does not. This is informative, not unfair.
- **"Security parameter $\rho$ never defined"**: This is folded into Weakness 2 (minor) above rather than kept as a standalone point.
- **Missing appendix / unverifiable proofs from appendix**: The parser strips appendices; these exist in the original submission.
- **Typographical / formatting artifacts**: These are parser errors, not author errors.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- **Clarify the rotation mechanism.** This is the single most important fix. If $\mathbf{C}$ is applied blockwise to disjoint chunks of $\mathbf{z}^{(2)}$, state this explicitly, specify the block structure, and show why the spherical 3-design guarantee still holds for the full vector. If a different mechanism is used, describe it in full and provide the corresponding theoretical analysis.
- **Align formal definitions with actual evidence.** Replace "computationally indistinguishable" and $\text{negl}(\rho)$ with a more accurate characterization (e.g., "matches the standard Gaussian up to 3rd-order moments, and classifiers cannot empirically distinguish").
- **Acknowledge the security trade-off explicitly.** Add a sentence noting that a single compromised $\mathcal{K}$ breaks all watermarks, whereas per-image-key schemes localize the damage.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>