The favorability signals are clear: the two Major weaknesses (undefined notation and gappy proof sketch) both score 0.00, the experiments weakness scores 0.10, and the non-characterization of the limit is milder at 0.42. The strengths are solid (0.74 and 1.00). The undefined $\tilde{\Theta}$ and incomplete proof are the dominant negatives that prevent evaluation of the paper's central claim.

Let me now write the final consolidated review.

---

## Summary

This paper theoretically analyzes the NTK of infinitely wide ReLU networks as depth $L \to \infty$ (under the regime where width grows much faster than depth). It shows that the normalized limiting kernel approaches the matrix of ones (Theorem 2), and argues via rough differential equations that the closed-form NTK predictor nevertheless converges to a well-defined limit (Theorem 3). Supporting results include a convergence lemma for the correlation $\rho^{(L)}$ and a useful alternative recurrence for the normalized kernel (Proposition 4).

## Strengths

- **Clear problem framing and positioning relative to prior work.** The paper (Section 5, lines 128–131) explicitly distinguishes its setting from Hanin & Nica (2020) — where depth can dominate width, yielding a stochastic NTK — and from Xiao et al. (2020), whose analysis requires an invertibility assumption that fails when the kernel approaches a constant matrix. This correctly identifies a genuine gap in the literature.

- **Theorem 2 is clean and verifiable.** The normalized kernel $\bar{\Theta}_\infty^{(L)}(x, x')$ strictly increases to 1 for all pairs on the sphere. The result follows reasonably from Proposition 4 and Lemma 1 and is stated with appropriate precision. This is a solid, self-contained contribution.

- **Proposition 4 provides a useful alternative formulation** of the normalized NTK recurrence, connecting the kernel evolution to the correlation $\rho^{(L)}$. This is a helpful technical lemma.

## Weaknesses

### Fatal
None.

### Major

- **Undefined notation $\tilde{\Theta}_\infty^{(L)}$.** The paper's central result (Theorem 3) uses $\tilde{\Theta}_\infty^{(L)}$ throughout its statement (lines 183, 187, 189), proof (lines 195, 197, 201, 221, 222), and experimental discussion (line 245), yet this notation is never defined in the main text. The Notation section (line 35) explicitly lists $\Theta_\infty^{(L)}$ and $\bar{\Theta}_\infty^{(L)}$ — the latter as the "normalized version" — but omits $\tilde{\Theta}_\infty^{(L)}$. Definition 4 defines only $\bar{\Theta}_\infty^{(L)}$. The reader cannot determine whether $\tilde{\Theta}$ is identical to $\bar{\Theta}$ (in which case, why the different symbol?), a different normalization, the unnormalized kernel, or something else. This makes Theorem 3 unverifiable in its current form.

- **The proof sketch of Theorem 3 (lines 193–225) has significant gaps that prevent evaluation of the claimed result.** Three specific problems stand out: (i) The interpolation construction shows that consecutive solutions can be linked by a path whose driving signal shrinks, which is a necessary condition for convergence but does not establish standard convergence of the sequence without summability — no rate analysis is provided. (ii) The inequality chain (lines 219–223) bounding ratios of determinants is not adequately justified. The interaction between $\psi_{\mathcal{D}}$ (whose argument depends on $L$) and the determinants is not analyzed, and the claimed convergence to 0 does not follow from the inequalities as written without additional reasoning about the relative rates of numerator and denominator. (iii) The invocation of rough path theory (Lyons' Universal Limit Theorem) is made without establishing that the key preconditions are met given the sketchy inequality argument; the heavy machinery obscures rather than clarifies the reasoning.

### Minor

- **Experiments do not directly validate Theorem 3 with quantitative evidence.** The third column of Figure 1 plots $\bar{\kappa}^{(l)}(x^\top X^\top)(\bar{\kappa}^{(l)}(XX^\top))^{-1}$, which is relevant to Theorem 3, but the analysis is purely qualitative ("it is immediate at first glance"). No error bars, convergence metrics, or quantitative comparison to the claimed limit are provided. Additionally, the convergence rate discussion (lines 245–246) references undefined variables $K$ and $\delta$, making that part of the argument unclear without the appendix.

- **Theorem 3 asserts existence of a limit but does not characterize it.** The limit is said to be "dependent on $x$ and non-trivial" and equals $e_i$ at training points (which is essentially the interpolation condition). For out-of-sample $x$, no characterization is given. While the paper is honest about this limitation, it substantially reduces the practical insight the result provides.

- **The list of properties for generalizing to other kernels (lines 237–242) is stated at a level of generality that limits its usefulness.** Property 1 (diagonal $\geq$ off-diagonal) is satisfied by many kernels; Properties 2 and 3 essentially restate consequences of Theorem 2. No nontrivial example beyond the NTK is analyzed.

### Trivial
None.

## Nice-to-Haves

- **Define $\tilde{\Theta}$ explicitly** and reconcile it with $\bar{\Theta}$. This is the single most actionable fix.
- **Replace the RDE sketch with a more transparent argument.** The paper could analyze the eigendecomposition of the kernel matrix as it approaches the rank-1 matrix $\mathbf{1}_n\mathbf{1}_n^\top$ and characterize the limiting predictor as a projection onto the all-ones direction.
- **Provide quantitative empirical validation of Theorem 3 directly** — compute $\tilde{\Theta}_\infty^{(L)}(x^\top X^\top)(\tilde{\Theta}_\infty^{(L)}(XX^\top))^{-1}$ for multiple $L$, report distances between consecutive solutions, and compare convergence rates.
- **Characterize the limiting solution for simple special cases** (e.g., two datapoints) to build intuition for what the limit means.

## Removed Points

These points from the input reviews are removed with justification:
- "Lemma 1 has no proof in main text" → REMOVED (missing appendix/proof content; the proof exists in the appendix).
- "Paper references appendix definitions without summarizing them" → REMOVED (missing appendix content rule).
- "The use of rough path theory appears disproportionate" → MERGED into the broader proof-sketch weakness rather than kept as a standalone point; it is a subjective framing of the same gap.
- "Proposition 1 proof sketch too terse" → REMOVED (nitpick about a standard result).
- "Overstated contrast with prior work in Introduction" → REMOVED (too vague to verify against the paper).
- "Not exploring other kernels experimentally" → REMOVED (scope creep; paper states this is future work).

## Novel Insights

The core observation — that the normalized NTK approaches the matrix of ones while the closed-form predictor nevertheless converges to a well-defined limit rather than collapsing — is the paper's key insight. The proposed use of rough differential equations to handle the singular limit of the kernel matrix is an interesting technical approach, though the execution as presented is incomplete. None beyond the paper's own contributions.

## Suggestions

1. **Fix the notation.** Define $\tilde{\Theta}_\infty^{(L)}$ explicitly, or if it is the same as $\bar{\Theta}_\infty^{(L)}$, use one symbol consistently and state the equivalence.
2. **Strengthen the proof of Theorem 3.** Either provide a complete, self-contained argument in the main text or replace the RDE sketch with a more direct approach (e.g., analyzing the eigendecomposition as the kernel approaches rank-1).
3. **Add quantitative experiments.** For the quantity in Theorem 3, report distances between consecutive depths, convergence rates, and whether the values stabilize to the claimed limit.
4. **Characterize the limit for at least one simple case** (e.g., $n=2$ datapoints, or data with a known covariance structure).

## Score and Decision

The paper has genuine strengths: a clearly identified gap in prior work, a clean supporting result (Theorem 2), and a useful technical lemma (Proposition 4). However, the paper's central claimed contribution (Theorem 3) uses an undefined notation ($\tilde{\Theta}_\infty^{(L)}$) and its proof sketch is too incomplete to be evaluable. These are structural issues that prevent assessment of the main result, not mere presentation shortcomings. The experiments provide only qualitative evidence and do not directly validate Theorem 3 quantitatively.

Given the balance — solid supporting results weighed against an unverifiable central claim — the paper is a borderline reject in its current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>