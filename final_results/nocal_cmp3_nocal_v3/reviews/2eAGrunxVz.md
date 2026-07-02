## Summary

This paper proposes Spherical Watermark, a method to embed binary watermarks into the latent Gaussian noise of diffusion models without modifying model weights. The approach has three modules: (1) binary embedding that mixes repeated watermark bits with random padding via an invertible matrix, (2) spherical mapping that projects the result onto the unit sphere, rotates it, and scales it by a chi-square-distributed radius, and (3) integration into the diffusion process. The method eliminates per-image key storage (required by Gaussian Shading) and avoids the heavy cryptographic decoding of PRC Watermark while maintaining undetectability and achieving strong robustness.

## Strengths

- **Elimination of per-image key management (Section 3.2).** Prior lossless methods (Gaussian Shading) require a unique key and nonce per generated image. Spherical Watermark replaces this with a single fixed signature {T, C}. This is a genuine practical improvement over the Gaussian Shading line of work.

- **Massive computational advantage over PRC Watermark (Figure 4, Section 4.2).** Extraction is roughly four orders of magnitude faster (~10^−3.5 s vs. ~10^1.0 s). The comparison correctly isolates the watermark transformation from diffusion sampling/inversion, which is the right design choice for comparing the core methods fairly.

- **Stronger adversarial robustness than existing lossless methods (Table 2).** Under WEvade attacks, Spherical Watermark achieves ACC=98.12% and TPR=99.83% vs. PRC Watermark's 97.69%/95.38% and Gaussian Shading's 88.06%/99.23%. The explanation—that lossy embeddings enable trained classifiers which can be adversarially attacked—is coherent and supported by the data.

- **Better capacity scaling than PRC (Figure 6(a)).** Spherical Watermark maintains high detection rates across the full capacity range (l_m up to ~4000), while PRC Watermark's decoding fails entirely beyond l_m=2000. This is practically meaningful for large-payload applications.

- **Non-trivial theoretical analysis (Section 3.3).** The connection between 3-wise independent binary vectors and spherical 3-designs is not obvious, and the proof chain from 3-wise independence → spherical 3-design → rotated 3-design → approximate Gaussian provides formal grounding that most prior watermarking papers lack. This is a genuine contribution beyond the empirical results.

## Weaknesses

### Fatal

None.

### Major

- **"Exact Gaussian" claim overstates what the spherical 3-design proves.** The abstract states the method can "recover exact multivariate Gaussian noise" and calls the scheme "lossless." However, Theorem 3.2 shows the distribution on the sphere is a *spherical 3-design* — an *approximate* uniform distribution that matches moments only up to degree 3. Lemma 3.4 proves that exact Gaussian noise requires *exact* uniform distribution on the sphere (plus chi-square radius and independence), which is not what the method delivers. The paper acknowledges this in the Limitations section ("higher-order moments may deviate") and uses "≈" in Lemma 3.4, but the abstract, introduction, and contribution list use language implying exact equivalence. Additionally, the "lossless" label depends on DDIM inversion, which the paper itself (Section 3.1) calls an "approximate inverse mapping." The core method is sound; this is a framing gap that must be corrected before publication. The paper should reframe its theoretical guarantee as "matching the Gaussian prior up to third-order moments, with empirical indistinguishability."

### Minor

- **Gaussian Shading comparison uses fixed keys without showing per-image-key performance (Section 4.1).** The paper acknowledges that "with fixed keys, Gaussian Shading no longer achieves true losslessness" and then compares Spherical Watermark (designed for fixed keys) against Gaussian Shading in this degraded mode. This makes it impossible to separate how much of the robustness gap (Table 2: 88.06% vs. 98.12% adversarial ACC) is due to the method itself vs. the key-management decision. Including Gaussian Shading with per-image keys (its intended mode) would clarify this.

- **Figure 5 caption is inconsistent with the main text and uses undefined metrics.** The main text (line 273) states the figure compares against PRC Watermark, but the caption refers to a "Diffusion" baseline. The abbreviations "REC ACC" and "DNR ACC" appear in the caption but are never defined anywhere in the main text, making the figure difficult to interpret as presented.

- **No formal statistical test for Gaussianity.** The paper's central distributional claim is that watermarked noise is "statistically indistinguishable" from Gaussian, but the evaluation relies entirely on a binary classifier accuracy test (Figure 2). A formal goodness-of-fit test (e.g., Mardia's test for multivariate normality, Anderson-Darling) would provide complementary evidence and is standard for this type of claim.

- **No finite-sample bound quantifying the approximation.** The theory shows that as l_x → ∞, marginal coordinates converge to N(0, 1/l_x) (Lemma 3.3), but no finite-sample bound on the divergence (e.g., total variation, Wasserstein) between the spherical-3-design-based distribution and the true Gaussian is provided. This is a gap in the theoretical analysis.

### Trivial

- **Notation reuse in Eq. 6.** The equation writes l_m = N × l_m, redefining l_m in a confusing way. The superscript on the left l_m (l_m with a tilde or prime) is visually hard to distinguish from l_m.

## Nice-to-Haves

- Include a per-image-key variant of Gaussian Shading as an additional baseline to quantify the degradation from fixed keys.
- Report a formal multivariate normality test (Mardia, Henze-Zirkler) on the watermarked latents.
- Discuss whether the 1% FPR operating point (used for TPR reporting) is sufficient for deployment scenarios where false accusations carry high cost.
- Evaluate undetectability against more powerful classifiers (e.g., ViT) for completeness.

## Removed Points

These points were flagged in the input but are removed (with brief justification):

- *"Encryption-free" label criticism* — The paper uses "encryption-free" to contrast with Gaussian Shading's stream cipher and PRC's cryptographic constructs, not to claim there are no secrets. The Signature {T, C} is a fixed secret key, but the paper never claims otherwise. This is a semantic distinction, not a substantive flaw.

- *Asymmetric watermark bit lengths (32-bit vs. 512-bit)* — The paper explicitly explains that traditional methods embed 32-bit watermarks while latent methods use 512-bit. This is a standard design choice explained in the text.

- *Request for ViT/stronger classifiers for undetectability* — Demoted to nice-to-have; the current 2-layer MLP + ResNet-18 evaluation is standard in the watermarking literature.

- *Request for larger dataset justification* — The paper states 1000 prompts per dataset and explains the image-level evaluation uses 100 users × 10 images. The design is adequately described.

- *"Encryption-free" criticism (duplicate)* — Already discussed above.

## Novel Insights

None beyond the paper's own contributions. The reviewer observations primarily concern framing, comparison transparency, and experimental completeness — not new scientific insights about the method.

## Suggestions

1. **Reframe the theoretical claims throughout the paper.** Replace "exact multivariate Gaussian noise" in the abstract with "noise matching the Gaussian prior up to third-order moments, with empirical evidence of statistical indistinguishability." Distinguish clearly between the theoretical guarantee (3rd-order approximation) and the empirical evidence (classifier-based undetectability).

2. **Add Gaussian Shading with per-image keys** as an additional row in Table 2 to separate the effect of key management from inherent robustness.

3. **Fix Figure 5's caption** to match the main text (replace "Diffusion" with "PRC Watermark") and define "REC ACC" and "DNR ACC" in the caption or main text.

4. **Add a formal normality test** (e.g., Mardia's test) on the watermarked latents to strengthen the distributional claim.

5. **Clarify Eq. 6 notation** so l_m and N×l_m are visually distinguishable.

## Score and Decision

The paper presents a clever, empirically strong method with genuine practical advantages (no per-image key storage, 4-orders-of-magnitude faster extraction than PRC, superior adversarial robustness). The core method is sound and the contributions are significant. The main weaknesses are in framing (overclaiming "exact" Gaussian guarantees) and in a somewhat asymmetric comparison with Gaussian Shading — both fixable without rewriting the method or experiments.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>