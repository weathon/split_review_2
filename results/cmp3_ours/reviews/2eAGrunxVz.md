Now let me produce the final review.

## Summary

This paper proposes Spherical Watermark, a lossless watermarking framework for diffusion models that embeds binary watermarks into the latent Gaussian prior without modifying model weights or requiring per-image key storage. The method proceeds through three modules: binary embedding (mixing watermark bits with random padding via an involutive matrix over 𝔽₂), spherical mapping (normalization → orthogonal rotation → chi-square scaling), and diffusion integration. The paper proves that the watermarked noise matches the standard Gaussian up to third-order moments via a spherical 3-design argument, and presents strong empirical results on undetectability, robustness, and computational efficiency—including a ~4-order-of-magnitude extraction speedup over the leading lossless competitor (PRC).

## Strengths

1. **Clean, encryption-free design with demonstrated efficiency gains.** The pipeline (binary embedding via involutive matrix T over 𝔽₂, spherical mapping via normalization + orthogonal rotation + chi-square scaling) is conceptually simple. The extraction speed advantage over PRC—roughly 4 orders of magnitude (Figure 4)—is substantial and practically meaningful. Eliminating per-image key storage (required by Gaussian Shading) is a genuine usability improvement. (Verified in lines 131–153, Figure 4.)

2. **Principled theoretical grounding via spherical 3-design.** Theorems 3.1–3.2 and Lemmas 3.3–3.4 establish a clear chain: the binary embedding produces 3-wise independent Bernoulli(½) bits; the ±1/√lₓ mapping places results on hypercube vertices forming a spherical 3-design; orthogonal rotation preserves the design property; chi-square scaling yields a vector matching N(0,I) up to third-order moments. This is more principled than most prior lossless schemes. (Verified in lines 161–186.)

3. **Strong empirical evidence for practical undetectability.** The classifier-based test (Figure 2) shows that both PRC and Ours produce near-chance detection accuracy, while Tree-Ring and Gaussian Shading (with fixed keys) are easily detected. FID scores (Table 1) are essentially identical to the original for Ours and PRC, while other methods show visible degradation. (Verified in lines 235–254, Table 1, Figure 2.)

4. **Robustness across a wide range of distortions with favorable capacity scaling.** Table 2 and Figure 5 show the method maintains high ACC and TPR under JPEG compression, Gaussian noise, brightness changes, blur, median filtering, and resize—outperforming PRC at stronger distortion levels. The capacity scaling result (Figure 6a) is striking: Ours sustains high accuracy up to lₘ ≈ 5000 bits while PRC collapses beyond 2000. (Verified in lines 271–273, Table 2, Figure 6a.)

## Weaknesses

### Fatal
None.

### Major

1. **Overclaimed theoretical guarantees: the paper asserts cryptographic-level indistinguishability without proof.** The Problem Formulation (Section 3.1, Eq. 2, lines 56–62) defines undetectability via computational indistinguishability against probabilistic polynomial-time adversaries, using the formalism `negl(ρ)` and "computationally indistinguishable." The Introduction (line 26) says the paper "proves that the final noise is statistically indistinguishable from standard Gaussian noise." However, the actual theory (Theorems 3.1–3.2, Lemmas 3.3–3.4) only establishes that the noise matches the Gaussian up to **third-order moments** via a spherical 3-design. A 3-design is a finite point set whose averages match the uniform distribution only for polynomials of degree ≤ 3—this is far weaker than full distributional equivalence, let alone cryptographic indistinguishability. Lemma 3.4 shows that *if* z⁽³⁾ were exactly uniform on the sphere then z_w would be exactly Gaussian, but the paper only proves z⁽³⁾ is a 3-design, not uniform. The abstract (line 9) correctly states "preserves the target prior up to third-order moments," but this honest qualification is abandoned in the body in favor of stronger, unsupported claims. This mismatch between what is claimed and what is proven is structural and runs through the paper's central narrative. *(Verified: abstract line 9 vs. introduction line 26 vs. Section 3.1 lines 54–62 vs. Theorem 3.2 line 175 and Lemma 3.3 line 179.)*

2. **Conflation of "spherical 3-design" with "uniformly distributed."** The text introducing Lemma 3.3 (line 177) states: "the orthogonally rotated vector z⁽³⁾ remains uniformly distributed on S^{lₓ−1}." But Lemma 3.3 itself (line 179) only proves that z⁽³⁾ is a *spherical 3-design*, not that it is uniformly distributed. A 3-design is not a uniform distribution—it only matches moments up to degree 3. This conflation means that the chain of reasoning supporting the Gaussian claim (Lemma 3.4) is not as clean as the paper suggests, since Lemma 3.4 requires exact uniformity of the direction vector, not a 3-design approximation. *(Verified: lines 177–179.)*

### Minor

3. **Gaussian Shading baseline tested in a configuration that breaks its losslessness guarantee, with the comparison framed as general superiority.** The paper tests Gaussian Shading with fixed keys (line 193: "Note that with fixed keys, Gaussian Shading no longer achieves true losslessness") and uses this to position Ours as having superior undetectability. While the practical motivation (avoiding per-image key management) is valid, the narrative could more clearly present this as a trade-off rather than a general advantage. Gaussian Shading with per-image keys provides a provable losslessness guarantee that Ours (which uses a fixed signature) does not match at the theoretical level. *(Verified: line 193, Figure 2.)*

4. **Unclear evaluation of traditional baselines at mismatched bit lengths.** The paper states traditional methods (DwtDct, DwtDctSvd, RivaGAN) are "configured to embed 32-bit watermarks" but "All schemes are evaluated with 512-bit watermarks" (line 193). It is not explained how 32-bit-embedding schemes are evaluated at 512 bits. If the watermark is simply repeated, that inflates their effective robustness; if evaluation uses a subset of bits, the comparison with 512-bit schemes is apples-to-oranges. *(Verified: line 193.)*

5. **Cryptographic formalism without any cryptographic argument.** Section 3.1 (lines 54–68) imports the full cryptographic apparatus—`negl(ρ)`, probabilistic polynomial-time adversaries, "computational indistinguishability"—but the paper provides no cryptographic argument whatsoever. The actual analysis is about moment-matching under exact computation (no noise, no ODE inversion error). This formalism is mismatched with what the paper delivers. *(Verified: lines 54–62.)*

### Trivial
- The paper notes it uses fixed secret keys (T, C) but does not discuss what happens if the key leaks (a reasonable concern for a fixed-key scheme), nor whether key rotation is feasible.

## Nice-to-Haves
- The efficiency comparison (Figure 4) measures only the embedding/extraction transform, excluding diffusion sampling/inversion. The paper acknowledges this explicitly. Adding wall-clock total-time numbers (or noting that ODE inversion dominates) would give a more complete picture of practical runtime.
- Undetectability evaluation relies on binary classifier accuracy. Adding standard two-sample tests (e.g., maximum mean discrepancy) on raw noise vectors would strengthen the distributional claim.

## Removed Points
These points were flagged in the input review but are removed with brief justification:

- **"Key security / fixed key single point of failure"** — This is a real observation but it applies equally to PRC (which also uses a fixed key). Demoted from a weakness to a Trivial note for fairness.
- **"QR decomposition sign ambiguity not specified"** — Implementation-level nitpick that does not affect the validity of the method. Removed.
- **"Extraction speed advantage over PRC is only for a tiny fraction of the pipeline"** — The paper explicitly states it measures only the transform time (line 256: "excluding any diffusion sampling or inversion procedures"). This is a fair comparison for the overhead of the watermarking mechanism itself. Reduced to nice-to-have.
- **"Statistical tests beyond classifier accuracy"** — A constructive suggestion, not a weakness. Moved to nice-to-have.
- **"Error bounds on extraction / ODE inversion approximation"** — The paper provides exhaustive ablation on ODE solvers and timesteps (Tables 4–5) showing the method is empirically robust to inversion inaccuracies. Demanding formal bounds on ODE approximation error for a specific solver is well beyond standard practice for watermarking papers. Moved to nice-to-have.
- **"Missing related work"** — Must be removed per instructions.

## Novel Insights
The harsh critic's most valuable insight is the precise identification of where the paper's theoretical claims exceed its proof: the abstract correctly limits the guarantee to "up to third-order moments," but the Problem Formulation (Section 3.1) deploys full cryptographic indistinguishability language (`negl(ρ)`, PPT adversary) that is never substantiated. The critic also correctly notes the conflation in Lemma 3.3's exposition between "spherical 3-design" (proved) and "uniformly distributed" (not proved). These structural framing issues are distinct from the method's empirical merit and point to a clear revision path. None of the paper's genuine contributions are invalidated; they simply need to be described accurately.

## Suggestions
1. **Align all theoretical claims with what is actually proven.** Replace "computationally indistinguishable" and "statistically indistinguishable" in Sections 1 and 3.1 with the precise statement: "We prove the watermarked noise matches the standard Gaussian up to third-order moments, and provide empirical evidence of practical indistinguishability." Remove the cryptographic formalism (`negl(ρ)`, PPT adversary) or clearly mark it as aspirational framing, not a proven result.
2. **Fix the conflation in Lemma 3.3's exposition** (line 177): change "remains uniformly distributed on S^{lₓ−1}" to "remains a spherical 3-design on S^{lₓ−1}" and explain the relationship between 3-design and the Gaussian claim precisely.
3. **Clarify the Gaussian Shading comparison** by explicitly acknowledging that per-image keys provide a theoretical losslessness guarantee that a fixed-key scheme cannot match, and frame the comparison as a practical trade-off.
4. **Explain how 32-bit-embedding baselines are evaluated at 512 bits** (line 193).
5. **Add the honest qualification about higher-order moments** (from Section 5) to the Introduction where stronger claims are currently made.

## Score and Decision

### Calibration Anchors
All anchors from Rounds 1–2 of calibration_search:

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| PRC Watermark (jlhBFm7T2J) | 6.50 / Accept | R1, R2 | Direct competitor. Accepted despite loose theoretical bound (~½) because it provided a genuine cryptographic proof framework. This paper has a stronger method empirically (speed, capacity) but a weaker theoretical claim relative to its own language. |
| A Recipe for Watermarking DMs (HexshmBu0P) | 5.33 / Reject | R1 | Applied recipe paper with limited novelty. This paper has stronger novelty and better empirical results. |
| Shallow Diffuse (1IwoEFyErz) | 6.00 / Reject | R1 | Strong score but rejected. This paper is comparable in contribution level. |
| Hidden in the Noise (ll2nz6qwRG) | 5.83 / Accept | R2 | Two-stage watermark, accepted. Similar empirical rigor but no theory-distortion issue. |
| The Good, Bad & Ugly (wE5xp3zBaQ) | 5.00 / Reject | R2 | Formalization paper with clean theory but limited empirical scope. |
| Plausibly Deniable Encryption (7suavRDxe8) | 4.80 / Reject | R2 | Overclaimed crypto guarantees—closest structural analog to this paper's framing issue. |
| Semantic-aware Watermarking (LdIlnsePNt) | 6.00 / Reject | R2 | Strong theory paper rejected for unclear reasons. |

### Calibration Narrative
**Round 1 bracket:** [4.0, 6.5]. The paper is clearly stronger than the 1–3 band (rejected papers there are either off-topic or fatally flawed). It sits between the mid-band (3.5–5.5, where "SuperMark" at 3.75 and "Recipe" at 5.33 reside) and the upper-mid band (5.5–7.5, where PRC at 6.50 and "Hidden in the Noise" at 5.83 reside).

**Round 2 narrowing:** The structural overclaiming issue (weakness #1) is the decisive factor. The Plausibly Deniable Encryption paper (4.80) provides the closest analogy: a paper that overstates its theoretical guarantees relative to what is actually proved. This paper's empirical contribution is stronger than its 4.80 counterpart, but the central framing issue is similarly problematic. PRC (6.50) was accepted despite a *different* kind of theoretical gap (loose bound) because it correctly framed what it proved. This paper would need its claims fixed to reach the 6+ range.

**Final score: 5.0.** The core method is well-designed and the empirical results are strong, but the structural mismatch between claimed and proved guarantees is a significant flaw that cannot be overlooked in the current version. With the honest reframing suggested above, the paper would be a solid 6+.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>