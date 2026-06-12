Now I'll produce the final consolidated review.

**Round 1 Bracket**: Based on the calibration search, the most direct anchors are the PRC watermark paper (6.50, accepted), Shallow Diffuse (6.00, rejected), Hidden in the Noise (5.83, accepted), and Spread them Apart (4.40, rejected). The paper clearly sits above Spread them Apart and is comparable to Shallow Diffuse and Hidden in the Noise. The narrowest plausible range is 5.5–6.5.

**Final Score**: 6.0

Here is the final review:

---

## Summary

Spherical Watermark proposes a lossless watermarking framework for diffusion models. It converts binary watermark bits into Gaussian noise via three invertible modules: binary embedding (mixing repeated watermark bits with random padding to achieve 3-wise independence), spherical mapping (projecting onto the unit sphere, applying a fixed orthogonal rotation, and rescaling by a chi-squared radius), and standard diffusion integration. The key theoretical contribution is proving that the intermediate vectors on the sphere form a spherical 3-design, matching the uniform distribution up to third-order moments, and that the final noise is a standard Gaussian by polar decomposition. The method eliminates per-image key storage required by Gaussian Shading and achieves substantially faster extraction than PRC Watermark.

## Strengths

1. **Clever spherical 3-design construction with formal moment guarantees (Theorem 3.2, Lemmas 3.3–3.4)**. The paper proves that the set of intermediate vectors z^(2) on the unit sphere constitutes a spherical 3-design, meaning the watermarked noise matches the target Gaussian up to third-order moments. This is a formally bounded distributional guarantee that prior lossless methods do not provide — Gaussian Shading guarantees marginal correctness but does not analyze joint moments, and PRC's guarantees are about bit-decoding rather than distributional. The polar decomposition argument (Lemma 3.4) elegantly connects spherical uniformity to the Gaussian distribution.

2. **Elimination of per-image key management (Section 3.2, Build Phase)**. The method constructs a single fixed signature {T, C} during an offline build phase and reuses it for all images. This is a genuine practical advantage over Gaussian Shading, which requires a distinct cipher key and nonce per image. The paper shows empirically (Table 2) that watermark extraction remains highly accurate (99.99% ACC clean, 98.12% ACC adversarial) with this fixed-key setup, providing evidence that encryption-wide per-image overhead is unnecessary.

3. **Extraction roughly four orders of magnitude faster than PRC Watermark (Figure 4, Section 4.2)**. The extraction time is ~10^−3.5 s for Spherical Watermark vs. ~10^1.0 s for PRC Watermark — a gap of about 4 orders of magnitude. This is a direct consequence of avoiding belief-propagation decoding and represents a clear practical benefit.

4. **Sustained detection at large watermark capacities where PRC fails entirely (Figure 6a, Section 4.2)**. Under JPEG-70 compression, PRC's decoding "deteriorates rapidly and fails entirely beyond l_m = 2000," while Spherical Watermark maintains high detection rates across the full tested capacity range. This is a qualitative robustness advantage, not merely incremental.

5. **Systematic module ablation isolating each component's contribution (Section 4.3, Figure 6b,c)**. Removing either the binary embedding (B) or the spherical mapping (S) causes sharp degradation in undetectability or robustness, cleanly validating the design rationale. The parameter ablation (Table 3) shows the expected trade-offs for s and N, and the ODE solver/timestep ablations (Tables 4, 5) demonstrate robustness to these choices.

## Weaknesses

### Major

1. **The comparison against Gaussian Shading uses a deliberately weakened configuration, undermining the claim of "outperforming lossless approaches."** The authors acknowledge (line 193): "Note that with fixed keys, Gaussian Shading no longer achieves true losslessness." With this setup, GS predictably produces degraded FID (Table 1: GS FID ~49–51 vs. original ~46–49) and becomes detectable (97% classifier accuracy). The paper then uses these results as evidence for the Abstract's claim of outperforming "both lossy and lossless approaches" and the Conclusion's claim of "outperforming existing schemes." The correct comparison would evaluate GS with per-image keys (its designed configuration, which is lossless by construction) on undetectability metrics. The paper does not report this configuration anywhere. As a result, readers cannot assess whether Spherical Watermark achieves comparable undetectability to a properly-configured lossless baseline, or whether its main advantage is purely operational (key management + speed). The PRC comparison is fair, but the headline claim about "lossless approaches" in the plural is unsupported.

2. **The theoretical guarantee is stated more strongly than what is actually proven.** The Abstract claims watermarked noise is "statistically indistinguishable from a standard multivariate normal distribution," and the Introduction claims it is "provably... statistically indistinguishable." Section 3.3 states "z_w is distributed as N(0, I_lx)." The actual proof (Theorem 3.2) shows that z^(2) forms a spherical 3-design — meaning the distribution matches the uniform sphere up to third-order moments. The paper acknowledges this gap in the Limitations (line 332: "higher-order moments may deviate from the true prior"), but the framing throughout the Abstract, Introduction, and claim statements is substantially stronger. A distribution matching up to third-order moments is not necessarily "provably indistinguishable" in the sense of Eq. 2's computational indistinguishability requirement, since an adversary with access to 4th-order statistics could in principle distinguish it. The paper should state the guarantee as "matches up to third-order moments" rather than implying full provable indistinguishability from standard Gaussian noise.

### Minor

3. **Under post-processing attacks, even weakened Gaussian Shading outperforms Spherical Watermark by a non-trivial margin that the paper understates.** From Table 2: GS Post-Processing ACC 98.43% vs. Ours 95.02%, GS Post-Processing TPR 99.97% vs. Ours 97.50%. This is a consistent 2-3 percentage point gap. The paper calls this "a slight robustness trade-off relative to Gaussian Shading" (line 271), which downplays the gap. The advantage under adversarial attacks (Ours 98.12% vs. GS 88.06%) is a real and important advantage, but the post-processing comparison should be presented more honestly rather than minimized.

4. **The handling of random padding r for extraction is underspecified, creating ambiguity about whether per-image storage is truly eliminated.** The paper states r is "drawn i.i.d. from a Bernoulli(1/2) distribution on each invocation" (line 76). For the extractor to invert the watermark, it must know r. If r is stored per-image, this re-introduces the key-management overhead the method claims to eliminate. If r is derived deterministically (e.g., from a seed or user ID), this must be explained. The paper provides no specification for how r is shared between embedder and extractor.

### Trivial

5. **Notational issue in Eq. 6.** The equation defines "l_m = N × l_m" which is self-contradictory — the same symbol l_m is used for two different quantities (original watermark length vs. its N-repeat length).

## Nice-to-Haves

- Add a comparison against Gaussian Shading with proper per-image keys on undetectability (binary classifier accuracy). This would show that Spherical Watermark achieves the same undetectability as a properly lossless baseline while eliminating key storage — which is the actual claim that matters.
- Discuss model-shift robustness: what happens if the extractor uses a different version of the diffusion model or a fine-tuned variant?
- Consider specifying wall-clock times (in ms) for the extraction comparison in addition to the log-scale bar chart, to aid interpretability.

## Removed Points

These points were raised by reviewers but removed per the filtering rules:

- **"Missing appendix/proofs for Theorem 3.1"**: The appendix is part of the original submission but was stripped by the PDF parser. This is not an author issue.
- **"FID measured against unwatermarked distribution needs clarification in caption"**: The caption and text (Section 4.1) state this clearly enough for the intended comparison.
- **"No evaluation of extraction under model mismatch"**: This is a nice-to-have extension beyond the paper's stated scope; not a core weakness.
- **"DDIM inversion is computationally expensive"**: This is inherent to diffusion-model-based extraction in general, not specific to this method. The paper's contribution is in the embedding/extraction transforms, not the inversion process.
- **"l_c factor specification is underspecified"**: The paper gives an example (l_c = ⌊√(l_x)⌋) in footnote 1, which is sufficient for reproducibility.
- **"Related work missing"**: Per policy, this cannot be verified without external sources.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Revise the Gaussian Shading comparison.** Include GS with proper per-image keys on undetectability metrics. Then cleanly separate the discussion of (a) the practical advantage (no key management) from (b) claims of quantitative superiority in undetectability. Currently these are conflated.

2. **Sharpen the theoretical language.** Replace "provably indistinguishable from standard Gaussian" with "matches the first three moments of the standard Gaussian; higher-order deviations are bounded in practice" throughout the Abstract, Introduction, and claim statements. This would be more credible and still impressive.

3. **Specify the r derivation protocol.** Clarify whether the random padding vector r is derived deterministically from a seed shared with the extractor, or stored per-image. If the latter, explain how this differs from Gaussian Shading's key management.

4. **Acknowledge the post-processing robustness gap with GS more honestly.** Present the 2-3% gap as a trade-off rather than "slight," while highlighting the adversarial robustness advantage.

## Score and Decision

**Round 1 bracket**: 5.5–6.5, based on comparison with the PRC watermark paper (6.50, accepted), Shallow Diffuse (6.00, rejected), Hidden in the Noise (5.83, accepted), and VideoShield (5.83, accepted). The paper is clearly stronger than Spread them Apart (4.40, rejected).

**Final calibration**: PRC watermark (6.50) is the most directly comparable anchor — it has stronger cryptographic guarantees but worse practical performance (slower extraction, poorer capacity scaling). The current paper has a genuine, novel contribution (spherical 3-design approach, eliminated key management, faster extraction, better capacity) but is weakened by the unfair GS comparison and overstated theoretical framing. These issues are fixable. The overall contribution is comparable to Hidden in the Noise (5.83) and somewhat below the PRC paper (6.50).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>