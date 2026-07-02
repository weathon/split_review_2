Now let me write the final consolidated review.

## Summary

This paper studies the deterministic NTK of infinitely-wide ReLU networks as depth \(L \to \infty\). It proves that the normalized kernel converges to the matrix of all ones (Theorem 2) and attempts to prove that the kernel-product expression \(\kappa_x^\top \kappa^{-1}\) from the gradient-flow closed-form solution converges to a well-defined limit despite the kernel becoming singular (Theorem 3). The proof of Theorem 3 uses an interpolation via a smoothing function \(\psi_d\) and rough differential equations.

## Strengths

1. **Theorem 2 is a clean, well-supported result.** The convergence of the normalized NTK \(\bar{\Theta}_\infty^{(L)}\) to the matrix of ones follows naturally from Lemma 1 (convergence of the correlation \(\rho^{(L)}\to 1\)) and the recursive formulation of Proposition 4. This part of the paper is its most solid contribution.

2. **The problem is well-motivated.** Understanding how depth affects the NTK is a genuine open question, and the paper correctly identifies a gap in existing work: Xiao et al. (2020) requires an invertibility decomposition that fails when the kernel approaches singularity, and Hanin & Nica (2020) considers a different (stochastic) regime where depth grows faster than width.

3. **Theorem 3 addresses a genuinely non-trivial problem.** Proving convergence of \(\kappa_x^\top \kappa^{-1}\) when the kernel matrix becomes singular (determinant \(\to 0\)) is the paper's main intellectual claim. The attempt to use rough differential equations is an interesting technical direction that departs from the standard NTK analysis toolkit.

## Weaknesses

### Fatal
None.

### Major

1. **Notation inconsistency: \(\tilde{\Theta}\) vs \(\bar{\Theta}\) is unresolved.**  
   Definition 4 (line 137–139) defines \(\bar{\Theta}_\infty^{(L)}\) (bar) as the normalized kernel. Section 3 (line 35) also references only \(\bar{\Theta}_\infty^{(L)}\). However, Theorem 3 and its entire proof (lines 173–227) use \(\tilde{\Theta}_\infty^{(L)}\) (tilde) about 14 times without ever defining it. The figure captions (line 258) return to using \(\bar{\kappa}\). The reader cannot determine whether \(\tilde{\Theta} = \bar{\Theta}\) (a LaTeX inconsistency that should be fixed), whether a different normalization is intended, or whether a different object is being analyzed. Since the proof manipulates determinants of \(\tilde{\Theta}\) matrices, this ambiguity is not cosmetic — it prevents evaluation of the proof's validity.

2. **The proof of Theorem 3 has significant gaps that prevent it from being judged rigorous.**  
   **(a)** The key inequality chain (lines 220–223) is meant to show that the Cramer's rule derivative terms \(v_{(i,j)}\) converge to 0. The paper states "the strictly positive determinants are all smaller than 1" for large L and uses this to bound the denominator, but it does not establish that the numerator does not also vanish at a comparable rate — without this, the ratio is indeterminate.  
   **(b)** The application of Lyons' Universal Limit Theorem from rough path theory is invoked without verifying its prerequisites. The rough path lift is never explicitly constructed, and the core difficulty of rough path theory (defining iterated integrals / area) is not addressed.  
   **(c)** The argument using property (4) of \(\psi_d\) (all derivatives vanish as \(d\to 0^+\)) involves a parameter \(\mathcal{D}\) (the product of two determinants) that itself tends to 0 as \(L\to\infty\). The paper does not break this potential circularity.

3. **Gap between what is claimed and what is proved.**  
   The abstract (line 9) and conclusion claim that "the corresponding closed-form solution approaches a fixed limit on the sphere." However, Proposition 3 gives the closed-form solution as \(f_\infty(x) = f_0(x) + \kappa_x^\top \kappa^{-1}(y^* - y_0)\). Theorem 3 only addresses convergence of the normalized kernel-product term \(\tilde{\Theta}_\infty^{(L)}(x^\top X)^\top (\tilde{\Theta}_\infty^{(L)}(XX^\top))^{-1}\). The terms \(f_0(x)\) (initial network output) and \((y^*-y_0)\) also depend on depth \(L\) through the network architecture, and their behavior as \(L\to\infty\) is not analyzed. The paper thus establishes convergence of a *portion* of the closed-form expression, not the full solution.

### Minor

4. **Experimental validation of Theorem 3 is merely illustrative, not confirmatory.**  
   Figure 1 shows curves flattening for the third column \((\bar{\kappa}^{(l)}(x^\top X^\top)(\bar{\kappa}^{(l)}(XX^\top))^{-1})\), which is consistent with convergence. However, the experiments do not compare against a predicted limiting value (the theorem does not characterize the limit, only its existence). No error bars or multiple random seeds are reported. For a theory paper this is not fatal, but the experiments do not substantiate Theorem 3 beyond showing non-divergence.

5. **The claim about exponential convergence speed (line 245) is unsupported.**  
   The paper asserts that \(\tilde{v}_{i,j}\) converges "exponentially faster" than the determinant, attributing this to "inspection of the proof of Theorem 3" — the very proof whose gaps are identified above. No numerical evidence of this faster convergence is provided.

6. **The function \(\psi_d\) (Definition 6) is central but poorly motivated.**  
   There is no explanation of why this particular functional form (a logistic-style function with denominator \(d(1-z^2)\)) is chosen, or why the parameter \(\mathcal{D}\) in the proof is specifically the product of the two determinants. Property (4) (all derivatives vanish as \(d\to 0\)) is stated without justification.

### Trivial
None.

## Nice-to-Haves

- A more detailed discussion of the rate condition \(L \in o(\min_i n_i)\) and its practical implications would strengthen the paper.
- Characterizing the limiting value of the kernel-product expression — even a non-closed-form characterization — would significantly strengthen the contribution beyond merely proving existence.
- A numerical comparison with the approach of Xiao et al. (2020) would concretely illustrate what the new method enables that prior work could not.

## Removed Points

These points from the input reviews were removed:
- "No connection to the finite-width case" — removed as outside the stated scope (the paper analyzes the infinite-width limit of the deterministic NTK).
- "Proof sketch of Proposition 1 is too terse" — removed; this is a known result (Cho & Saul, 2009) and the paper acknowledges it is a sketch.
- "Arbitrary sequence of kernels criteria are informal" — removed; these are presented as observations from the proof, not as formal theorems.
- Missing related works — removed per meta-review guidelines (cannot verify references from memory).
- Formatting/style nitpicks and typos — removed per hard rules (parser artifacts, not author errors).
- "No error bars / multiple seeds" — subsumed into Minor weakness 4 above.
- "No comparison with Xiao et al. (2020) numerically" — moved to Nice-to-Have; the paper's contribution is theoretical.
- Any criticism related to "not yet released" or "cannot be independently verified" — removed per hard rules.

## Novel Insights

None beyond the paper's own contributions. The reviews raise specific technical concerns but do not suggest new connections, alternative interpretations, or broader implications that the paper itself does not articulate.

## Suggestions

1. **Resolve the tilde/bar notation.** Either state explicitly that \(\tilde{\Theta} = \bar{\Theta}\) (and fix the inconsistency throughout) or define \(\tilde{\Theta}\) as a new object. This must be done before the proof can be evaluated.

2. **Rigorously work out the key estimates in Theorem 3's proof.** The determinant ratio inequalities need to be justified — in particular, establishing that the numerator does not vanish at the same rate as the denominator. The RDE prerequisites (p-variation topology, explicit construction of the rough path lift) must be verified.

3. **Either prove convergence of the full closed-form solution \(f_\infty(x)\) (addressing the dependence of \(f_0(x)\) on \(L\)) or scale back the claims to match what is proved** (convergence of the normalized kernel-product term).

4. **Motivate the choice of \(\psi_d\)** and clarify why its specific form (and particularly the denominator \(d(1-z^2)\)) is needed for the proof.

5. **Strengthen the experiments** by adding error bars, testing multiple random dataset configurations, and ideally verifying against a computable limit.

---

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>