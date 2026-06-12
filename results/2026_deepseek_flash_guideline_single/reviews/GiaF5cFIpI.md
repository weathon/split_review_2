Now I have sufficient calibration. Let me write the final review.

## Summary

This paper proposes a streaming framework for learning stimulation-response mappings in latent neural spaces and optimizing high-dimensional stimulation patterns to drive low-dimensional latent dynamics. The pipeline integrates streaming latent space construction (including a novel streaming jPCA variant), dynamical modeling of neural latents, adaptive nonparametric kernel regression for stimulus-response mapping, and constrained optimization for selecting stimulation patterns under experimental feasibility constraints. The method is tested on simulated data and on real neural recordings (calcium imaging and electrophysiology) with synthetically injected stimulation effects.

## Strengths

- **Modular and comprehensive framework design.** The pipeline decomposes a hard real-time neural control problem into well-defined, swappable components: streaming dimensionality reduction (proSVD, sjPCA, mmICA), dynamical modeling (KF, VJF, Bubblewrap), kernel-regression-based stimulus-response learning, and constrained optimization (Sections 2.1–2.4). Running multiple representations and dynamics models in parallel (Figure 1c) is a practical strength for an eventual experimental tool, as it allows direct comparison across competing latent-space hypotheses.

- **Thoughtful handling of non-stationarity.** The temporal kernel in the stimulus-response regression (Equation 7) allows the model to discount old observations and adapt to instabilities like probe drift or plasticity. The toy experiments with a flip (180° at t=25s) and rotation (1 revolution/30s) of the ground-truth mapping (Figure 2d–e) demonstrate that this mechanism works in principle, with quantified recovery times (~15s for a flip).

- **Real-time computation speeds are demonstrated.** The paper reports end-to-end runtimes averaging <10ms and always <100ms (lines 23, 154), which is a concrete prerequisite for future *in vivo* closed-loop use. This is verified across the component stack, not just a single submodule.

## Weaknesses

### Major

- **Weak evaluation baselines.** The stimulus-response model is compared only against a "blind" model that ignores stimulation entirely (lines 186–188). The optimization is compared only against random single neurons, random groups, and shuffled versions of the designed stimuli (Figure 4a). Both comparisons are sanity checks: any reasonable method that models stimulation effects should outperform one that ignores them, and any reasonable optimization should beat random. The paper cites related stimulation design methods (Minai et al., 2024, Bayesian optimization; Wagenmaker et al., 2024, active learning; Yang et al., 2021, input-output modeling) but does not compare against any of them. Without stronger baselines, it is impossible to assess whether the optimization framework constitutes a meaningful advance over existing approaches or simply re-discovers trivial improvements over random.

- **"Real data" experiments test recovery of an injected synthetic mapping, not real closed-loop control.** The real neural recordings are used as background, with stimulation effects synthetically injected via an autoregressive model: y_t = r_t + a_t, a_t = 0.8·a_{t-1} + u_t (lines 177–178). Every "real data" result (Figures 3–4) tests the algorithm's ability to recover this known injected mapping—a substantially weaker proposition than learning a true biological stimulus-response function involving real opsin expression, off-target effects, tissue response, and biological variability. The paper acknowledges this in the Discussion (lines 258–259: "performed offline, though in a realistic streaming setting"), but the abstract and introduction do not flag the distinction, creating an impression of broader validation. The core claim—that the framework can drive real neural dynamics in a closed-loop setting—remains untested.

- **Parallel representation tracking and adaptive space selection are described but unvalidated.** The paper claims the ability to compare across latent spaces in parallel and adaptively select the most predictive representation (lines 92–93, 108, Figure 1c), and the abstract lists this as a contribution. However, no experiment shows that this adaptive selection improves stimulation design, dynamics prediction, or any downstream outcome. The mechanism is presented without quantitative evaluation.

### Minor

- **sjPCA receives minimal validation.** The novel streaming jPCA method (Section 2.1) is validated only on simulated data via a convergence plot showing its subspace matches an offline computation (Figure 1a, N=10). The paper does not report whether sjPCA converges faster or more accurately than simply recomputing jPCA on a sliding window, how sensitive it is to the Procrustes alignment step, whether the stabilization improves downstream stimulus-response modeling, or how it compares against other online subspace tracking methods beyond proSVD. Since the paper bills sjPCA as a "novel streaming formulation" (line 83), this validation is thin.

- **The sparsity-encouraging optimization term is unconventional and underspecified.** Equation (8) uses λ₁(‖u‖₀^max − ‖u‖₁) with u ∈ [0,1]^N. Minimizing this term pushes ‖u‖₁ toward ‖u‖₀^max (i.e., encourages large total activation), which is the opposite of sparsity. The sparsity must arise from interaction with the cosine-similarity term, but the paper does not explain how λ₁ is chosen, how sensitive solutions are to this parameter, or why this formulation is preferable to standard L1 or L0-relaxation approaches.

- **Kernel bandwidth tuning is underspecified.** The kernel regression (Equation 7) uses RBF kernels where "each scaling constant is optionally tuned by stochastic coordinate descent at each new observation" (lines 136–137). No details are given on initialization, update frequency, or how multiple scaling constants (for x, u, and t kernels) are handled jointly, making reproduction harder than necessary.

- **Statistical reporting is inconsistent.** Figure 1a reports N=10 runs with error bars, toy experiments use 50 runs (line 186), and Figure 5 states 10 experiments with 100+ stimulations each. However, the real-data results (Figure 3c) show single traces without any error bars or replication information, making it impossible to assess variability on the data where the method is most meaningfully tested.

### Trivial

None.

## Nice-to-Haves

- Running one actual closed-loop experiment (even in a simplified preparation such as cultured neurons or an invertebrate with optogenetics) would substantially strengthen the validation, as would testing the method's robustness to realistic failure modes (e.g., non-responsive neurons, point-spread-function overlap).
- Comparing the optimization against at least one existing stimulation design method from the cited literature (e.g., Bayesian optimization from Minai et al., 2024).
- Adding the identity mapping (open-loop optimization, already used in some experiments) as an explicit baseline for the closed-loop case to quantify the benefit of learning the stimulus-response mapping.
- Validating the adaptive space selection component quantitatively, or tempering the claims about it.

## Removed Points

- "The core problem is well-motivated and genuinely open" (Strength) — generic praise lacking specific anchoring to this paper's concrete contributions; removed per filtering rules.
- "The framework is modular and comprehensive" was originally kept — kept as a genuine strength.
- Various formatting/style comments from the harsh critic's section-by-section notes — these are parser artifacts or presentation issues with no bearing on the scientific contribution.
- Concerns about missing appendix content (e.g., "see Appendix C for comparison across all models") — the appendix is stripped by the parser; the paper references its own appendix, which exists in the original submission.
- The harsh critic's "Strengthening the Paper on Its Own Terms" section — moved to Nice-to-Haves as constructive suggestions rather than weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add at least one non-trivial baseline.** The identity/open-loop mapping (already present in the paper's own framework) provides a natural comparison for the closed-loop learned mapping. An explicit comparison showing that learning the S-mapping via kernel regression outperforms open-loop projection would directly demonstrate the value of the adaptive component. If possible, also compare against a simple non-adaptive linear regression baseline.

2. **Clarify the validation scope in the abstract and introduction.** State explicitly that the real-data experiments use synthetic stimulation effects injected into real neural recordings, not closed-loop biological stimulation. This would better align reader expectations with what is actually demonstrated.

3. **Provide error bars or confidence intervals for the real-data experiment (Figure 3c).** Without replication information, the variability on the most interesting test data is unknown.

4. **Either validate the adaptive space selection quantitatively or remove the claim.** A simple experiment showing whether switching to the best-predicting latent space improves stimulation alignment compared to using a fixed space would substantiate this claimed contribution.

5. **Provide more detail on key algorithmic choices:** the λ₁ selection in the optimization objective and the kernel bandwidth tuning procedure. These affect both reproducibility and the reader's ability to assess the method's robustness.

6. **For sjPCA, provide a comparison against the natural baseline of recomputing jPCA on a sliding window** and show whether the Procrustes stabilization step measurably improves downstream performance.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `wCUw8t63vH` (Spectral learning of shared dynamics) | 6.80 | Round 1 | Stronger mathematical contribution with baseline comparisons; scored higher but still rejected |
| `WQwV7Y8qwa` (Modeling state-dependent communication) | 5.80 | Round 1 | More thorough real-data validation and baseline comparisons; scored higher and accepted |
| `PdZkfSttGK` (Nonparametric Covariance Regression) | 5.25 | Round 1 | Similar evaluation approach (neural data + method); reviewers cited limited novelty and weak results |
| `N83O2FcqzN` (Time-Dependent VAE) | 5.00 | Round 1 | Similar profile (neural LVM method, weak baselines); scored 5.00, rejected |
| `vfHISoWo2m` (Meta-Learning Nonlinear Dynamical Systems) | 4.00 | Round 2 | Similar in having interesting method but limited evaluation; scored 4.00 |

### Bracket

Round 1 bracketing placed the paper between the 3.5–5.5 band. The most topically similar anchors (nonparametric neural data modeling, latent dynamics papers) occupy the 4.00–5.25 range. The paper under review has a well-motivated framework but weaker baselines and more limited real-data validation than even the lower-scored anchors, placing it near the bottom of this band.

### Final Score

This paper addresses a genuinely important and difficult problem. The modular framework design and non-stationarity handling are sensible. However, the evaluation is substantially weaker than what the claims require: the only baselines are a "blind" model (which ignores stimulation) and random, no existing stimulation-design method is used for comparison, and the "real data" experiments test recovery of an injected synthetic mapping rather than real closed-loop control. The novel sjPCA component receives minimal validation, and the adaptive space selection is described but not evaluated. These issues do not invalidate the framework, but they significantly limit what can be concluded from the paper as presented.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>