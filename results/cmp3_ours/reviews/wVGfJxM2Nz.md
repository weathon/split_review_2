Now let me write the final review.

## Summary

The paper argues that structure-preserving inductive biases (SPD constraints via Riemannian optimization for dissipative systems, symplectic structure for conservative systems) allow smaller models to outperform larger structure-naive models on dynamical systems tasks. It presents two case studies: a 2D heat transfer system identified via SPD-constrained LSSM, and an 18D Fermi-Pasta-Ulam-Tsingou (FPUT) system modeled via symplectic Hamiltonian neural networks (SHNN). The FPUT experiment is the centerpiece and provides genuine evidence for the thesis.

## Strengths

1. **The FPUT experiment provides compelling evidence for the core claim.** Table 2 and Figure 3 show an SHNN with 1,441 parameters achieving lower rollout MSE and dramatically lower energy drift than an LSTM with 97,074 parameters—a factor-of-67 difference in model size. The sweep over model sizes on one-step MSE, rollout MSE, and energy drift is thorough and makes the point quantitatively.

2. **Energy-drift diagnostic is well-chosen for the conservative case.** Instead of only reporting prediction error, the paper measures drift from the true Hamiltonian (Section 3.2), which directly tests whether the model respects the conservation law. This gets at the mechanism behind long-horizon failure, not just the symptom.

3. **Clear, well-motivated framing.** The paper makes a coherent argument that geometry-informed inductive biases can reduce reliance on large models, and the two case studies are plausibly chosen to span both dissipative and conservative systems.

## Weaknesses

### Fatal
None.

### Major

1. **The dissipative case study does not support the paper's central "smaller models" claim.** RieOpt and EucOpt have *exactly the same number of parameters* (same 2×2 + 2×1 LSSM structure). The comparison is between constrained vs. unconstrained optimization of the same-size model, not between a smaller structure-aware model and a larger naive one. The RF/XGBoost/LSTM baselines (lines 155–156) are entirely different model classes with different inductive biases beyond just "structure awareness." The paper's title and conclusion claim that "structure-aware models can reduce dependence on model size" (line 250), but the dissipative experiment provides no evidence for this—it shows that structure *constraints* improve accuracy at the same size, which is a related but distinct claim. Only the FPUT experiment supports the size-reduction thesis.

2. **Equation (7) contains a mathematical error.** The loss is written as:

   $$\mathcal{J}(X | \Phi_A, \Phi_B) = \sum_{i=1}^{n-1} \|\Phi_A \mathbf{T}_i + \Phi_B \mathbf{T}_i - \mathbf{T}_{i+1}\|_2^2$$

   but the correct state update from Equation (4) is $\mathbb{T}_{t+1} = \Phi_A \mathbf{T}_t + \Phi_B \mathbf{U}_t$ where $\mathbf{U}$ is the forcing input. The loss function as written applies $\Phi_B$ to $\mathbf{T}_i$ rather than $\mathbf{U}_i$. Given the surrounding text consistently references the forcing input U, this is almost certainly a typographical error, but it is a material inconsistency in the mathematical presentation that must be corrected.

3. **The RF, XGBoost, and LSTM baselines in the dissipative case are not informative comparisons.** As the paper acknowledges (line 177), these models "learn the forced response of the system as a time series" rather than incorporating the forcing input. A model that does not accept the forcing input is an expected fail rather than a meaningful baseline for evaluating generalization to unseen forcing. The MSE values for RF and XGBoost on the Chicago test set (24.1 and 22.3, Table 1) are nearly two orders of magnitude larger than RieOpt—consistent with these models having no mechanism to use the forcing.

### Minor

1. **Dimensional inconsistencies in Section 3.1.** The measurement data is described as $T \in \mathbb{R}^{8759 \times 1}$ (line 153), but the state has two temperatures (T_ext1, T_ext2). The forcing is described as $U \in \mathbb{R}^{8759 \times 2}$, but the model in Equation (2) uses a scalar T_ext input. These dimensional details are inconsistent across the paper.

2. **Training convergence claim lacks quantitative support.** The claim that structure-naive models have "significantly slower" training convergence (line 175) is stated without summary statistics—no epoch counts to reach a given error threshold, no timing comparisons. Figures 7 and 8 may show this, but the text should provide quantitative evidence.

3. **LSTM sweep in the FPUT experiment is asymmetric.** The LSTM varies only width W, not layers L, while SHNN and NeuralODE sweep both (line 183). The paper acknowledges this but does not justify whether a deeper (multi-layer) LSTM might perform differently.

4. **The s-plane/z-plane mapping discussion (line 75) is confused.** The text says eigenvalues are wrapped "within the unit circle in the $s$-plane where $\text{Re}(\lambda_i) > 0$." The standard bilinear transform maps the left half of the s-plane (continuous-time stability region) inside the unit circle in the *z*-plane, not the *s*-plane. This appears to be a conceptual error in the exposition.

5. **No error bars or confidence intervals.** Tables 1 and 2 report point estimates with no variance measures or multiple seeds. While acceptable for the deterministic optimization of LSSMs, this is a weakness for the stochastic baselines (LSTM, RF, XGBoost).

### Trivial
1. Repetition ("where where" on line 105) and minor grammatical issues.
2. No training time or computational cost reported, making the practical advantage of smaller models unclear despite the parameter-count argument.

## Nice-to-Haves
- An ablation comparing symmetric (but not necessarily SPD) vs. SPD-constrained optimization in the dissipative case would disentangle whether the benefit comes from stability enforcement, reduced degrees of freedom, or Riemannian gradient geometry.
- A discussion of failure cases or regimes where structure-preservation might not help would strengthen the contribution.

## Removed Points

These points were flagged for removal from the input reviews; treat them with caution:
- **"No novelty in methodology"** — The paper does not claim methodological novelty; it applies existing techniques (Riemannian optimization, SHNNs) as an empirical demonstration. This framing is clear from the abstract and introduction. Lack of novelty per se is not a weakness.
- **"FPUT experiment confirms what SHNN literature already established"** — Overstated. The paper's contribution is the explicit size-vs-performance sweep, which is a different framing from prior SHNN work. However, the incremental nature of this contribution is relevant to the overall assessment.
- **"Ethics statement: code/data promise has no verification"** — Standard practice; not a substantive weakness.
- **Formatting and typographical nitpicks** — Removed per hard rules (parser artifacts, not author errors).

## Novel Insights

None beyond the paper's own contributions. The reviews surface a genuine tension: the FPUT experiment is compelling and clearly supports the "smaller models" thesis, but the dissipative experiment is misaligned with that thesis and the overall contribution is an empirical application of two existing methods rather than a methodological advance. The weakness about Equation (7) is the most actionable finding for the authors.

## Suggestions

1. Correct Equation (7) to read $\|\Phi_A \mathbf{T}_i + \Phi_B \mathbf{U}_i - \mathbf{T}_{i+1}\|_2^2$.
2. Restructure the dissipative experiment to directly compare models of different sizes with and without structure constraints, or reframe the paper's claim to separate the two cases (e.g., "structure constraints improve accuracy" and "symplectic structure enables smaller models").
3. Provide summary statistics for training convergence (epoch counts, timing).
4. Clarify dimensional notation in Section 3.1 — what exactly are the dimensions of T and U?
5. Fix the s-plane/z-plane mapping description.
6. Add error bars or multiple-seed results for the stochastic baselines.

## Score and Decision

**Calibration anchors used:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NRRHkJE03w.md | 3.00 | R1 | "Beyond Dynamics: Learning to Discover Conservation Principles" — weaker presentation and positioning, rejected. This paper is clearer. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0Y26tFG3WF.md | 3.67 | R1 | "Inducing Precision in Lagrangian Neural Networks" — proof-of-concept with minimal experiments, rejected. Current paper has stronger experiments. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2AWZTv6kgV.md | 4.75 | R1/R3 | "Projected Neural Differential Equations" — novel method but found to have prior art, rejected. Current paper has no novelty claim but has cleaner FPUT results. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XqDM97DtMf.md | 4.67 | R1/R3 | "Learning Chaotic Dynamics with Embedded Dissipativity" — novel method with guarantees, but mixed reviews, rejected. Current paper has less novelty but clearer framing. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/uL1H29dM0c.md | 7.00 | R1 | "Efficiently Parameterized Neural Metriplectic Systems" — novel method with theoretical results, accepted. Clearly stronger contribution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/U1DjXQeJRx.md | 6.60 | R1 | "Poisson-Dirac Neural Networks" — novel framework, accepted. Clearly stronger contribution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/EyWKb7Ltcx.md | 5.00 | R2 | "Intrinsic Riemannian Classifiers on Deformed SPD Manifolds" — proposed framework, rejected. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ZNnmcddaB3.md | 6.20 | R2 | "Robust System Identification" — theoretical guarantees, accepted. Stronger contribution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/saFH7zTtQs.md | 5.17 | R2 | "Learning Linear Dynamical Systems with Sparse System Matrices" — novel algorithm, rejected. |

**Round 1 bracket:** 4–6 (based on broad comparison with structure-preserving dynamics papers)
**Round 2 narrowing:** 4.0–5.0 (comparing against SPD/system-ID papers at various score levels)
**Final score:** 4.5 — The paper has one genuinely compelling experiment (FPUT) and a clear thesis, but the dissipative experiment does not support the paper's central claim, the baselines in that experiment are not informative comparisons, and there are several presentation issues. The FPUT results are the strongest part, but they largely confirm known advantages of symplectic models. The paper reads more like a workshop or arXiv-level demonstration than a conference paper that advances the state of knowledge. With substantial revisions (correcting Equation (7), restructuring the dissipative case, adding analysis of why the SPD constraint helps), the paper could be strengthened, but in its current form the contribution is not sufficient for ICLR.

MY FINAL SCORE: 4.5
MY FINAL DECISION: Reject