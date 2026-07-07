Now I'll produce the consolidated final review.

## Summary

This paper proposes **Spherical Watermark**, a lossless watermarking framework for diffusion models that embeds arbitrary binary watermarks into the latent Gaussian noise without modifying the pretrained model. The method uses two key components: (1) a **binary embedding module** that mixes repeated watermark bits with random padding via a binary matrix T, producing a 3-wise independent bitstream; and (2) a **spherical mapping module** that projects this bitstream onto the unit sphere, applies an orthogonal rotation C, and scales by a chi-distributed radius to reconstruct Gaussian noise. The approach is "encryption-free" (no cryptographic primitives), uses a single fixed secret key (T, C), and eliminates per-image key storage. Experiments on Stable Diffusion v1.5/v2.1 demonstrate losslessness (FID matching unwatermarked generation), extraction ~4 orders of magnitude faster than PRC, high capacity (maintaining accuracy beyond 2000-bit watermarks), and robustness to attacks.

## Strengths

- **Empirical losslessness is convincingly demonstrated.** Table 1 shows FID values for the proposed method that are essentially identical to the unwatermarked original (e.g., 48.1224 vs 48.1256 on COCO SD v1.5), holding consistently across two datasets and two model versions. Only PRC achieves comparable losslessness. Binary classifier experiments (Figure 2) further show near-50% detection accuracy for both PRC and Ours, confirming that the watermarked outputs are not distinguishable by learned detectors.

- **Extraction speed advantage is large and practically meaningful.** The paper reports extraction being ~4 orders of magnitude faster than PRC Watermark (Figure 4). For deployment at scale, this difference is significant — PRC's belief-propagation decoding is replaced by simple matrix inversion and rounding.

- **High-capacity watermarking without degradation.** Figure 6(a) shows that the method maintains high detection accuracy as watermark length \(l_m\) increases beyond 2000 bits under JPEG-70 compression, while PRC Watermark's performance collapses entirely. This is a genuine advantage for applications needing to embed substantial metadata (e.g., long user IDs, timestamps, metadata).

- **Careful ablation studies.** The paper ablates each module (binary embedding, spherical mapping), key hyperparameters (\(s\), \(N\), \(l_m\), \(l_r\)), ODE solvers (DDIM, PNDM, DPM-Solver++), and timestep schedules. The ablations isolate the contributions of each component and systematically explore sensitivity.

## Weaknesses

### Major

- **Gaussian Shading baseline is evaluated only in a weakened configuration.** The paper evaluates Gaussian Shading (GS) exclusively with *fixed keys* (Line 193: "Note that with fixed keys, Gaussian Shading no longer achieves true losslessness"), and then uses the resulting degraded FID and detectability (Table 1, Figure 2) to argue that the proposed method is superior. GS was designed for per-image keys — that mechanism is what guarantees its losslessness. By evaluating GS only in a configuration that breaks its core property, the comparison conflates two separable questions: (a) whether the method is lossless when used as designed, and (b) whether its key-management overhead is acceptable. The paper should either evaluate GS with per-image keys for losslessness and discuss key management as a separate trade-off, or explicitly frame the comparison as "when forced into a fixed-key regime" rather than implying the method is inherently inferior. The paper's note about fixed keys is transparent but insufficient — the evaluation design still favors the proposed method.

- **The theoretical guarantee is oversold in the conclusion and Section 3.3.** The conclusion (Line 336) states that "Watermarked latent inputs are provably and empirically indistinguishable from a standard Gaussian prior," and Section 3.3 (Line 157) opens with "the final latent code \(\mathbf{z}_w\) is distributed as \(\mathcal{N}(\mathbf{0}, \mathbf{I}_{l_x})\)." However, the actual theoretical result is that \(\mathbf{z}^{(2)}\) is a *spherical 3-design* — matching moments of the uniform spherical distribution only up to degree 3, not exact uniformity. Lemma 3.4 requires *exact* spherical uniformity to yield a Gaussian, which the construction provably does not provide (the set of possible \(\mathbf{z}^{(2)}\) values is finite). The paper acknowledges this gap in the limitations section (Line 332: "higher-order moments may deviate from the true prior"), but the abstract, introduction, and conclusion present the theory as stronger than it actually is. The guarantees are for moments up to degree 3, not full computational indistinguishability.

### Minor

- **The security model is under-discussed.** The paper markets itself as "encryption-free" (title, abstract, introduction) and contrasts this with Gaussian Shading's stream cipher and PRC's cryptographic constructs. While the label is technically accurate (no cryptographic encryption algorithm is used), the scheme relies entirely on a single fixed secret \(\mathcal{K} = \{\mathbf{T}, \mathbf{C}\}\) (Line 82: "\(\mathcal{K}\) is kept fixed and secret during runtime"). The paper does not discuss what happens if \(\mathcal{K}\) leaks — a single point of catastrophic failure that compromises all watermarks, unlike per-image-key schemes. It does not mention Kerckhoffs's principle, discuss key leakage scenarios, or compare the security posture of its fixed-key design against alternatives. A more precise framing (e.g., "fixed-key" rather than "encryption-free") and explicit discussion of this trade-off would improve the paper.

- **The undetectability evaluation relies on two binary classifiers (2-layer MLP, ResNet-18) with 1000 prompts.** While the results are convincing (near-50% accuracy), the paper does not report statistical two-sample tests (e.g., MMD) on the latent noise distributions or test with stronger classifiers (e.g., Vision Transformers). Given that the theoretical guarantee only covers moments up to degree 3, and the security argument hinges on undetectability, a slightly more thorough empirical investigation of higher-order deviations would strengthen confidence. (This is a nice-to-have, not a core flaw — what is presented is already competitive with standards in the field.)

### Trivial

- **Notation reuse:** The variable \(r\) is used both for the padding vector (Eq. 5) and for the chi-distributed radius (Eq. 10), which is momentarily confusing.

## Nice-to-Haves

- Evaluate Gaussian Shading with per-image keys for the losslessness comparison, then discuss key management overhead as a separate qualitative trade-off.
- Add a brief discussion of the security model: what happens if \(\mathcal{K}\) leaks, and how the fixed-key design compares to per-image-key schemes under Kerckhoffs's principle.
- For completeness, report the false positive rate for unwatermarked images run through the extraction pipeline.

## Removed Points

These points from the input review are removed with brief justification:

- **"Encryption-free claim is structurally misleading / security model is undefined"** (original Issue 1, strongly stated version): The paper *does* define a formal security model (computational indistinguishability, Section 3.1). "Encryption-free" is accurate in that no encryption algorithm is used. The valid core (under-discussed fixed-key trade-offs) is retained as a Minor weakness above. The stronger claim of "no security model" is inaccurate.
- **"DDIM inversion imperfection unanalyzed"** (original Issue 5): The paper provides extensive ablations on three ODE solvers (Table 4) and timestep schedules (Table 5) showing near-perfect extraction across all settings. This effectively addresses the concern.
- **"No false positive rate analysis"**: TPR@1%FPR is explicitly reported (Line 229), which controls and measures FPR.
- **"No collusion analysis"**: Not a standard requirement for ICLR watermarking papers.
- **"Reproducibility limited (seed unspecified)"**: Seed details for random operations are a minor implementation detail not expected in the main paper.
- **"Table 2 shows 0.00 std — suspicious"**: Standard deviations of 0.00 over 5 runs with fixed keys and deterministic operations are plausible due to rounding.
- **"Lossy methods claim asserted without evidence"**: The paper cites Appendix E and Section 4.2 for this evidence; the appendix is stripped by the parser.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Re-evaluate Gaussian Shading with per-image keys for the losslessness comparison, then discuss key management overhead as a separate qualitative trade-off rather than conflating the two.
2. Tighten the language in the conclusion and Section 3.3 to match what is actually proven: state clearly that the guarantee covers moments up to degree 3, and that higher-order indistinguishability is empirically validated.
3. Add a brief discussion of the security model: what happens if \(\mathcal{K} = \{\mathbf{T}, \mathbf{C}\}\) leaks, and how the fixed-key design compares to per-image-key schemes under Kerckhoffs's principle.

## Score and Decision

**Round 1 bracket:** After comparing my draft's weighted items against the anchors, the paper sits above the 5.33–6.00 range of similar watermarking papers (which carry much heavier negatives: -7.56, -9.36 for the 5.33 anchor; -5.91, -6.50 for the 5.83 anchor; -6.78, -7.88 for the 6.00 anchor) but below the 7.60 anchor (which has a different contribution profile — lightweight framework with SOTA performance). My draft's negatives (-2.60, -2.33, -1.97) are the mildest of all anchors, while positives are strong (+5.70, +5.03, +4.11, +3.46). The two major weaknesses (uneven GS comparison, oversold theory) are real but addressable — they concern framing and evaluation design, not the method's validity. I narrow the bracket to **6.0–7.0**.

**Anchors referenced:**
- `HexshmBu0P` — 5.33, Round 1, itemized — "A Recipe for Watermarking Diffusion Models" — similar topic but has much heavier novelty/methodology negatives (-7.56, -9.36). My paper has stronger positives and weaker negatives, placing it above 5.33.
- `ll2nz6qwRG` — 5.83, Round 1, itemized — "Hidden in the Noise" — two-stage watermarking with positives (+6.70) but heavy negatives (-4.00, -5.91, -6.50). My paper's negatives are uniformly milder.
- `1IwoEFyErz` — 6.00, Round 1, itemized — "Shallow Diffuse" — watermarking with low-dimensional subspace, positives at +4.93 but negatives at -6.78, -7.88, -7.40. My paper's weighted profile is substantially more positive.
- `T0ebbDO60R` — 3.75, Round 1 — "SuperMark" — has extremely heavy negatives (-12.46, -10.36, -9.25) and lower positives. Not comparable to this paper.
- `j7b4mm7Ec9` — 7.60, Round 1, itemized — "Lightweight Deep Watermarking" — different contribution type (framework optimization rather than new lossless construction), with a -9.08 novelty negative and strong positives. My paper's method is more novel but has framing issues that prevent reaching this level.

**Final score grounded in weighted-item comparison:** My paper shares with the 5.83–6.00 anchors the positive items of "empirical losslessness demonstrated" and "speed advantage" but crucially *lacks* the heavy negative items those anchors carry (novelty concerns, missing comparisons, limited evaluation). The Gaussian Shading comparison issue (-2.60) and theoretical overselling (-2.33) are real but mild in magnitude compared to those anchors' -5 to -9 negatives. The paper's method is clever, practical, and well-executed; the weaknesses are primarily about presentation and framing, not methodological validity.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>