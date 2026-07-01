## Summary

This paper argues that structure-preserving inductive biases (SPD constraints for dissipative systems via Riemannian optimization, and symplectic structure for conservative systems via SHNNs) reduce the need for large models. It studies two cases: a 2D heat transfer system learned with an SPD-constrained linear state-space model, and an 18D FPUT system learned with an SHNN. The FPUT experiment is the paper's strongest evidence, showing a small SHNN (1,441 params) achieving ~3 orders of magnitude better energy drift than the best LSTM (97,074 params).

## Strengths

1. **The FPUT/SHNN result is genuinely striking.** Table 2 shows the smallest SHNN (361 params, L=1, W=18) achieves rollout energy drift of 3.697×10⁻³, while the best LSTM (97,074 params) achieves drift of 5.914 — roughly three orders of magnitude better with 0.37% of the parameters. Even the best NeuralODE (drift 1.787×10⁰, 2,682 params) is ~500× worse than the worst SHNN. The gap is large enough to survive concerns about random seed variance.

2. **Clean controlled comparison (RieOpt vs EucOpt) in the dissipative case.** Table 1 shows the same LSSM learned with Riemannian optimization outperforms Euclidean optimization on both states and both test distributions. For T_ext1 in London: RieOpt MSE 0.40 vs EucOpt 1.28; for Chicago: 1.36 vs 3.35. Same model class, same optimizer except for the manifold constraint — this cleanly isolates the benefit of enforcing SPD structure.

3. **Thorough model size sweep.** The paper systematically sweeps over L ∈ {n_f, 2n_f, 4n_f, 8n_f} and W ∈ {n_f, 2n_f, 4n_f, 8n_f} for SHNN and NeuralODE (and W for LSTM), covering a wide range of model complexities. This allows the reader to assess the size-performance Pareto frontier across 30+ configurations.

## Weaknesses

### Fatal
None.

### Major

1. **Limited novelty relative to the ICLR bar.** The paper applies *existing methods* throughout: SHNNs (David & Méhats, 2023), Riemannian Adam (Bécligneul & Ganea, 2019), the geoopt library (Kochurov et al., 2020), and the system identification setup builds on Xuereb Conti et al. (2023). No new architecture, preservation mechanism, theoretical result, or design principle is introduced. The core finding — that structure-preserving models generalize better and need less capacity — is the foundational premise of the HNN/SHNN literature (Greydanus et al., 2019; David & Méhats, 2023). The paper reads as a competent empirical demonstration rather than a methodological contribution, which falls below the novelty bar typical of ICLR.

2. **No statistical rigor.** All results in Tables 1 and 2 are reported as single numbers with no confidence intervals, standard deviations, or multiple random seeds. The NeuralODE drift in Table 2 varies from 1.194 to 1.802×10³ across configurations, indicating that training variance is high. Without repeated runs, the reader cannot determine whether the reported SHNN numbers are typical or a lucky outlier. While the gap is large enough that the FPUT conclusions likely survive, this is a basic expectation for any comparative ML paper.

3. **The dissipative case adds little evidentiary weight.** The LSSM has ~5 learnable parameters in a hand-specified physics template for a 2D linear system (A is 2×2 symmetric with 3 independent parameters, B is 2×1 with 2 parameters). This is system identification on a known parametric form, not "a small model" in the ML sense. The comparison against RF, XGBoost, and LSTM is fundamentally asymmetric — the LSSM encodes almost the entire physics. Compounding this:
   - **Parameter counts for the dissipative baselines are not reported**, making the size comparison unverifiable for that case.
   - **The LSTM achieves MSE 25.7 on London T_ext1** (vs the physics-initialized LSSM at 2.86 and RieOpt at 0.40), which is suspiciously poor for a linear 2D system that LSTMs can model trivially, suggesting insufficient tuning. The EucOpt comparison (which is fair) shows a narrower gap: RieOpt 0.40 vs EucOpt 1.28 for London T_ext1. The paper would be more honest if it led with the RieOpt vs EucOpt comparison and acknowledged the ML baselines are peripheral.

### Minor

4. **Equation 7 has an error.** The loss term reads `‖Φ_A T_i + Φ_B T_i - T_{i+1}‖` (line 93), but should be `‖Φ_A T_i + Φ_B U_i - T_{i+1}‖` to be consistent with equation 4 (`T_{t+1} = Φ_A T_t + Φ_B U_t`, line 83).

5. **Data dimensionality inconsistencies.** (a) T is described as ℝ^{8759×1} (line 153) — a single temperature time series — yet the model has 2 states (T_ext1, T_ext2). It is not clarified whether both states are measured or one is latent. (b) The input U has three inconsistent dimensional descriptions across the paper: ℝ^{2×1} (line 49), ℝ^{1×1} (line 49, later), and ℝ^{8759×2} (line 153). For a single forcing (ambient temperature), the time series should be ℝ^{8759×1}.

6. **Confusing exposition in Section 2.1.1.** The description of the s-plane/z-plane mapping (line 75) states: "wrapping the stable eigenvalues located in the left half-plane (i.e., Re(λ_i) < 0) within the unit circle in the s-plane where Re(λ_i) > 0." The unit circle belongs to the z-plane, not the s-plane, and the phrase "s-plane where Re(λ_i) > 0" contradicts the left-half-plane stability condition stated in the same sentence. This needs correction.

7. **No discussion of limitations.** The conclusion (lines 249–251) summarizes findings but does not address what happens when the assumed structure is misspecified, the system is not exactly Hamiltonian/dissipative in the assumed form, or the geometry is unknown. These are natural concerns for a paper advocating structure-preserving approaches.

### Trivial
None.

## Nice-to-Haves

- **Reframing the contribution**: The paper would be stronger if it positioned the contribution as "structure creates discontinuities in the size-performance Pareto frontier" rather than the more generic "smaller models work better." The FPUT data already supports this framing.
- **Multiple random seeds with error bars** in Table 2 would significantly strengthen the empirical case.
- **A stronger dissipative case study** (e.g., nonlinear dissipative system or higher-dimensional thermal network) would make the claim of general applicability more convincing.

## Removed Points

- **"Honest acknowledgment of AI writing assistance"** (strength): Sycophantic/generic. Not a scientific strength.
- **"Training convergence claim without appendix figures"**: The appendix was stripped by the parser; this is not a paper flaw.
- **"Related work gaps"**: As per policy, missing related works are not flagged.
- **Reproducibility nitpicks about missing hyperparameters** (e.g., LSTM architecture in dissipative case): Partially retained in weakness #3 as the poor LSTM performance suggests tuning issues, but the broader "implementation details" framing is removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any perspective on the paper's findings that is not already present in the paper itself. The key tension (empirical demonstration of an expected property vs. methodological novelty) is inherent to the paper's framing and is not a new insight from the review process.

## Suggestions

1. Correct the equation 7 typo (`Φ_B U_i` instead of `Φ_B T_i`) and resolve the data dimensionality inconsistencies (T dimensions, U dimensions).
2. Add at least 5 random seeds with mean ± std to Table 2. The NeuralODE variance alone (drift ranging from 1.194 to 1.802×10³) demands this.
3. Either replace the dissipative case with a more challenging problem (nonlinear, higher-dimensional) or reframe it as a targeted validation of the Riemannian optimization approach rather than a general "smaller models" argument.
4. Report parameter counts for all dissipative baselines (RF, XGBoost, LSTM) in Table 1.
5. Add a limitations paragraph discussing what happens when the assumed structure is misspecified.
6. Correct the s-plane/z-plane confusion in Section 2.1.1.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>