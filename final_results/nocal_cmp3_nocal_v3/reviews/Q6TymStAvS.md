## Summary

This paper introduces ShadowFM, a geometric flow matching framework for generating classical shadows of quantum many-body ground states. The key insight is that Pauli-6 POVM shadows naturally live on the Bloch sphere (S²), and the paper proposes two geometry-aware approaches: **Spherical Flow** (Riemannian flow matching on S² with closed-form exp/log maps) and **Anisotropic Dirichlet Flow** (a generalization of Dirichlet flow that introduces a target/anti-target pairing structure via a γ-parameterized probability path). Empirically, the methods consistently outperform non-geometric baselines across TFIM and Heisenberg models at multiple system sizes, including a genuine out-of-distribution extrapolation task (time dynamics) and a 2D Heisenberg model.

## Strengths

1. **Principled geometric motivation grounded in quantum mechanics.** The paper draws a clear mathematical chain from the Bloch sphere / CP¹ geometry (Section 3.1) to the design of generative models. The toy experiment (Fig 2) empirically anchors why geometry matters — spin errors are more detrimental than basis errors — and this directly informs the method design (antipodal separation on S² for spin-flipped pairs, target/anti-target pairing in AD flow).

2. **Two complementary geometric approaches, both technically well-specified.** The Spherical Flow correctly identifies Pauli shadows as points on S² and applies RFM with closed-form exp/log maps (Eq 3). The Anisotropic Dirichlet Flow is a non-trivial generalization of Dirichlet flow (Stark et al., 2024): the derivation of C(x_i,t) and D(x_ī,t) from the continuity equation (Eqs 6-9), and the recovery of standard Dirichlet flow when γ=0, demonstrate technical competence.

3. **Consistently strong empirical results across multiple settings.** Across six tables (TFIM L=10, L=30; Heisenberg L=10, L=30; time dynamics; 2D Heisenberg), the proposed methods — especially Spherical Flow — consistently outperform all baselines by substantial margins. For example, TFIM L=10 (Table 1): Spherical achieves RMSE correlation 0.041 vs. StatisticalFM's 0.126 at 100k shadows. AD Flow approaches the exact CS oracle's 10k accuracy using 100k generated samples (0.021 vs. 0.027).

4. **Broad evaluation scope.** The paper tests on two distinct physical models, multiple system sizes (L=10, L=30, 4×4), multiple tasks (ground state prediction, phase transition capture, real-time dynamics extrapolation, training sample scaling), and extends to tetrahedral POVM shadows.

5. **Phase transition dynamics and time dynamics experiments.** Figure 5(a,b) shows the method captures physically meaningful structure (abrupt derivative change at the critical point) that simpler baselines miss. The extrapolation from t∈[0,1) to t∈[1,2) in Table 5 is a genuine out-of-distribution test.

## Weaknesses

### Fatal
None.

### Major

1. **The "generalization to unseen Hamiltonians" claim is not cleanly validated.** The paper's abstract (line 9) and introduction (lines 17-18, 37-38) prominently frame generalization to *unseen* coupling constants as a key capability: "more accurate prediction of an unseen quantum state's observables" and "for unseen Hamiltonians, we will be able to estimate observables that we could only otherwise evaluate by naive interpolation." However, the main experiments (Tables 1-4, 6) report RMSE "averaged over a test set of 100 ground states" without specifying whether the coupling constants c in the test set were held out during training. The training sample scaling experiment (Section 4.4, line 301) is explicitly labeled "on seen Hamiltonians," making the ambiguity in the main experiments conspicuous. The time-dynamics experiment does test out-of-distribution extrapolation (unseen *times*), but this is a qualitatively different form of generalization. The paper should either (a) explicitly state the train/test split of coupling constants for every experiment, or (b) redesign the evaluation to include a held-out set of c values.

2. **Multi-qubit generation mechanism is underspecified.** Sections 3.2.1-3.2.2 describe per-qubit state spaces (S² with K=3 for Spherical Flow, Δ⁵ with K=6 for AD Flow) but never clarify how these are composed for an L-qubit system. The velocity field v_θ(x_t, t|c) and denoising classifier p_θ(x₁|x_t, c) operate on *some* representation of the full L-qubit shadow, but the paper does not state whether (a) each qubit is generated independently (product distribution), which would factorize the joint distribution and miss connected correlations ⟨Z_i Z_j⟩, or (b) the model operates jointly on the product manifold (S²)^L or (Δ⁵)^L. The empirical results (low RMSE on correlation functions) implicitly confirm the model captures cross-qubit correlations, so option (b) is what is implemented, but the paper never states this, describes the network architecture for the L-dimensional input, or discusses whether the model is permutation-equivariant. This is a structural clarity gap.

### Minor

3. **AD flow velocity field integral computation not specified.** Equations (8)-(9) define C(x_i,t) and D(x_ī,t) via integrals involving incomplete Beta and digamma functions. The limitations section (line 333) vaguely mentions "pre-computations ... involving the computation of integrals, which introduces additional overhead" but does not describe how these are computed in practice (numerical quadrature? precomputed tables? closed-form for special cases?). While this is a standard numerical computation, the absence of any implementation description is a reproducibility gap.

4. **No direct evidence for the claimed error-suppression mechanism.** The paper's core thesis is that respecting Bloch-sphere geometry improves shadow generation by suppressing spin errors. The toy experiment (Fig 2) motivates why spin errors matter, and the methods are designed to separate spin-flipped pairs. However, there is no direct analysis showing that Spherical Flow actually produces fewer spin errors than baselines (e.g., confusion matrices over the 6 Pauli outcomes, or rates of spin-flip vs. basis-flip errors). The evidence is entirely downstream (lower RMSE on observables), which is consistent with the mechanism but does not verify it directly.

5. **Performance reversal on TFIM L=30 not discussed.** Table 2 shows that for TFIM L=30 correlation at 100k shadows, StatisticalFM (0.120) outperforms Spherical Flow (0.153). At L=10, Spherical is far better (0.041 vs 0.126). This reversal is not mentioned or discussed in the paper, leaving the reader to wonder whether the geometric advantage degrades at larger system sizes for certain observables.

6. **AD flow γ sensitivity not reported.** The paper states "For our AD flow, we evaluate for γ ∈ {0, 0.05, 0.1} and report the best value" (line 223) but does not state which γ was chosen for each experiment or how sensitive results are to this choice. Since γ=0 recovers standard Dirichlet flow and γ>0 is the claimed contribution, this analysis is needed.

7. **Standard deviations in some tables lack provenance.** Table 4 (Heisenberg L=30) shows ±0.001 for nearly every correlation entry. The paper states results are "averaged over a test set of 100 ground states" (line 221) but does not clarify whether the standard deviations are over random seeds, over test Hamiltonians, or over generated shadow sets.

8. **Toy experiment limited scope.** The motivating experiment (Fig 2) tests only L=6 with three observables (XX, YY, ZZ). The conclusion that "spin errors are more detrimental" is reasonable but its generality across system sizes could be explicitly noted as a limitation.

### Trivial

9. The Spherical Flow prior (pushforward from C³ to S²) concentrates density at the six Pauli directions, matching the target distribution well. This is a favorable choice that is not analyzed or discussed.

## Nice-to-Haves

- Analyze error types produced by Spherical Flow vs. baselines to directly validate the claimed spin-error suppression mechanism.
- Report which γ value was selected for each AD Flow experiment and provide a sensitivity curve.
- Clarify what the standard deviations in Tables 1-6 represent.
- Discuss whether a uniform prior on S² (instead of the pushforward from C³) would change results.
- Include a brief discussion of why the TFIM L=30 correlation performance reverses relative to L=10.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Algorithm 1 and 2 are referenced but in the stripped appendix"** — REMOVED: parser strips appendix content; these sections exist in the original submission.
- **"Missing baselines (autoregressive models)"** — REMOVED: the paper explicitly acknowledges this limitation (line 333); evaluating against every possible method is not required.
- **"Missing comparison with Tang et al. (2025) diffusion"** — REMOVED: Diff-LM is a diffusion baseline addressing this.
- **"Background section is adequate but brief"** — REMOVED: generic observation, not a weakness.
- **"The noise distribution properties are not discussed"** — MERGED into Trivial item 9 (weakened from the reviewer's stronger framing about "data leakage").
- **"The tetrahedral POVM table is referenced but removed"** — REMOVED: appendix content stripped by parser.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface a perspective on the paper that is not already present in the paper's own framing.

## Suggestions

1. Explicitly state the train/test split of coupling constants for all main experiments (Tables 1-6). If feasible, add an experiment with a cleanly held-out set of c values to directly validate the "unseen Hamiltonians" claim.
2. Describe the multi-qubit generation mechanism in detail: how L qubits are composed, the neural network architecture for the L-dimensional input, and whether the model is permutation-equivariant.
3. Provide implementation details for the AD flow integral computation (Eqs 8-9).
4. Add an error-type analysis (spin vs. basis error rates in generated shadows) to directly validate the geometric mechanism.
5. Discuss the TFIM L=30 correlation performance reversal.

## Score and Decision

**Score:** 7

**Decision:** Accept

**Rationale:** The paper presents a novel, physically principled geometric approach to shadow generation with consistently strong empirical results across multiple settings. The two proposed methods (Spherical Flow and Anisotropic Dirichlet Flow) are technically well-developed, and the geometric motivation is clearly grounded in quantum mechanics. However, two structural clarity gaps — the ambiguous validation of the "unseen Hamiltonians" generalization claim and the underspecified multi-qubit generation mechanism — prevent this from being a stronger paper. Both are addressable with clarification and do not undermine the core technical contribution or the main empirical findings. With these clarifications, this would be a strong paper.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>