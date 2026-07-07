Now let me write the final consolidated review.

## Summary

This paper proposes Spherical Watermark, a watermarking method for diffusion models. The core idea maps binary watermarks to Gaussian noise via: (1) binary embedding that mixes repeated watermark bits with random padding using an invertible matrix over F₂, producing a 3-wise independent bitstream; and (2) spherical mapping that normalizes to the unit sphere, applies an orthogonal rotation, and scales by a chi-square radius. This yields noise matching the standard Gaussian up to third-order moments (spherical 3-design). The method eliminates per-image key storage and achieves extraction roughly 10,000× faster than the PRC baseline.

## Strengths

- **Novel geometric insight.** The connection between 3-wise independent binary sequences, spherical 3-designs, and the Gaussian prior via polar decomposition (Section 3.2–3.3) is elegant and well-motivated. Using a spherical 3-design so the distribution matches standard Gaussian up to third moments is a genuine intellectual contribution.

- **Dramatic computational advantage over PRC.** Extraction time is roughly four orders of magnitude lower than the PRC watermark (Gunn et al., 2025), as shown in Figure 4. For practical deployment, this is a decisive improvement that makes the method viable where PRC is too slow.

- **Elimination of per-image key management.** Unlike Gaussian Shading (Yang et al., 2024), which requires a unique key and nonce per image, this method uses a single fixed Signature, eliminating a real practical barrier (Section 3.2, Figure 1(a)).

- **Strong empirical undetectability against PRC and Tree-Ring.** Binary classifier experiments (Figure 2) show that watermarked noise is empirically indistinguishable from standard Gaussian noise when compared against PRC and Tree-Ring baselines, consistent with the spherical 3-design theory.

## Weaknesses

### Major

- **Unfair evaluation of Gaussian Shading.** The paper evaluates Gaussian Shading with **fixed keys** (line 193: "Note that with fixed keys, Gaussian Shading no longer achieves true losslessness"), which the paper itself acknowledges breaks Gaussian Shading's theoretical guarantees. This degraded version is then used as a baseline for undetectability (Figure 2: 97% detectability), FID (Table 1: inflated FID of ~50.7 vs Original ~48.1), and adversarial robustness (Table 2). Claiming superiority over Gaussian Shading in these dimensions from this comparison is misleading. The paper's genuine advantages over Gaussian Shading are in key storage and simplicity, not undetectability. The proper approach would be to evaluate Gaussian Shading as intended (with per-image keys) for detectability comparisons and separately discuss key storage costs.

- **Mismatch between cryptographic framing and actual guarantee.** The paper defines a computational indistinguishability framework (Eq. 2–4) with a security parameter ρ and polynomial-time adversaries, but ρ is **never instantiated or tied to any construction parameter**. The actual theoretical guarantee is statistical (matching up to third-order moments via spherical 3-design), not computational. As the paper partially acknowledges in the Discussion (line 332): "higher-order moments may deviate from the true prior." The formal definition in Section 3.1 is disconnected from the method and proofs — it does no work in the paper. This overstates the security guarantee.

### Minor

- **FID claims are overclaimed.** Table 1 shows that all methods' FID values overlap within 1-sigma error bars (e.g., on SD v1.5 COCO: Original 48.13±1.37, DwtDct 48.30±1.39, Ours 48.12±1.55). The paper states "only PRC Watermark and our method match the original in FID" — this cannot be supported from these overlapping intervals. Gaussian Shading's inflated FID is also partly an artifact of the fixed-key evaluation.

- **Confusing notation.** Line 84 defines `l_m = N × l_m` within the matrix equation, redefining the variable in place. The paper later uses `l_{Nm}` for a related quantity (line 153, line 191). This impairs readability.

- **Ablation design conflates removal with replacement.** The ablation (Section 4.3) replaces the spherical mapping module with "the Gaussian Shading transform," which is substituting an entirely different method's mechanism rather than a clean module removal. This makes the ablation results harder to interpret as evidence for the individual contribution of the spherical mapping component.

### Trivial

- Notation issue in Eq. 6 where `l_m` is redefined in place.

## Nice-to-Haves

- Empirically evaluating fourth-order moments (e.g., kurtosis of marginal distributions) would strengthen the undetectability claims beyond what the spherical 3-design theoretically guarantees.
- The paper could discuss the security implications of the shared fixed Signature: if the Signature K = {T, C} is leaked, all watermarks are forgeable/removable. This is a meaningful trade-off compared to Gaussian Shading's per-image keys where compromise is isolated.
- Formal significance tests would help support conclusions given overlapping error bars in Table 1.

## Removed Points

These points from the input review were removed for the following reasons:

- **"Lossless" claim imprecision** (Harsh Critic Issue 3). The paper explicitly defines "losslessness" as undetectability (line 56: "**Undetectability (Losslessness)**" — Eq. 2–3 formalize this as noise indistinguishability). The extraction is modeled as probabilistic with negligible error (Eq. 4), which is standard. The paper's usage is internally consistent; the criticism conflates embedding losslessness with extraction perfection.

- **Spherical 3-design interpretation concern** (Theorem 3.2). The critic questions whether the theorem applies to the distribution over (m, r) draws rather than a finite set. This framing — that the *distribution* yields a spherical 3-design — is standard in the design literature and not a flaw in the paper.

- **Statistical significance critique.** A generic critique applicable to most ML papers. The paper provides 1-sigma error bars over 5 runs, which is standard.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Re-evaluate Gaussian Shading with proper per-image keys** for the undetectability comparison, or restructure the comparison to clearly separate the key-storage discussion (where the paper has a genuine advantage) from detectability.
2. **Align the theoretical framing with the actual guarantee.** Replace the cryptographic indistinguishability language (Eq. 2–4) with a statistical indistinguishability framework matching what the spherical 3-design provides, or properly define ρ and connect it to a construction parameter.
3. **Tone down FID claims** to reflect that all methods' error bars overlap.
4. **Fix the notation in Eq. 6** to avoid redefining `l_m` in place (use `l'` or `l_{N_m}` consistently throughout).
5. **Restructure the module ablation** to compare against simply omitting the spherical mapping component rather than substituting a different method's mechanism.

---

## Score Calibration

**Round 1 bracket: 5.0–6.0**

**Anchors retrieved across all rounds:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| PRC Watermark (Christ & Gunn) | jlhBFm7T2J.md | 6.50 | R1 | Yes | Direct competitor; similar undetectable watermark space. Spherical Watermark has faster extraction but more evaluation issues (Gaussian Shading comparison problem). |
| Shallow Diffuse | 1IwoEFyErz.md | 6.00 | R1 | Yes | Another diffusion watermark; similar evaluation gaps, comparable contribution level. |
| Hidden in the Noise (Two-Stage) | ll2nz6qwRG.md | 5.83 | R1 | Yes | Similar space; less theoretical novelty but cleaner evaluation. |
| Spread Them Apart | 9XEBFywIW7.md | 4.40 | R2 (narrowing) | Yes | Weaker paper with scalability issues. Spherical Watermark has better structure and novelty. |
| SuperMark | T0ebbDO60R.md | 3.75 | R1 | Yes | Weak novelty, limited contribution. Spherical Watermark is significantly stronger. |

**Weighted-item comparison driving the final score:**

The paper's strongest shared features with the PRC anchor (6.50) are: genuine theoretical novelty (+4 equivalent), good image quality, and undetectability. However, unlike PRC whose main weakness was moderate robustness, this paper has two structural issues that weigh more heavily: (1) the Gaussian Shading evaluation is a fairness problem that undermines a central comparison, and (2) the cryptographic framing mismatch overstates the guarantee. These are similar in severity to the "limited novelty" and "insufficient experiments" criticisms that pulled SuperMark (3.75) down, though the paper under review has much stronger novelty. The paper is clearly above SuperMark (3.75) and Spread Them Apart (4.40) due to its genuine theoretical contribution and computational advantage, but the evaluation issues place it below the clean PRC paper (6.50). The closest comparator is Shallow Diffuse (6.00), which had similar evaluation gaps but cleaner comparisons. Given the need for the authors to redo a significant comparison and reframe a core theoretical claim, **5.5** reflects a borderline-accept with required revisions.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>