## Summary

This paper proposes Spherical Watermark, a watermarking scheme for diffusion models that embeds binary messages into the Gaussian noise prior without modifying model weights. The method uses binary linear encoding (with repetition codes and random padding), spherical projection to the unit sphere, orthogonal rotation, and chi-square scaling to produce noise that is theoretically indistinguishable from standard Gaussian up to third-order moments. The key claimed advantages over prior lossless schemes (Gaussian Shading, PRC Watermark) are: (1) no per-image key storage, (2) competitive robustness, and (3) lower computational overhead.

## Strengths

- **Elimination of per-image key management is a genuine practical contribution.** Gaussian Shading requires a unique key and nonce per generated image, creating storage and synchronization overhead; PRC replaces this with cryptographic error-correcting codes that add decoding latency. Spherical Watermark uses a single fixed signature for all images, which is a clean operational improvement well-motivated in the paper (Section 2).

- **The spherical-mapping construction is conceptually elegant and mathematically sound.** The pipeline (binary embedding → map to ±1/√l_x on the unit sphere → orthogonal rotation → chi-square scaling) naturally converts discrete bits into continuous Gaussian-like noise. The use of the polar decomposition of the Gaussian (Lemma 3.4) to justify the construction is correctly stated.

- **Undetectability evidence is convincing.** Table 1 shows FID values for the proposed method that are essentially identical to the unwatermarked baseline (e.g., 48.12 vs 48.13 on COCO SD v1.5), matching PRC and outperforming every other baseline. The classifier experiments (Figure 2) showing near-chance (50%) detection for the proposed method and PRC, while Tree-Ring and Gaussian Shading (with fixed keys) are detected at 97–100%, provide clear empirical support.

- **Robustness under adversarial attacks is strong.** In Table 2, the proposed method achieves 99.83% TPR under adversarial conditions, substantially higher than every lossy baseline and slightly higher than PRC (95.38%). Computational efficiency results (Figure 4) show extraction roughly four orders of magnitude faster than PRC.

## Weaknesses

### Fatal
None.

### Major

1. **Theoretical presentation gap in the main text.** The paper's central theoretical claim (Theorem 3.2) states that the set of z^(2) points forms a spherical 3-design, but the main text provides insufficient reasoning for why this follows from the stated properties. Specifically: the paper asserts that because z^(2) has entries ±1/√l_x and is 2-wise and 3-wise independent, the set of its possible values is a spherical 3-design. The support has only 2^{l_m+l_r} points (≈2^{1024} with default parameters), far fewer than the 2^{l_x} (≈2^{16384}) hypercube vertices. Why this specific subset inherits the spherical 3-design property from the full hypercube is a non-trivial claim that requires the reader to reconstruct a geometric argument from 3-wise independence of the distribution. While the paper correctly states that full proofs are in Appendix C (line 157), the main text's presentation leaves a noticeable gap. This weakness does **not** mean the claim is wrong — the Appendix C proof may well be correct — but the main text should at least sketch the reasoning so readers can follow the logic without consulting the appendix. As written, this gap weakens the paper's claim of providing a clear theoretical guarantee.

2. **FID methodology is underspecified.** The paper reports FID values of ~48 for unwatermarked Stable Diffusion v1.5 on COCO (Table 1). These absolute values are unusually high — typical FID for SD v1.5 on COCO is substantially lower — suggesting the FID computation may use small sample sizes (the paper specifies 1000 prompts but does not state the reference set size or the exact comparison protocol). The paper states FID is "measured against the unwatermarked output distribution" (line 229) without clarifying whether this means comparing the 1000 generated images against the full COCO validation set, against a second set of generated images, or against some other reference. The relative comparisons (Ours ≈ Original ≈ PRC) are internally consistent and still informative, but the underspecification prevents readers from assessing whether the metric is being computed in a standard way or whether ceiling effects are at play.

### Minor

1. **Gaussian Shading comparison framing.** The paper evaluates Gaussian Shading with fixed keys and notes (line 193) that this configuration "no longer achieves true losslessness." This comparison is valid for the fixed-key deployment scenario the paper advocates, but the high-level framing (abstract, introduction) presents this as evidence that Gaussian Shading is *inherently* detectable rather than detectability arising from key reuse in a scheme not designed for it. The paper's own contribution — fixed-signature losslessness — is strong enough to stand on its own without this framing.

2. **Higher-order moments limitation treated too lightly.** The Limitations section (line 332) acknowledges that "higher-order moments may deviate from the true prior" but frames this as a minor caveat. Since the theoretical guarantee only covers up to third-order moments, this is the ceiling of the approach, not a peripheral issue. The paper would benefit from a more forthright discussion of what practical consequences (if any) this could have.

3. **Ablation descriptions are vague.** In Section 4.3, the module ablation describes variants opaquely: "omit the spherical mapping S and substitute the Gaussian Shading transform" (line 291) — it is not clear what "substitute" means operationally. Results are described only qualitatively via figures that cannot be fully parsed from the extracted text.

### Trivial

1. **Equation (6) notation slip.** The equation writes "l_m = N × l_m" (line 84), using l_m for both the original message length and the repeated message length, which is dimensionally inconsistent. The paper later uses l_{Nm} for the repeated length (line 191); the notation in Equation (6) should be harmonized.

2. **Algorithm 1 notation ambiguity.** The algorithm uses "l_m" in the tensor initialization (0^{N × l_m × l_r}, line 96) to mean the original watermark length, but the loop variable j (line 98) iterates over l_m (original length), making the tensor dimensions clear only after close reading. The reshape step (line 107) from (N, l_m, l_r) to (l_m, l_r) is also ambiguous about which l_m is which.

3. **Classifier-free guidance mismatch.** Generation uses guidance scale 7.5 while inversion uses scale 1.0 with empty prompts (line 191). The empirical results show this works well, but a brief discussion of why the mismatch is tolerated would strengthen the paper.

## Nice-to-Haves

- Report a two-sample statistical test (e.g., maximum mean discrepancy) directly on the latent noise vectors to provide a cleaner empirical test of the distributional claim beyond classifier-based detection.
- Clarify the effective code rate comparison with PRC (the raw rate is ~3%; stating PRC's rate in the experiments would allow readers to contextualize the robustness comparison).
- Describe the TPR@1%FPR threshold calibration procedure for the proposed method, since extraction is deterministic (rounding + majority vote).

## Removed Points

These points from the input review are excluded with justification:

- **"True Ring" in Figure 2 caption** — This is a parser artifact from embedded figure text, not an author error. The original figure label is almost certainly "Tree-Ring."

- **Reproducibility concerns about Algorithm 1 permutations** — The random permutation in Algorithm 1 is used during the build phase to construct the fixed matrix T. It is not a runtime parameter. The algorithm is sufficiently specified for its purpose.

- **"Existence of Appendix C"** — The harsh critic's concern about proofs being "relegated to Appendix C, which is not available for review" is addressed by the fact that appendices exist in the original submission. The critic's substantive concern about the presentation gap in the main text is retained as a Major weakness (see above).

- **Request for formal two-sample test on latent noise** — Moved to Nice-to-Haves. This would strengthen the paper but is not a core weakness; the existing classifier-based detection evidence is already strong.

## Novel Insights

The most interesting observation emerging from the review is that the paper's core practical differentiator (no per-image key storage) is arguably more significant than its theoretical framing suggests. The spherical mapping approach achieves this fixed-signature property through pure geometry (spherical 3-design + polar decomposition) rather than cryptography, which is a qualitatively different design point from the PRC/Gaussian Shading line of work. This geometric perspective is the paper's most distinctive intellectual contribution, even though the theoretical guarantee is limited to third-order moments.

## Suggestions

1. Expand the main-text justification of Theorem 3.2 to sketch how 3-wise independence of z^(1) entries translates to the spherical 3-design property for z^(2), given the reduced support size. Even a paragraph of geometric intuition would bridge the current gap.

2. Specify the FID computation protocol explicitly: number of reference images, whether the reference is the full COCO validation set or a generated set, and whether the same prompts are used for all methods.

3. Reframe the Gaussian Shading comparison to clearly separate the fixed-key ablation (showing cost of key reuse) from the standard-configuration comparison with PRC.

4. In Algorithm 1, use distinct variable names for the original message length and the repeated message length to avoid confusion.

## Score and Decision

**Calibration details.** Round 1 bracket: 5.0–7.0. Anchors consulted:
- PRC Watermark paper (avg 6.50, Accept; scores 8,6,6,6) — closest competitor, stronger theoretical presentation but similar empirical methodology.
- Shallow Diffuse (avg 6.00, Reject; scores 6,6,6,6) — similar presentation issues led to rejection despite solid technical content.
- WMAdapter (avg 5.20, Reject; scores 6,6,6,5,3) — weaker novelty, less rigorous evaluation.
- SuperMark (avg 3.75, Reject; scores 3,5,5,5,3,3,3,3) — significant novelty and understanding gaps.
- A Recipe for Watermarking (avg 5.33, Reject; scores 5,6,5) — more of a survey/recipe, less novel.

The current paper is strongest in its practical contribution (fixed-signature operation) and empirical evaluation, but its theoretical presentation in the main text is sketchier than the PRC paper's. The weaknesses are addressable and do not undermine the core claims, placing it solidly in the borderline-to-accept range.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>