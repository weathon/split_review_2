## Summary

This paper studies the dynamics of the quantity *r* (a weighted average of eigenvalues) in steepest descent for convex quadratics under a scaled Cauchy step length \( \alpha = \frac{1}{t\, r_k} \). It claims that varying the scalar *t* changes the *r*-iterates from fixed-point convergence (*t* < 1) to 2-cycle alternation (*t* = 1) to irregular/"chaotic" behavior (*t* > 1), and attempts to analyze this via a recurrence function *G*(*r*).

---

## Strengths

- **The central question is a legitimate theoretical curiosity.** Whether scaling the Cauchy step produces qualitatively distinct dynamical regimes for the Rayleigh-quotient-like quantity *r* is a natural question worth asking. The observation that a single parameter *t* can move the iterates through different dynamical patterns is, in principle, interesting.

- **The 2D derivations (Eqs. 15–17) appear internally consistent.** The derivation of *G*(*r*) from the 2D recurrence (Eq. 15) — eliminating the *g*<sub>*k*</sub> terms via the relationship between *r*<sub>*k*</sub> and the gradient component ratio — is mathematically valid (can be verified by working through the algebra). The resulting closed form (Eq. 16) and its derivative (Eq. 17) are correctly stated for the 2D case.

---

## Weaknesses

### Major

1. **Equations (11) and (13) contain an algebraic error, creating a deep inconsistency in the paper's exposition.**  
   Equation (11) (line 61) reads:  
   \[
   r_{k+1} = \frac{\sum a^{(i)} g_k^{(i)2} (r_k-a^{(i)})^2}{\sum a^{(i)} g_k^{(i)2} (r_k-a^{(i)})^2}
   \]  
   The numerator and denominator are **identical**, yielding the trivial (and incorrect) result \(r_{k+1}=1\). Equation (13) (line 69) has the same defect. The correct recurrence should have **no \(a^{(i)}\) factor in the denominator**.  
   Crucially, the 2D recurrence used for the paper's main analysis — Eq. (15) — *does* have the correct denominator (without \(a^{(i)}\)), which means the paper's own derivations contradict the general formulas it presents. This inconsistency signals a lack of rigor in the paper's foundation: the reader cannot trust that the general N-dimensional framework (Eqs. 11–13) has been derived correctly, and the N-dimensional analysis (Section 3, which references Eq. 11) is particularly suspect.

2. **No connection between *r*-dynamics and actual optimization performance.**  
   The paper studies *r* in isolation but never establishes why the dynamical behavior of this quantity matters for minimizing \(f(x)\). There is:  
   - no convergence rate analysis (function value or gradient norm vs. iteration),  
   - no proof or even an argument that the scaled method produces descent for *t* ≠ 1,  
   - no comparison of iteration counts, wall-clock time, or solution accuracy against standard SD or any baseline, and  
   - no evidence linking the "unstable" regime (*t* > 1) to faster convergence.  

   The conclusion (Section 5) speculates that the unstable regime "can potentially accelerate convergence" but offers zero supporting theory or evidence. The paper describes a dynamical curiosity without demonstrating its relevance to optimization.

3. **The "experimental" evaluation is nearly nonexistent.**  
   Section 4 shows *r*-trajectories for a single synthetic problem (arithmetic progression eigenvalues, one random initial point) at three *t* values. There are:  
   - no function value plots,  
   - no comparisons to any baseline (the BB method is mentioned in Figure 7 but never quantitatively evaluated),  
   - no variation of condition number or dimension,  
   - no statistical replication, and  
   - no wall-clock time or iteration-to-tolerance measurements.  

   Three figures of *r* trajectories on one problem instance are insufficient to support any empirical claim.

4. **The "chaos" claim is stated without rigorous definition or evidence.**  
   The paper repeatedly describes the *t* > 1 regime as "chaos motion" (Sections 2.1, 3.2, 5) but provides none of the standard diagnostics of chaotic dynamics: no Lyapunov exponents, no sensitivity-to-initial-conditions analysis, no topological transitivity argument, and no definition of what "chaos" means in this context. This is an informal label, not a substantiated finding.

5. **The N-dimensional analysis (Section 3) is sketchy and the derivation of Eq. (32) is unclear.**  
   The paper states that Eq. (32) follows "from Eqs(10) and (11)" but does not show the derivation. Given that Eq. (11) is incorrect (see point 1), the N-dimensional analysis starts from an unreliable foundation. The heuristic argument about weighting (Section 3 prose) is informal and unsupported. The claims about convergence behavior for *t* ≠ 1 are stated without proof or adequate experimental backing.

### Minor

- **The fixed-point analysis and stability classification are incompletely justified.**  
  Key conditions (e.g., \(t > \frac{a^{(1)}+a^{(2)}}{2a^{(1)}}\) in Section 2.3) appear without derivation. The discussion of \(a^{(1)}\) as a "fixed point" in Section 2.1 is confusing: it is not a fixed point of *G* in the standard sense (the reasoning that "if *r* approaches \(a^{(1)}\), *G*(*r*) will also approach \(a^{(1)}\)" is insufficient to establish it as a fixed point of the recurrence).  

- **Section 2.2 (*t* = 1) reproduces known results from Akaike (1959) and Forsythe (1968) without adding new insight.** The observation that *r* alternates between two values for standard SD in 2D is well-established; the paper's derivation (Eqs. 26–29) is consistent with the known result but does not extend it.

- **The derivation from Eq. (15) to Eq. (16) is presented without explanatory steps**, making it harder to verify. (It is verifiable with additional algebra, but the paper should show or sketch the elimination of the *g*<sub>*k*</sub> terms.)

### Trivial

None.

---

## Nice-to-Haves

- A corrected version of the paper could benefit from showing that the 2D analysis uses Eq. (15) (which has the correct denominator) rather than the erroneous Eq. (11)/(13), and reconciling the inconsistency in the general N-dimensional formulas.
- If the "unstable" regime is to be claimed as potentially useful, the paper would need at minimum a proof of descent for *t* > 1 and a numerical demonstration on a range of problems with standard optimization metrics.

---

## Removed Points

These points from the input review were removed with justification:

- **"CONFERENCE SUBMISSIONS" in the title** — This is a PDF extraction / formatting artifact, not an author error. Removed per hard rule on formatting artifacts.
- **"Numerous grammatical errors"** — Removed per hard rule: criticisms about grammar/typos in extracted text are parser artifacts.
- **Figure captions duplicated as alt-text** — This is a parser artifact from the PDF-to-text extraction. Removed per hard rule.
- **Claim that the error in Eq. (11)/(13) invalidates *every* subsequent derivation** — This is factually incorrect. The 2D analysis uses Eq. (15), which has the **correct** denominator structure (without \(a^{(i)}\)). The harsh critic's blanket statement that the entire mathematical core is invalid overstates the actual propagation of the error. The error is real and serious (it creates an inconsistency), but the 2D *G*(*r*) derivations are based on the correct Eq. (15), not on the erroneous Eq. (11)/(13). Demoted from "fatal" to a major inconsistency weakness.

---

## Novel Insights

The input review's primary novel insight — that Eq. (11) and (13) have numerator = denominator — is factually correct and has been retained as a major weakness. However, the review's further claim that this invalidates the entire paper is itself incorrect, as the 2D analysis uses a different (correct) recurrence. The remaining insights (lack of connection to optimization, minimal experiments, non-rigorous chaos claim) are straightforward observations about what the paper omits rather than novel diagnoses.

---

## Suggestions

1. **Correct the error in Eqs. (11) and (13):** the denominator should read \(\sum g_k^{(i)2} (r_k - a^{(i)})^2\) (without the \(a^{(i)}\) factor), consistent with Eq. (15).
2. **Reconcile the inconsistency** between the general N-dimensional formulas and the 2D specialization used in the analysis.
3. **Provide a proof of descent** for the scaled method when *t* ≠ 1, or at a minimum verify numerically that the method decreases the objective.
4. **Add meaningful experiments:** function value vs. iteration, comparison with standard SD and the BB method over a range of condition numbers and dimensions, with multiple random initializations.
5. **Either provide a rigorous definition and evidence for "chaos"** (Lyapunov exponents, sensitivity analysis) **or drop the term** in favor of a more conservative description (e.g., "irregular", "non-convergent").
6. **Reconsider whether the paper's scope** — a dynamical analysis of *r* without connection to optimization performance — is sufficient for the venue. If the goal is a theoretical dynamical-systems paper, the analysis of *G*(*r*) needs to be substantially deepened and rigorously justified.

---

## Score and Decision

**Score:** 3  

**Decision:** Reject  

**Key reasons:** The paper contains a mathematical error/inconsistency in its core general recurrence (Eqs. 11, 13), provides no connection between the quantity it studies and actual optimization performance, presents essentially no experimental validation, and makes unsupported claims about chaotic dynamics. Even though the 2D analysis appears internally consistent, the paper as a whole does not meet the standard for publication.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>