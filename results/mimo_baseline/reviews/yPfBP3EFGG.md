## Summary

The paper proposes STNAdam, an enhanced Adam algorithm for "nonconvex + weakly-convex" composite optimization that maintains two intertwined iteration trajectories (an extrapolation track and a regular update track) governed by Nesterov momentum and Adam-style adaptive conditioning. The stochastic gradient can be supplied by any variance-reduced estimator (SVRG, SAGA, SARAH). Under the Kurdyka-Łojasiewicz property, the authors establish convergence to a stationary point with explicit rates, and they demonstrate strong performance on low-light image enhancement (LIE) tasks.

## Strengths

- **Sound convergence analysis:** The paper provides a thorough KL-based convergence proof in three steps (energy decrease via Lemma 2, subgradient boundedness via Lemma 3, and KL-driven convergence via Theorems 1–2), establishing finite-length property, convergence in expectation, and explicit convergence rates depending on the KL exponent ϑ. This is technically competent work.

- **Generality of gradient estimator framework:** The algorithm is designed to accept any variance-reduced gradient estimator satisfying the conditions in Lemma 1 (SGD, SAGA, SARAH, SPIDER), and internal hyperparameters can be dynamically scheduled within iterate-dependent intervals. This flexibility is a genuine design advantage over methods tightly coupled to a single estimator.

- **Clear algorithmic exposition:** The paired-notation table (Table 1), iterative trajectory comparison (Figure 1), and step-by-step algorithm description make the two-track mechanism understandable and distinguishable from single-track predecessors (NAG, Adam, NAdam).

## Weaknesses

### Fatal

None.

### Major

- **Extremely narrow experimental evaluation:** For a paper proposing an enhanced Adam variant—a general-purpose optimizer—the experiments are confined entirely to a single specialized task (low-light image enhancement on the LOL dataset). There are no experiments on standard ML benchmarks (image classification, language modeling, reinforcement learning, etc.), which is essential for any optimizer paper at ICLR. The LIE model (14) is a highly structured composite problem with specific non-smooth terms (ℓ₁/₂-norm, nuclear norm); the results do not convincingly demonstrate general utility.

- **Insufficient baseline comparisons for the optimizer:** Among general optimizers, the comparisons are limited to SGD, SAdam, and SNAdam. Missing are prominent Adam variants such as AMSGrad (Reddi et al., 2018), RAdam (Liu et al., 2020), AdaBound, AdaFactor, Lion, and SAM—baselines the community would expect to see. The comparison with LIE-specific methods (NPE, DeHz, LIME, Retinex-Net, LR3M) is orthogonal to the optimization algorithm contribution.

- **No ablation study or sensitivity analysis:** The two-track mechanism is the paper's core novelty, yet there is no experiment isolating its contribution (e.g., single-track vs. two-track under identical conditions). There is no analysis of sensitivity to the numerous hyperparameters (μ, ν, α, ε, γ_{k+1}, α_{k+1}, λ_{k+1}), whose feasible intervals depend on unknown problem constants (L, τ, V₁, V₂, V_Υ, ρ). The practical viability of the dynamic scheduling claim is unsupported.

- **Scalability not addressed:** Variance-reduced estimators like SAGA require storing N gradient tables, and SARAH requires periodic full-gradient computations. For large-scale deep learning (the paper's stated motivation), this is a significant practical limitation that is never discussed. No experiments test the method on problems where N is large.

### Minor

- **Mismatch between motivation and validation:** The introduction highlights "massive network parameters and data sets" and "modern deep learning tasks," but the only experiment is on a classical image processing model with two variables (R, L) solved via a Retinex-Net training framework. The gap between the motivation and the experimental setting is large.

- **Table 2 timing claims are suspicious:** All methods show per-iteration times on the order of 10⁻⁵ seconds, yet STNAdam-SARAH shows the *lowest* time (2.64e-05) despite maintaining two trajectories and a variance-reduced estimator. This counterintuitive result warrants explanation.

- **KL exponent dependence of rates:** The convergence rate in Theorem 2 depends on the KL exponent ϑ, which is problem-dependent and generally unknown a priori. While this is standard in KL-based analyses, the paper does not discuss which ϑ applies to problem (1) or the LIE model, limiting the informativeness of the rate results.

### Trivial

- The abstract says "almost surely converges" but the main convergence result (Theorem 1) establishes convergence "in expectation." These are different claims; the abstract should be corrected.

## Nice-to-Haves

- Experiments on at least one standard deep learning benchmark (e.g., training a CNN on CIFAR-10) to validate the optimizer's general applicability.
- An ablation comparing single-track (equivalent to SNAdam + variance reduction) vs. two-track to isolate the benefit of the dual-trajectory mechanism.
- Convergence plots showing the trajectory of objective value vs. iteration/time, rather than only final metrics.
- Discussion of computational overhead per iteration relative to single-track baselines.

## Novel Insights

The two-track framework maintaining separate extrapolation and regular update trajectories, where both are governed by Adam-style adaptive conditioning and interactively coupled, is a conceptually interesting structural idea. The resulting "larger update neighborhood" could be meaningful, particularly in nonconvex landscapes. However, the paper does not provide empirical or theoretical evidence quantifying this benefit over single-track alternatives, so the insight remains suggestive rather than substantiated.

## Suggestions

- Add experiments on standard ML benchmarks (image classification with ResNets/ViTs, language modeling with Transformers) to justify the claim that STNAdam is an enhanced optimizer for modern deep learning.
- Conduct an ablation study removing the two-track component while keeping variance reduction, to demonstrate the specific value of the dual-trajectory design.
- Add convergence plots (objective value vs. iterations) for the LIE task to illustrate convergence behavior, not just final performance.
- Compare against at least AMSGrad and RAdam as baselines, as they address known issues with Adam that STNAdam should also address.

## Score and Decision

The paper presents competent theoretical work on convergence analysis for a novel two-track Adam variant, and the generality of the gradient estimator framework is appealing. However, the experimental evaluation is far below the standard expected for a method paper at ICLR: only one specialized task, few optimizer baselines, no ablation study, and no evidence that the method works on the large-scale deep learning problems it is motivated by. The theoretical contribution alone does not compensate for the lack of empirical validation.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: Reject