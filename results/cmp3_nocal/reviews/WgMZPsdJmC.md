## Summary

This paper analyzes the steepest descent (SD) method for convex quadratic optimization by introducing a multiplicative factor *t* on the Cauchy step size and studying the dynamics of *rₖ = 1/(2αₖ)* (a Rayleigh quotient of the Hessian with respect to the gradient). The key observation is that different values of *t* produce qualitatively different dynamical regimes in the recurrence *rₖ₊₁ = G(rₖ)*: for *t* < 1 the fixed point is attractive (single limiting value), for *t* = 1 the system enters a 2-cycle (standard SD), and for *t* > 1 the fixed point becomes repulsive (unstable/chaotic behavior). A 2D analysis is worked out in some detail; an N-dimensional extension and numerical experiments on one synthetic quadratic are also presented.

---

## Strengths

- **The parametric analysis of the *rₖ* dynamics is a genuine mathematical observation.** The paper correctly identifies that the multiplicative factor *t* changes the qualitative nature of the recurrence from stable fixed point → 2-cycle → unstable/chaotic behavior. The core dependence on *t*—via the derivative *G′(rₑ)* crossing through −1 at *t* = 1—is a real property of the scaled Cauchy step and, to my knowledge, has not been explicitly documented in this form.

- **Working with *rₖ = 1/(2αₖ)* is a sensible choice.** Since *rₖ* is a Rayleigh quotient of *A* w.r.t. the gradient, it carries more structural information about the system state than the raw step size, and the recurrence admits a closed form.

---

## Weaknesses

### Major

- **No measurement of actual optimization performance.** The paper analyzes the dynamics of *rₖ* exclusively and never measures function value *f(xₖ) − f(x\*)*, gradient norm, or iteration count to reach a tolerance. The experiments (Section 4) plot only *rₖ* itself. The conclusion acknowledges that the *t* < 1 and *t* = 1 regimes "do not offer any advantage" and only speculates that the *t* > 1 regime could "potentially accelerate convergence." Without any evidence that different *t* values affect the quantity that actually matters—convergence to the minimizer—the analysis remains disconnected from the stated goal of understanding how "different coefficients affect the state of the entire system convergence" (abstract). The paper cites accelerated SD variants (Yuan, RSD, RSDA) in the introduction but never compares against them.

- **The fixed point *rₑ = (a⁽¹⁾ + a⁽²⁾)/(2t)* is claimed but not verified.** The paper states "we can find fixed points *rₑ* (*rₑ = G(rₑ)*) obviously" (line 103) and gives Eq(22), but performs no substitution into *G(r)* to confirm this. The subsequent stability analysis of the three regimes depends on *rₑ* being a genuine fixed point; this is a mathematical gap central to the paper's core claim. (The special case *t* = 1 is correct as it reduces to the known midpoint of the 2-cycle.)

- **The N-dimensional analysis (Section 3) is heuristic and non-rigorous.** Section 3.1 derives Eq(32) for *rₖ + rₖ₊₁* but then argues based on visual inspection of heatmaps of *A(x,y)* and *B(x,y)* that the dynamics concentrate on the extremal eigenvalues, concluding *rₖ + rₖ₊₁ ≈ a⁽¹⁾ + a⁽ⁿ⁾* (Eq 35). There is no formal argument about convergence rates, no derivation of how the weighting suppresses interior eigenvalues, and no analysis of how the result generalizes the classic theory of Akaike (1959) and Forsythe (1968). Section 3.2 (*t* ≠ 1) is three paragraphs of qualitative description. The N-dimensional case is where the paper would need to demonstrate analytical value, but the treatment falls short of the rigor applied to the 2D case.

- **Experiments are too thin to support meaningful conclusions.** The experiment (Section 4) runs 200 iterations of the modified SD on a single synthetic quadratic (10000 variables, arithmetic progression eigenvalues, one random initialization) at three *t* values. There are no statistical replicates, no measurement of function value convergence, no comparison to standard SD or any method cited in the introduction in terms of optimization performance. The Barzilai-Borwein comparison (Figure 7) is a purely qualitative scatter-plot comparison with no quantitative metric.

### Minor

- **"Strange attractor" terminology is used incorrectly.** The paper calls *rₑ* a "strange attractor" when *|G′(rₑ)| < 1* (lines 163, 171). A fixed point with derivative magnitude less than 1 is a *stable fixed point* (sink), not a strange attractor—which denotes a set with fractal dimension supporting chaotic dynamics. The *t* < 1 regime produces convergence to a single value, the opposite of chaotic behavior. This mislabeling undermines the paper's framing about "chaotic systems."

- **The justification that *a⁽¹⁾* is a fixed point is confusing.** The text (line 117) cites Eq(18) (a root of *G′(r)=0*) to argue that *r → a⁽¹⁾* implies *G(r) → a⁽¹⁾*. This reasoning is non-sequitur. (The claim itself is mathematically correct—one can verify *G(a⁽¹⁾) = a⁽¹⁾* from Eq(16) for *t* ≠ 1—but the paper's justification is muddled.)

### Trivial

- **Eq(11) and Eq(13) have identical numerator and denominator**, which would force *rₖ₊₁ = 1* and is clearly wrong. The correct form is evident from the 2D version (Eq 15). This appears to be a typo in the *n*-D equations.

---

## Nice-to-Haves

- If the paper wishes to pursue its own thesis, the single most impactful addition would be to connect *rₖ* dynamics to convergence. This could be a bound on *f(xₖ) − f(x\*)* in terms of the *rₖ* trajectory, or an analysis of how different *t* values affect the per-iteration reduction in function value.
- Verify the claimed fixed point *rₑ = (a⁽¹⁾ + a⁽²⁾)/(2t)* by direct substitution into *G(r)*, to place the stability analysis on solid ground.
- Show at least one concrete setting (even a 2D quadratic) where *t* > 1 reaches a given tolerance in fewer iterations than *t* = 1, and explain the mechanism.

---

## Removed Points

*These points were flagged by the reviewer but are removed in the final review for reasons stated below; they are retained here for transparency.*

- **"Paper does not establish connection to ICLR/ML audience"** — Removed as a scope-demand criticism. A purely theoretical analysis of optimization dynamics can be relevant to ICLR, and the Hard Rules instruct against penalizing papers for not addressing problems outside their stated scope.
- **"Transition from Eq(15) to Eq(16) not derived"** — Removed (moved to minor). Skipping algebraic derivations of this complexity is standard practice; the derivation is tedious but straightforward given the relationship between *gₖ⁽¹⁾²* and *gₖ⁽²⁾²* implied by *rₖ*.
- **"Paper lacks internal coherence between motivation, method, and conclusion"** — Merged into the Major weakness about missing convergence measurements. The coherence gap is a symptom of the same root problem.
- **"Reproducibility: experimental setup under-specified"** — Removed per Hard Rules. Criticisms about undisclosed random seeds and vague distribution descriptions are minor reproducibility nits not suitable for a final review.
- **Generic framing/nitpicks about "missing related work" or "formatting"** — Removed per Hard Rules.

---

## Novel Insights

None beyond the paper's own contributions. The reviewer correctly identifies the core observation (parametric transition in the *rₖ* dynamics) as novel, but does not uncover any additional insight absent from the paper.

---

## Suggestions

1. Either connect *rₖ* dynamics to a convergence guarantee (bound on function value or gradient norm), or reframe the paper as a purely dynamical-systems study with a different title and venue.
2. Verify all claimed fixed points by direct substitution into *G(r)* and clearly distinguish them from critical points of *G*(*r*).
3. Replace the heuristic N-dimensional argument with a rigorous one, or explicitly state the limitations of the analysis for *n* > 2.
4. Replace "strange attractor" with the correct terminology (stable fixed point, sink) throughout.

---

## Score and Decision

This paper identifies a genuine parametric phenomenon in the dynamics of the scaled Cauchy step, but it does not deliver on its implicit promise: it provides no evidence that the different dynamical regimes matter for optimization. The mathematical analysis has gaps (unverified fixed points, confusing justification, heuristic N-dimensional treatment), and the experiments measure only an internal variable rather than convergence. In its current form, the paper reads as an unfinished draft of a specialized numerical analysis result, not a complete contribution to a machine learning conference.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>