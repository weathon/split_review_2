Now I have all the data I need. Let me produce the final consolidated review.

## Summary

Spherical Watermark proposes a fixed-key lossless watermarking scheme for diffusion models. The method uses a binary embedding matrix (T) and a fixed orthogonal rotation (C) to convert watermark bits into Gaussian noise that is provably indistinguishable from the standard prior up to third-order moments. It eliminates per-image key management (needed by Gaussian Shading) and heavy cryptographic decoding (needed by PRC), achieving ~10⁴× faster extraction while maintaining strong undetectability and robustness.

## Strengths

1. **Fixed-signature design with practical advantages.** The paper's clearest contribution is replacing per-image (key, nonce) pairs (Gaussian Shading) and heavyweight cryptographic decoding (PRC) with a single fixed signature {T, C} and per-image randomness from only a padding vector. The ~10⁴× speedup in extraction time over PRC (Figure 4) makes this concrete, and the design is conceptually simpler than both prior lossless approaches.

2. **Spherical 3-design theoretical analysis.** Proving that z^(2) forms a spherical 3-design (Theorem 3.2) and that the final noise matches the standard Gaussian up to third-order moments (Lemma 3.3, Lemma 3.4) is a clean theoretical contribution. The connection between 3-wise independence of the binary code and the spherical 3-design property is well-drawn.

3. **Strong undetectability evidence.** Binary classifier experiments (Figure 2) convincingly show Tree-Ring and Gaussian Shading (with fixed keys) detected at 100% and 97% accuracy, while the proposed method stays at chance level (~50%). FID results (Table 1) show only the proposed method and PRC match the original distribution without degradation. The module-level ablation (Figure 6b,c) cleanly demonstrates that both the binary embedding and spherical mapping components are necessary.

4. **Thorough experimental scope.** The evaluation covers two datasets (COCO, SDP), two model versions (SD v1.5, v2.1), multiple attacks (post-processing, adversarial), ablation on parameters (s, N, l_m), ODE solvers, and sampling timesteps — with consistent advantages for the proposed method.

## Weaknesses

### Major

1. **Gaussian Shading baseline evaluated in a weakened configuration.** The paper evaluates Gaussian Shading with five fixed keys rather than per-image (key, nonce) pairs, which breaks its losslessness guarantee. The paper acknowledges this ("Note that with fixed keys, Gaussian Shading no longer achieves true losslessness," Sec. 4.1) but then presents Gaussian Shading's degraded FID (~50-51 vs original ~46-49 in Table 1) and 97% classifier detection accuracy (Figure 2) as evidence of the proposed method's superiority. This comparison is against a hobbled version of the baseline. The paper should either (a) compare against Gaussian Shading in its intended per-image-key configuration, accepting the storage cost, or (b) reframe the comparison explicitly as "fixed-key vs fixed-key" and state clearly that Gaussian Shading's core guarantee does not apply in this regime.

2. **The "encryption-free" framing overstates the departure from prior work.** The method uses a fixed secret signature K = {T, C} that is "kept fixed and secret during runtime to prevent unauthorized removal" (Sec. 3.2). The actual distinction from Gaussian Shading is that the secret is *fixed* rather than *per-image*, not that there is no secret. "Encryption-free" (title, abstract, introduction, conclusion) implies a stronger claim (no secrets at all) than what is delivered. More importantly, this fixed-secret design introduces a single-point-of-failure vulnerability: if {T, C} is ever leaked, all watermarks can be forged or removed — a trade-off the paper does not acknowledge. Per-image key schemes limit damage from a single key leak to one image.

### Minor

3. **The adversarial attack explanation is asserted without evidence.** The paper explains lossy methods' poor adversarial robustness by claiming "their embeddings enable effective classifiers to be trained for watermark detection, which can then be adversarially attacked" (Sec. 4.2). This is a plausible mechanism, but the paper provides no evidence connecting detectability to adversarial vulnerability — no ablation, no gradient analysis, no correlation experiment. The empirical result (lossless methods outperform lossy ones under adversarial attack) stands on its own, so this does not threaten the core claims, but the explanation is unsupported.

4. **"Lossless" language creates an impression of perfect end-to-end reversibility.** The paper defines losslessness as noise-space computational indistinguishability (Eq. 2), but the end-to-end pipeline involves DDIM inversion, lossy VAE encoding/decoding, and the rounding operation in Eq. 13. The paper acknowledges this indirectly through the traceability definition (Eq. 4) requiring ≥ 1 - negl(ρ) accuracy — and indeed achieves ~99.9% extraction accuracy. However, the repeated language of "lossless watermarking" and "exact multivariate Gaussian noise" could mislead readers into expecting perfect pixel-level reversibility rather than the distributional guarantee that is actually delivered.

### Trivial

5. **Notation inconsistency in Eq. 6.** "l_m = N × l_m" redefines the variable; a distinct name (e.g., l_{Nm}) would be clearer.

6. **Rotation matrix dimension note is slightly underspecified.** The footnote says l_c is chosen as "a factor of l_x" while the main text sets l_c = l_x "for notational convenience." The specification is present but could be stated more clearly in the main text.

## Nice-to-Haves

- Acknowledge the fixed-secret single-point-of-failure risk explicitly, as suggested by the harsh critic's detailed suggestion #1.
- Report FID against a natural image reference distribution (e.g., COCO training images) in addition to the unwatermarked output distribution, to strengthen the quality claim from a second angle.
- Provide simple evidence for the detectability→adversarial-vulnerability claim (e.g., correlate classifier detection accuracy with attack success rate across methods).

## Removed Points

These points were flagged by the input review but are removed or demoted for the reasons stated:

- **"The 'lossless' claim conflates noise-space invertibility with end-to-end reversibility"** as a major weakness. The paper defines losslessness as computational indistinguishability (a standard crypto definition), not literal pixel-level reversibility. The traceability definition already accounts for the practical gap. Demoted to minor weakness #4 above.
- **"The paper does not report FID against a real-image reference distribution"** — treated as a nice-to-have rather than a weakness, since FID against the unwatermarked output distribution is the appropriate reference for measuring distribution shift from watermarking.
- **The harsh critic's suggestion about detecting a dimension mismatch** — re-reading the paper confirms the footnote addresses this: "For notational convenience, we set l_c = l_x" and the footnote explains the practical choice. Kept as a trivial specification clarity issue.
- **Genuine strength about "thorough ablation study"** kept as strength #4, but the specific claim about Table 3 being "difficult to parse" is a minor presentation opinion that does not threaten the paper's claims.
- **Section-by-section notes about l_m overloading, and "spherical-to-Gaussian mapping novelty"** — these are not substantial weaknesses but editorially useful; folded into trivial issues and nice-to-haves where relevant.
- **"Strengthening the Paper on Its Own Terms" suggestions** are folded into "Nice-to-Haves" and "Suggestions" sections.
- **Weakness about "the Gaussian Shading caveat should be elevated"** — the paper does prominently state it (parenthetical at end of a paragraph in Sec. 4.1), but it could be more prominent. This is captured by Major weakness #1.

## Novel Insights

Beyond the paper's own contributions, the harsh critic's analysis draws out an interesting tension that the paper itself avoids addressing explicitly: the fixed-signature design trades per-image key management for a single point of failure. This is a genuine design trade-off shared by any single-key system, and articulating it would make the paper stronger. The spherical 3-design analysis also stands out as a neat connection between binary code properties (k-wise independence) and spherical geometry that is more elegant than prior approaches.

## Suggestions

1. Replace "encryption-free" with "fixed-key" or "single-key" throughout the paper, or at minimum add a clear explanation that the secret is fixed rather than per-image.
2. Either evaluate Gaussian Shading with per-image keys (accepting the storage cost in the comparison) or explicitly frame the comparison as "fixed-key vs fixed-key" and note that Gaussian Shading's losslessness guarantee does not carry over.
3. Acknowledge the single-point-of-failure risk of a fixed secret upfront, and explain the threat model under which this is acceptable (e.g., server-side enforcement, TEE).
4. Better separate the theoretical losslessness guarantee (noise-space indistinguishability) from practical end-to-end extraction accuracy in the framing language.
5. Fix the l_m notation in Eq. 6 and clarify the rotation matrix dimension specification in the main text.

## Score and Decision

**Round 1 bracket (5.5 – 6.5).** Based on calibration search against the ICLR 2026 human-review corpus:

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| PRC Watermark (jlhBFm7T2J) — "An undetectable watermark for generative image models" | 6.50 | R1 | Direct competitor; comparable contribution but stronger cryptographic formalism. This paper has better efficiency and a simpler design. |
| Hidden in the Noise (ll2nz6qwRG) — "Two-Stage Robust Watermarking" | 5.83 | R1 | Similar undetectability focus; this paper has stronger theoretical grounding. |
| Shallow Diffuse (1IwoEFyErz) — "Robust and Invisible Watermarking through Low-Dimensional Subspaces" | 6.00 | R1 | Rejected despite 4×6 scores due to presentation/ablation issues. This paper is better on those dimensions. |
| Image Watermarks are Removable (mDKxlfraAn) — "Controllable Regeneration" | 6.40 | R1 | Watermark removal paper; accepted. Different topic but comparable execution quality. |
| DIAGNOSIS (f8S3aLm0Vp) — "Detecting Unauthorized Data Usages" | 6.50 | R1 | Similar topic area; accepted. Comparable experimental rigor. |
| A Recipe for Watermarking (HexshmBu0P) | 5.33 | R1 | Rejected; less theoretical depth and conceptual clarity issues. This paper is stronger. |
| Sparse Watermarking in LLMs (jbfDg4DgAk) | 3.00 | R1 | Different domain (LLMs); clearly lower quality. |

**Narrowing:** Within the 5.5–6.5 bracket, the most direct comparator is the PRC Watermark paper (6.50, accepted). The current paper has a cleaner design and better empirical efficiency, but its framing issues ("encryption-free" overreach, Gaussian Shading comparison) prevent it from reaching the same level of presentation candor. Shallow Diffuse (6.00) was rejected for presentation issues that this paper does not share. This paper's theoretical rigor and experimental thoroughness place it above Hidden in the Noise (5.83). The final score of 6.0 reflects a paper with real technical contributions and strong experiments that needs minor but substantive framing corrections.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>