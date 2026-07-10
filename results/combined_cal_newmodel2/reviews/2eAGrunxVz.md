Now I have comprehensive calibration data. Let me compile the final review with the appropriate calibration-based score.

## Summary

This paper introduces Spherical Watermark, a lossless watermarking framework for diffusion models that embeds binary watermark messages into Gaussian noise inputs without per-image key storage. The method uses three modules: binary embedding (mixing watermark bits with random padding via an invertible matrix), spherical mapping (projecting onto the unit sphere, orthogonal rotation, and chi-square scaling), and diffusion integration. The paper provides theoretical analysis showing the watermarked noise forms a spherical 3-design (matching moments up to third order) and demonstrates strong empirical results on Stable Diffusion, including undetectability, computational efficiency (~4 orders of magnitude faster extraction than PRC), and improved robustness under attacks.

## Strengths

- **Conceptually clean method design (Section 3.2).** The three-module pipeline — binary embedding via invertible matrix T, spherical mapping (normalize → orthogonally rotate → chi-square scale), and diffusion integration — is well-structured with each step serving a clear purpose. The random padding vector r mixed via sparse matrix R, with r discarded after generation but its randomness diffused, is a clever trick to avoid per-image key storage. **Favorability: 11.32**

- **Theoretical analysis of moment matching (Section 3.3, Theorems 3.1–3.2, Lemmas 3.3–3.4).** Showing that z^(2) forms a spherical 3-design and matches the uniform spherical distribution up to third-order moments is a nontrivial contribution. The chain of reasoning (3-wise independent Bernoulli → hypercube vertices uniform on sphere → spherical 3-design → rotation invariance → chi-square scaling approximating Gaussian) is coherent. **Favorability: 15.95**

- **Dramatic computational efficiency advantage (Figure 4).** Extraction time is roughly four orders of magnitude faster than PRC Watermark (~10^1 s vs. ~10^{-3.5} s). This is a practically significant improvement documented clearly. **Favorability: 12.23**

- **Consistency with PRC on undetectability while improving on several robustness metrics (Table 2, Figure 5).** Both PRC and the proposed method achieve near-chance classification accuracy (undetectable). On post-processing and adversarial robustness, the proposed method achieves higher TPR (97.50% vs. 87.03% for post-processing; 99.83% vs. 95.38% for adversarial). **Favorability: 14.44**

## Weaknesses

### Major

- **The Gaussian Shading comparison is structurally misleading.** The paper tests Gaussian Shading with fixed keys across all images (line 193: "Note that with fixed keys, Gaussian Shading no longer achieves true losslessness"), then shows it is detectable (97% accuracy, Figure 2) with degraded FID (Table 1). Gaussian Shading's core design guarantees losslessness only when each image uses a unique key+nonce. By stripping this away, the evaluation weakens its main lossless competitor on the very property (undetectability) central to the comparison. The abstract's claim of "outperforming both lossy and lossless approaches" is then partially supported by these results. A valid comparison would either (a) evaluate Gaussian Shading with proper per-image keys (showing Spherical Watermark matches its undetectability while eliminating key management) or (b) clearly separate the comparison into two independent axes — undetectability and key-management overhead. The paper's real advantage over Gaussian Shading is key-management efficiency, not undetectability superiority. **Favorability: -1.78**

- **The theoretical guarantee is overstated relative to what is actually proven.** The introduction claims to "prove that the final noise is statistically indistinguishable from standard Gaussian noise" (line 26) and Section 3.3 states that "z_w is distributed as N(0, I)" (line 157). However, the proof only establishes third-order moment matching via the spherical 3-design property. Lemma 3.4's conclusion that z_w ~ N(0,I) requires u to be uniformly distributed on the sphere, but the paper only establishes that z^(3) is a spherical 3-design (matching moments up to degree 3) — not exact uniformity. The limitations section (line 332) acknowledges "higher-order moments may deviate," but the abstract and introduction do not carry this qualification. The abstract does say "up to third-order moments" in one place, but other parts of the paper make stronger unqualified claims. This inconsistency should be resolved by consistently presenting the result as moment-matching up to order 3. **Favorability: 1.80**

### Minor

- **"Encryption-free" is an imprecise label.** The method requires signature K = (T, C) to be kept secret (line 82: "K is kept fixed and secret during runtime to prevent unauthorized removal"). This is a secret key — just not a per-image one. "Encryption-free" could suggest no secret material exists at all. A more precise description would be "per-image-key-free" or "fixed-key." The actual practical advantage (eliminating per-image key management) remains legitimate, but the framing overstates what is eliminated. **Favorability: 8.01**

- **Clean ACC is 99.99% rather than 100% (Table 2).** The rounding operation in extraction (Eq. 13, line 151) introduces small bit errors even under ideal conditions. While the paper reports this honestly and the "lossless" terminology in the literature refers to distributional preservation rather than bit-perfect recovery, the paper should clarify this distinction earlier rather than leaving it implicit. **Favorability: 6.30**

- **The FID values reported in Table 1 (46–51 even for "Original" unwatermarked images) are unusually high.** This warrants a brief explanation in the main text (e.g., whether FID is computed comparing generated images against other generated images rather than real images), as the absolute values may confuse readers even though the relative comparisons are valid. **Favorability: 6.82**

### Trivial

None.

## Nice-to-Haves

- Adding per-user traceability results (e.g., confusion matrix or per-user success rates) would strengthen the traceability claims.
- Quantifying the approximation gap (e.g., total variation distance or KL divergence between the 3-design distribution and true uniform distribution on the sphere) would strengthen the theoretical analysis.
- Reporting bit error rate (BER) alongside ACC would help readers understand practical reliability (99.99% ACC on 512 bits means ~0.05 errors per message on average).

## Removed Points

These points are flagged to be removed; treat them with caution.
- Critic's claim about Appendix E reference: REMOVED. The appendix exists in the original submission; the parser strips it from the review copy.
- Critic's claim about adversarial attack definition being missing: REMOVED. The paper references WEvade (Jiang et al., 2023) and Appendix F.4 for details. Missing appendix details are parser artifacts.
- Critic's suggestion about per-user traceability confusion matrix: Moved to Nice-to-Haves. Not a required criterion for acceptance.
- Critic's question about whether "100 distinct users" uses distinct messages: The paper says "100 distinct users" which implies distinct messages per user. This is a very minor clarity point.

## Novel Insights

Beyond the paper's own contributions, the review process surfaces one noteworthy observation: the paper's claimed advantage over Gaussian Shading is fundamentally about key-management efficiency, not undetectability — yet the evaluation is framed to suggest undetectability superiority by using a deliberately weakened configuration of Gaussian Shading. The authors should restructure their narrative to clearly separate these two axes. This reframing would strengthen rather than weaken the paper, since eliminating per-image key storage while maintaining losslessness is itself a meaningful practical contribution.

## Suggestions

1. Add a proper evaluation of Gaussian Shading with per-image keys (or clearly reframe fixed-key results as demonstrating what happens when key-management is simplified, not as undetectability superiority).
2. Consistently qualify the theoretical guarantee throughout the paper as "moment-matching up to third order" rather than claiming exact distributional equivalence.
3. Replace "encryption-free" with "per-image-key-free" or "fixed-key" to more accurately describe the method's contribution.
4. Clarify early in Section 3 that "lossless" refers to the distributional property (statistically indistinguishable noise) rather than bit-perfect extraction, and note that extraction has a small residual error rate (~0.01%).

## Score and Decision

**Calibration summary:**

All anchors retrieved across rounds:

| Anchor Paper | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| PRC Watermark (jlhBFm7T2J) | 6.50 | R1 | Yes | Most directly comparable — this paper improves on PRC's efficiency and robustness but has weaker theoretical rigor and a Gaussian Shading evaluation issue PRC didn't have |
| Shallow Diffuse (1IwoEFyErz) | 6.00 | R1 | Yes | Similar watermarking space; this paper has stronger theoretical contribution but similar evaluation concerns |
| Hidden in the Noise / WIND (ll2nz6qwRG) | 5.83 | R2 | Yes | Accepted paper with less severe weaknesses; this paper's method is cleaner but WIND's evaluation was more complete |
| Spread them Apart (9XEBFywIW7) | 4.40 | R1 | Yes | Lower-scoring watermarking paper with more significant method issues |
| SuperMark (T0ebbDO60R) | 3.75 | R1 | Yes | Significantly weaker — limited novelty, insufficient experiments |
| Recipe for Watermarking (HexshmBu0P) | 5.33 | R2 | Yes | Similar scope but less theoretical depth |
| TabWak (71pur4y8gs) | 7.20 | R2 | Yes | Stronger paper with thorough experiments and clear novelty in a new domain |
| SAT-LDM (ETFfXGM3e4) | 5.50 | R2 | No | Similar watermarking space |
| DIAGNOSIS (f8S3aLm0Vp) | 6.50 | R2 | No | Different sub-area (data usage detection) |

**Bracket reasoning:**

Round 1 established the paper sits between 5.5 and 7.5 based on topic similarity. Round 2 narrowed by comparing against specific anchors. The PRC paper (6.50) is the most informative comparison point. My paper's draft has stronger favorability on strengths (11-16 vs PRC's 7-10) but its worst weakness (-1.78) is less severe than PRC's worst (-3.02). However, my paper's theoretical claim overstatement and Gaussian Shading comparison fairness issues are important concerns that PRC didn't share. The paper's method is clever and the efficiency results are impressive, but the evaluation framing needs correction. I place the paper slightly below the PRC anchor at **6.0**.

**Score:** Papers scoring 6.0 in this calibration set (e.g., Hidden in the Noise / WIND at 5.83 accepted, Shallow Diffuse at 6.00 rejected) show that this score range supports acceptance for papers with solid contributions and fixable weaknesses. My draft's items: the two MAJOR weaknesses have negative or near-zero favorability (-1.78 and 1.80), while the three MINOR weaknesses all have positive favorability (6-8 range), meaning they barely count as weaknesses. The strengths all have very high favorability (11-16). This profile — high-favorability strengths plus one costly weakness and one mildly negative weakness — supports a score that acknowledges real contributions but also notes significant framing issues. Compared to the PRC anchor, this paper has higher-rated strengths but its evaluation fairness issue (Gaussian Shading comparison) is a cleaner, more fixable problem than PRC's fundamental robustness limitations.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>