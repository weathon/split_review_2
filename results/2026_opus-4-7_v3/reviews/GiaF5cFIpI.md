Now let me verify specific claims about the optimization formulation and the experiments more carefully.Now I have a thorough understanding of the paper. Let me draft the review.Now let me calibrate. I'll search for anchor papers across the score spectrum.Let me read some of the most topically relevant anchor papers to calibrate my score.Now let me read the iSSM paper more closely since it's the most topically similar anchor.Now I have sufficient information to finalize my calibrated review. Let me synthesize everything.

---

## Summary
This paper proposes a streaming framework for real-time adaptive neural stimulation in latent spaces, comprising three integrated components: (1) streaming latent space construction methods including a novel sjPCA, (2) a nonparametric kernel regression estimator for stimulus-response mapping in latent space, and (3) a constrained optimization formulation for selecting high-dimensional stimulation patterns to drive low-dimensional dynamics along desired directions. The framework is validated on toy models and real neural data (calcium imaging, electrophysiology) with simulated stimulations, demonstrating real-time feasibility (<100ms per timepoint).

## Strengths
- **sjPCA is a concrete algorithmic contribution** (Section 2.1, Eq. 1–2): The use of the Sherman–Morrison formula for iterative updates to the skew-symmetric fit, combined with per-plane Orthogonal Procrustes stabilization, is a clean extension of Churchland et al. (2012) to the streaming setting. Figure 1a demonstrates convergence to offline jPCA with appropriate error metrics.

- **The kernel regression stimulus-response estimator (Eq. 7) is well-designed for its intended regime:** The product-of-kernels structure over latent state, stimulus, and sample age handles the key challenges: few observations, state-dependent responses, and non-stationarity. Figure 2d-e convincingly demonstrates adaptation to both abrupt discontinuities (180° flip at t=25s) and continuous drift (rotation starting at t=45s) in the toy model.

- **The constrained optimization (Eq. 8) captures genuine experimental constraints:** Non-negativity for excitation-only opsins, sparsity for limited simultaneous holographic targets, and bounded magnitude are all real constraints in holographic optogenetic experiments. The paper correctly notes these are often ignored in prior work.

- **Runtime benchmarking demonstrates practical feasibility:** End-to-end computation averages <10ms per timepoint (Section 3), essential for the paper's real-time goal and not trivially achievable for a multi-component pipeline.

- **The closed-loop optimization experiment (Fig. 5) shows the value of learned $\hat{S}$:** The comparison between open-loop (identity mapping) and closed-loop (learned non-trivial mapping) optimization demonstrates that the adaptive stimulus-response model improves stimulation alignment with the target direction.

## Weaknesses

### Fatal
None.

### Major
- **Real data experiments validate only against trivially simple simulated stimulations.** Section 4.1 states: "we simulated stimulations using an autoregressive function… $y_t = r_t + a_t$, $a_t = 0.8 \cdot a_{t-1} + u_t$." This model is linear, additive, channel-specific, and time-invariant — precisely the easy case that any flexible estimator should handle. The paper's own Section 2.3 motivates the method by listing complexities (network effects, state-dependent responses, opsin variability, PSF artifacts), but none appear in the real-data validation. While the toy model (Fig. 2, Fig. 5) does test state-dependent and non-trivial mappings, these are low-dimensional synthetic settings (3D latent space). The gap between what the method claims to handle and what is tested on real neural data is significant.

- **All optimization baselines are uninformed.** Section 4.2, Fig. 4a compares designed stimuli against: random single neurons, random groups, and shuffled designed stimuli. Despite the Introduction positioning the work against Bayesian optimization (Minai et al., 2024), optimal experimental design (Wagenmaker et al., 2024), and other methods, none are used as comparators. Even a simple projection heuristic ($u \propto \max(Q v, 0)$, clipped and sparsified) would be a more informative baseline. Beating random selection is necessary but insufficient to establish the optimization's value.

- **The $L_1$ relaxation in Eq. 8 is questionable as a sparsity-inducing mechanism.** Under box constraints $u \in [0,1]^N$, $\|u\|_1 = \sum u_i$ is linear in $u$ and does not induce sparsity the way $L_1$ does in unconstrained settings. Furthermore, minimizing $\|u\|_0^{\max} - \|u\|_1$ amounts to maximizing $\|u\|_1$, which pushes toward *dense* solutions — the opposite of the paper's stated intent to "encourage a solution with the number of non-zero elements close to $n$" (Section 2.4). The notation $\|u\|_0^{\max}$ is undefined. No analysis of whether optimized solutions are actually sparse is provided, which matters for practical holographic photostimulation requiring discrete target selection.

### Minor
- **The abstract and introduction claim the framework enables "adaptive selection of stimulations to best distinguish amongst neural subspace hypotheses," but no experiment demonstrates this.** The system is only used to drive dynamics along predetermined directions (Q₀, random feasible directions, etc.). The hypothesis-testing use case remains purely aspirational.

- **The parallel latent-space comparison method (Section 2.2, Fig. 1c) is described as a "novel streaming estimator" but is methodologically thin.** It amounts to comparing one-step-ahead prediction errors across models, aggregated by spatial location. No formal model selection criterion, hypothesis testing, or statistical characterization of the heatmaps is provided. This is a useful heuristic but overstated as a distinct methodological contribution.

- **Kernel bandwidth tuning is underspecified for the stated low-data regime.** The paper claims learning within 10–20 stimulations (Introduction) and tunes bandwidth via "stochastic coordinate descent at each new observation" (Section 2.3), but with so few observations, sensitivity to bandwidth choices could be high. No analysis of this sensitivity is provided.

- **The optimization experiments in Fig. 4a-c use an identity stimulus-response mapping** ($S(u) = Q^\top u$, confirmed in the paragraph preceding Fig. 5: "The above experiments assumed that the result of a stimulation $u$ was simply its projection into the latent space"). While Fig. 5 tests a non-trivial mapping, the main optimization results (Fig. 4) reflect a setting where the mapping requires no learning, making the near-perfect alignment (<1° for Feasible and Q₀ conditions) less informative.

### Trivial
None.

## Nice-to-Haves
- Test stimulus-response modeling on simulations with network-mediated effects (stimulating neuron $i$ activates neurons $j, k$ through recurrent connections), state-dependent nonlinear gain, and partial failures — even without real experimental data. This would test the kernel regression in the regime the paper motivates.
- Report the distribution of $\|u^*\|_0$ across optimization conditions to verify whether the relaxation actually produces sparse solutions suitable for holographic photostimulation.
- Analyze the optimization landscape: convergence properties, sensitivity to initialization, and frequency of local optima for the non-convex cosine similarity objective.
- Provide guidance on when to prefer each latent space method (sjPCA vs proSVD vs mmICA) beyond the observation that independence "may construct better latent spaces."

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Reviewer claimed the $L_1$ term "pushes toward zero stimulation."** This is factually incorrect: under box constraints, minimizing $\|u\|_0^{\max} - \|u\|_1$ maximizes $\|u\|_1$, pushing toward density, not zero. The underlying concern about the formulation not inducing sparsity is valid and retained as a Major weakness, but the specific mechanism claimed was wrong.

- **Criticism that the Discussion's suggestion about behavioral modeling is "overly optimistic."** This is the authors' honest acknowledgment of a limitation and future direction, not a weakness of the paper. Papers should discuss future work.

- **Criticism that mmICA convergence test uses data matching its own assumptions.** While true (Section 2.1 states the data has "Laplace random variables where the dimensions are jointly independent"), this is standard practice for validating convergence of an algorithm — you first show it works under its assumptions before testing generalization. This is a minor presentation issue at most, and the paper is transparent about it.

- **Criticism that the paper should compare against missing related works.** Per hard rules, we do not evaluate missing related work comparisons.

## Novel Insights
The integration of streaming latent space construction, adaptive kernel regression with temporal discounting, and constrained optimization into a single real-time pipeline is architecturally novel for the neural stimulation domain. The temporal kernel in the stimulus-response estimator (Eq. 7) — enabling automatic adaptation to both abrupt and gradual non-stationarities in the stimulus-response map — is a practical insight applicable beyond this specific application. The demonstration that closed-loop optimization with learned $\hat{S}$ outperforms open-loop optimization (Fig. 5b) provides initial evidence that adaptive stimulus-response modeling matters for stimulation design, though this is shown only in the toy model.

## Suggestions
- Replace the simple autoregressive stimulation model in real data experiments with one incorporating recurrent network effects and state-dependent gain, even staying fully in simulation.
- Add at least one informed baseline for the optimization comparison — a projection-based heuristic ($u = \max(Qv, 0)$ sparsified) would be easy to implement and far more informative than random stimulation.
- Fix or clarify the $L_1$ relaxation: either reformulate to actually induce sparsity (e.g., use an explicit $L_1$ constraint $\|u\|_1 \leq n$) or report the sparsity of actual solutions to demonstrate the current formulation works in practice despite the theoretical concern.
- Demonstrate the hypothesis-distinguishing capability described in the abstract, or remove the claim.
- Provide sensitivity analysis for kernel bandwidth in the low-data regime (10-20 stimulations).

## Score and Decision

**Anchor papers retrieved (all rounds):**

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Financial Markets NN | nSDOkm0SKo | 1.0 | 1 | Far weaker — not a real research contribution |
| Time-dependent UMAP | P49gSPmrvN | 1.0 | 1 | Far weaker — trivial method, no evaluation |
| IC-Light | u1cQYxRI1H | 10.0 | 1 | Far stronger — complete method with extensive real validation |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.0 | 1 | Far weaker — fundamental methodology issues |
| Hyperdimensional Computing | NYPJz0CL5X | 3.0 | 1 | Weaker — less coherent framework, but also underdeveloped |
| **TAVRNN** | NPzuN3Rxi8 | **3.0** | 1 | Weaker — poor presentation, minimal improvement over baselines; this paper has cleaner contributions |
| Successor Representations DHTM | fnO5h1CFyh | 3.0 | 1 | Different domain; similar issue of limited validation |
| Reservoir Learning | Z1E0EahS5w | 3.33 | 1 | Different domain; theoretical contribution with limited scope |
| **Stabilized Neural Dynamics (HDA)** | LNp7KW33Cg | **5.0** | 1 | Similar domain; comparable validation level but with established baselines |
| **Nonparametric Covariance Regression** | PdZkfSttGK | **5.25** | 1 | Similar domain; stronger theoretical grounding |
| **Interventional SSM (iSSM)** | FwW3jqchtY | **5.0** | 1 | Most directly comparable — also models neural dynamics under perturbations; has real perturbation data AND identifiability proofs but still scored 5.0 with Reject decision |
| Time-Dependent VAE | N83O2FcqzN | 5.0 | 1 | Similar domain; comparable issues with validation scope |
| **Closed-loop EEG** | 4ltiMYgJo9 | **5.75** | 1 | Similar closed-loop framework; has real experiments but weak presentation |
| **Consistent Neural Embeddings (FDA)** | F5lcN7329a | **6.0** | 1 | Stronger theoretical grounding with stability analysis |
| **BRAID** | 3usdM1AuI3 | **6.25** | 1 | Similar domain; stronger validation with real data, established baselines |
| SPDIM | CoQw1dXtGb | 6.2 | 1 | Different domain; more rigorous evaluation |
| Optimal Transport Neural | cNmu0hZ4CL | 8.0 | 1 | Stronger — novel metric with theoretical backing and comprehensive validation |
| Feedback Neural ODEs | cmfyMV45XO | 8.0 | 1 | Stronger — theoretical guarantees with broad experimental validation |
| Brain Bandit | RWJX5F5I9g | 8.0 | 1 | Stronger — clean theory-to-experiment pipeline |
| Conformal Isometry Grid Cells | Xo0Q1N7CGk | 8.0 | 1 | Stronger — theoretical + numerical validation aligned |

**Round 1 bracket: 4.0 – 5.5**

The paper under review is clearly better than the 3.0-band papers (TAVRNN, DHTM, etc.) which suffer from poor presentation, minimal improvements, and incoherent contributions. However, it is weaker than the most directly comparable anchor, iSSM (5.0, Reject), which has real perturbation data and identifiability proofs. The closed-loop EEG paper (5.75) has actual closed-loop experiments despite other weaknesses. BRAID (6.25) demonstrates its framework on real data with established baselines.

**Narrowing to final score:** The paper has well-designed algorithmic components and targets an important problem, but the evidence gap is substantial: (1) real data experiments use trivially simple simulated stimulations that don't test the method's stated advantages, (2) all optimization baselines are uninformed, and (3) the sparsity mechanism in the optimization has a formulation issue. Compared to iSSM (5.0), which was rejected despite having real perturbation data and theoretical guarantees, this paper's weaker validation suggests it sits at or below 5.0. The clean framework architecture and runtime feasibility keep it above the 3.0-band papers. The paper is more like a borderline reject — the ideas are sound and the problem is real, but the validation does not yet support the claims.

**Final score: 4.5**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>