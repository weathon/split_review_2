Now I have enough calibration data. Let me write the final consolidated review.

## Summary

This paper empirically compares structure-preserving models against "structurally naive" baselines on two dynamical system learning tasks: (1) a dissipative 2D heat transfer system identified via a linear state-space model with SPD constraint and Riemannian optimization, and (2) a conservative 18D Fermi-Pasta-Ulam-Tsingou (FPUT) system modeled via symplectic Hamiltonian neural networks (SHNNs). The core thesis is that geometry-informed inductive biases enable robust generalization with smaller models.

## Strengths

- **FPUT size-sweep experiment is well-executed and provides striking evidence.** Table 2 systematically sweeps hidden layers and widths for SHNN, NeuralODE, and LSTM, cleanly showing the relationship between parameter count, rollout accuracy, and energy drift. The finding that a 1,441-parameter SHNN achieves better 1000-step rollout quality and energy drift than the best LSTM (97,074 parameters) is a concrete, non-trivial result that directly supports the paper's thesis about the value of structure-preserving inductive biases.

- **Energy drift RMS is a well-chosen diagnostic.** Measuring drift from the true Hamiltonian surface provides a mechanistic explanation for why rollout quality degrades for naive models—they leave the correct energy surface—going beyond reporting rollout MSE alone. This metric cleanly separates SHNN from NeuralODE and LSTM in Table 2.

- **The two case studies genuinely span complementary physical regimes.** A dissipative linear system (2D heat transfer) and a conservative nonlinear Hamiltonian system (18D FPUT lattice) are qualitatively different classes. Showing benefits in both broadens the paper's relevance.

## Weaknesses

### Fatal
None.

### Major

1. **The A matrix symmetry claim is insufficiently justified for the heat transfer system, weakening the "structure-preserving" framing.** Section 2.1.1 (line 69) states that the system matrix A in Equation 2 "belongs to the symmetry matrix manifold Sym_n where A = A^T." The off-diagonal entries are `U/C_ext1` and `U/C_ext2`; these are equal only when C_ext1 = C_ext2. The paper describes the material as "homogeneous" (line 153) and uses a lumped-parameter discretization—which would indeed give equal capacitances for equal-size cells in a homogeneous material—but it never explicitly states that C_ext1 = C_ext2 nor provides the actual parameter values (relegated to the stripped appendix). The entire geometric framing—SPD manifold portraits in Figure 1, the Riemannian optimization narrative, the claim that "every point is equivalent to a unique and valid physical system"—rests on this premise without sufficient explicit justification. This is not necessarily wrong, but the paper needs to justify it clearly. **Why it matters:** If the physical A matrix is not symmetric, constraining Φ_A to the SPD manifold is an externally imposed regularization, not a "structure-preserving" inductive bias. The paper should either explicitly justify the symmetry (e.g., by confirming that C_ext1 = C_ext2 follows from the homogeneous material and equal cell sizes) or reframe the constraint as a stability-enforcing prior rather than a structure-preserving one.

2. **The dissipative case study's comparison conflates "structure-preserving" with "physics-informed model class."** RieOpt and EucOpt use an LSSM whose 2×2 topology is derived from the known physics (Equation 2). The baselines (RF, XGBoost, LSTM) are generic time-series forecasting methods with no access to this dynamical structure. The comparison therefore does not isolate the effect of the SPD constraint—it compares a physics-informed model class against model-agnostic methods. A fairer test would include a model-agnostic method that can learn dynamics (e.g., a NeuralODE or a learned Koopman operator without structural constraints). The poor OOD generalization of RF and XGBoost (Chicago test set) is unsurprising and provides weak evidence for the specific value of SPD-constrained Riemannian optimization. **Why it matters:** The dissipative results do not cleanly support the paper's geometric narrative; they may simply show that having the right model class matters more than any geometric constraint.

3. **Missing baseline: a standard HNN (without symplectic integrator) is needed to isolate the source of SHNN's benefit.** The paper compares SHNN (Hamiltonian parameterization + symplectic midpoint integrator) against LSTM and NeuralODE, neither of which has Hamiltonian structure. Comparing SHNN to a standard HNN (Greydanus et al., 2019) with a non-symplectic integrator would isolate whether the benefit comes from (a) the Hamiltonian parameterization, (b) the symplectic integrator, or (c) both. Since HNNs are a well-established six-year-old method, this omission weakens the paper's causal attribution to "symplectic structure preservation" as distinct from "having a Hamiltonian prior." **Why it matters:** The paper's core claim about the FPUT system is that *symplectic* structure preservation drives the advantage, but the experimental design cannot distinguish this from the Hamiltonian parameterization alone.

### Minor

1. **The "smaller models" title and framing are overstated.** Table 2 shows that larger SHNNs (e.g., L=8, W=144 at 149,041 params) achieve better one-step MSE and energy drift than smaller SHNNs. The evidence supports "structure-preserving models achieve better performance per parameter" rather than "smaller models are categorically better." The dissipative case contributes little to this claim since the LSSM is always 6 parameters regardless.

2. **Equation 7 has a likely typo.** The loss is written as `J = Σ ||Φ_A T_i + Φ_B T_i - T_{i+1}||²`, but the dynamics (Equation 4) are `T_{t+1} = Φ_A T_t + Φ_B U_t`. The term should be `Φ_B U_i`, not `Φ_B T_i`. If this is only a typesetting error it should be fixed; if the implementation uses `T_i`, the loss does not match the stated dynamics.

3. **XGBoost beats RieOpt on T_ext2 for London (in-distribution) without comment.** Table 1 shows XGBoost achieves MSE 0.106 vs RieOpt's 0.507 on T_ext2 for the London test set. The paper highlights RieOpt's advantages but does not discuss this reversal, which undercuts the claim of uniform superiority.

4. **No error bars or statistical significance.** Table 1 and Table 2 report point estimates only. Without multiple seeds or confidence intervals, it is unclear whether the reported differences are meaningful beyond single-run variation.

5. **NeuralODE drift RMS values appear implausibly large.** Values range from 1.194 to 1802 (Table 2), compared to SHNN's ~10⁻³ to 10⁻⁴. This may indicate poor tuning rather than a structural limitation of NeuralODEs. Reporting the typical energy scale of the FPUT system would contextualize these numbers.

### Trivial

- The s-plane/z-plane mapping description in Section 2.1.1 (line 75) is garbled: it refers to "the unit circle in the s-plane" where it should say "z-plane," and the sign condition for discrete-time stability is confused.
- Data dimensionality: T is described as ℝ^{8759×1} (line 153) but the LSSM has two temperature states (T_ext1, T_ext2), creating ambiguity about what the data actually represents.
- Training/test split for the London data is not specified in the main text.

## Nice-to-Haves

- Adding a standard HNN baseline (without symplectic integrator) to the FPUT experiments would cleanly separate Hamiltonian parameterization effects from symplectic integration effects.
- Adding a learned Koopman operator or NeuralODE without structural constraints to the dissipative comparison would better isolate the value of the SPD constraint.
- Including error bars or multiple-seed results would strengthen the quantitative claims.
- Describing the unseen initial conditions used in Figures 4b/4c would improve reproducibility.

## Removed Points

- **The critic's "fatal" claim about A matrix asymmetry being a structural flaw (Weakness 1, framed as fatal):** The paper describes a "homogeneous material system" with a lumped-parameter discretization into equal cells—reasonable grounds for C_ext1 = C_ext2. The critic's stronger claim that the matrix "does not naturally have" symmetric structure is not verifiably true from the paper alone; the actual parameter values (Table 3) are in the stripped appendix. Demoted from "fatal" to "major" with a narrower framing: the justification is insufficiently explicit rather than factually incorrect.
- **Missing appendix content / Table 3 not in main text:** Removed per hard rule on appendix stripping by the parser.
- **Citation inconsistency ("Xuereb Conti" vs "Xueréb Conti"):** Removed as a pure formatting nitpick.
- **Abstract overclaiming about "identified" vs parameter estimation:** "System identification" is standard terminology for this type of parameter estimation; reasonable usage.
- **"All conservative systems can be represented in a Hamiltonian formulation" caveat:** The paper's Section 2 clearly distinguishes conservative from dissipative systems, so this criticism misreads the scope.
- **Generic/superficial strengths from the input** (e.g., "the paper addresses an important problem") were removed as lacking specific evidence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Explicitly justify the symmetry of A: state that C_ext1 = C_ext2 follows from the homogeneous material with equal-size discretization cells, or provide the parameter values from Table 3 in the main text.
2. Add a standard HNN baseline to the FPUT experiments.
3. Fix the typo in Equation 7 (Φ_B T_i → Φ_B U_i).
4. Acknowledge and discuss the XGBoost success on T_ext2 (London).
5. Tone down the "smaller models" framing to something like "better performance per parameter through structure preservation."
6. Consider dropping or substantially reframing the dissipative case study if the symmetry justification cannot be cleanly made; the FPUT results alone provide sufficient evidence for the paper's thesis.

## Score and Decision

**Calibration anchors:** I retrieved and inspected papers across all score bands. The most relevant anchors in the 3.5–6.5 range were: *Learning Chaotic Dynamics with Embedded Dissipativity* (4.67, Reject), *Projected Neural Differential Equations* (4.75, Reject), *NN-ResDMD* (5.25, Reject), *Benchmarking Structural Inference Methods* (5.50, Reject), *Learning Dynamical Systems with Helmholtz-Hodge Decomposition and GPs* (5.80, Reject), and *Poisson-Dirac Neural Networks* (6.60, Accept). Also relevant were *Efficiently Parameterized Neural Metriplectic Systems* (7.00, Accept) and *Port-Hamiltonian Architectural Bias* (7.00, Accept) in the 5.5–8.5 range. All retrieved anchors are listed below.

**Round 1 bracket:** 3.5–6.5. The paper has genuine evidence (FPUT experiments comparable to accepted papers in the 6–7 range) but is weighed down by the flawed dissipative case study and missing HNN baseline, placing it below the accept threshold.

**Narrowing:** Compared to *NN-ResDMD* (5.25, Reject), which had solid methodology but incremental contribution, the current paper has more striking experimental results (the 67× parameter advantage) but also more significant methodological issues in the dissipative case study. Compared to *Poisson-Dirac Neural Networks* (6.60, Accept), which proposed a new framework with comprehensive evaluation, the current paper has substantially less novelty. The paper sits between these anchors.

**Final score: 5.0.** The FPUT experiments are genuinely impressive and the energy drift diagnostic is insightful. However, the dissipative case study's insufficiently justified A matrix symmetry claim, the unfair comparison design there, and the missing HNN baseline in the FPUT experiments prevent the paper from making a fully coherent case for its stated thesis. Major revision (particularly reframing or replacing the dissipative case study and adding the HNN baseline) could raise this to an accept-level paper.

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| KL Divergence Optimization for Stochastic GFlowNets | 1.00 | 1 | Far weaker; no relevance to dynamical systems |
| Scaling In-the-Wild Training for Illumination | 10.00 | 1 | Far stronger; accepted paper in different field |
| Systematic Review of LLMs | 1.00 | 1 | Far weaker; survey paper |
| All Pairs Minimax Path Problem | 1.00 | 1 | Far weaker; algorithms paper |
| Data-Driven Discovery of PDEs via Adjoint Method | 3.00 | 1 | Weaker; narrower scope, less compelling experiments |
| Fusion over the Grassmannian | 3.00 | 1 | Weaker; different topic (matrix completion) |
| Manifold Kernel Rank Reduced Regression | 3.00 | 1 | Weaker; different topic |
| Probabilistic Approach to MRI Hardware Control | 3.00 | 1 | Weaker; different domain |
| Learning Chaotic Dynamics with Embedded Dissipativity | 4.67 | 1 | Similar topic, comparable quality; split reviews, limited experiments |
| NN-ResDMD: Learning Koopman Representations | 5.25 | 1 | Similar topic; incremental method but solid experiments; our paper has more striking results but more flaws |
| Projected Neural Differential Equations | 4.75 | 1 | Similar topic; new method but limited baselines; comparable quality |
| Inducing Precision in Lagrangian Neural Networks | 3.67 | 1 | Weaker; narrower scope |
| Port-Hamiltonian Architectural Bias for Deep Graph Networks | 7.00 | 1 | Stronger; accepted paper with principled framework |
| Towards Cross Domain Generalization of Hamiltonian Representation | 5.75 | 1 | Similar topic; accepted but lower score |
| Efficiently Parameterized Neural Metriplectic Systems | 7.00 | 1 | Stronger; accepted paper with theoretical guarantees |
| Poisson-Dirac Neural Networks | 6.60 | 1 | Stronger; accepted paper with new framework |
| Learning Distributions of Complex Fluid Simulations | 7.60 | 1 | Stronger; accepted paper in related area |
| Oscillatory State-Space Models | 8.00 | 1 | Much stronger; accepted SOTA method paper |
| Latent Representation of Markov Processes | 8.00 | 1 | Much stronger; accepted paper |
| Unified Generative Modeling of 3D Molecules | 8.00 | 1 | Much stronger; different domain |
| Learning Dynamical Systems with Helmholtz-Hodge Decomposition and GPs | 5.80 | 2 | Similar topic; physics-informed method paper; comparable quality |
| Benchmarking Structural Inference Methods | 5.50 | 2 | Similar genre (empirical comparison); comprehensive but limited novelty |
| Lyapunov Stability Learning via Inductive Biases | 4.00 | 2 | Similar topic; weaker paper |

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>