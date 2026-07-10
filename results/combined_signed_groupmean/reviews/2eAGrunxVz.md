## Summary

This paper introduces Spherical Watermark, a lossless watermarking framework for diffusion models that avoids both per-image key storage (required by Gaussian Shading) and heavy cryptographic constructs (required by PRC Watermark). The core idea is to encode binary watermarks into Gaussian noise inputs by: (1) mixing repeated watermark bits with random padding via an invertible binary matrix to create a 3-wise independent bitstream, (2) mapping the result to the unit sphere (forming a spherical 3-design), applying an orthogonal rotation, and scaling by a chi-square-distributed radius to approximate the polar decomposition of a Gaussian vector. The paper provides theoretical analysis up to third-order moments and demonstrates through extensive experiments that the method preserves FID, achieves ~50% classifier-based detection (chance level), extracts watermarks with ~99.99% accuracy, and does so with extraction times ~4 orders of magnitude faster than PRC Watermark.

## Strengths

- **Clean theoretical foundation (Section 3.3).** The paper correctly identifies that normalized hypercube vertices (±1/√n vectors) form a spherical 3-design, and shows through Lemma 3.4 that after orthogonal rotation and chi-square-radius scaling, the resulting noise matches the Gaussian prior up to third-order moments via the polar decomposition. The analysis of each intermediate distribution (z^(1) → z^(2) → z^(3) → z_w) is well-structured and theoretically sound.

- **Strong empirical evidence for undetectability (Table 1, Figure 2).** FID values for Spherical Watermark are essentially indistinguishable from the "Original" baseline (e.g., 48.12 vs 48.13 on SD v1.5/COCO), matching PRC Watermark and clearly separating from lossy methods. The classifier-based detection experiment showing ~50% accuracy for both PRC and the proposed method is convincing evidence that the watermarked noise is not statistically detectable by a learned classifier.

- **Computational efficiency advantage (Figure 4).** Extraction time is roughly four orders of magnitude faster than PRC Watermark (10^−3.5 s vs 10^1 s). PRC requires expensive belief-propagation decoding; the paper's simpler linear-algebra-based extraction is a genuine operational advantage for deployment.

- **Ablation on modules (Figure 6b, 6c) cleanly isolates each component's contribution.** Removing the binary embedding makes the noise trivially detectable; removing the spherical mapping causes robustness to collapse under brightness adjustment. This provides clear evidence that both components are necessary and that their specific combination drives the overall performance.

## Weaknesses

### Major

- **Gaussian Shading evaluated in a degraded configuration for undetectability (Figure 2, line 235).** The paper evaluates Gaussian Shading with fixed keys (line 193: "Note that with fixed keys, Gaussian Shading no longer achieves true losslessness") and reports 97% classifier detection as evidence that the method is detectable. Gaussian Shading's losslessness guarantee *requires* per-image keys — its design intentionally trades key-management convenience for undetectability. Evaluating it with fixed keys tests it outside its designed operating regime. The paper's abstract claim of "outperforming both lossy and lossless approaches" is inflated if the lossless comparison relies on a degraded configuration. The paper should separate the undetectability comparison (using per-image keys for Gaussian Shading, its intended mode) from the separate discussion of key-management overhead as a practical limitation. The comparison with PRC Watermark is fair and favorable, so this issue does not invalidate the core contribution, but it must be corrected.

### Minor

- **Self-referential notation in Equation 6 and ambiguous dimensions in Algorithm 1.** Equation 6 writes `l_m = N × l_m`, which is mathematically incoherent (l_m cannot equal N·l_m unless N=1). From implementation details (line 191), l_m = 512, N = 31, and the total repeated dimension is l_{Nm} = 15872 = N·l_m. The matrix T's top-left block should be I_{N·l_m}, not I_{l_m} with l_m redefined mid-equation. Algorithm 1 initializes R as N × l_m × l_r then reshapes to (l_m, l_r) — the reshape dimension should be (N·l_m, l_r). A reader attempting to reproduce the method cannot determine the correct dimensions from the current description.

- **Extraction step (Equation 13) does not account for the chi-square radius r.** In the forward pass (Eq. 10), z_w = r·z^(3) where r² ∼ χ²(l_x). Extraction computes ẑ^(2) = C^{-1}ẑ_T ≈ r·z^(2). The entries of r·z^(2) are ±r/√(l_x), not ±1/√(l_x). The subsequent rounding step ẑ^(1) = round((ẑ^(2)+1)/2) only recovers the original bits because r/√(l_x) ≈ 1 in expectation (E[r] ≈ √(l_x) with small variance). The paper should either justify this explicitly or include an explicit normalization step in the extraction.

- **Figure 2 caption appears inconsistent with the text.** The caption (lines 217–219) mentions only "True Ring" and "PRC watermark" curves, while the text (line 235) discusses Gaussian Shading detection accuracy of 97%. This mismatch between what the figure shows and what the text claims is confusing.

- **No explicit false-positive analysis for non-watermarked images.** The paper reports TPR@1%FPR, which controls the per-bit false positive rate among watermarked samples, but does not evaluate what happens when extraction is applied to an image not generated by the model (e.g., a real photograph). In a tracing/forensic scenario, false accusation rates on non-watermarked inputs are a practical concern that should be addressed.

### Trivial

- **Abstract language overstates the theoretical guarantee.** The abstract says "recover exact multivariate Gaussian noise" while the guarantee is up to third-order moments (the same abstract paragraph does include "up to third-order moments," but the "exact" framing could mislead casual readers). The Limitations section (line 332) correctly notes that higher-order moments may deviate.

- **WEvade adversarial attack not described in the main paper.** The text (line 271) only references Appendix F.4. A one-sentence description of what WEvade does would help readers interpret Table 2's "Adv." column without consulting the appendix.

## Nice-to-Haves

- Provide a side-by-side undetectability comparison that evaluates Gaussian Shading with per-image keys (its intended configuration) alongside the fixed-key results, cleanly separating the key-management discussion.
- Explicitly note in the extraction description that r/√(l_x) ≈ 1 and justify why the rounding step works without normalization.
- Add a brief false-positive analysis on non-watermarked images (e.g., real photographs or images from a different generator).
- Include a one-sentence summary of the WEvade attack in the main text.

## Removed Points

These points from the input review are removed with justification:

- **"Padding r recovery is unclear"** — Removed. The paper explains in Eq. 5 and 13 that x = [m ... m r]^T and extraction via T^{-1} recovers the full x̂ including r̂. The padding is part of x̂ but simply not used after extraction; the first l_{Nm} entries suffice for majority-vote decoding.
- **"Missing related works"** — Removed per policy (no external sources to confirm).
- **"Abstract language mismatch" (escalated from structural to trivial)** — Removed from major tier because the abstract does include the "up to third-order" qualification in the same paragraph. It's a minor wording tension, not a structural flaw.
- **"Comparison with 32-bit vs 512-bit methods"** — Removed. The paper clearly states (line 193) which methods use 32-bit vs 512-bit watermarks. The comparison in Table 2 separately compares against latent-based methods (all 512-bit). The asymmetry favors the baselines (32-bit is easier to extract), not the proposed method.
- **Several generic critique framings** — Removed per filtering rules (speculation without concrete textual anchor).

## Novel Insights

The key insight — using spherical 3-designs from normalized hypercube vertices combined with chi-square-radius scaling to approximate the polar decomposition of a Gaussian — is a clever departure from the cryptography-heavy approach of prior lossless methods (stream ciphers in Gaussian Shading, error-correcting codes in PRC). This paper shows that a carefully designed linear-algebraic transform in the latent space can achieve comparable undetectability to cryptographic methods while being orders of magnitude faster. It shifts the design space for diffusion watermarking from "crypto for randomness" to "geometry for distribution matching." The recognition that perfect uniformity on the sphere is unnecessary — a 3-design suffices because the chi-square scaling step dominates the distributional approximation — is the paper's most interesting intellectual contribution.

## Suggestions

1. **Fix the Gaussian Shading comparison.** Evaluate Gaussian Shading with per-image keys for the undetectability experiment and present both configurations, clearly separating the discussion of key-management overhead from the undetectability comparison.
2. **Fix the notation in Eq. 6** (use l_{Nm} or N·l_m instead of self-referential l_m = N·l_m) **and Algorithm 1** (clarify the reshape dimension).
3. **Add a brief justification for the extraction rounding** — explicitly note that r/√(l_x) ≈ 1 in expectation since E[r²] = l_x with variance 2l_x.
4. **Add a false-positive analysis** on images not generated by the model to address forensic concerns.
5. **Tone down "exact" in the abstract** or pair it more tightly with the "up to third-order moments" qualifier.

## Score and Decision

**Final score: 7.0 — Borderline Accept leaning toward Accept.**

The paper makes a genuine contribution: a novel geometry-driven lossless watermarking method that is faster than PRC, avoids per-image keys required by Gaussian Shading, and demonstrates strong undetectability and robustness. The main weakness (fairness of the Gaussian Shading evaluation) is real but fixable and does not threaten the core contribution, which rests primarily on the favorable comparison with PRC Watermark — a comparison that is conducted fairly. The notation and extraction-clarity issues are addressable in revision. The paper is positioned between the PRC anchor (avg 6.50, weaker on efficiency/robustness) and the TabWak anchor (avg 7.20, different domain but comparable rigor).

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>