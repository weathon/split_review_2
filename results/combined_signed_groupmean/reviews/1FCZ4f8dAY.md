Now I have all the information needed. Here is my final consolidated review.

---

## Summary

This paper uses invariant theory to characterize polynomial (and entire) equivariant functions mapping tensors to tensors under the diagonal action of O(d), the indefinite orthogonal group O(s,d−s) (including Lorentz), and Sp(d). It distills these general results into computationally tractable corollaries for the vector-input-to-tensor-output case (Corollaries 1 and 3) and demonstrates them on three diverse applications: hyperelastic stress–strain prediction, path-signature estimation from sparse samples, and sparse vector recovery. The theoretical characterization extends beyond the scope of existing equivariant frameworks like e3nn/escnn, which are limited to SO(d)/O(d) for d=2,3.

## Strengths

- **Genuinely general theoretical characterization.** Theorem 1 (O(d) equivariant polynomials on arbitrary-order tensors) and Theorem 2 (Lorentz and symplectic groups, entire functions) go substantially beyond prior work. The progression to Corollaries 1 and 3 (vector inputs → tensor outputs) provides a clear, actionable path for practitioners. The honest discussion of computational complexity (O(k'! n^{k'} (Q d n² + d^{k'}))) is a useful practical caveat.

- **Three diverse and structurally different applications.** The experiments on hyperelastic stress–strain, path-signature estimation, and sparse vector recovery are not re-runs of a single benchmark and demonstrate breadth. The path-signature application is particularly novel, connecting equivariant tensor learning with signature methods in a way not previously exploited.

- **Honest presentation of mixed results.** Table 3 clearly shows that SoS methods outperform the learned approach under identity covariance, and the paper discusses why ("the SoS methods perform best when their assumptions are met"). This candor strengthens credibility.

## Weaknesses

### Major

- **No empirical comparison against existing general-purpose equivariant architectures on applicable O(d) tasks.** The related work (lines 31–35) extensively discusses e3nn (Geiger & Smidt, 2022), escnn (Cesa et al., 2022), and Domina et al. (2025), and the paper asserts that "the computational and approximation power should be equivalent" to Corollaries 1 and 3. Yet none of the experiments include a comparison against any of these methods on an O(d) task where they apply (e.g., stress–strain in d=3 would be a natural candidate). The baselines are non-equivariant MLPs (with only 4 augmentation samples) and one task-specific method (TFENN). Without this comparison, the reader cannot determine whether the invariant-theory parameterization offers any practical advantage (or incurs any penalty) relative to the existing state of the art in equivariant architectures. This is a significant evidential gap for a paper framed as developing practical machine learning architectures.

### Minor

- **Weak data augmentation baseline.** The MLP-augmented baselines in the stress–strain and path-signature experiments use only 4 random rotations/transformations (lines 243, 264). Four augmentations is too small to reliably approximate full equivariance; the gap between the method and the augmented baseline could partly reflect the weakness of augmentation rather than the full benefit of built-in equivariance. The paper would be strengthened by reporting performance as a function of augmentation strength to show saturation.

- **The "Ours (Diag)" anomaly in sparse vector estimation is not discussed.** In Table 3, the variant that uses only norm-based features ("Ours (Diag)") outperforms the full method ("Ours") in 6 out of 12 settings (not 8 as stated by one reviewer), concentrated in the Diagonal and Identity covariance structures. When the full pairwise inner-product machinery (the core of Corollary 1) is used, it performs worse on these restricted-covariance settings. The paper does not acknowledge or discuss this pattern. Even a brief comment on why the additional expressivity might hurt under simpler covariance structures would be helpful.

### Trivial

None.

## Nice-to-Haves

- Report parameter counts and approximate FLOPs for the proposed Corollaries 1/3 versus e3nn/escnn to substantiate the claim of comparable efficiency.
- The path-signature experiment would benefit from specifying n and d in the main text (currently deferred to the appendix).

## Removed Points

These points are flagged to be removed; treat them with caution.

- Missing hyperparameters (n, M, d) from main text: REMOVED (appendix sections are stripped by the PDF parser, not absent from the submission).
- TFENN numbers reported without standard deviation: REMOVED (they are from a cited paper — standard practice).
- Metric formula `\frac{d_F}{d_F}` in Table 2 caption: REMOVED (formatted by parser, not a paper error).
- "Universally expressive" overstatement in abstract: REMOVED (standard phrasing).
- Levi-Civita symbol role not discussed: REMOVED (implied by the restriction to vector inputs in the corollaries used).
- Request for additional related works: REMOVED (cannot verify existence of uncited works).
- The harsh critic's claim that "Ours (Diag) outperforms Ours in 8 out of 12 settings" is factually incorrect; the correct count is 6 out of 12.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add at least one comparison against an existing general-purpose equivariant architecture (e.g., e3nn) on an O(d) task where d is small, to empirically validate the claim of comparable performance.
2. Report the data-augmentation baseline with stronger augmentation (32+ rotations) or a sweep over augmentation strength to demonstrate saturation.
3. Add a brief discussion in Section 5 of why Ours (Diag) matches or exceeds Ours on Diagonal/Identity covariance — this would help the reader understand the regimes where the full pairwise inner-product machinery is beneficial vs. harmful.
4. Report parameter counts and approximate inference cost for the proposed architecture to back the memory-efficiency claims in Section 3.

## Score and Decision

**Calibration summary:**

All anchors retrieved during rounds 1 and 2:

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|---|---|---|---|---|
| `kyVzYpDxHg.md` (equivariant tensor functions, sparse vector) | 5.75 | 1 | Yes | Earlier version focusing only on sparse vector recovery — the current paper adds two more experiments and has clearer presentation |
| `tzpXhoNel1.md` (GRepsNet) | 4.25 | 1 | Yes | Different architecture for arbitrary matrix groups; criticized for missing baselines and unclear method |
| `soaOqFTaHJ.md` (EKAN) | 4.00 | 1 | Yes | Equivariant KAN; limited novelty cited as main weakness |
| `oMfZUSbVwf.md` (parameter space symmetries) | 3.00 | 1 | Yes | Different topic; weak empirical validation |
| `79FVDdfoSR.md` (characterization theorem, point-wise activations) | 7.00 | 2 | No | More focused theoretical result with clear practical corollaries |
| `gyfXuRfxW2.md` (SL(2,R)-equivariance) | 7.00 | 2 | Yes | Strong theory + surprising non-universality result; well-executed experimental validation despite some presentation issues |
| `sOte83GogU.md` (group downsampling) | 6.25 | 1 | No | Different setting (G-CNNs); clean empirical evaluation |

**Round-1 bracket:** 5.5–7.5, derived by comparing to the closest anchor `kyVzYpDxHg.md` (5.75) — the current paper is clearly stronger (more experiments, better presentation, broader scope) but does not reach the level of `gyfXuRfxW2.md` (7.00) or `79FVDdfoSR.md` (7.00), which have tighter empirical validation and more surprising findings.

**Narrowing:** The scoring model gives the paper's core theoretical strength impact +10.00 (decisive positive) and the diverse applications +9.91, but the missing equivariant-baseline comparison pulls at -9.99 — nearly canceling. The strongest anchor `kyVzYpDxHg.md` faced a similar structural issue (limited experiments, -5.21 impact, unclear presentation -6.31) and averaged 5.75. The current paper resolves those specific weaknesses (more experiments, better presentation) but introduces the new missing-baseline issue at higher severity. The final score lands above 5.75 but below the 7.00 of anchors with stronger empirical grounding, settling at **6.0**.

**Final score: 6.0 — borderline accept.** The theoretical contribution is solid and novel, the scope extends meaningfully beyond prior work, and the experiments demonstrate utility across diverse domains. However, the absence of any empirical comparison against existing equivariant architectures on O(d) tasks prevents the paper from making a fully convincing case as an applied methods paper. The paper would benefit from adding such comparisons, strengthening the augmentation baseline, and discussing the Ours(Diag) pattern before it reaches the level of a clear accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>