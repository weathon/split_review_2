## Summary

The paper studies the steepest descent (Cauchy) method for convex quadratic minimization, introducing a multiplicative factor \( t = 1/s \) on the exact step length \(\alpha_k^{SD}\). It analyzes the dynamics of the reciprocal step-size parameter \( r_k = 1/(2\alpha_k) \) as a discrete map \( r_{k+1} = G(r_k) \). In the two-dimensional case, the paper identifies three regimes: \( t>1 \) leads to chaos, \( t=1 \) gives two-point oscillation (standard SD), and \( t<1 \) yields convergence to a fixed point. Preliminary experiments on a synthetic high-dimensional problem illustrate that \( r \) exhibits single-value convergence (\( t<1 \)), two-value oscillation (\( t=1 \)), or seemingly chaotic wandering (\( t>1 \)).

## Strengths

- The paper attempts to characterize the dynamics of the step-size reciprocal \( r \) in steepest descent, which is a less common perspective compared to analyzing function-value or gradient norms.
- The observation that a simple scaling of the Cauchy step size can produce qualitatively different dynamical regimes (fixed point, period-2 oscillation, chaotic-like behavior) is potentially interesting.
- The derivation of the recurrence for \( r \) in the quadratic diagonal case and the analytic computation of fixed points in two dimensions show some algebraic effort.

## Weaknesses

### Fatal

- **Core equation contains an algebraic error that invalidates the main analysis.** Equation (13) writes \( r_{k+1} = \frac{\sum a^{(i)} g_k^{(i)2} (t r_k - a^{(i)})^2}{\sum a^{(i)} g_k^{(i)2} (t r_k - a^{(i)})^2} = 1 \), which is identically 1 and contradicts every subsequent derivation. The correct denominator should be \( \sum g_k^{(i)2} (t r_k - a^{(i)})^2 \) (consistent with Eq. (11) and Eq. (15)). This mistake propagates through the paper and makes the claimed mathematical results unreliable.

- **No validation of optimization performance.** The paper studies the dynamics of \( r \) but never links it to the actual performance (convergence of function values or gradient norms) of the modified steepest descent method. The practical significance of the three regimes (fixed point, oscillation, chaos) is not demonstrated. Without such validation, the contribution is merely a qualitative curiosity.

- **The claim of “chaotic behavior” is unsupported.** No definition of chaos is given, no Lyapunov exponent or sensitivity analysis is performed, and the plots (described textually) only show seemingly irregular values. In a two-dimensional quadratic system, the dynamics should be low-dimensional; the paper does not rule out that the iterates simply fill a 1D manifold without sensitivity to initial conditions.

### Major

- **The analysis is restricted to a highly specialized setting:** convex quadratics with a diagonal Hessian (axis-aligned ellipsoid). The extension to the general \( n \)-dimensional case is heuristic (Section 3) and lacks rigorous justification. The paper essentially analyzes a recurrence derived for the diagonal case and then assumes without proof that the same behavior holds for arbitrary symmetric positive-definite matrices.

- **The derivation of the recurrence (Eqs. (10)–(11) and (13)) is opaque and missing key steps.** It is not shown how the gradient components and the recurrence for \( r \) are derived from the update \( x_{k+1} = x_k - \alpha_k \nabla f(x_k) \) with the modified step length. The derivation appears to assume initial gradients are aligned with eigenvectors, which is not generally true after the first iteration.

- **Experiments are minimal and not reproducible.** Only one problem instance (arithmetic progression eigenvalues, random initial point) is tested for 200 iterations each. There is no statistical replication, no comparison with the standard steepest descent or other methods, no study of convergence rate or final function value. The figures (described only textually) cannot be inspected.

- **The paper does not cite the relevant literature on step-size dynamics in steepest descent** (e.g., the known “zigzag” phenomenon and the work by Akaike, Forsythe, and others is mentioned, but the paper does not build on or properly contextualize the well-understood 2D case where the iterates converge to a 2-cycle in the \( r \) variable for exact line search – this is actually the standard result, not a new finding).

- **Writing and notation are unclear.** The parameter \( s \) is introduced as \( s = 1/t \) but then definitions of \( t \) and \( s \) are confused in the text. The variable \( r \) is defined both as \( r_k = 1/(2\alpha_k) \) and later as a continuous variable \( r \in (a^{(2)}, a^{(1)}) \). Several equations contain missing parentheses, undefined symbols, or ambiguous statements.

### Minor

- The paper states in Section 2.1 that when \( t>1 \), “the \( r \) value is a chaos motion,” but the argument relies on the derivative at the fixed point being \( < -1 \), which only proves local instability, not global chaotic behavior.
- In Section 2.3, the condition \( t > \frac{a^{(1)} + a^{(2)}}{2a^{(1)}} \) is claimed but its derivation is not shown, and the subsequent discussion of the attractor is vague.

### Trivial

- The title includes “CONFERENCE SUBMISSIONS” in all caps, which seems like a placeholder or unintentional.
- References are incomplete (missing page numbers, some citations appear without year).

## Nice-to-Haves

- A clear link between the dynamics of \( r \) and the actual convergence of the optimization method (e.g., residual reduction per iteration).  
- Experiments on a range of problem condition numbers and comparisons with Barzilai-Borwein, conjugate gradient, or other step-size rules.  
- A formal definition of chaos (e.g., positive Lyapunov exponent, topological transitivity) and numerical computation of such metrics.

## Novel Insights

None beyond the paper’s own contributions. The core observation that scaling the steepest descent step can change the behavior of \( r \) is not new in the optimization literature (over-relaxation and under-relaxation are well-studied). The specific recurrence and its fixed-point analysis are not validated sufficiently to provide a reliable new insight.

## Suggestions

1. Correct the algebraic error in Equation (13) and re-derive all subsequent results.
2. Provide a complete, step-by-step derivation of the recurrence for \( r \) from the gradient update, including handling of general quadratic Hessians.
3. Connect the dynamical regimes (fixed point, 2-cycle, chaos) to actual optimization performance (e.g., function-value convergence plots, iterations to reach a tolerance).
4. Perform experiments on multiple random instances with varying condition numbers and provide statistical summaries.
5. Clearly state the assumptions needed for the analysis (e.g., diagonal Hessian, alignment of initial gradient with eigenvectors) and discuss limitations.
6. Improve the exposition: define all variables, separate derivation from discussion, and avoid ambiguous phrases like “chaos motion” without formal definition.

## Score and Decision

Score: 2 (strong reject)

The paper has a fatal algebraic error in its core equation, lacks validation of optimization performance, relies on a highly restricted setting, and does not make a compelling contribution to the ICLR community. The analysis is insufficiently rigorous, and the experiments are too limited to support the claimed conclusions. The paper does not meet the standards for acceptance at a top venue.

MY FINAL SCORE: <score>2</score>
MY FINAL DECISION: <decision>Reject</decision>