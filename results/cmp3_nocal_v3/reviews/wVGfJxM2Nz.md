## Summary

This paper argues that geometry-informed inductive biases (symplectic structure for conservative systems, SPD manifold constraints for dissipative systems) reduce the need for large models when learning dynamical systems from data. Two case studies are presented: a 2-dimensional heat transfer system identified via Riemannian optimization on the SPD manifold, and an 18-dimensional Fermi-Pasta-Ulam-Tsingou (FPUT) system modeled with a symplectic Hamiltonian neural network (SHNN). The FPUT experiment provides strong evidence that structure-preserving models achieve qualitatively better energy conservation with far fewer parameters than structure-naive baselines.

## Strengths

- **The FPUT experiment (Section 3.2, Table 2) is the paper's strongest contribution.** A systematic sweep over hidden layers L ∈ {1,2,4,8} and widths W ∈ {18,36,72,144} for SHNNs, NeuralODEs, and LSTMs generates a clear empirical picture. The result that a 1,441-parameter SHNN achieves rollout MSE comparable to—and energy drift (RMS ≈ 10⁻³) orders of magnitude lower than—a 97,074-parameter LSTM (drift RMS ≈ 5.9) genuinely demonstrates that symplectic structure can substitute for raw capacity. The drift RMS metric is the right diagnostic for this claim.

- **The paper's framing is well-motivated and clearly stated.** The observation that naive ML models learn dynamics in flat Euclidean space while physical systems evolve on structured manifolds (Section 1) connects to a real problem in scientific ML and provides a clear rationale for the two case studies.

## Weaknesses

### Fatal

None.

### Major

1. **The heat transfer experiment does not cleanly support the "smaller models" thesis claimed in the title and conclusion.** Within the LSSM family (Physics, RieOpt, EucOpt), model size is fixed at 6 parameters and never varied — the RieOpt vs. EucOpt comparison is a meaningful ablation of optimization quality, not model size. The comparison against RF, XGBoost, and LSTM compares fundamentally different hypothesis classes (physics-derived linear model vs. black-box time-series predictors), and the model sizes of those baselines are not reported, so the reader cannot assess the size differential. The experiment shows that Riemannian optimization improves over Euclidean optimization for the same model (Table 1: RieOpt vs. EucOpt on Chicago T_ext1: 1.36 vs. 3.35) and that a small structured model beats black-box methods on OOD data — both meaningful findings — but this does not constitute evidence that _varying_ model size reveals a structural advantage. The conclusion (line 250) states "varying model size revealed that stable generalization… is achievable with models that are much smaller," which is accurate for the FPUT case but unsupported for the heat transfer case.

2. **No variance or statistical significance is reported for any result.** Every number in Table 1 and Table 2 is a single value with no error bars, standard deviations, or mention of random seeds or independent runs. Neural network training is stochastic. For the FPUT case (Table 2), SHNN one-step MSE spans 3.09e-09 to 6.05e-08 across model sizes — a range larger than the gap between SHNN and NeuralODE at many individual configurations — making it impossible to assess which differences are reliable. The drift RMS numbers (10⁻³ for SHNN vs. 10⁰–10³ for baselines) show such a large qualitative gap that this concern is less acute for the paper's main claim, but it remains a standard expectation for empirical ML work.

### Minor

3. **Equation (7) has an apparent error in the loss function.** The equation (line 93) reads ‖Φ_A T_i + Φ_B **T**_i − T_{i+1}‖²₂, but the model definition in Equation (4) (line 83) states T_{t+1} = Φ_A T_t + Φ_B **U**_t. The loss function incorrectly uses the state T instead of the input U in the second term. If the implementation matches what is written, the optimization fits a different model than claimed.

4. **Data dimensionality is confusingly reported.** Line 153 states T ∈ ℝ^{8759×1} for the heat transfer data, but the state space in Equation (2) is 2-dimensional (T_ext1, T_ext2). The forcing matrix U is correctly given as ℝ^{8759×2}. This is likely a typo (should be ℝ^{8759×2} or ℝ^{2×8759}), but it introduces ambiguity about how the data were structured for training.

5. **The LSTM sweep in the FPUT experiment is asymmetric.** SHNN and NeuralODE are swept over both hidden layers L and widths W (16 configurations each), while LSTM is swept over W only (4 configurations). The paper highlights the "1,441 params vs. 97,074 params" comparison, but because LSTM was never varied over L, it is unclear whether the gap could be narrowed with a different LSTM architecture. This does not invalidate the result, but the asymmetry should be discussed.

6. **The description of the bilinear transform (Section 2.1.1, line 75) contains a confusing domain error.** The text states that eigenvalues are mapped "within the unit circle in the **s**-plane" when the context makes clear the unit circle should be in the **z**-plane. The sentence switches between s-plane and z-plane mid-argument in a way that obscures the intended geometric mapping.

7. **The convergence speed claim (line 175) is asserted without supporting evidence accessible in the paper.** The paper states structure-naive models have "significantly slower" training convergence, citing figures that are not visible in the extracted text. Even if visible, convergence curves without wall-clock time or iteration counts do not constitute a rigorous comparison — the LSSM models have 6 parameters while RF, XGBoost, and LSTM involve substantially different training procedures.

### Trivial

None.

## Nice-to-Haves

- **Vary model size for the LSSM family in the heat transfer experiment.** Using higher-dimensional LSSMs (e.g., 10- or 50-state) and showing that the SPD-constrained version works well with relatively few parameters while the unconstrained version and black-box methods need many more would directly test the paper's thesis for the dissipative case.
- **Add a controlled experiment with deliberately misspecified physics** to test whether Riemannian optimization recovers from a wrong structural prior better than Euclidean optimization.
- **Discuss limitations** — when structure preservation might fail (e.g., when the system is not approximately Hamiltonian, when the dissipation model is not SPD, when dynamics are not low-dimensional).
- **Report computational cost** — Riemannian optimization has higher per-iteration cost (exponential/logarithmic maps, tangent-space projections); a practitioner would want to know whether the parameter savings offset this.
- **Discuss the mismatch between the 2-state lumped-parameter model and the high-fidelity EnergyPlus data** — making this explicit would strengthen the motivation for why the SPD constraint matters.

## Removed Points

- **"Heat transfer baselines do a different task"** — The critic argued that comparing physics-derived LSSMs against black-box methods is unfair because "the LSSM knows the correct model structure by design." This is a strawman: the paper's thesis is that encoding correct structure helps, so comparing against models without that structure is exactly the experiment needed. The sub-point about misspecified physics is valid and moved to Nice-to-Haves.
- **"No code or data availability"** — Removed per hard rule: questions about the release status of cited models/datasets are not to be included.
- **"Missing discussion of limitations"** — A valid suggestion, moved to Nice-to-Haves.
- **"Computational cost comparison missing"** — A valid suggestion, moved to Nice-to-Haves.
- **"Two-case-study structure provides useful breadth"** — Generic strength, removed.
- **"Section 1/1.1 PINNs positioning"** — Suggestion to better relate to existing structure-preserving NN work; not a core weakness, moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a genuinely novel observation about the paper that the authors did not already make.

## Suggestions

- Fix the error in Equation (7) — the second term should be Φ_B U_i, not Φ_B T_i.
- Clarify the dimensionality of the heat transfer data (line 153).
- Report error bars (mean ± std over at least 3 random seeds) for all main results, particularly Tables 1 and 2.
- Add a paragraph explicitly acknowledging what the heat transfer experiment does and does not demonstrate about model size, and adjust the conclusion to match.
- Add a symmetry argument or explicit discussion for the LSTM sweep in FPUT.
- Fix the s-plane/z-plane confusion in Section 2.1.1.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>