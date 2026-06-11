## Summary
# Final Review Report

## Summary

This paper presents a comparative study of structure-preserving vs. structure-naive machine learning approaches for learning dynamical systems. Two use-cases are investigated: (1) a 2D dissipative heat transfer system, where Riemannian optimization on the symmetric positive definite (SPD) manifold is used for linear state-space system identification, and (2) an 18D conservative Fermi-Pasta-Ulam-Tsingou (FPUT) system, where a symplectic Hamiltonian neural network (SHNN) learns the Hamiltonian dynamics. The central claim is that geometry-informed inductive biases enable accurate and stable long-horizon prediction with substantially smaller models compared to black-box baselines (LSTM, NeuralODE, RF, XGBoost).

The paper has a clear conceptual motivation and the experimental results directionally support the claimed benefit of structure preservation. The SHNN results on the FPUT system are particularly compelling, demonstrating that a small symplectic model (1,441 parameters) can outperform a much larger LSTM (97,074 parameters) on energy drift and rollout stability. However, the manuscript has several significant weaknesses: (1) a critical formula error in the loss function for the dissipative case (Eq. 7 uses T_i instead of U_i in the B term), (2) a technically confused description of the s-to-z plane mapping in Section 2.1.1, (3) insufficient baseline tuning and missing statistical significance in the experimental comparisons, (4) a conclusion that overclaims generalization beyond the two evaluated systems, and (5) missing limitations and reproducibility-critical details. External literature verification was not available in this run (retrieval-disabled mode), so novelty and comparison conclusions are deferred for manual verification.

## Strengths
1. **Clear and compelling motivation.** The paper addresses an important research question: can geometric inductive biases replace the need for large models in learning dynamical systems? The motivation—that structure-rich manifolds are mismatched with flat Euclidean learning—is well articulated and scientifically grounded.

2. **Informative experimental design for the FPUT system.** The conservative use-case is well-designed: it includes a sweep over multiple model sizes (SHNN, NeuralODE, LSTM), evaluates both one-step and rollout accuracy, and measures energy drift as a physically meaningful metric. The finding that SHNN with 1,441 parameters achieves lower drift than LSTM with 97,074 parameters is a striking demonstration of the value of structure preservation.

3. **Physically meaningful evaluation metrics.** The use of energy drift RMS as an evaluation metric for the conservative system is a strong choice—it directly measures whether the learned model respects the fundamental physics (energy conservation). This is more informative than MSE alone and reveals failure modes that one-step accuracy metrics would miss.

4. **Connecting two distinct physical regimes.** The paper covers both dissipative and conservative systems, which demonstrates that the principle of structure preservation is not limited to a single class of dynamics. This breadth strengthens the generality of the paper's core message.

5. **Ethics transparency.** The authors disclose the use of ChatGPT and Google Gemini for writing polish, which is commendable for double-blind review transparency.

## Weaknesses
### W1. Critical formula error in the loss function (Page 2-3, Section 2.1.2, Eq. 7)

The loss function defined in Eq. (7) is:
$$\mathcal{J}(X | \Phi_A, \Phi_B) = \sum_{i=1}^{n-1} \|\Phi_A \mathbf{T}_i + \Phi_B \mathbf{T}_i - \mathbf{T}_{i+1}\|_2^2.$$

This contains a critical error: the term $\Phi_B \mathbf{T}_i$ should be $\Phi_B \mathbf{U}_i$ (the forcing input), according to the model definition in Eq. (4): $\mathbb{T}_{t+1} = \Phi_A \mathbf{T}_t + \Phi_B \mathbf{U}_t$. Using $\mathbf{T}_i$ instead of $\mathbf{U}_i$ would feed the state vector into the input matrix, which would either be dimensionally inconsistent (if $\Phi_B \in \mathbb{R}^{2 \times 1}$ and $\mathbf{T}_i \in \mathbb{R}^2$) or would learn a different (incorrect) model. This error undermines the reproducibility of the core optimization procedure. The index notation $n$ is also used ambiguously—it previously denoted the matrix dimension, not the number of time steps.

**Severity:** Major. **Fixability:** Straightforward correction of Eq. (7) to use $\mathbf{U}_i$ and clarify $n$.

---

### W2. Technically incorrect description of eigenvalue mapping (Page 3, Section 2.1.1)

The manuscript states: "$e^{A\tau}$ is a bilinear map that geometrically maps the complex $s$-plane to the complex unit circle in the $z$-plane where system stability is preserved by wrapping the stable eigenvalues located in the left half-plane (i.e., $\text{Re}(\lambda_i) < 0$) within the unit circle in the $s$-plane where $\text{Re}(\lambda_i) > 0$)."

There are two errors here: (a) the matrix exponential $e^{A\tau}$ is not a "bilinear map"—the bilinear (Tustin) transform is a different discretization method; (b) the $s$-plane and $z$-plane are conflated—the unit circle belongs to the $z$-plane, not the $s$-plane. The correct statement is: the matrix exponential maps eigenvalues from the continuous-time domain to the discrete-time domain via $\lambda_z = e^{\lambda_s \tau}$, so stable eigenvalues with $\text{Re}(\lambda_s) < 0$ map to $|\lambda_z| < 1$.

**Severity:** Major. **Fixability:** Rewrite the passage with technically correct mapping language.

---

### W3. Unfair baseline comparisons and missing experiment controls (Pages 5-7, Sections 3.1-3.2)

Several issues compromise the experimental fairness:

(a) **LSTM severely undertuned:** The LSTM achieves MSE of 25.7 on the London test set (vs. RieOpt's 0.4). This is two orders of magnitude worse, strongly suggesting undertuning rather than a fundamental limitation. No hyperparameter search details are reported for the baselines. A properly tuned LSTM (with appropriate sequence length, regularization, learning rate scheduling) should perform far better on a 1D time-series prediction task.

(b) **Standardization asymmetry (FPUT experiment):** LSTM and NeuralODE inputs are standardized (zero mean, unit variance), while SHNN is trained on raw physical coordinates. This introduces a confounding factor: different input preprocessing pipelines may affect optimization dynamics, loss landscapes, and ultimately model quality. An additional control (LSTM on raw coordinates) is needed.

(c) **Asymmetric hyperparameter sweeps:** For the FPUT system, SHNN and NeuralODE are swept over both layer count ($L$) and width ($W$), while LSTM is swept over width only. The depth of LSTM is not varied, potentially missing configurations where deeper LSTMs perform better.

(d) **No statistical significance:** All results are reported as point estimates without variance, confidence intervals, or multi-seed experiments. Given the stochastic nature of neural network training, single-run results are not reliable indicators of model quality.

(e) **Missing dataset statistics:** MSE values are reported without temperature scale information, making them uninterpretable. The reader cannot assess whether an MSE of 0.4 is excellent or merely adequate without knowing the data variance.

**Severity:** Major. **Fixability:** Add multi-seed variance, controlled standardization experiment, extended LSTM sweeps, and dataset statistics.

---

### W4. Contradictory results narrative (Page 6, Section 3.1.1)

The results paragraph states that structure-naive models (RF, XGBoost, LSTM) "seem to roll-out the test segments accurately," but Table 1 shows LSTM has MSE 25.7 (vs. RieOpt's 0.4), which is catastrophic failure, not accuracy. For the Chicago OOD test, RF (24.1) and XGBoost (22.3) also fail dramatically. The narrative is misleading and inconsistent with the reported data.

**Severity:** Major. **Fixability:** Revise the paragraph to accurately characterize baseline performance (acknowledge LSTM failure, discuss relative degradation patterns), and provide mechanistic analysis of *why* structure-naive models fail on OOD data.

---

### W5. Overclaimed generalization in conclusion (Page 8, Section 4)

The conclusion states that "stable generalization across initial conditions is achievable with models that are much smaller than equally robust, structure-naive baselines" without bounding this claim to the two specific systems evaluated. The claim that structure-aware models broadly "reduce dependence on model size while improving robustness" extrapolates beyond the evidence—only one dissipative system (2D heat transfer with a known physics-derived initial model) and one conservative system (FPUT with a known Hamiltonian structure) were tested. The paper also does not discuss scalability of the SPD approach to higher-dimensional systems.

**Severity:** Major. **Fixability:** Add explicit limitations bounding claims to evaluated settings, and discuss challenges for extending to unknown/nonlinear/dissipative systems.

---

### W6. Missing method reproducibility details (Pages 4-5, Sections 2.1.2 and 2.2.1)

(a) The SHNN section lacks the implicit midpoint update equation and the training objective formulation, making the method non-reproducible from the text alone.

(b) The lumped-parameter discretization from the PDE (Eq. 1) to the LSSM (Eq. 2) is unexplained—critical spatial discretization choices (finite difference, finite volume, number of nodes) are omitted.

(c) Hyperparameters for Riemannian optimization (learning rate, batch size, number of epochs, convergence criteria) are not reported in the main text and the referenced Appendix Table 3 is not visible in the provided manuscript.

**Severity:** Moderate. **Fixability:** Add the SHNN update equations, describe the spatial discretization method, and report all optimization hyperparameters.

---

### W7. Narrative structure and writing quality issues

(a) The introduction lacks a clear gap statement—it argues for structure-preserving biases but does not explicitly state what specific limitation of existing methods (beyond generic "data-intensive training") is being addressed.

(b) Section 1.1 reads as a shallow citation list rather than a categorized comparison of related approaches. The paper's own contribution is not clearly differentiated from HNNs/SHNNs (which are adopted, not invented) and prior Riemannian optimization work.

(c) The abstract uses "robust generalisation" without defining robustness or generalization in the context of the specific experiments.

**Severity:** Moderate. **Fixability:** Restructure introduction with explicit gap statement, reorganize related work by comparison axes, bound abstract claims to evaluated settings.

---

### W8. Missing limitations and future work (Pages 8-9)

The paper has no dedicated limitations section, and the conclusion does not discuss boundary conditions of the proposed approaches (e.g., need for known physics model for SPD approach, restriction to Hamiltonian systems for SHNN, sensitivity to noise, scalability to higher dimensions). The ethics statement is present but very brief.

**Severity:** Minor-to-Moderate. **Fixability:** Add a limitations paragraph in the conclusion or as a separate section.

---

### W9. Novelty assessment deferred (all sections)

Because external paper search was unavailable during this review run (retrieval-disabled mode), all novelty and prior-art comparison conclusions are intentionally deferred. The paper adopts established methods (SHNN from David & Méhats 2023; Riemannian optimization from Bécligneul & Ganea 2019), so the primary novelty lies in the comparative study design and the application of SPD-constrained identification to heat transfer. A manual literature verification is required before final novelty judgment.

**Severity:** Deferred. **Fixability:** Conduct systematic literature search to verify whether the specific application of Riemannian SPD optimization to heat transfer system identification is novel, and whether the SHNN comparison on FPUT with parameter-efficiency analysis has been reported before.

## Score
**Final Score: 5/10**

**Rationale:** This score prioritizes research value and scientific validity as primary dimensions. The paper addresses a worthwhile and timely research question—whether geometric inductive biases can reduce model size while improving prediction stability for dynamical systems. The core idea is sound and the experimental direction (especially the FPUT/SHNN comparison) provides initial positive evidence.

However, the manuscript has several significant weaknesses that limit its current research value and validity:

1. **Formula error (W1):** The loss function in Eq. (7) contains a critical ambiguity/error that undermines the core optimization formulation. While fixable, this reduces confidence in the reported results until corrected.

2. **Technical inaccuracy (W2):** The incorrect description of the $s$-plane to $z$-plane mapping signals insufficient technical rigor in a paper whose central thesis depends on geometric and dynamical systems concepts.

3. **Experimental fairness concerns (W3):** The baseline comparisons are not sufficiently controlled. The LSTM appears significantly undertuned, and the standardization asymmetry between SHNN and baselines introduces a confounding factor. Without multi-seed variance reporting, the statistical reliability of all results is unknown.

4. **Overclaimed conclusions (W5):** The conclusion extrapolates the comparative findings to a general principle without bounding claims to the two evaluated systems or discussing limitations.

5. **Novelty assessment deferred:** Since the paper adopts established methods (SHNN, Riemannian optimization) and the primary contribution is a comparative study, the novelty level cannot be fully assessed without external literature verification, which was unavailable in this run.

These weaknesses are fixable through careful revision, but in their current form they materially reduce the paper's contribution strength and validity confidence. The 5/10 score reflects a paper with a solid conceptual core that requires substantial technical and experimental corrections before it meets a publishable standard.