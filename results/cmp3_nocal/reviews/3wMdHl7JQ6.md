Now let me write the final consolidated review.

## Summary

This paper proposes a streamlined spectral algorithm for community detection in the two-community stochastic block model (SBM) that removes the degree-based deletion preprocessing step and the subsequent Correction step from the algorithm of Chin et al. (2015). The paper claims that Spectral Partition alone achieves inverse-logarithmic error rates previously thought to require the Correction step, and provides a combination of theoretical analysis (Chernoff bounds, normal approximations) and experimental validation.

## Strengths

- **Well-motivated question.** The paper correctly identifies that a standard preprocessing step (degree-based deletion) and the subsequent Correction step in the Chin et al. (2015) algorithm may be unnecessary. Determining whether algorithmic complexity can be safely reduced is a worthwhile investigation.

- **Clean framing of the dependency structure.** The paper pinpoints exactly which lemmas in Chin et al. (2015) depend on the deletion step (Theorem 2.2) and which depend on the Correction step, cleanly scoping the analysis.

- **Multi-pronged analytical approach.** The paper attempts Chernoff concentration bounds, normal approximations, Monte Carlo simulation, and direct spectral experiments, providing multiple lenses on the same empirical phenomenon.

## Weaknesses

### Fatal

- **Central claim is not proved.** The paper's headline claim is that Spectral Partition alone achieves inverse-logarithmic error rates (i.e., the condition of Theorem 1.3: `(a-b)²/(a+b) ≥ C₂ log(2/γ)`). This is not established by any of the analysis presented.

  The paper's own theoretical results are:
  - Theorem 3.2: `γ ≤ C₂ √(a+b)/(a-b)` — a polynomial bound, not inverse-log.
  - The Chernoff bounds (Equation 11) and normal approximation (Equation 12) produce complex expressions not resolved into inverse-log form, and are explicitly acknowledged to be conservative relative to empirical results (line 244: "the gap between these approaches becomes particularly pronounced for small error rates").

  The supposed bridge to the inverse-log claim appears in Section 4 (lines 268–272): an empirical curve fit `sin θ = C / ∛(log 2/γ)` (Equation 13) which, "combined with the claims of Theorems 2.2 and 3.1, directly yields the final result stated in Theorem 1.3." This is not a derivation. Equation 13 is a data-driven fit to a single experimental condition, not a theoretical result. The paper shows no algebraic manipulation connecting this empirical fit — together with theorems that do not involve γ or log(1/γ) — to the claimed inverse-log condition. The central result is asserted, not proved, and the gap between what is claimed and what is demonstrated is structural.

### Major

- **Experimental scope is too narrow to support the generality of the claims.** The paper tests only one parameter setting: `a = 0.06n`, `b = 0.04n`, varying `n` from 500 to 1000 (line 254). There is no independent variation of `a` and `b` — no sparser regime (even while respecting the constant-density scope), no near-threshold regime, no exploration of different signal-to-noise ratios. The central claim concerns achieving theoretical bounds across the parameter space, but the evidence covers a single ray.

- **No comparison to the original algorithm.** The paper never runs the original Spectral Partition (with deletion + Correction) and compares its error rate to the simplified version. Without this comparison, it is impossible to empirically verify whether the Correction step is actually unnecessary — the most direct test of the paper's thesis is absent.

- **Missing error quantification.** Despite reporting multiple repetitions (50 for Monte Carlo in Section 3.4, 10 for scaling experiments in Section 4), no error bars, confidence intervals, or standard deviations are reported for any experimental result. This makes it impossible to assess the reliability or variability of the findings.

### Minor

- **The appendix proof sketch for Theorem 2.2 without the deletion step** is a single paragraph that cites standard spectral norm bounds (Füredi-Komlos, Krivelevich-Vu) and provides a variance bound, but does not address non-trivial steps such as applying concentration to the eigenvalue bound to obtain the high-probability statement in Equation 6. (The full appendix is truncated by the parser; this assessment is based on the visible material.)

## Nice-to-Haves

- The paper could be strengthened by systematically charting, via experiments, the region of the `(a,b,n)` parameter space where the Correction step is and is not needed, producing an empirical taxonomy rather than claiming a general theoretical result.
- A direct comparison between the original algorithm's error rate and the simplified version would be the most informative experimental result for the paper's thesis.

## Removed Points

These points were flagged during review but are removed from the final assessment for the reasons stated:

- **"The simplification argument conflates removing code with proving the algorithm still works"** — The reviewer claimed the appendix sketch "does not actually handle the issue that motivated the deletion step: when vertex degrees vary substantially, the entries of A do not have bounded variance uniformly across all rows." This is factually incorrect. The paper provides a uniform variance bound at lines 324–328 (`σ²_ij ≤ (a+b)/n`) that depends only on the model parameters, not on realized degrees, and correctly cites Krivelevich & Vu (2000) for the relaxation of the common-variance assumption. The criticism misreads the paper.

- **"Sharpness analysis is internally contradictory and misdirected"** — The paper's structure (first showing the old bound is tight in general, then arguing the algorithm's vectors have special structure that makes the bound loose) is a standard and appropriate rhetorical framing. The fact that the subsequent improved bounds do not reach the inverse-log form is a restatement of the first fatal weakness, not a separate problem with this section.

- **"The claim that [the optimization] defines a convex optimization is plausible but under-supported"** — The constraints are linear inequalities plus a quadratic norm constraint, and the objective is linear. Convexity follows directly from construction; the claim is not under-supported.

- **Missing appendix content / reproducibility concerns about hyperparameters** — Per policy, these are parser artifacts or standard-practice issues not suitable for penalization.

## Novel Insights

None beyond the paper's own contributions. The review surfaces a structural disconnect between the paper's claims and its evidence that is already visible in the paper itself: the theoretical bounds do not reach the advertised rate, and the claimed bridge via an empirical fit is not demonstrated.

## Suggestions

1. Either provide a rigorous proof that the simplified algorithm achieves the inverse-log bound of Theorem 1.3, or substantially reframe the paper as an empirical investigation (with broader experimental coverage across the parameter space) that charts where the Correction step is and is not needed.
2. Add a direct experimental comparison between the original Chin et al. algorithm (with deletion + Correction) and the simplified version.
3. Report confidence intervals, standard deviations, or quantiles for all experimental results.
4. Vary `a` and `b` independently in experiments rather than holding `a/n` and `b/n` fixed.

## Score and Decision

**MY FINAL SCORE:** <score>3</score>
**MY FINAL DECISION:** <decision>Reject</decision>