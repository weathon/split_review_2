## Summary
Spherical Watermark proposes an encryption-free, lossless watermarking framework for diffusion models. Binary watermark bits are mixed with random padding via an invertible embedding matrix, normalized onto the unit sphere (forming a spherical 3-design), orthogonally rotated, and scaled by a chi-square-distributed radius to produce approximate Gaussian noise. The key claimed advantages over prior lossless methods are: elimination of per-image key storage, ~4 orders-of-magnitude faster extraction than PRC Watermark, and stronger adversarial robustness.

## Strengths

- **Concrete and large speedup** (Figure 4, Section 4.2): Extraction is ~4 orders of magnitude faster than PRC Watermark due to replacing belief-propagation decoding with simple majority-vote over a spherical 3-design. The time difference is directly traceable to the architectural choice, not experimental noise.
- **Elegant polar-decomposition design** (Theorem 3.2, Lemma 3.4): The factorization N(0,I) = χ(n)·Uniform(S^{n−1}) is a well-known but cleverly exploited result. Building a watermark scheme around it — with 3-wise independence from binary embedding enforcing the 3-design property — is a structurally clean and original contribution.
- **Strong adversarial robustness** (Table 2, Adv. rows): 98.12% ACC under WEvade-style attacks vs. 49–52% for all lossy methods. The structural link between losslessness and adversarial robustness (no detectable distributional signal means no attack surface) is well-motivated and empirically borne out.
- **Substantive ablations** (Tables 3–5, Figure 6): Module ablation, hyperparameter sweeps (s, N, l_m), ODE solver choice, and timestep variation all confirm robustness of the design and clarify what each component contributes.

## Weaknesses

### Fatal
None.

### Major

- **Formal theoretical guarantee (Eq. 2) overstates what is proved**: The undetectability requirement stated as Eq. 2 is *full computational indistinguishability* against any PPT adversary: |Pr[A(z_w)=1] − Pr[A(z)=1]| ≤ negl(ρ). However, Theorem 3.2 + Lemmas 3.3–3.4 only establish that z^(2) is a *spherical 3-design*, meaning it matches the continuous uniform distribution on S^{n−1} up to degree-3 polynomials. Lemma 3.4's converse — "if r²∼χ²(n) and u∼Uniform(S^{n−1}), then r·u ∼ N(0,I)" — requires u to be *exactly* uniformly distributed; z^(3) is a discrete approximation matching only up to degree-3 moments. A PPT adversary exploiting kurtosis or higher cumulants could in principle distinguish z_w from z. The paper itself acknowledges this in the abstract ("up to third-order moments") and Section 5 ("higher-order moments may deviate from the true prior"), but makes no connection back to Eq. 2. No cryptographic reduction, Berry–Esseen-type TV-distance bound, or distinguishing-advantage argument is provided to close the gap. The paper should either (a) weaken Eq. 2 to moment-based indistinguishability, (b) provide a quantitative bound on the distinguishing advantage as a function of l_x, or (c) invoke a formal approximation result. The adversarial robustness argument (Appendix E) rests on the losslessness guarantee; if the guarantee is only approximate, that argument requires re-grounding. The scheme works in practice, but the formal statement promises more than the theorems deliver.

### Minor

- **Gaussian Shading comparison in Figure 2 uses a degraded evaluation configuration**: Section 4.1 notes (in the experimental settings paragraph) that "with fixed keys, Gaussian Shading no longer achieves true losslessness," but Figure 2's analysis presents Gaussian Shading's 97% classification accuracy as evidence of a design weakness rather than a protocol limitation. Readers encountering Figure 2 before the detailed experimental settings paragraph may incorrectly conclude that Gaussian Shading's *design* is flawed when the detectability is an artifact of the fixed-key configuration used here. The caveat should appear in the main-text discussion of Figure 2.

### Trivial

- **Notation ambiguity in Eq. 6**: The embedding matrix dimension is written as "l_m = N × l_m", where l_m appears on both sides. The left-hand side should read l_{Nm} (or equivalent notation) to avoid self-referential ambiguity.

## Nice-to-Haves

- A higher-order statistical test (e.g., multivariate kurtosis, or MMD with a polynomial kernel of degree > 3) characterizing where the 3-design approximation breaks down as a function of l_x would substantially strengthen the empirical case for undetectability.
- A direct comparison with Gaussian Shading under its intended per-image-key configuration would clarify whether eliminating key management comes at any robustness cost.
- The losslessness → adversarial robustness argument (currently in Appendix E) should appear in the main text, since it is the central justification for the design philosophy.

## Removed Points

*These points are flagged as removed; treat them with caution.*

- **Strength (generic importance)**: "The paper addresses an important and timely provenance problem." Removed as generic; no specific evidence cited beyond scope.
- **Fatal-level severity assessment of theoretical gap**: The harsh critic labels the theoretical gap "structural" and potentially "fatal." Demoted to Major: the gap is real and on the page, but the scheme demonstrably works empirically. The paper is transparent about the approximation in the abstract and Section 5. Collapsing the score based on a formal mismatch that does not affect practical performance would misrepresent the contribution.
- **Missing per-image-key Gaussian Shading comparison as a fatal flaw**: The paper's scope is specifically to *improve on* the per-image-key limitation of Gaussian Shading; comparing against that configuration would be a nice validation, but its absence doesn't undermine the core claims.

## Novel Insights

The paper's most original observation is that normalized ±1/√l_x binary vectors constitute a spherical 3-design, and that combining this with an independent chi-square radius reproduces the polar decomposition of a multivariate Gaussian through degree-3 polynomial tests. The adversarial robustness advantage follows structurally from losslessness: without a distributional signal, gradient-based adversarial attacks (WEvade-style) that exploit distinguishable statistics gain no foothold. This "losslessness ⟹ adversarial robustness" connection, empirically verified in Table 2, is broadly applicable to any latent watermarking scheme built on distribution-preserving noise injection.

## Suggestions

1. **Tighten Eq. 2**: Derive a TV-distance or distinguishing-advantage bound as a function of l_x (e.g., via concentration inequalities on the finite 3-design's deviation from the continuous uniform distribution), or explicitly weaken the formal claim to match what is proved.
2. **Connect Section 5 to Eq. 2**: The limitations section acknowledges higher-order moment deviation; it should explicitly note this means the formal computational indistinguishability of Eq. 2 is not fully established by the current proofs.
3. **Highlight the Gaussian Shading evaluation caveat** near Figure 2 in the main text, not only in the experimental settings paragraph.
4. **Fix notation in Eq. 6**: l_{Nm} vs. l_m on the left-hand side.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| jlhBFm7T2J (PRC Watermark) | 6.50 | R1 | Direct predecessor; Spherical Watermark improves on efficiency and robustness but lacks PRC's formal cryptographic guarantee |
| ll2nz6qwRG (Hidden in the Noise) | 5.83 | R1+R2 | Two-stage distortion-free watermarking; accepted; comparable scope, this paper has stronger efficiency advantage |
| 1IwoEFyErz (Shallow Diffuse) | 6.00 | R1+R2 | Lossless subspace watermarking; similar quality tier; this paper has stronger ablations and efficiency story |
| 16O8GCm8Wn (VINE) | 6.40 | R2 | Robust watermarking with benchmark; accepted; similar impact level |
| T0ebbDO60R (SuperMark) | 3.75 | R1 | Training-free watermarking; rejected; weaker theoretical and empirical contribution |
| HexshmBu0P (Recipe for Watermarking) | 5.33 | R1 | Recipe/survey-style diffusion watermarking; rejected; less technically novel |
| f8S3aLm0Vp (DIAGNOSIS) | 6.50 | R1+R2 | Unauthorized-usage detection; accepted; different goal but similar quality tier |

**Round 1 bracket**: 5.5–7.0 (cluster of closely related papers ranging 5.83–6.5)

**Round 2 narrowing**: The closest topical anchor is PRC Watermark (6.5), which Spherical Watermark explicitly improves upon. PRC received 6.5 with rigorous formal cryptographic proofs as a core strength; Spherical Watermark improves on speed and robustness empirically but trades the rigorous formal guarantee for a weaker moment-matching argument. This places it slightly below PRC's anchor, but not significantly — the empirical evidence is strong, the design is novel, and the paper is transparent about the approximation. The Hidden in the Noise and Shallow Diffuse anchors (5.83–6.0) lack the efficiency story and breadth of ablation present here.

**Final calibration**: The paper sits at 6.5 — a genuine contribution with well-supported claims, substantive experiments, and a novel design, held back from a higher score primarily by the unresolved formal gap between the claimed indistinguishability definition and the proved moment-matching guarantee.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>