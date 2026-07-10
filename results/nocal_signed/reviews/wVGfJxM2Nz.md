Now let me write the final consolidated review.

## Summary

This paper presents a comparative study of structure-preserving vs. structure-naive ML methods on two dynamical systems: (1) a 2D heat transfer (dissipative) system where a linear state-space model is constrained to the SPD manifold via Riemannian optimization, and (2) an 18-dimensional FPUT (conservative) system where a symplectic Hamiltonian neural network (SHNN) enforces symplectic structure. The central thesis is that structure-preserving inductive biases enable smaller, more generalizable models.

## Strengths

- **Clean FPUT experiment with thorough hyperparameter sweeps (Table 2, Figure 3).** SHNN achieves dramatically lower energy drift (RMS ~10⁻³) vs. LSTM (~10⁰) and NeuralODE (~10⁰–10³) across a wide range of model sizes (L, W sweeps). The smallest SHNN (1,441 params) outperforms the best LSTM (97,074 params) on rollout and drift. This is the paper's strongest empirical evidence and convincingly demonstrates the value of symplectic structure.

- **Energy drift as an evaluation metric (Section 3.2).** The drift RMS metric directly measures whether a model respects the Hamiltonian invariant, going beyond MSE to genuinely test structure preservation. Figures 4(a)–(c) visually support this metric in a compelling way.

- **Honest framing of limitations.** The paper acknowledges that its dissipative system is small (2D), that data is synthetic, and that the methods (Riemannian optimization on SPD, SHNN) are adopted from prior work.

## Weaknesses

### Major

- **The SPD constraint justification is not physically grounded for the specific heat transfer system.** The A matrix in Equation 2 has off-diagonal entries U/C_ext1 and U/C_ext2, which are equal *only if* C_ext1 = C_ext2 — a condition the paper never verifies or discusses. The paper claims (line 69) that A "belongs to the symmetry matrix manifold Sym_n where A = A^T", but for a general material these heat capacities differ, making A non-symmetric. If the continuous-time A is not symmetric, its matrix exponential e^{Aτ} is not symmetric either, and constraining Φ_A to the SPD manifold does not "preserve the geometric structure" of the system — it imposes a structure the true system may not possess. This undermines the geometric motivation in Section 2.1.1, which occupies a substantial fraction of the paper's methodological exposition. The empirical results (RieOpt performs well) may still be valid, but the claimed mechanism is at odds with the physics as written.

- **No uncertainty quantification for stochastic models.** Tables 1 and 2 report single values with no error bars, standard deviations, or mention of how many random initializations were used. For LSTM and NeuralODE training — which are inherently stochastic and whose reported values span many orders of magnitude (e.g., NeuralODE drift RMS from 1.194 to 1.802e+03 across different architectures) — it is impossible to assess whether the reported differences between methods are statistically significant or within run-to-run noise. This is a basic expectation for an empirical comparison paper that makes strong claims about which method is "better."

### Minor

- **Equation 7 contains a substantive inconsistency with the stated dynamics.** The loss function writes ‖Φ_A T_i + Φ_B T_i − T_{i+1}‖², but the system dynamics in Equation 4 require Φ_B multiplied by the input U_i, not the state T_i. Unless this is a typesetting error, the loss function as written is inconsistent with the model it aims to fit. The paper should clarify whether the implementation uses U_i (as Equation 4 dictates) or T_i (as Equation 7 writes).

- **The "smaller models" claim is conflated in the dissipative experiment.** The LSSM (at most 6 parameters for a 2×2 A and 2×1 B) is compared against LSTMs with tens of thousands of parameters — this is a comparison of *model class* (linear state-space vs. recurrent neural network), not a controlled test of whether the SPD constraint enables smaller models. A structure-naive linear model of the same parameter count would isolate the benefit of the SPD constraint from the benefit of using a linear state-space model. Moreover, EucOpt (which does not enforce SPD) also generalizes well OOD (Table 1, Chicago: RieOpt 1.36 vs EucOpt 3.35 on T_ext1; both far better than RF/XGBoost/LSTM), suggesting the LSSM structure itself, not the SPD constraint, drives OOD generalization.

- **The training convergence claim (line 175) is not a meaningful comparison.** The paper states structure-naive models have "significantly slower" training convergence, referencing figures in the (stripped) appendix. Comparing convergence speed across XGBoost, LSTM, and gradient-based LSSM optimization — which use fundamentally different training paradigms, loss surfaces, and optimizers — conflates incomparable quantities. This claim should either be removed or restricted to comparisons within the same optimization framework.

## Nice-to-Haves

- Add a standard HNN baseline (without symplectic midpoint integrator) for the FPUT experiment to ablate whether the benefit comes from the Hamiltonian parametrization or the symplectic integrator.
- Report normalized error metrics (NRMSE, R²) for the dissipative case to make MSE values interpretable relative to the scale of the temperature variables.
- Test the dissipative approach on higher-dimensional systems or systems where the A matrix is clearly non-symmetric to characterize when the SPD constraint helps vs. hurts.

## Removed Points

- *Criticism that PINNs are incorrectly positioned as "structurally naive":* The paper's characterization that PINNs encode physics through loss penalties rather than architectural biases is broadly accurate for standard PINNs. This nuance does not affect the paper's experiments.
- *Request for HNN (without symplectic integrator) baseline as a weakness:* A reasonable suggestion but not a flaw — the existing comparison against LSTM and NeuralODE is informative.
- *Missing SINDy reference:* Per policy, missing related works are not flagged.
- *Criticism that the paper lacks novelty because it applies existing methods:* The paper is framed as a comparative demonstration. The contribution is judged on the strength of that demonstration.
- *Request for higher-dimensional dissipative systems:* The paper scopes itself to a 2D system and acknowledges this; this is scope creep.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the FPUT experiment is a solid empirical validation of known structure-preserving methods, while identifying that the dissipative case's geometric justification is partially invalid and that the "smaller models" thesis is overstated.

## Suggestions

1. **Address the symmetry issue**: Either verify that C_ext1 = C_ext2 for the specific material parameters used (Table 3), or reformulate the geometric justification to avoid relying on A's symmetry (e.g., argue the SPD constraint as a stability-promoting inductive bias rather than a structure-preserving one tied to the physics).
2. **Fix Equation 7** to use U_i instead of T_i in the Φ_B term, and clarify the actual implementation.
3. **Report uncertainty**: Provide results across multiple random seeds with error bars for all stochastic baselines (LSTM, NeuralODE).
4. **Add a naive linear baseline**: Include a structure-naive linear model with the same parameter count as the LSSM to isolate the specific effect of the SPD constraint.
5. **Add an HNN baseline** for the FPUT system to ablate the symplectic integrator's contribution.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>