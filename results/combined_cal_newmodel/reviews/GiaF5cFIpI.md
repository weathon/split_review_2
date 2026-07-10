Now let me compile the final review with all the calibration evidence.

## Calibration Summary

**Round 1 anchors (bracketing):**

| Path | Avg Score | Round | Itemized? | Comparison to Reviewed Paper |
|------|-----------|-------|-----------|-----|
| FwW3jqchtY.md (iSSM) | 5.00 | R1 | Yes | Most relevant anchor. Tests on real neural perturbation data and has identifiability proof, both advantages over our paper. But shares the same "lack of baselines" weakness (favorability -1.15). Our paper is below this anchor. |
| 3usdM1AuI3.md (BRAID) | 6.25 | R1 | Yes | Stronger validation with proper baselines, better experiments. Our paper is significantly below this. |
| MFCjgEOLJT.md (interpretable control) | 5.75 | R1 | Yes | Has proper behavioral validation. Our paper is below this. |
| 4AlNpszv66.md (FCCA) | 4.75 | R1 | Yes | Novel theoretical contribution but technical derivation issues. Our paper has cleaner methods but weaker validation. Comparable tier but slightly below. |

**Round 2 narrowing (3.0–5.5):** All results consistent with R1 findings. iSSM (5.00) remains the closest comparison. The iSSM paper was rejected despite testing on *real* neural perturbations and having an identifiability proof — its weaknesses were lack of baselines and strong assumptions. Our paper shares the baseline weakness but additionally lacks real neural response validation. This places us clearly below 5.00.

**Final bracket:** 3.5–4.5. The paper has a genuine framework contribution but the evidence gap (simulated stimulations, weak baselines) is too large for the claims made.

---

## Summary

This paper proposes an integrated real-time framework for adaptive stimulation design in latent neural spaces, combining streaming dimensionality reduction, online dynamical modeling, a kernel-regression-based stimulus-response map, and constrained optimization. Tested on simulated data and two real neural datasets (calcium imaging, electrophysiology) but with *simulated* AR(1) stimulation responses added to real background activity.

## Strengths

- **Integrated real-time framework.** The paper combines streaming dimensionality reduction, online dynamical modeling, a learnable stimulus-response map, and constrained optimization into a single closed-loop pipeline (Algorithm 1). No prior work assembles all four components in a streaming setting with realistic experimental constraints.

- **Non-stationarity handling.** The temporal kernel K₃ in Eq. (7) allows the stimulus-response model to discount older observations, demonstrated against abrupt flips and continuous drift (Fig. 2e). This is a practically important feature for real experiments where photobleaching, plasticity, or probe movement change response properties.

- **Realistic feasibility constraints.** The optimization problem (Eq. 8) incorporates non-negativity (excitation-only opsins), a sparsity penalty approximating an L0 constraint on the number of stimulated neurons, and box constraints on stimulation magnitude. These reflect real optogenetic limitations.

- **Cross-modality testing and runtime benchmarks.** The method is tested on calcium imaging (15 Hz) and electrophysiology (30 Hz) data, and runtime is confirmed below 100 ms end-to-end. This establishes computational feasibility for real-time closed-loop experiments.

- **Streaming methods converge to offline fits.** Fig. 1a shows sjPCA, proSVD, and mmICA converge to their offline counterparts, which is a necessary sanity check for the streaming components.

## Weaknesses

### Major

1. **Real-data experiments use simulated, not real, neural responses to stimulation.** Section 4.1 (line 178) states: "For each of the real datasets, we simulated stimulations using an autoregressive function... a_t = 0.8·a_{t-1} + u_t." The "response" the method learns (Fig. 3) is this pre-specified AR(1) model added to real neural traces. The method is never tested on actual neural responses to optogenetic or electrical stimulation. The central claim — that the method can "design neural stimulations that perturb latent dynamics in arbitrary directions" — is not supported by evidence from real neural responses. A simple linear autoregressive process is vastly easier to learn than real neural responses (which involve network effects, opsin expression variability, point-spread function spillover, and state-dependent dynamics). This is the most consequential weakness and substantially limits what the paper can claim.

2. **Baseline comparisons are too weak to support the specific modeling choices.** The only comparison is against a "blind" model that ignores stimulations (Figs. 2e, 3c) — any method accounting for stimulation effects should outperform one that does not. The optimization comparisons (Fig. 4a) are against random single-neuron, random group, and shuffled stimuli — trivial baselines that any directed optimization method should dominate. The paper cites Bayesian optimization (Minai et al., 2024), active learning (Wagenmaker et al., 2024), and input-output dynamical modeling (Yang et al., 2021) as relevant prior work but does not compare against any of them. Without such comparisons, the reader cannot assess whether the specific kernel-regression-based approach has advantages over simpler or more established alternatives.

### Minor

3. **The high-dimensional kernel regression (K₂ in Eq. 7) operates in the full N-dimensional stimulus space (up to 592 dimensions) without discussion of the curse of dimensionality.** Kernel regression with RBF kernels in high-dimensional spaces suffers from distance concentration, making weights uninformative. The claim that 10-20 stimulations suffice to learn the mapping is unsupported by any analysis of how N or latent dimension k affects sample requirements. (The sparsity constraint on *u* partially mitigates this, but the paper does not make this argument.)

4. **The additive decomposition assumption in Eq. (3) is unexamined.** The model assumes stimulation responses add linearly to autonomous dynamics: x_{t+1} = f(x_t) + S(x_t, u_t). Stimulation could instead modify dynamics multiplicatively, shift the latent state non-additively, or interact with f. The paper does not discuss what kinds of neural responses violate this assumption or how robust the method is to such violations.

### Trivial

None.

## Nice-to-Haves

- Validate on data with real (not simulated) neural responses to stimulation, or at minimum use a substantially more realistic generative model (e.g., a spiking network model with known optogenetic drive) rather than a simple AR(1) process.
- Compare against at least one existing stimulation design method (e.g., Bayesian optimization with GP response, linear regression on u→s) to isolate the benefit of the nonparametric modeling choice.
- Add an ablation study removing each kernel component (K₁, K₂, K₃) to clarify which dependencies are essential.
- Provide analysis of how many stimulation observations are needed as a function of N and latent dimension k.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **sjPCA not compared against sliding-window jPCA** (harsh critic): The paper shows sjPCA converges to offline jPCA (Fig. 1a), which is the primary validation needed. This is a reasonable suggestion but a minor methodological nitpick, not a core weakness. → Moved to Nice-to-Haves.
- **Non-convex optimization with no analysis of solution quality** (harsh critic): The paper explicitly acknowledges this (line 144: "more approximate optimization and solution"). This is a known tradeoff the authors flag. → Moved to Nice-to-Haves.
- **Toy model uses binary u=0 or 1** (harsh critic): The toy model is explicitly for basic validation of location-dependent effects; the high-dimensional stimulus testing uses real data with up to 592 neurons. The toy model's scope is clearly stated.
- **Parallel latent space selection not integrated into stimulation experiments** (harsh critic): This is presented as a capability, not a tested component. It's a scope note, not a weakness.
- **Various section-by-section restatements** of paper content rather than specific identified problems.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. The single highest-leverage improvement is to validate on data where actual stimulations were delivered with real neural responses. Without this, the gap between claims and evidence remains too large.
2. Add proper baselines — at minimum linear regression on u→s (to isolate nonlinear modeling benefit) and one existing method (e.g., Bayesian optimization with GP).
3. Ablate the three kernel components to show which dependencies are essential.
4. Provide a sample-efficiency analysis showing how N and k affect the number of stimulations needed.

**Score and Decision:** The paper addresses a genuine need and assembles a well-motivated framework with practical constraints. However, the validation is insufficient for the claims: all "real data" experiments use simulated AR(1) stimulation responses, not actual neural responses, and the baselines are too weak to support the specific modeling choices. The evidence gap between the stated contribution and the experiments is too large.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>