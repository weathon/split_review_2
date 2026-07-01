Now I have all the information I need. Let me produce the final consolidated review.

---

## Summary

This paper develops a theoretical framework for constructing equivariant tensor-to-tensor functions using invariant theory rather than representation theory (Clebsch–Gordan decomposition). The parameterization relies on isotropic tensors (Kronecker deltas and Levi-Civita symbols) and covers the orthogonal group O(d), the indefinite orthogonal groups O(s, d−s) (including the Lorentz group), and the symplectic group Sp(d). Starting from a general characterization (Theorem 1), the paper derives practical parameterizations for common special cases (Corollaries 1–3) and tests them on three diverse problems: stress–strain prediction in materials, path signature estimation for time series, and sparse vector recovery.

## Strengths

- **Group generality beyond existing equivariant tensor methods.** The framework covers O(d), the indefinite orthogonal groups (including Lorentz), and Sp(d) — genuinely broader than e3nn/escnn, which are specific to SO(d)/O(d) for d = 2, 3. The paper explicitly acknowledges this scope difference and discusses the trade-off in computational efficiency (line 33).

- **Novel invariant-theoretic parameterization.** The construction using isotropic tensors avoids Clebsch–Gordan coefficients entirely. Theorem 1 and Corollary 1 provide a clean, unified mathematical characterization of equivariant polynomials. The example in Section 3 (lines 141–155) showing how the familiar form β₀δ + β₁⟨a,a⟩δ + β₂a⊗a emerges from the general theory is pedagogically effective.

- **Three diverse experimental domains.** The paper tests on materials science (stress–strain tensors), time series (path signatures), and sparse vector estimation — genuinely different problems. The sparse vector experiment is carefully designed, systematically varying sampling methods and covariance structures, and the discussion honestly acknowledges where SoS methods outperform the learned approach (Table 3, lines 268–293).

## Weaknesses

### Fatal

None.

### Major

- **Limited comparison against existing equivariant architectures for O(d) tasks.** The paper claims (line 33) that the proposed parameterization has "comparable" computational and approximation power to representation-theoretic methods (e3nn, escnn), but provides no head-to-head experimental comparison against these established equivariant baselines on any O(d) task. The stress–strain experiment includes TFENN (Garanger et al., 2024), which is also equivariant, but TFENN is a specific numerical method rather than a general-purpose equivariant architecture like e3nn/escnn. For the path signature experiment (O(d) case), e3nn or a CG-based equivariant MLP is directly applicable and would ground the comparative claim. Without such a comparison, the practical value of this specific parameterization over prior equivariant approaches on their home turf (O(3)) is not empirically assessed.

### Minor

- **Gap between theoretical generality and experimental scope.** Theorems 1–2 and the theory cover arbitrary tensor inputs/outputs of mixed orders and parities, as well as the symplectic group. However, all experiments use only the simplest corollaries (vector inputs, symmetric 2-tensors), and no experiment exercises the symplectic group. The paper acknowledges that the general form is "impractical" (line 121), but the framing ("first work to provide a recipe… at this level of generality," line 301) overshoots what was actually built and tested.

- **The large performance gap against TFENN is unexplained.** Table 1 shows the proposed method outperforming TFENN by 1–2 orders of magnitude. Since TFENN is also described as equivariant (line 243), this gap warrants discussion. Is TFENN a different model class (e.g., not a learned method)? Does the gap reflect the eigenvalue-based parameterization of Corollary 2 rather than equivariance alone? The paper provides no explanation.

- **Computational practicality details deferred to appendix.** The complexity of Corollary 1 is given as O(k'! n^{k'} (Q d n² + d^{k'})) (line 135), but concrete values (truncation level M, number of sampled points n, dimension d, output tensor orders k' used in path signatures; wall-clock times; parameter counts) are in the appendix. A brief summary in the main text would help readers assess the method's practical regimes.

- **Discussion section lacks limitations.** The discussion (Section 6) is two paragraphs with no limitations paragraph addressing computational bottlenecks, when the method would not be advantageous, or the gap between the full theory and what is practical.

### Trivial

- In Table 2, the O(d) "Ours" entry reports "0.002" without variance, though the caption explains this is because standard deviation < 1e-3. This is fine but could be explicitly noted.

## Nice-to-Haves

- A small synthetic experiment validating the symplectic group case would strengthen the claim of group generality.
- Reporting wall-clock training times or parameter counts in the main text (rather than only the appendix) would help practitioners assess practical trade-offs.
- A brief comparison against e3nn on a small O(3) task (e.g., stress–strain or a simple force-moment prediction) would ground the claim of comparable efficiency.

## Removed Points

These points were flagged in the input review but are removed with justification:

- **Stone–Weierstrass universality criticism (Issue 4 from harsh review).** REMOVED. The reviewer claims the paper does not establish that the specific polynomial subclass separates points and contains constants for a proper Stone–Weierstrass argument. However, Theorem 1 characterizes **all** O(d)-equivariant polynomials, and Corollary 1 characterizes **all** such polynomials for the vector-input case. Since the architecture can represent the full space of equivariant polynomials, and polynomials are dense in continuous functions by Stone–Weierstrass, the universal approximation claim is standard and correctly supported. The reference to Yarotsky (2022) is appropriate. This criticism reflects a misunderstanding of the theorem's scope.

- **Code release concern.** REMOVED (moved here). While mentioning code availability is a reasonable reproducibility suggestion, it is a minor formatting/availability concern rather than a substantive weakness about the paper's content.

- **Missing hyperparameter details in main text as a weakness.** REMOVED (moved here). Deferring architectural details, hyperparameters, and full training specifications to the appendix is standard practice at ICLR and other major venues. The paper consistently references appendix sections for these details (Appendices H, I, J). This is not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a limitations paragraph that discusses computational bottlenecks, the gap between general theory and what is practical, and when the method would not be advantageous over existing approaches.
2. Include concrete values for M (truncation level), n, d, and k' used in the path signature experiment in the main text, not only the appendix.
3. Briefly explain why TFENN (which is also equivariant) performs substantially worse than the proposed method on the stress–strain task — is it not a learned method? Does the eigenvalue-based parameterization offer an advantage beyond equivariance?

---

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>