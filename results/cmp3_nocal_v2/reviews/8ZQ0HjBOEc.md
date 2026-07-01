Now let me write the final review.

## Summary

This paper studies how the neural tangent kernel (NTK) of infinitely wide fully-connected ReLU networks behaves as depth $L$ increases, while width grows much faster than depth. The authors show that the normalized kernel $\bar{\Theta}_\infty^{(L)}$ converges entrywise to the all-ones matrix (Theorem 2) and attempt to prove that despite this singularity, the closed-form predictor $\Theta_\infty^{(L)}(x^\top X)^\top (\Theta_\infty^{(L)}(XX^\top))^{-1}$ converges to a well-defined limit (Theorem 3), using rough differential equations.

## Strengths

1. **Well-motivated question.** The paper targets a genuine gap in the NTK literature: most NTK analyses fix depth and send width to infinity, but the combined effect of increasing both depth and width is poorly understood. The observation that as the normalized kernel converges to the matrix of ones (Theorem 2), standard invertibility-based arguments break down, motivating a more sophisticated approach.

2. **Lemma 1 and Theorem 2 are clean, sound results.** Lemma 1 (convergence of the correlation coefficient $\rho^{(L)} \to 1$) and Theorem 2 (convergence of the normalized kernel $\bar{\Theta}_\infty^{(L)} \to 1$) are precisely stated, flow naturally from the recursive definitions, and are distinct from existing results — they characterize the *depth* asymptotics of the deterministic NTK, not the width asymptotics.

3. **Technical ambition.** The attempt to handle the singular-kernel limit using rough differential equations (Lyons' Universal Limit Theorem) is genuinely novel in the NTK context.

## Weaknesses

### Fatal

**The proof of Theorem 3 (the paper's central claimed contribution) is not valid as written.** The proof contains multiple gaps that cannot be dismissed as missing details:

- **Unjustified determinant inequality (lines 220–222).** The proof bounds $\det(A(t))$ below by $\det(\tilde{\Theta}_\infty^{(L+1)})^{\psi}\det(\tilde{\Theta}_\infty^{(L)})^{1-\psi}$, where $A(t)$ is a non-linear interpolation between two consecutive-depth kernel matrices. No argument is given for why this inequality should hold; it does not follow from any standard matrix inequality (e.g., the determinant of a convex combination of matrices is not a simple function of the endpoint determinants, and here the interpolation involves a nonlinear function $\psi_{\mathcal{D}}$). This step is the lynchpin of the proof, and it is unsupported.

- **Rate comparison is asserted, not proved (lines 222–223).** The proof bounds the relevant ratio by the numerator over $\det(\tilde{\Theta}_\infty^{(L+1)})\det(\tilde{\Theta}_\infty^{(L)})$ and claims this $\to 0$ as $L\to\infty$ because the determinants go to 0. But the numerator also involves differences of kernel matrices that themselves approach the all-ones matrix, so both numerator and denominator tend to 0. Whether the *ratio* tends to 0 depends on the *relative rates* — an asymptotic comparison that the proof never establishes. The later discussion (Section 6) acknowledges this matters ("$\tilde{v}_{i,j}$ converges to 0 exponentially faster") but says this can be "seen by inspection of the proof," whereas the proof contains no such rate analysis.

- **Rough path connection is not properly established.** The proof identifies terms $v_{(i,j)}$ from Cramer's rule, claims they are of bounded variation and converge to 0, then invokes Lyons' Universal Limit Theorem to conclude convergence of $u$. But the rough differential equation being solved is never specified — what is the driving signal, what is the relationship between $v_{(i,j)}$ and the evolution of $u$? The leap from Cramer's-rule terms to an RDE is not concretely argued.

Because Theorem 3 is the paper's headline contribution (the claim that the limiting predictor converges despite the kernel becoming singular), these gaps are fatal to the paper's core thesis. Lemma 1 and Theorem 2 are separate, sound results, but they alone do not constitute the contribution advertised in the abstract.

### Major

**The notation $\tilde{\Theta}_\infty^{(L)}$ is never defined.** The paper defines $\Theta_\infty^{(L)}$ (original kernel) and $\bar{\Theta}_\infty^{(L)}$ (normalized kernel, Definition 4). Theorem 3 and its proof exclusively use $\tilde{\Theta}_\infty^{(L)}$, which appears in neither the notation section nor any definition. It is unclear whether $\tilde{\Theta}_\infty^{(L)} = \bar{\Theta}_\infty^{(L)}$, $\tilde{\Theta}_\infty^{(L)} = \Theta_\infty^{(L)}$, or some third object. The claim (line 135) that "the kernel can be normalized such that its diagonal elements are all equal to 1, and the resulting vector-matrix product is left unchanged" suggests invariance, but the proof never states the relationship. This makes the theorem statement and its proof ambiguous.

### Minor

- **Experiments provide only partial validation of Theorem 3.** The figure caption shows the third column plots $\bar{\kappa}^{(l)}(x^\top X^\top)(\bar{\kappa}^{(l)}(XX^\top))^{-1}$, which is the quantity Theorem 3 concerns. However, the experimental text (line 245) refers to the undefined $\tilde{\Theta}_\infty^{(L)}$, the caption does not clarify how the vector-valued quantity is summarized into a scalar plotted on the y-axis, and there is no analysis of what the limit actually is or comparison against a predicted value. The experiments mainly validate Lemma 1 and Theorem 2 (convergence of $\rho^{(L)}$ and $\bar{\Theta}_\infty^{(L)}$), which are not in dispute.

- **Case (c) in Section 4 states a geometrically impossible property.** The paper claims that after inverse stereographic projection, $x_i^\top x_j = 1$ for all datapoints $x_i, x_j$. On the unit sphere $S^{n_0}$, $x_i^\top x_j = 1$ implies $x_i = x_j$ by Cauchy-Schwarz, so a nontrivial dataset cannot satisfy this. The claim appears to be a mistake about the stereographic projection.

- **Conclusion contains an internal inconsistency.** Line 262 reads "while convergence for the limiting kernel is sublinear, the convergence for the limiting kernel is experimentally fast" — the same subject assigned opposite properties in one sentence. Context suggests the second instance should refer to the convergence of $\kappa_x^\top \kappa^{-1}$, but the text as written is incoherent.

- **The $\eta^{(L)}$ example (line 243) overloads notation.** The function $h$ is defined in Definition 5 as $h(z) = \frac{z\arcsin(z)}{\pi} + \frac{\sqrt{1-z^2}}{\pi} + \frac{z}{2}$, but line 243 redefines $h(z) = (1+e^{-z})^{-2}$ for the $\eta^{(L)}$ example without flagging the overloading.

- **Proposition 1 proof sketch is insufficient.** The sketch contains the undefined symbol $\mu$ and the statement "$\mu = 0$ implies $x^\top x' \geq 0$ with probability $1/2$" is unintelligible in context. Since Proposition 1 motivates the normalization in Definition 4, a clearer derivation is needed.

### Trivial

None beyond the minor issues above.

## Nice-to-Haves

- The paper would benefit from characterizing the limiting solution itself (what does the limit actually look like?), beyond proving existence.
- A more direct empirical validation: showing the actual values of $\bar{\Theta}_\infty^{(L)}(x^\top X)^\top (\bar{\Theta}_\infty^{(L)}(XX^\top))^{-1}$ as a vector for increasing $L$ and demonstrating convergence to a fixed limit.
- A detailed comparison with Xiao et al. (2020) on a simple concrete case (e.g., a 2-point dataset) would clarify the added value of the RDE approach.

## Removed Points

These points were flagged by the harsh critic but are removed with justification:

- *"Without seeing the appendix, this example is unverifiable" (about $\eta^{(L)}$).* The appendix was stripped by the PDF parser. The notation-overloading criticism is retained in Minor; the "unverifiable" framing is removed.
- *"The rough path theory application is not connected to the actual problem" — the full criticism about missing RDE specification.* Retained in the Fatal section as one of the proof gaps, but note that some rough path definitions may be in the stripped Appendix D; the core objection (the proof does not specify the RDE being solved or the driving signal) is verifiable from the main text.
- *Criticism claiming Proposition 1 is "not a standard ReLU NTK calculation."* The result for $\rho=1$ is standard in the NTK literature. The undefined $\mu$ issue is retained; the broader claim that the derivation is non-standard is removed.
- *"The proof of Theorem 3 missing details left to the appendix" — the specific framing.* The gaps identified (determinant inequality, rate comparison, RDE connection) are all verifiable from the main text and are retained; the generic claim that they are "details left to the appendix" is removed.
- *Reproducibility nitpicks and formatting complaints.* Removed per meta-reviewer guidelines.

## Novel Insights

Beyond the paper's own contributions (Lemma 1 and Theorem 2 are genuine, if incremental, additions to NTK theory), the review surfaces a novel meta-observation: the paper's proof attempt for Theorem 3, if made rigorous, would require establishing that certain Cramer's-rule ratios vanish faster than the kernel determinants — a delicate asymptotic comparison that the current proof merely asserts. This specific gap (rate comparison) is more fundamental than the missing determinant-inequality justification, because even if the determinant inequality were fixed, the rate comparison would remain unaddressed. Identifying this as the deeper bottleneck may help future work on singular-kernel limits.

## Suggestions

1. **Fix the proof of Theorem 3.** The determinant inequality requires a justification (or replacement with a different argument). The rate comparison between numerator and denominator must be established rigorously, not asserted. The rough path construction must explicitly connect to the evolution equation for $u(t)$. Consider whether a more elementary argument using the eigenspace structure of the NTK as $L\to\infty$ would be both more transparent and more rigorous.

2. **Define $\tilde{\Theta}_\infty^{(L)}$.** After establishing the normalization-invariance of $\kappa_x^\top\kappa^{-1}$ (line 135), pick one consistent notation and use it throughout. Currently, the paper uses $\Theta_\infty^{(L)}$, $\bar{\Theta}_\infty^{(L)}$, $\tilde{\Theta}_\infty^{(L)}$, $\kappa$, $\bar{\kappa}$, and $\tilde{\kappa}$ without always clarifying which is which.

3. **Validate the main claim empirically.** Show, for a concrete dataset and test point $x$, the vector $\bar{\Theta}_\infty^{(L)}(x^\top X)^\top (\bar{\Theta}_\infty^{(L)}(XX^\top))^{-1}$ for increasing $L$ and demonstrate convergence to a fixed vector. This would directly support Theorem 3 rather than only showing convergence of kernel entries (which follows from Theorem 2).

4. **Fix the geometric error** in case (c) of Section 4 regarding the stereographic projection.

5. **Edit for precision.** The self-contradictory conclusion sentence, undefined notation, and overloaded function names undermine the paper's readability, which is especially important for a theoretical paper.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>