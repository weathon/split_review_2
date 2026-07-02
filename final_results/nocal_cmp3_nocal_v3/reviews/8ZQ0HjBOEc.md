## Summary

This paper studies the behavior of the Neural Tangent Kernel (NTK) for infinitely wide ReLU networks as depth \(L \to \infty\) (with \(L \in o(\min n_i)\), so width grows faster than depth). Its two main contributions are: (1) a clean characterization showing that the normalized NTK converges entrywise to the all-ones matrix (Theorem 2, Proposition 4), and (2) an argument using rough differential equations that, despite this singularity, the term \(\kappa_x^\top \kappa^{-1}\) in the closed-form predictor converges to a well-defined limit (Theorem 3). The paper is explicit about its regime (data on the sphere, \(L \ll\) width) and situates itself clearly relative to prior work.

## Strengths

- **A well-motivated and non-obvious question.** The tension between Theorem 2 (the normalized kernel converges to the all-ones matrix, hence singular) and Theorem 3 (the quantity \(\kappa_x^\top \kappa^{-1}\) nonetheless converges) is a genuinely interesting observation that goes beyond routine extensions of existing NTK analyses.

- **Clean results on kernel convergence (Lemma 1, Theorem 2, Proposition 4).** The convergence of \(\rho^{(L)} \to 1\) and the normalized kernel entries to 1 are clearly stated, properly situated relative to known recurrence formulas (Cho & Saul 2009, Arora et al. 2019b), and the implications for the determinant going to zero are correctly drawn. These results are well-supported in the main text.

- **Honest delineation of scope.** The paper is explicit about its regime (depth \(L \in o(\min n_i)\), so width grows faster than depth), distinguishes itself from Hanin & Nica (2020) where the depth/width ratio can be arbitrary, and acknowledges the simplifying assumption of data on the sphere. This clarity helps the reader assess applicability.

## Weaknesses

### Fatal
None.

### Major

- **Theorem 3's proof sketch is insufficient to assess correctness from the main text.** This is the paper's central contribution, yet the sketch (lines 193–225) is too sparse for verification. Several specific concerns:
  - The construction interpolates between \(\tilde\Theta_\infty^{(L)}\) and \(\tilde\Theta_\infty^{(L+1)}\) using \(\psi_{\mathcal{D}}\), while \(b_n^{(L+1)}(t)\) is set to \(\tilde\Theta_\infty^{(L+1)}(x^\top X^\top)\) (constant in \(t\)). The connection between this interpolation scheme and the claimed result \(u_i^{(L)}(1) = \tilde\Theta_\infty^{(L)}(x^\top X)^\top (\tilde\Theta_\infty^{(L)}(XX^\top))^{-1}\) is asserted, not derived. The indexing (\(L\) vs \(L+1\)) between the theorem statement and the proof is confusing.
  - The inequality chain bounding \(v_{(i,j)}\) (lines 219–225) uses properties of \(\psi_{\mathcal{D}}\) and the fact that the determinants go to zero, but the reasoning by which this forces the \(v_{(i,j)}\) to converge to 0 in 1-variation—and why this rate is sufficient to apply the Lyons Universal Limit Theorem—is not established in the sketch.
  - The proof relies on rough path machinery (Lyons Universal Limit Theorem, Itô-Lyons map, \(p\)-variation topologies) but the sketch does not bridge the gap between the inequality bound and the invocation of these advanced tools.
  
  The full proof may be in the appendix (which is not accessible in this format), but the main-text sketch does not provide reasonable confidence in the theorem. This is a critical presentation gap for the paper's headline result.

### Minor

- **Abstract overclaims what is proved.** The abstract states that "the corresponding closed-form solution approaches a fixed limit on the sphere." However, Theorem 3 only addresses the \(\kappa_x^\top \kappa^{-1}\) term in the closed-form solution \(f_\infty(x) = f_0(x) + \kappa_x^\top \kappa^{-1}(y^* - y_0)\). The convergence of \(f_0(x)\) (the initial network output) with depth is not discussed, so the claim about the full closed-form solution is not fully supported by the results presented.

- **Empirical evaluation of Theorem 3's central claim is thin.** The third column of Figure 1 does plot \(\bar\kappa^{(l)}(x^\top X^\top)(\bar\kappa^{(l)}(XX^\top))^{-1}\), but the accompanying discussion is minimal. No quantitative comparison is made between the observed values and any identified limit, no ground truth is established, and no analysis of the limit's structure is provided. The paper relies on a heuristic argument that "convergence to the limiting solution is fast, provided the determinant is small." For the paper's headline result, more direct empirical evidence is needed.

- **Case (c) on invertibility via inverse stereographic projection is unclear.** The paper states that inverse stereographic projection maps datapoints such that \(x_i^\top x_j = 1\) for all \(i,j\), and that this "will result in an invertible \(\kappa\)." If all pairwise dot products equal 1, the kernel matrix becomes \(\mathbf{1}_n\mathbf{1}_n^\top\) (rank 1 and singular), which contradicts the claim of invertibility. Some clarification is needed—possibly the kernel recurrence transforms the initial correlations into distinct values, but this is not explained in the main text.

- **The practical interpretation of Theorem 3's limit is not characterized.** The theorem shows *that* the limit exists, but does not characterize *what* it is (beyond being "non-trivial" and equal to \(e_i\) when evaluated at training points). This limits the paper's ability to connect its theoretical result to insights about learning in deep networks.

- **Generalization to "arbitrary sequence of kernels" is aspirational.** Section 6 lists three properties satisfied by the NTK and one constructed example (\(\eta^{(L)}\)), but does not demonstrate that any other practically relevant kernel satisfies them. The claim to generalize the results is therefore not supported.

### Trivial

- **Proposition 1's proof sketch is too abbreviated.** The phrase "\(\mu = 0\) implies \(x^\top x' \geq 0\) with probability \(1/2\)" does not parse clearly and appears to contain undefined notation.

- **Conclusion contains a confusing repetition** (line 262): "while convergence for the limiting kernel is sublinear, the convergence for the limiting kernel is experimentally fast" — the intended contrast (kernel entries vs. \(\kappa_x^\top \kappa^{-1}\)) is obscured by the repeated phrase.

- **Experimental details are incomplete.** The dataset size \(n\) is not specified, and the number of curves in each plot (and which pairs they represent) is unclear.

## Nice-to-Haves

- Characterizing the limit of \(\kappa_x^\top \kappa^{-1}\) more explicitly (e.g., for small \(n\) or special data geometry) would significantly strengthen the paper.
- Providing explicit convergence rates for \(\tilde{v}_{i,j}\) rather than stating they are "exponentially faster" by inspection of the proof.
- Clarifying whether (and how) \(f_0(x)\) converges with depth, to fully substantiate the abstract's claim about the closed-form solution.

## Removed Points

These points were flagged by the harsh critic but removed after cross-checking against the paper:

1. **"Circularity in the convergence argument"** — Removed because it misreads the proof. The \(v_{(i,j)}\) terms are defined using the determinants (whose convergence to 0 follows from Theorem 2) and the properties of \(\psi_{\mathcal{D}}\); they do not assume the convergence of \(u(t)\) that is being proved. The argument uses known results about the determinants, not the quantity under proof.

2. **"Without access to the appendix"** — Removed because the appendix exists in the original submission; the parser strips these sections.

3. **"No analysis for networks with biases"** — Removed because the paper explicitly scopes this out (line 67: "this is the version of the theorem without biases"). Criticizing its absence is scope creep.

4. **Pure formatting/style nitpicks** (the Proposition 1 sketch's unclear notation is retained as Trivial because it genuinely affects readability; the reviewer's broader complaints about insufficient detail there are kept).

5. **Strength about technical novelty** (conditional on correctness) — Kept but note it is conditional; the approach is indeed novel even if the sketch is insufficient for verification.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's framing of the "tension" between the kernel becoming singular while \(\kappa_x^\top \kappa^{-1}\) converges is already the paper's central observation.

## Suggestions

1. **Expand the proof sketch of Theorem 3** in the main text to clarify: (a) how the interpolation scheme relates to the target quantity at \(t=1\), (b) why the index mismatch (\(L\) vs \(L+1\)) is notational rather than substantive, and (c) how the inequality bounds on \(v_{(i,j)}\) connect to the Lyons Universal Limit Theorem.

2. **Add direct empirical validation of Theorem 3's claim.** Compute \(\kappa_x^\top \kappa^{-1}\) for increasing \(L\) on a small dataset, show that the entries stabilize, and compare values across depths. For \(n=2\) or data with special symmetry, compute the exact limit numerically to verify convergence.

3. **Clarify the claim in the abstract** to reflect that only \(\kappa_x^\top \kappa^{-1}\) is shown to converge, and discuss (or cite known results on) the convergence of \(f_0\).

4. **Explain the inverse stereographic projection case** (case c) more carefully, specifying how the kernel recurrence ensures distinct off-diagonal NTK entries despite initial dot products being 1.

5. **State the claimed convergence rate** (\(\tilde{v}_{i,j}\) converges exponentially faster than the determinant) as an explicit bound, not just "by inspection of the proof."

## Score and Decision

This paper identifies a genuine and interesting tension in the NTK literature and presents clean results on kernel convergence (Theorem 2, Proposition 4). However, its central claimed contribution (Theorem 3) is not adequately supported in the main text: the proof sketch is too sparse to verify, the empirical evaluation is thin for the headline result, and the practical interpretation of the limit is left uncharacterized. The gap between what is claimed (the closed-form solution converges) and what is directly supported (only \(\kappa_x^\top \kappa^{-1}\) is addressed) further weakens the paper. The kernel convergence results alone, while clean, are incremental and do not by themselves constitute a strong acceptance. 

I recommend rejection in its current form, with the possibility of a stronger submission if the theoretical and empirical evidence for Theorem 3 are substantially expanded.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>