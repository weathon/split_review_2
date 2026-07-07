## Summary

This paper presents an empirical comparative study of structure-preserving vs. structure-naive approaches for learning dynamical systems from data. Two case studies are examined: (1) a **dissipative heat transfer system**, where a linear state-space model is constrained to the symmetric positive definite (SPD) manifold via Riemannian optimization (RieOpt), and (2) a **conservative Fermi-Pasta-Ulam-Tsingou (FPUT) system**, where a symplectic Hamiltonian neural network (SHNN) enforces symplectic structure. The central thesis is that encoding geometric inductive biases into model architecture enables dramatically smaller models with better long-horizon generalization compared to structure-naive baselines (LSTM, NeuralODE, RF, XGBoost). The FPUT results provide compelling support for this claim; the heat transfer case is more mixed.

## Strengths

- **The FPUT experiments provide genuinely strong evidence for the central thesis.** The best SHNN (1,441 params) achieves rollout MSE of 8.876e-09 and energy drift RMS of 1.322e-03, while the best LSTM (97,074 params—67× larger) achieves rollout MSE of 1.694e-06 and drift RMS of 5.914e+00. The energy drift gap is roughly three orders of magnitude, directly and concretely supporting the claim that structure-preserving models can be dramatically smaller while generalizing better (Section 3.2, Table 2).

- **The hyperparameter sweep over model sizes is well-conceived.** Varying hidden layers and widths over {1,2,4,8} × n_f allows the reader to see the performance-vs-size trade-off continuously rather than cherry-picking a single configuration. Figure 3 communicates the core result clearly (Section 3.2).

- **The dissipative case study includes a meaningful ablation.** Comparing Riemannian optimization (RieOpt) against Euclidean optimization (EucOpt) of the same LSSM architecture isolates the effect of the SPD constraint, while RF, XGBoost, and LSTM provide model-free baselines (Section 3.1, Table 1).

- **The overarching motivation is important and clearly stated.** The argument that geometric structure should be encoded into model architecture rather than relying on data volume or residual-based loss penalties is well-grounded in classical mechanics and differential geometry (Sections 1, 2).

## Weaknesses

### Fatal
None.

### Major

- **The symmetry assumption underlying the SPD manifold approach for the heat transfer system is not verified.** The state matrix A in equation (2) is symmetric *iff* C_{ext1} = C_{ext2}, but the paper provides no argument, evidence, or citation that this holds for the specific system parameters (Table 3 is referenced but its values are not discussed in relation to this condition). The paper hedges with "In several instances, the formulation of system matrix A in equation 2 belongs to the symmetry matrix manifold" (line 69), but does not verify this instance. If the true A is not symmetric, constraining Φ_A to the SPD manifold is an incorrect structural constraint rather than a structure-preserving one, and the comparison between RieOpt and EucOpt becomes uninterpretable without knowing whether the SPD constraint is physically correct. This gap significantly weakens the dissipative case study as a demonstration of structure-preserving learning.

### Minor

- **The loss function in equation (7) contains an apparent typo.** The equation writes `||Φ_A T_i + Φ_B T_i - T_{i+1}||²`, but the discrete-time dynamics in equation (4) are `T_{t+1} = Φ_A T_t + Φ_B U_t`. The loss should use the forcing input U_i, not the state T_i. This is almost certainly a transcription error rather than a code bug (the experiments produce sensible results), but the paper must clarify this discrepancy.

- **No statistical significance, confidence intervals, or multiple-seed results are reported for either case study.** For the heat transfer case (Table 1), single MSE values per model per location are presented with no indication of variance. For the FPUT case (Table 2), each configuration appears to be a single run. While the gap between SHNN and LSTM on energy drift (~1000×) is unlikely to be overturned by variance, the more moderate improvements (e.g., RieOpt vs EucOpt for T_ext2 Chicago: 1.79 vs 1.98) could easily be within noise.

- **The heat transfer results are partially mixed in a way the paper does not fully acknowledge.** Table 1 shows that for T_ext2 (London), XGBoost achieves MSE = 0.106, which is ~5× better than RieOpt's 0.507. The paper's narrative emphasizes that RieOpt and EucOpt demonstrate "global stability" while structure-naive approaches "demonstrate instability," but for the in-distribution London test, XGBoost achieves the best result on one of the two states by a wide margin. While this does not contradict the paper's overall thesis (the Chicago OOD test favors structure-aware methods), the text could be more candid about this tension.

- **The geometric exposition in Section 2.1.1 contains technically confused language.** Line 75 states that eigenvalues are wrapped "within the unit circle in the s-plane where Re(λ_i) > 0"—but the unit circle is a z-plane concept, not the s-plane, and Re(λ) > 0 in the s-plane indicates instability. The intended idea (that the matrix exponential maps stable continuous-time eigenvalues to the interior of the unit circle) is correct, but the phrasing is garbled.

- **The "smaller models" framing fits the FPUT case better than the heat transfer case.** In FPUT, SHNN (1,441 params) genuinely dwarfs LSTM (97,074 params). In heat transfer, the LSSM has 4–5 parameters regardless of optimization method; the comparison is between a tiny physics-motivated model and generic ML models of varying sizes. The title highlights "smaller models," but the dissipative case is more about "the right model structure" than "smaller" per se.

### Trivial

- The notation collision where T is used both for temperature states and the eigenvector matrix in the decomposition `A = VΛT⁻¹` (line 49) could confuse readers.

## Nice-to-Haves

- The paper would benefit from discussing when structure-preserving approaches might fail or be unnecessary, and acknowledging the computational overhead of Riemannian optimization.
- Both case studies use synthetic data; a brief discussion of challenges expected with real-world noisy/partial measurements would strengthen the paper.
- The 1,000-step rollout horizon and the choice of the 2-state lumped model could be empirically justified or discussed.

## Removed Points

These points were removed from the original harsh critic input with brief justification:

- **"The reference to Zhang et al. (2017) seems slightly mismatched"** — minor citation judgment call, not a verified weakness.
- **"PINNs section conflates parameter-space geometry with phase-space geometry"** — the paper's intended meaning is clear; this is an overly literal reading.
- **"The paper does not discuss when structure-preserving approaches might fail"** — generic limitation critique without a concrete anchor; partially covered in Nice-to-Haves.
- **"NeuralODEs trained with Adam at lr=3e-3 may not be standard protocol"** — speculative; the reviewer acknowledges the gap is too large for tuning to close.
- **"Generalization is used to mean two different things"** — the paper uses rollout on unseen time-steps and OOD generalization as complementary evaluations, which is standard.
- **Code/data availability concern** — the ethics statement commits to public release; questioning this violates the rule about citing the paper's own statements.

## Novel Insights

The review surfaces a mathematically-grounded concern about the SPD symmetry condition that the paper's own hedging ("In several instances…") suggests the authors are aware of but do not resolve. Combined with the confirmed typo in equation (7), roughly half of the paper's empirical evidence has an issue that needs direct verification before the dissipative case can be considered reliable. The FPUT evidence, however, stands on its own as a clean and compelling demonstration.

## Suggestions

1. **Resolve the symmetry issue for the heat transfer A matrix:** Either (a) show that for the specific system parameters (the thermal capacitances in Table 3), the matrix is indeed symmetric, or (b) if it is not symmetric, replace the SPD constraint with a more appropriate manifold (e.g., constrain stability directly via eigenvalue projection) or reframe the case study as constrained system identification without claiming the SPD geometry is the system's natural structure.

2. **Correct equation (7)** to use U_i instead of T_i, and confirm in the rebuttal that the implementation uses the correct form.

3. **Report multiple-seed statistics** for at least the best model configurations in the heat transfer case, where the performance margins are smaller.

4. **Acknowledge the mixed result** (XGBoost on T_ext2 London) more explicitly in the narrative.

5. **Clarify the s-plane/z-plane exposition** in Section 2.1.1.

## Score and Decision

**Calibration anchor list:**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `uL1H29dM0c` (Metriplectic) | 7.00 | 1 | Yes | Novel method + theory + extensive experiments. Current paper below this tier. |
| `U1DjXQeJRx` (Poisson-Dirac NNs) | 6.60 | 1 | Yes | Novel method, convincing experiments. Current paper below. |
| `53xxT3LwJB` (NN-ResDMD) | 5.25 | 1 | Yes | Incremental contribution concerns. FPUT evidence stronger. |
| `2AWZTv6kgV` (Projected NDEs) | 4.75 | 1 | Yes | Novelty concerns. Similar tier. |
| `XqDM97DtMf` (Chaotic Dynamics) | 4.67 | 1 | Yes | Novel approach but weak experiments. Current paper above. |
| `60FseFP084` (SPONs) | 4.25 | 1 | Yes | Weak experimental comparison. Current paper above. |
| `GRMfXcAAFh` (LinOSS) | 8.00 | 1 | No | Novel method with theoretical guarantees. Far above. |
| `NRRHkJE03w` (Conservation Principles) | 3.00 | 1 | No | Rejected paper. Below current paper. |
| `SYiOxXWlKU` (EPINN) | 2.50 | 1 | No | Rejected paper. Below current paper. |
| `VtP7CamOR5` (Mamba Neural Operator) | 3.00 | 1 | No | Rejected paper. Below current paper. |
| `HDmmwwTIlf` (Hyperbolic Conservation) | 2.50 | 1 | No | Rejected paper. Below current paper. |
| `qKf0tZtF6B` (Helmholtz-Hodge GP) | 5.80 | 1 | No | Rejected. Comparable domain, stronger in some aspects. |
| `AZGIwqCyYY` (Meta-Learning Hamiltonian) | 5.75 | 1 | No | Accepted. Novel meta-learning approach. |
| `twSnZwiOIm` (Stochastic Dynamical Systems) | 6.00 | 1 | No | Accepted. Strong theoretical contribution. |
| `03EkqSCKuO` (Port-Hamiltonian DGN) | 7.00 | 1 | No | Accepted. Strong theory + experiments. |

**Weighted-item comparison:** The current paper's strongest items (+6.28 FPUT evidence, +5.10 hyperparameter sweep) are competitive with the ~5.25 anchor's strongest items. However, the symmetry issue (-3.94) and lack of multiple seeds (-2.21) are notable negatives that the 6.60+ anchors do not carry. The paper also lacks the novel methodological contribution of those higher-tier papers. The FPUT evidence places it above the 4.25–4.75 anchors (whose experimental sections were weaker), but the unresolved gap in the heat transfer case prevents it from reaching the 6.60+ tier.

**Initial bracket (Round 1):** between 4.67 and 5.25.
**Narrowed final:** 5.0.

The paper makes a meaningful empirical contribution, particularly through the FPUT experiments. However, the unresolved symmetry issue undermines the dissipative case study, and the paper does not introduce novel methodology. The score reflects that the paper sits between the lower-tier anchors with weak experiments and the higher-tier anchors with novel methods and comprehensive validation.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>