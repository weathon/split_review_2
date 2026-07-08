Now I have all the calibration data I need. Let me construct the final review.

## Summary

Spherical Watermark proposes an encryption-free, lossless watermarking framework for diffusion models that embeds binary watermarks into the Gaussian noise prior while preserving the target distribution. The key innovation is a spherical mapping that converts 3-wise independent bits into a spherical 3-design, applies an orthogonal rotation, and scales by a chi-square radius to match N(0,I) up to third-order moments. Unlike prior lossless methods (Gaussian Shading requires per-image keys; PRC requires heavyweight cryptographic decoding), the method uses a single fixed signature for all images. Experiments on Stable Diffusion v1.5 and v2.1 demonstrate that the method matches FID of unwatermarked images within 1-sigma, achieves near-chance classifier detection rates, and delivers extraction ~4 orders of magnitude faster than PRC while maintaining competitive or superior robustness.

## Strengths

- **Clean resolution of the key-management problem.** Prior lossless methods (Gaussian Shading, PRC) require per-image key storage or heavyweight cryptographic primitives. Spherical Watermark uses a single fixed signature (matrices T and C) for all images while preserving distributional indistinguishability. This is a genuine architectural simplification with practical deployment value.

- **Well-matched theoretical framing via spherical 3-designs.** The paper traces the distribution through each transformation (Bernoulli → hypercube vertices → sphere → rotated sphere → scaled to Gaussian) and identifies precisely what statistical property is preserved (moments up to degree 3) and what is asymptotic (marginal convergence as l_x → ∞). This is responsible theoretical rigor for a practical watermarking scheme.

- **Large, concretely measured computational efficiency gains.** Figure 4 shows extraction ~4 orders of magnitude faster than PRC Watermark. This is the difference between a method that could run at API scale and one that would bottleneck on decoding.

- **Empirical undetectability convincingly demonstrated across multiple tests.** Table 1 shows FID values matching the unwatermarked original within 1-sigma across both datasets and model versions — something neither Gaussian Shading (FID ~50.7 on COCO SD1.5 vs original ~48.1) nor Tree-Ring (~49.3) achieves. Classifier-based detection tests (Figure 2) show near-chance accuracy for both PRC and Spherical Watermark, while Tree-Ring and Gaussian Shading are detected at 100% and 97%.

- **Comprehensive ablation studies** covering the role of each module (binary embedding, spherical mapping), parameters (s, N, l_m, l_r), ODE solvers (DDIM, PNDM, DPM-Solver++), and generation/inversion timestep combinations. The ablations confirm that both modules are necessary and that the method is robust across solver and timestep choices.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The C-matrix dimensionality is underspecified.** The main text states C ∈ ℝ^{l_c × l_c} and sets l_c = l_x "for notational convenience," but Footnote 1 says l_c is chosen as a factor of l_x (e.g., ⌊√l_x⌋ = 128). If l_c ≠ l_x, the single matrix C of size 128×128 cannot act on the 16384-dimensional vector z^(2) as a standard matrix-vector product. The paper does not clarify whether C is applied block-diagonally, tiled, or via some other construction. This ambiguity is a reproducibility concern, though a reasonable implementation (block-diagonal C) would not change the theoretical properties since orthogonality and the spherical 3-design guarantee are preserved under block-diagonal orthogonal transformations.

2. **Table 2 mixes methods with different watermark capacities without visual separation.** Traditional methods (DwtDct, DwtDctSvd, RivaGAN) embed 32-bit watermarks while the lossless methods (PRC, Ours, Gaussian Shading) embed 512 bits. The paper states the capacity difference in the text (line 193), but including both regimes in the same table without any separator or annotation could mislead a casual reader. The asymmetry favors the baselines (fewer bits = easier extraction), not the proposed method, so the concern is about presentation clarity rather than unfair comparison.

3. **Minor wording tension between the introduction and the formal guarantee.** The introduction (line 26) states that the paper proves the noise is "statistically indistinguishable from standard Gaussian noise," while the abstract (line 9) correctly qualifies the guarantee as holding "up to third-order moments." A spherical 3-design guarantees exact matching of moments up to degree 3; a fourth-moment test could in principle distinguish the distributions. The empirical evidence strongly supports practical indistinguishability and the Limitations section acknowledges this gap, but aligning the introduction's wording with the abstract's more precise qualification would eliminate unnecessary tension.

### Trivial

- Figure 4 uses a bar chart with a logarithmic y-axis marked in approximate powers of ten (10^-3.5, etc.), making precise comparison of the reported values difficult. A table of exact timing values alongside the figure would be more informative.

## Nice-to-Haves

- Quantify the extraction bit-error rate as an explicit function of the DDIM inversion error and repetition code parameters N, rather than treating extraction reliability as captured only by the aggregate ACC/TPR metrics.
- Show the detectability benefit of larger sparsity s (i.e., that higher s actually reduces classifier detection accuracy), completing the trade-off analysis that currently documents only the robustness cost of larger s.
- Include a brief note on whether the near-deterministic concentration of the chi-square radius (r ≈ √l_x for l_x = 16384) simplifies the practical implementation.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Critic's Critical Issue 1 (losslessness conflation):** REMOVED. The paper formally separates undetectability/losslessness (Eq. 2) from traceability (Eq. 4). "Losslessness" in the paper's terminology refers to distribution preservation, not extraction perfection. The extraction pipeline's reliance on inversion and repetition codes is explicitly documented (Eq. 12–13, Tables 5, N=31). The critic's claim that the paper conflates two meanings of "lossless" is not supported by the paper's formal treatment.
- **Binary field inversion concern (T^{-1}):** REMOVED. The paper explicitly documents the rounding step in Eq. (13) and ablates the effect of s on error propagation (Table 3). The concern is already addressed in the paper.
- **Redefinition of l_m (line 84):** REMOVED as a trivial notation artifact likely exacerbated by PDF parsing.
- **Near-deterministic chi-square radius:** REMOVED. This is an observation, not a weakness; the math is correct regardless.
- **Computational efficiency excluding diffusion times:** REMOVED. The paper explicitly states (Section 4.2) that the comparison isolates pre/post-processing transforms, which is the correct scope for comparing watermark transform overhead.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's core claims without uncovering novel limitations or unexpected failure modes beyond those the authors already acknowledge.

## Suggestions

1. Resolve the C-matrix dimensionality by explicitly stating whether it is applied as a single l_x × l_x matrix, a block-diagonal of l_c × l_c blocks, or via a structured orthogonal construction.
2. Add a visual separator or annotation in Table 2 distinguishing the 32-bit and 512-bit regimes.
3. Align the introduction's wording ("prove... statistically indistinguishable") with the qualification already present in the abstract ("up to third-order moments").

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Human Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `/home/.../jlhBFm7T2J.md` (PRC paper) | 6.50 | R1 | Yes | Directly comparable lossless image watermark; our paper has stronger strength weights (9.28–10.34 vs 6.89–12.85) and much milder weakness weights (3.81–6.32 vs -2.40–7.24, with several negative weights in PRC) |
| `/home/.../HexshmBu0P.md` (Recipe) | 5.33 | R1 | Yes | Less novel, more methodologically limited; our paper is clearly stronger |
| `/home/.../1IwoEFyErz.md` (Shallow Diffuse) | 6.00 | R1 | Yes | Similar domain; our paper has stronger theoretical framing and no negative-weight weaknesses |
| `/home/.../71pur4y8gs.md` (TabWak) | 7.20 | R2 | Yes | Tabular watermarking (different domain); comparable strength weights (~7.4–11.4 vs our ~9.3–10.3) but TabWak has negative-weight weaknesses (-1.46) and novelty concerns (1.89) that our paper lacks |
| `/home/.../j7b4mm7Ec9.md` (Lightweight Deep WM) | 7.60 | R2 | No | Deep watermarking (different domain); rejected despite high avg score |
| `/home/.../CxXGvKRDnL.md` | 8.00 | R2 | No | Compression, not watermarking |
| `/home/.../agHddsQhsL.md` | 7.50 | R2 | No | Diffusion protection (adversarial), not watermarking |
| `/home/.../ujpAYpFDEA.md` | 7.50 | R2 | No | LLM watermarking, different modality |
| `/home/.../sojpn00o8z.md` | 7.25 | R2 | No | Diffusion likelihood training, not watermarking |

**Round 1 bracket:** 6.5–8.5, based on comparison with the PRC paper (6.50) at the low end and the absence of watermarking papers above 8.0.

**Round 2 narrowing:** Comparison with TabWak (7.20) confirms the paper sits in the 7.0–8.0 range. Our paper's strengths are comparable to or stronger than TabWak's (all ≥9.28, none generic), and its weaknesses are strictly presentation-level (none question the core claims or empirical results, and none have negative weights from the scoring model). In contrast, TabWak has weaknesses that question its robustness vs. baselines (weight -1.46) and its novelty (weight 1.89).

**Final placement:** The paper is a clear accept. It resolves a genuine practical limitation of prior lossless watermarking (key management + computational overhead), provides sound theoretical grounding, and supports its claims with thorough experiments. The three minor weaknesses do not threaten the core contribution. Compared to the closest anchor (PRC paper at 6.50), our paper has uniformly stronger strengths and substantially milder weaknesses. Compared to TabWak (7.20, different domain), our paper has fewer and less severe weaknesses. I place the score at 7.5.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>