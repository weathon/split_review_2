Now I have sufficient calibration. Let me write the final review.

## Summary

This paper proposes Spherical Watermark, a fixed-key lossless watermarking scheme for diffusion models. The core innovation is a two-step construction: a binary embedding matrix mixes repeated watermark bits with random padding to achieve 3-wise independence, then a spherical mapping projects the result onto the unit sphere via a hypercube-vertex 3-design, applies an orthogonal rotation, and scales by a chi-squared radius to recover Gaussian noise. The method is evaluated on Stable Diffusion v1.5 and v2.1, demonstrating strong undetectability (classifier accuracy ~50%), computational efficiency (~4 orders of magnitude faster extraction than PRC Watermark), and competitive adversarial robustness.

## Strengths

1. **Clever and well-motivated construction (Sections 3.1–3.2).** The combination of a mixing matrix designed for 3-wise independence with the spherical 3-design property of normalized hypercube vertices is novel. This differs meaningfully from both the stream-cipher approach (Gaussian Shading) and the error-correcting code approach (PRC Watermark), and the theoretical grounding in spherical t-design theory is clean.

2. **Dramatic computational advantage over PRC Watermark (Figure 4).** Extraction is ~10⁴× faster than PRC's belief-propagation decoding. This is a practically significant gain — if the robustness claims hold, this alone makes the method preferable for deployment scenarios requiring high-throughput provenance verification.

3. **Strong adversarial robustness (Table 2, 'Adv.' columns).** Under WEvade adversarial attacks, the method achieves 98.12% ACC and 99.83% TPR, compared to PRC's 97.69% and 95.38%, while lossy methods collapse below 53% ACC. The paper's explanation (Appendix E) — that losslessness prevents adversaries from training effective detection classifiers — is plausible and supported by the data.

4. **Honest theoretical scope.** The paper explicitly states the guarantee holds "up to third-order moments" (abstract) and acknowledges in the limitations that "higher-order moments may deviate from the true prior." This is appropriately cautious about what the spherical 3-design formalism does and does not ensure.

## Weaknesses

### Fatal
None.

### Major

1. **Mismatch between the theoretical formalism and the actual analysis.** The problem definition (Section 3.1, Eq. 2–4) frames undetectability in terms of computational indistinguishability: PPT adversaries and a security parameter ρ such that the adversary's advantage is bounded by negl(ρ). The actual analysis (Section 3.3) proves a statistical property — that the watermarked noise matches the Gaussian up to third-order moments, with higher-order moments converging only as l_x → ∞. No computational hardness assumption is invoked, ρ is never instantiated, and the guarantee is asymptotic/statistical rather than computational. The formal language of Eq. 2–4 is therefore inappropriate for the analysis provided. The paper should either drop the computational-indistinguishability framing or provide a concrete reduction to a hardness assumption with an instantiated security parameter.

2. **"Encryption-free" framing elides a genuine security trade-off.** The paper presents the absence of per-image keys as an unqualified advantage (abstract, Section 1, Section 6). However, a fixed secret signature K = {T, C} means a single compromise — extracting the key from one API interaction or reverse-engineering the client — permanently breaks watermarking for *all* images generated under that model. Per-image key approaches (Gaussian Shading) provide forward secrecy: compromising one key does not affect other images. The paper does not discuss this trade-off at all. An adversary who obtains K can strip or forge watermarks from every image this model has ever produced or will produce. This is a structural limitation that should be acknowledged and weighed against the storage overhead it eliminates.

### Minor

3. **Ambiguous FID evaluation reference distribution.** The paper states (Section 4.1): "we employ the Fréchet Inception Distance (FID) measured against the unwatermarked output distribution." If the reference is the unwatermarked model output, the "Original" row in Table 1 should be near 0 (same distribution compared to itself), but it shows ~48. If instead FID is computed against real COCO images (standard usage), the description is wrong. Either way, the reader cannot determine which reference distribution was used. The conclusion (that "Ours" and "Original" are nearly identical) is likely unaffected, but the metric cannot be independently verified.

4. **Gaussian Shading comparison uses fixed keys.** The paper evaluates Gaussian Shading with fixed keys and notes it "no longer achieves true losslessness" (Section 4.1), then presents its detectability (97% accuracy, Figure 2) as evidence of inferiority. Gaussian Shading is designed for per-image keys; evaluating it in a mode it was not designed for conflates the keying design choice with the watermarking mechanism. The paper is transparent about this, but the framing exaggerates the advantage.

5. **"Lossless" is slightly overstated.** Clean ACC is 99.99% (Table 2), not 100%. The formal definition (Eq. 4) allows negligible error, and the paper does not claim exact 100% recovery under all conditions. However, the title and abstract use "lossless" in a way that implies exact invertibility through the full pipeline, whereas VAE encoding, ODE solving with numerical error, and rounding in extraction (Eq. 13) make the guarantee approximate rather than exact.

6. **FPR calibration for TPR@1%FPR is not described.** The paper reports TPR @ 1% FPR but does not explain how the 1% FPR threshold is calibrated for the proposed method. For a scheme that claims losslessness, the false-positive analysis is important — if an unwatermarked image's extracted noise matches some user's expected signature by chance, what is the probability? This should be discussed.

7. **Limited model generalization.** The paper claims the method "can generalize to any generative model with a Gaussian prior" (Section 5) but evaluates only on Stable Diffusion (v1.5, v2.1). Testing on at least one non-SD architecture (e.g., a GAN with Gaussian noise input, or a different diffusion backbone like Imagen) would substantiate this claim.

### Trivial

8. **Algorithm 1** uses `RandomPermutation` but does not specify how this is seeded or whether it is reproducible across invocations.
9. **Theorem 3.1** states the 3-wise independence guarantee holds when both **m** and **r** are independent Bernoulli(1/2) bits. In practice, **m** is fixed, so the guarantee holds only over the randomness of **r**. This should be acknowledged.

## Nice-to-Haves

- A concrete instantiation of the security parameter ρ would give practitioners a way to reason about the trade-off between capacity and security.
- The capacity comparison with PRC (Figure 6a) uses only JPEG-70; showing robustness across multiple distortion types at high capacity would strengthen the claim.
- An empirical or theoretical analysis of what an adversary knowing K can do (remove watermarks, forge them, extract K from a single image) would make the "encryption-free" claim more precise.

## Removed Points

These points were raised by the harsh critic but are removed for the following reasons:
- **"QR decomposition is not unique"** (Section-by-Section Notes): The paper states C is stored as part of the fixed signature and reused exactly, not regenerated. The non-uniqueness of QR does not affect the pipeline since C is stored directly.
- **"Comparison with PRC on capacity uses only JPEG-70"**: Moved to Nice-to-Haves above; it is a limited but not invalid comparison.
- **"Ablation on modules incompletely described"**: The description is sufficient for the purpose of ablation — replacing spherical mapping with "Gaussian Shading transform" is ambiguous, but the ablation's purpose (showing the binary embedding is essential) is clear.
- **"No discussion of false positive rate calibration"**: Retained as weakness #6 above.

## Novel Insights

Beyond the paper's own contributions, the review process surfaces a deeper tension that the paper does not fully engage with: the method achieves empirical undetectability through statistical moment-matching (spherical 3-design) rather than computational hardness, yet the paper borrows cryptographic formalism (PPT adversaries, negligible functions) that the analysis does not deliver. This is not just a presentational flaw — it reflects an unresolved question about what kind of guarantee is appropriate for this class of scheme. Cryptographic lossless schemes (PRC) pay substantial computational cost for formal guarantees; moment-matching schemes (this paper) are fast but provide asymptotic/approximate guarantees. The paper would benefit from explicitly discussing this trade-off rather than presenting its approach as a straightforward improvement.

## Suggestions

1. Align the theoretical framing with the analysis: replace the computational-indistinguishability formalism (Eq. 2–4) with an explicit statement that the guarantee is statistical (moment-matching up to degree 3, with asymptotic convergence), or provide a proper reduction to a hardness assumption with an instantiated ρ.
2. Add a discussion of the fixed-key security trade-off, including the forward-secrecy advantage of per-image key approaches and the practical scenarios where each design is preferable.
3. Clearly state the FID reference distribution and, if it is real COCO images, correct the text in Section 4.1. Consider reporting KID or LPIPS as a secondary metric.
4. Describe how the 1% FPR threshold is calibrated in the extraction pipeline.
5. Test on at least one non-Stable-Diffusion generative model to support the generalization claim.

## Score and Decision

**Calibration Anchors:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| jlhBFm7T2J.md (PRC Watermark) | 6.50 | R1 | Most directly comparable lossless scheme; stronger theory but weaker empirical robustness and slower |
| ll2nz6qwRG.md (Hidden in the Noise) | 5.83 | R1/R2 | Similar-level contribution; two-stage watermark with comparable evaluation breadth |
| 1IwoEFyErz.md (Shallow Diffuse) | 6.00 | R1/R2 | Rejected despite score 6; had incomplete ablations — this paper's evaluation is more thorough |
| mDKxlfraAn.md (Image Watermarks Removable) | 6.40 | R2 | Watermark removal paper; not directly comparable but in the same venue quality band |
| HexshmBu0P.md (Recipe for Watermarking) | 5.33 | R1 | Lower-scored watermark paper; less technical depth |

**Round 1 bracket:** [5.5, 6.5]

**Narrowing:** The paper is slightly weaker than PRC Watermark (6.50) in theoretical rigor due to the formalism-mismatch issue, but stronger empirically (speed, adversarial robustness). It is comparable to Shallow Diffuse (6.00, rejected) and Hidden in the Noise (5.83, accepted), but has a more thorough evaluation than the former and a cleaner construction than the latter. The core flaws are fixable framing issues rather than methodological invalidity.

**Final Score:** 6.0 — The method is novel and empirically strong, but the theoretical overclaim and the omitted security trade-off discussion prevent a higher score. With revision addressing these issues, the paper would be a solid contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>