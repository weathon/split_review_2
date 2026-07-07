Now I have all the data I need. Let me compile the final review.

## Summary

This paper makes three contributions to the theory and practice of separable neural networks (SepNNs): (1) a universal approximation theorem for SepNNs covering CP, TT, and Tucker architectures via the Stone-Weierstrass framework, (2) an NTK analysis that characterizes SepNN training dynamics in the infinite-width limit—distinguishing deterministic (infinite rank) from random (fixed rank) kernel regimes—and (3) a separable preconditioned gradient descent method (SepPGD) that enjoys O(nD) complexity versus O(n^D) for standard NTK-based PGD. The approximation theory and NTK analysis are solid, novel contributions. The SepPGD method is well-motivated with a clear complexity advantage, but the "provably adjusts the NTK spectrum" claim in the abstract is not fully substantiated by the body's theoretical argument.

## Strengths

- **Universal approximation theorem (Theorem 1) fills a genuine gap.** Prior work (Cho et al., 2023) only covered the bivariate (D=2) CP case. Extending this to arbitrary D ≥ 2 and to TT/Tucker architectures via the Stone-Weierstrass framework is a clean and nontrivial generalization. The proof covers CP, TT, and Tucker architectures in a unified manner.

- **NTK analysis (Lemma 1, Theorem 2, Corollary 1) is the first characterization of SepNN training dynamics in the infinite-width limit.** Lemma 1's decomposition of the SepNN NTK into a sum of factor MLP NTKs weighted by products of other factors' outputs is nontrivial. The distinction between the infinite-rank regime (deterministic kernel, Theorem 2) and fixed-rank regime (random kernel, Corollary 1) correctly identifies that rank must also go to infinity—not just width—for the NTK to converge deterministically, a genuinely novel observation.

- **Computational complexity advantage of SepPGD is substantial and clearly argued.** The reduction from O(n^D) to O(nD) for preconditioner application (Table 1) is the paper's strongest practical contribution. For D=3 and n=256, this is a difference that makes preconditioning feasible where it would otherwise be prohibitive.

- **Lemma 2 (equivalence between SepPGD and classical NTK-based PGD for D=2) is elegant.** Showing that the Kronecker-product decomposition recovers the full preconditioner while admitting efficient factorization is a neat theoretical connection that justifies the method on principled grounds.

- **The paper explicitly acknowledges scope limitations** (CP focus in NTK analysis via Footnote 1, grid-input assumption, D=2 formal proof with D>2 as extension), which is good scientific practice.

## Weaknesses

### Fatal
None.

### Major

- **Mismatch between abstract claims and body evidence on "provably" adjusting the NTK spectrum.** The abstract (line 9) and contribution list (line 50) claim SepPGD "provably adjusts its NTK spectrum" / "provably adjusts the eigenvalue distribution of NTK matrix." However, the theoretical argument in Section 4 (lines 197–201) is incomplete: (a) it relies on the conditional statement "Suppose that \tilde{K} is close to the true NTK matrix K," (b) it argues that \tilde{S} has a better spectrum than \tilde{K} but does not formally connect this to the product K\tilde{S} (whose spectral properties govern convergence), and (c) the paper itself states "This is left for future research" regarding convergence and solution consistency. The body uses hedging language like "could provably" and "This can possibly be verified" that conflicts with the definitive claim in the abstract. This mismatch must be resolved by either completing the proof or removing the "provably" claim from the abstract and contributions.

### Minor

- **Lack of quantitative result tables with error bars in the main text.** While Figures 2–4 show convergence curves and visual results, and Figure 1 properly uses multiple seeds for NTK verification, the experimental results (KRR, image representation, PINNs) are presented only as convergence plots and figure-caption numbers. No tabular summary with means and standard deviations across multiple random seeds is provided, making it difficult to assess statistical significance.

- **Modest PINN improvements without variance reporting.** The SepPINN MSE of 0.042 vs SepPINN (SepPGD) MSE of 0.037 (Figure 4) represents only ~12% relative improvement, and without error bars it is unclear whether this difference is significant. The broader claim of spectral bias alleviation would benefit from larger-scale or more challenging PINN problems where spectral bias is a known critical bottleneck.

- **Theoretical scope limited to specific architectures.** The NTK analysis and SepPGD formal proof (Lemma 2) are primarily for CP decomposition with D=2 grid inputs and two-layer factor MLPs. The paper acknowledges this (Footnote 1, line 201) and states that D>2 and TT/Tucker extensions are "believed" rather than proven. While this is reasonable scope-bounding, it limits the theoretical support for the architectures of greatest practical interest.

### Trivial
None.

## Nice-to-Haves

- Adding a tabular summary (mean ± std across ≥5 seeds) for all experimental tasks would significantly strengthen the empirical contribution.
- A brief intuitive explanation in the main text for why the Kronecker-product structure in Lemma 2 implies efficient preconditioning for D>2 (even without a full formal proof) would help readers.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Missing standard PGD baseline" (Harsh Critic's Critical Issue 2): REMOVED.** The paper explicitly compares SepPGD with "the classical NTK-based PGD, the modified spectrum kernel (MSK)" (line 221). MSK from Geifman et al. *is* that method, and "SepNN (MSK)" in Figures 2 is this baseline. The critic's claim that this baseline is missing is factually wrong.

- **"Lemma 3 is missing from main text": REMOVED.** Lemma 3 is referenced as being in the appendix, which was stripped by the parser. The original submission contains it.

- **"Paper does not grapple with random NTK tension": REMOVED.** Remark 3 (lines 136–137) explicitly discusses this limitation and points to future work.

- **"MSK is different from standard PGD": REMOVED.** The paper explicitly states MSK is "the classical NTK-based PGD" (line 221).

- **Generic scope-bounding criticisms about narrow assumptions: DEMOTED to Minor (above).** The paper acknowledges its scope limitations explicitly. These are scope choices, not oversights.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the mismatch between abstract claims and body evidence: either complete the spectral analysis of K\tilde{S} or replace "provably" with empirically supported language.
2. Add a quantitative results table (mean ± std across ≥5 seeds) for all experimental tasks to the main text.
3. Consider a larger-scale or more challenging PINN experiment where spectral bias is more pronounced, to strengthen the empirical case.
4. Provide a brief discussion in the main text connecting the D=2 Lemma 2 result to the D>2 case, even if a full proof is deferred.

---

**Calibration Report**

All retrieved anchors:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/.../nSDOkm0SKo.md` | 1.00 | R1 | No | Irrelevant pseudoscientific paper; incomparable |
| `/home/.../gwZ90hFSL2.md` | 1.00 | R1 | No | Irrelevant cross-lingual robotics paper; incomparable |
| `/home/.../u1cQYxRI1H.md` | 0.50 | R1 | No | Score is outlier (10,10,10,10 vs 1 from a single reviewer); not comparable |
| `/home/.../P49gSPmrvN.md` | 1.00 | R1 | No | Unrelated visualization paper; incomparable |
| `/home/.../kkVTeMvC9D.md` | 3.40 | R1 | Yes | Empirical GD analysis on tiny models; much weaker theory, more severe weaknesses (-11.84, -8.88) |
| `/home/.../fUz6Qefe5z.md` | 3.00 | R1 | No | NTK with derivative labels; narrower scope |
| `/home/.../xpmDc76RN2.md` | 2.33 | R1 | Yes | Flawed theory with missing proofs; fatal weaknesses (-12.75, -11.34) |
| `/home/.../2NwHLAffZZ.md` | 2.33 | R1 | No | NTK linearization paper; narrower scope |
| `/home/.../YN4uWzcbtt.md` | 4.25 | R1 | Yes | Pure NTK theory with incremental contribution; weaknesses at -6.53, -7.78, -8.82 are much heavier than our paper's worst (-4.64) |
| `/home/.../WH9NhxOeu9.md` | 5.00 | R1 | No | NTK generalization bounds; comparable theory depth |
| `/home/.../kOtFuzoA93.md` | 4.00 | R1 | No | Novel kernel models; comparable scope |
| `/home/.../bWz8aOPwsJ.md` | 3.75 | R1 | No | NTK trace dynamics; more empirical |
| `/home/.../FK8tl47xpP.md` | 6.25 | R1 | No | Learning to optimize; comparable method contribution |
| `/home/.../h7GAgbLSmC.md` | 7.00 | R1 | Yes | Tight NTK convergence guarantees; stronger theoretical depth but has a -9.12 weakness |
| `/home/.../Q0TEVKV2cp.md` | 6.75 | R1 | No | Optimization/preconditioning for deep learning; comparable area |
| `/home/.../PJjHILiQHC.md` | 6.25 | R1 | No | Spectral dynamics of weights; comparable topic |
| `/home/.../TTrzgEZt9s.md` | 8.00 | R1 | No | DRO optimization; different subfield |
| `/home/.../STUGfUz8ob.md` | 7.60 | R1 | No | Transformer reasoning; different subfield |
| `/home/.../4xWQS2z77v.md` | 8.00 | R1 | No | Loss landscape theory; different subfield |
| `/home/.../AoraWUmpLU.md` | 8.00 | R1 | No | Neural ODE activation functions; different subfield |
| `/home/.../8wAL9ywQNB.md` | 6.00 | R2 | Yes | Generalization bounds; has heavier weaknesses (-8.93) than our paper |
| `/home/.../dpDw5U04SU.md` | 7.00 | R2 | Yes | Min width for universal approximation; comparable weaknesses (-4.59, -5.09) but slightly stronger top strengths (+7.37) |
| `/home/.../hoEanaoP4i.md` | 6.00 | R2 | No | Linear separability monitoring; different topic |
| `/home/.../VEJzjAvaIy.md` | 5.75 | R2 | No | NTK divergence in classification; comparable topic |
| `/home/.../GqI4fTVUXC.md` | 6.00 | R2 | No | Theory-practice disconnect; relevant critique angle |

**Round 1 bracket**: between 4 and 7. The paper is clearly stronger than YN4uWzcbtt (4.25) which has heavier theoretical weaknesses and only one narrow contribution. It is clearly weaker than h7GAgbLSmC (7.00) which has tight, complete convergence proofs.

**Final score (6.0) grounded in weighted-item comparison**: Our draft's strongest weakness (-4.64, overclaiming "provably") is lighter than the heaviest weaknesses of 4.25-anchor YN4uWzcbtt (-8.82) but comparable in magnitude to the weaknesses of 7.00-anchor dpDw5U04SU (-4.59, -5.09). However, our strongest strengths (+5.92, +5.95) are lower than dpDw5U04SU's (+7.37). The paper sits between these anchors: it has three distinct contributions (vs. dpDw5U04SU's single tight bound), but the central "provably" claim is incomplete (unlike dpDw5U04SU's complete proofs), and the experiments lack the reporting rigor expected at the 7.0 level. Hence 6.0.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>