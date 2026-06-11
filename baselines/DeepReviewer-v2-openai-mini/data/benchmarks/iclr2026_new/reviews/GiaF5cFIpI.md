## Summary
# Final Review Report

## Summary

This paper presents a streaming framework for adaptive stimulation-response modeling of latent neural dynamics, targeting closed-loop neuroscience experiments where neural activity must be tracked, stimulation effects must be learned, and stimulation patterns must be optimized in real time. The framework combines three components: (1) **sjPCA** — a novel streaming approximation of jPCA for real-time latent space construction; (2) **adaptive stimulus-response mapping** — a kernel regression estimator that learns nonparametric mappings from high-dimensional stimulation patterns to latent-space perturbations, with temporal discounting to handle non-stationarity; and (3) **constrained optimization** — a differentiable objective with L1 sparsity and box constraints that designs stimulation patterns to drive latent dynamics in a desired direction.

The paper demonstrates these components on a toy model (circular linear dynamical system) and on two real neural datasets (calcium imaging from mouse visual cortex, electrophysiology from nonhuman primate sensorimotor cortex), though both real-data experiments use simulated stimulation effects added via an autoregressive process rather than genuine optogenetic or electrical stimulation. Runtimes are reported under 10 ms per timepoint on average, supporting real-time feasibility.

**Core contributions (C1–C3):**
- **C1 (sjPCA):** Streaming latent space construction for rotation-structured neural manifolds
- **C2 (Stimulus-response modeling):** Nonparametric kernel regression with temporal adaptation for learning stimulation effects
- **C3 (Stimulation optimization):** Differentiable optimization with sparsity and box constraints for designing high-dimensional stimulation patterns

**Novelty/comparison assessment:** Deferred to manual literature verification due to Retrieval-Disabled Mode (external paper search unavailable in this run). The paper claims several methodological firsts that require comparison with prior closed-loop stimulation work (e.g., Minai et al. 2024, Wagenmaker et al. 2024, Draelos & Pearson 2020).

## Strengths
**S1 — Timely and important problem.** The paper tackles a genuinely important challenge in systems neuroscience: how to design targeted neural stimulations that manipulate latent dynamics in a principled, automated way. As optogenetic and electrical stimulation technologies advance toward single-neuron resolution, the need for algorithmic methods to select which neurons to stimulate and when is pressing. The paper's framing of this as a streaming latent-space estimation and constrained optimization problem is well-motivated.

**S2 — Integrated framework design.** Rather than addressing only one subproblem (latent space estimation, stimulus-response modeling, or stimulus optimization), the paper proposes an end-to-end streaming framework (Algorithm 1) that combines all three. The modular design — where latent space construction, dynamical modeling, stimulus-response learning, and optimization are separate but interoperable components — is a practical strength that could facilitate adoption and extension by the community.

**S3 — Real-time computational feasibility.** The paper reports end-to-end runtimes under 10 ms per timepoint on standard hardware (NVIDIA 3060 Ti, 32-core CPU). This is a clear strength for the intended application domain, where neural data acquisition rates range from 15 Hz (calcium imaging) to 30+ Hz (electrophysiology). Demonstrating that the algorithmic pipeline can keep pace with data acquisition is a necessary condition for closed-loop operation.

**S4 — Nonparametric modeling of stimulation effects.** The kernel regression estimator in Eq (7), with its product kernel over latent state, stimulus, and sample age, provides a flexible framework that does not assume linearity or stationarity of stimulation responses. The temporal discounting mechanism is a sensible design choice for handling biological non-stationarities such as plasticity, photobleaching, or electrode drift.

**S5 — Multiple latent representations in parallel.** The paper considers three different latent space hypotheses (high-variance via proSVD, rotational structure via sjPCA, statistical independence via mmICA) and provides an online mechanism to compare their predictive performance. This parallel-comparison approach is methodologically sound and could be valuable for distinguishing between competing neural manifold hypotheses in vivo.

## Weaknesses
### W1 — Real-data validation uses simulated, not genuine, stimulation effects (Critical)
*Page 1 — Section 4.1 (Real data)*

The paper states it validates on "real neural data," but stimulation effects are emulated by adding a linear autoregressive process ($a_t = 0.8 a_{t-1} + u_t$) to existing neural recordings. This is a critical methodological gap because:

- The AR process is additive, linear, and state-independent. It does not capture the nonlinear, network-mediated, state-dependent effects of genuine optogenetic or electrical stimulation — which is precisely the complexity that motivates the nonparametric estimator $\hat{S}$.
- The "ground truth" stimulation effect is known by construction, so the comparison between predicted and observed effects only tests whether the estimator can fit a simple AR model, not whether it can handle real biological complexity.
- The paper's motivation emphasizes non-robust, off-target, and non-stationary stimulation responses (Section 2.3), yet the validation uses a stationary model with perfect on-target effects.

**Required action:** (Must) Either (a) validate on a published dataset with paired optogenetic stimulation and recording, or (b) explicitly rename all instances of "simulated stimulations" to "emulated stimulation effects" throughout the manuscript and add a dedicated limitations paragraph stating that genuine closed-loop stimulation validation is essential future work. The abstract should also be revised to avoid implying in-vivo validation.

### W2 — Optimization evaluation lacks meaningful baselines (Major)
*Page 1 — Section 4.2*

The stimulation optimization is compared only against random baselines (random single neurons, random groups, shuffled patterns). This is insufficient for several reasons:

- The cited prior work (Minai et al., 2024 — Bayesian optimization; Wagenmaker et al., 2024 — active learning; Draelos & Pearson, 2020 — Bayesian variational inference) constitutes directly relevant baselines that are not compared against.
- A simple heuristic baseline — such as selecting neurons with the highest absolute loading on the target latent dimension — would provide a much more informative comparison and likely outperform random selection.
- The "Shuffled" baseline (randomly permuting the optimized pattern) does not control for total stimulation power, making it a weak control.

**Required action:** (Must) Add at least two non-random baselines: (a) a loading-based heuristic (stimulate neurons with highest $|Q^\top v|$), and (b) one existing adaptive stimulation method from the cited literature (e.g., Bayesian optimization with 50 acquisitions). Report alignment angle, sample efficiency (number of stimulations needed to reach a target alignment), and computational cost.

### W3 — Toy model does not validate the continuous optimization formulation (Major)
*Page 1 — Experiments (Toy model)*

The toy model uses binary stimulation ($u_t \in \{0,1\}$) with a location-dependent effect that does not depend on specific stimulus components. In Eq (9), when $u_t=1$, the effect only depends on the latent state $(x_1, x_2)$, not on which neurons are stimulated or at what magnitude. This means:

- The toy model does not exercise the continuous $u \in [0,1]^N$ regime that the optimization in Eq (8) is designed for.
- The L1 sparsity penalty in Eq (8) is never tested because the toy model has no concept of "which neurons to stimulate" — there is only a binary global decision.
- The differentiable closed-loop optimization (using $\hat{S}$ to predict $s(u)$ for arbitrary continuous $u$) is validated only in the open-loop identity-mapping case (Section 4.2, Fig 5), not on the toy model.

**Required action:** (Must) Add a synthetic experiment where $u \in [0,1]^N$ is a continuous vector and $S$ depends nontrivially on individual components of $u$, then demonstrate that the optimization in Eq (8) recovers the desired latent perturbation. This is essential to validate the core algorithmic claim.

### W4 — Mathematical imprecision in sjPCA formulation (Major)
*Page 1 — Section 2.1 (Novel streaming method)*

The sjPCA derivation contains a significant technical inaccuracy. The text states "jPCA makes a basis out of $M_t$'s eigenvectors: $U_t \Sigma_t U_t^\top = M_t$." However, $M_t$ is constrained to be skew-symmetric ($M_t = -M_t^\top$). A real skew-symmetric matrix has purely imaginary eigenvalues and cannot be diagonalized with real $U_t$ and real $\Sigma_t$. The correct decomposition for skew-symmetric matrices is the real Schur form: $M_t = Q_t \Lambda_t Q_t^\top$ where $\Lambda_t$ is block diagonal with $2\times2$ rotation blocks.

Additionally, the connection between the Sherman-Morrison formula and solving Eq (1) in a streaming setting is not explained, leaving readers to guess how the online update works.

**Required action:** (Must) Replace the eigen-decomposition with the correct real Schur decomposition. Clarify (or remove) the reference to the Sherman-Morrison formula. Define dimensions of all matrices explicitly ($X_t \in \mathbb{R}^{k \times T}$, $M_t \in \mathbb{R}^{k \times k}$).

### W5 — Optimization objective has ambiguous L0/L1 mixing (Major)
*Page 1 — Section 2.4, Eq (8)*

The term $\lambda_1(\|u\|_0^{\max} - \|u\|_1)$ in Eq (8) has several issues:

- $\|u\|_0^{\max}$ appears to be a scalar constant (the maximum allowed number of nonzero entries), but the $L_0$ notation makes this ambiguous. It should be denoted $n_{\text{target}}$ for clarity.
- With $u \in [0,1]^N$, $\|u\|_1 = \sum_i u_i$ is the sum of activation values, not the count of active neurons. Driving $\|u\|_1$ toward $n_{\text{target}}$ does not guarantee approximately $n_{\text{target}}$ neurons are stimulated — it could spread activation across many neurons at low amplitudes.
- The two objective terms (cosine similarity in $[-1,1]$ and L1 penalty scaling with $N$) are on incomparable scales. The choice of $\lambda_1$ critically affects behavior, but no value, range, or selection procedure is reported anywhere in the paper.

**Required action:** (Must) Replace the L0/L1 term with a clean formulation: $\min_u -\cos(v, s(u)) + \lambda (n_{\text{target}} - \sum_i u_i)$. Define $n_{\text{target}}$ explicitly. Report the $\lambda$ value used in experiments and describe how it was selected.

### W6 — No statistical testing or variance reporting for key comparisons (Major)
*Page 1 — Section 4.2*

The optimization comparison (Fig 4) reports alignment angles across many trials, but the paper does not report whether the improvements over random baselines are statistically significant. No confidence intervals, standard deviations, or p-values are provided for the key claim that "our optimization outperforms random methods." Similarly, Figure 5 shows learning curves without error bands or significance tests for the open-loop vs. closed-loop comparison.

**Required action:** (Must) Add 95% confidence intervals or standard deviations to all quantitative comparisons. For the Designed vs. random baselines comparison (Fig 4a), report the effect size and a paired significance test (e.g., Wilcoxon signed-rank test).

### W7 — Delayed response model assumption limits throughput (Major)
*Page 1 — Section 2.3 (Delayed response model)*

The model assumes "a new stimulus is not delivered before we see the effects of a previous stimulus," meaning no overlapping stimulation responses. This serialization constraint is not quantified, tested, or discussed in the experiments. For calcium imaging at 15 Hz with a 0.2 s response delay, the effective stimulation rate would be capped at approximately 5 Hz. This is a significant practical limitation for any closed-loop application where rapid iterative stimulation is needed.

**Required action:** (Must) Quantify the effective stimulation rate under the delayed response model for each experimental setting. Discuss how the assumption could be relaxed (e.g., linear superposition with deconvolution). Add this as a dedicated limitation in the Discussion.

### W8 — Reproducibility: key hyperparameters not reported (Major)
*Page 1 — Section 7 (Reproducibility Statement)*

The Reproducibility Statement promises code release, but the paper itself does not report several hyperparameters essential for reproduction:
- Kernel bandwidths for $K_1$, $K_2$, $K_3$ (or initialization ranges for stochastic coordinate descent)
- The sparsity penalty $\lambda_1$ in Eq (8)
- Latent dimension $k$ for each dataset
- Delay parameter $d$ and $\beta$ coefficients for the delayed response model
- Stopping criteria for the optimization solver

**Required action:** (Must) Add a table in the Appendix listing all hyperparameters per experiment, including default values and the range searched during tuning.

### W9 — Discussion overclaims novelty ("for the first time") (Minor)
*Page 1 — Discussion*

The Discussion opens with "This provides, for the first time, a method for adaptive stimulation of latent neural activity." This absolute claim requires explicit comparison to prior work that addresses closed-loop or adaptive stimulation (Minai et al., 2024; Wagenmaker et al., 2024; Draelos & Pearson, 2020). Without delineating what capability is uniquely new, the claim is vulnerable to challenge. Since Retrieval-Disabled Mode prevents comprehensive literature verification, the authors should either remove "for the first time" or replace it with a scoped claim that specifies the novel combination of components.

**Required action:** (Nice-to-have) Remove "for the first time" or replace with a bounded statement specifying the unique combination of components.

### W10 — Convergence evaluation lacks cross-method comparability (Minor)
*Page 1 — Section 2.1 (All methods converge to offline fits)*

The convergence comparison in Figure 1a uses different metrics (principal angles, Frobenius norm) and different synthetic data generators for each method, preventing quantitative cross-method comparison. The text claims "all methods converge" but does not specify convergence thresholds or report the number of timepoints required.

**Required action:** (Nice-to-have) Add a common evaluation metric (e.g., held-out prediction error) to enable cross-method comparison. Report the time to reach within 5% of the offline solution for each method.

## Score
**Final Score: 5/10**

The paper addresses a timely and important problem — adaptive closed-loop stimulation of latent neural dynamics — and proposes a well-structured framework that combines streaming latent space construction, nonparametric stimulus-response modeling, and constrained optimization. The engineering integration is commendable, and the real-time computational benchmarks (<10 ms per timepoint) demonstrate practical feasibility.

However, the empirical validation has a critical gap: the "real data" experiments use simulated stimulation effects (linear additive AR process), not genuine optogenetic or electrical stimulation, which means the core claim of handling non-robust, non-stationary, network-mediated responses remains untested. The optimization evaluation lacks comparison against existing methods (only random baselines are used), and the toy model does not exercise the continuous high-dimensional optimization it claims to validate. Several mathematical formulations need correction (skew-symmetric eigen-decomposition, L0/L1 mixing in the objective). Reproducibility is hindered by unreported hyperparameters.

**Score justification (10-point scale):**
- Research value + novelty (primary dimension): 5/10. The integrated framework is novel in concept, but without validation on genuine stimulation data or comparison to existing methods, the practical novelty is unverified. (Deferred literature verification due to Retrieval-Disabled Mode may affect this assessment.)
- Validity + soundness: 4/10. Two critical issues (simulated stimulations, missing baselines) and several mathematical inaccuracies reduce confidence in the reported results.
- Reproducibility: 4/10. Key hyperparameters (kernel bandwidths, λ₁, latent dimensions per dataset) are not reported.
- Significance + potential impact: 6/10. If validated with genuine closed-loop stimulation data, the framework could have substantial impact on causal neuroscience experimentation.

**Summary:** The paper has a solid conceptual core and a well-designed algorithmic pipeline, but the current empirical evidence is insufficient to support the claimed capabilities. Major revision with genuine stimulation validation, stronger baselines, and corrected mathematical formulations is needed before the work meets the standards for a top conference publication.