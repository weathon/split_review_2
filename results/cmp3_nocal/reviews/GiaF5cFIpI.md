## Summary

This paper proposes a modular, streaming framework for adaptive stimulation of latent neural dynamics. It combines online dimensionality reduction (including a novel streaming jPCA variant), dynamical modeling, nonparametric stimulus-response regression via kernel regression, and constrained optimization to design high-dimensional stimulation patterns that drive low-dimensional latent activity in desired directions. The framework handles non-stationarity in the stimulus-response mapping and accounts for realistic experimental constraints such as non-negative stimulation amplitudes and limits on simultaneous targets.

## Strengths

- **Modular architecture with clear separation of concerns.** The pipeline (Algorithm 1) cleanly decouples streaming latent space construction, dynamical modeling, stimulus-response kernel regression, and constrained optimization. Individual components can be swapped independently (e.g., different latent representations, different dynamical models), which is a genuine design strength for a framework targeting real-time neural experiments.

- **Explicit handling of non-stationarity in the stimulus-response mapping.** The temporal kernel in Eq. (7) allows the regression to discount old samples, and the paper validates this on both an abrupt 180° flip (t=25s) and continuous drift (rotation at 1 rev/30s) in the toy model (Fig. 2d-e). The model demonstrably recovers from these perturbations within ~15s, addressing a realistic concern in long-duration neural recordings.

- **Realistic experimental constraints are incorporated into the optimization.** The formulation in Eq. (8) includes non-negativity constraints (excitation-only photostimulation), a limit on the number of simultaneous targets (via the sparsity-related penalty), and box constraints [0,1]^N. The optimization leverages the differentiable kernel regression to compute gradients through the learned mapping, which is a pragmatic design choice.

## Weaknesses

### Major

- **The validation does not match the strength of the central claims.** The paper's core claim is about *designing stimulations to drive latent neural dynamics*, but the "real data" experiments (lines 178, 188) apply synthetic AR(1) perturbations overlaid on real background neural activity, not real stimulations. This means: (a) the stimulus-response mapping the method must learn is a known, simple linear generative process (AR(1): a_t = 0.8·a_{t-1} + u_t); (b) the optimization results in Figs. 4-5 validate the ability to invert a known synthetic mapping, not to handle realistic neural responses involving network-mediated effects, nonlinear interactions, or opsin expression heterogeneity. The abstract states "demonstrate our approach on both simulated and real neural data" without qualifying that the *stimulation effects* on real data are entirely simulated. While the paper acknowledges this in the Discussion (line 252: "simulated effects of arbitrary stimulations"; line 258: "performed offline"), the framing throughout the abstract and introduction inflates what has actually been demonstrated. This is the paper's most significant weakness.

- **The only quantitative baseline is a straw man.** The sole comparison is against a "blind" model that receives no information about stimulation times or effects (lines 186-188, Fig. 2e, Fig. 3c). Any method that accounts for stimulations must outperform a method that ignores them entirely; this comparison tells the reader nothing about whether the proposed approach is better than reasonable alternatives. The paper cites active learning (Wagenmaker et al., 2024), Bayesian optimization (Minai et al., 2024), and input-output dynamical modeling (Yang et al., 2021) but implements none of them. Even a simple parametric alternative (e.g., a linear model or fixed finite-impulse-response model) would provide a meaningful comparison. The claimed "outperformance" is unsupported without a nontrivial baseline.

- **No comparison against any existing stimulation design method.** Related work on stimulation design (Minai et al., 2024; Wagenmaker et al., 2024; Draelos & Pearson, 2020; Yang et al., 2021) is cited but never used as an experimental baseline. Even a random-search baseline over stimulation patterns would be more informative than the "blind" comparison for evaluating the optimization component's added value.

### Minor

- **The optimization formulation has two unaddressed issues.** First, Eq. (8) minimizes a non-convex objective (because s(u) involves RBF kernel predictions), but the paper does not discuss initialization strategy, sensitivity to local minima, or convergence criteria. Second, the sparsity penalty λ₁(‖u‖₀^max − ‖u‖₁) is unusual: under box constraints [0,1]^N, minimizing this term drives ‖u‖₁ toward ‖u‖₀^max, which pushes entries toward 1 rather than toward sparsity. The paper's explanation that it "encourages a solution with the number of non-zero elements close to n" (line 148) is not logically connected to the L1 norm under these constraints, since many small entries could also sum to the target. This does not invalidate the approach but the formulation is confusing and the reasoning is unclear.

- **Quantitative evidence lacks statistical rigor.** Performance is described qualitatively throughout ("quickly learns," "out-performed," "significantly lower error"). Fig. 2e shows smoothed traces over 50 experiments but no numeric summary statistics or effect sizes. Fig. 3c shows error traces with no error bars despite multiple runs. Fig. 5 shows learning curves with no error bars across the stated 10 experiments. The paper reports mean±std exactly once (line 233-234). For claims about which method "outperforms" which, the absence of confidence intervals, bootstrapped estimates, or any hypothesis testing weakens the evidence.

- **The parallel-representation comparison is not validated in a closed-loop stimulation setting.** The abstract promises "adaptive selection of stimulations to best distinguish amongst neural subspace hypotheses." Section 2.2 describes this capability conceptually, and Figure 1c shows a descriptive heatmap of predictive probabilities across latent spaces. However, there is no experimental demonstration that switching representations based on this signal actually improves stimulation targeting or yields better predictions during stimulation periods. It is described as something the method *could* do, not something shown to work.

- **sjPCA is an incremental contribution with limited validation.** The novel streaming jPCA (lines 70-83) composes off-the-shelf pieces (proSVD, Sherman-Morrison update, Orthogonal Procrustes stabilization). It is validated only for convergence to an offline jPCA fit (Fig. 1a), not tested in the context of the *stimulation task* or compared against simply running jPCA on an expanding window. The method description is underspecified for reproducibility (the Sherman-Morrison update rule is not given explicitly).

### Trivial

None.

## Nice-to-Haves

- An ablation study isolating the contribution of each framework component (streaming latent space, kernel choice, temporal kernel length scale, sparsity penalty weight λ₁) would help identify which design decisions matter most.
- The β coefficients for modeling continuing effects of stimulation (line 134) are described but never evaluated experimentally; including even a simple test case would clarify their utility.
- A basic timing table in the main text (currently deferred to Supplementary Materials) would strengthen the real-time feasibility claim.

## Removed Points

- **"Abstract is misleading"** (from critic's section notes): The abstract's phrasing "demonstrate our approach on both simulated and real neural data" is technically accurate (the neural data is real). The paper explicitly discloses the simulated nature of stimulations at line 178 and in the Discussion (line 252-253). Removed because the paper is transparent about this limitation, and the critic's characterization overstates the degree of misrepresentation.
- **Section-by-section notes on Fig. 1c/parallel selection** (from critic's section notes): Redundant with the Minor weakness above; folded into that entry rather than listed separately.
- **"The method description is under-specified for reproducibility"** (critic's Section 2.1 note on sjPCA): This is a legitimate point but it is a reproducibility concern that falls under the "nitpick about undisclosed details" scope — the specific Sherman-Morrison update is standard and the paper points to the right technique. Demoted to a note within the sjPCA weakness above rather than a standalone weakness.
- **"No ablation studies"** (from critic's Missing Parts): Not a weakness per se — many papers do not include full ablation studies — but a nice-to-have. Moved to Nice-to-Haves.
- **Strength: "The problem is well-motivated and timely"**: Generic; removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The modular framework combining streaming jPCA with kernel-regression-based stimulus-response modeling and constrained optimization is the paper's primary architectural contribution. The reviews do not surface a novel perspective that the paper itself did not articulate.

## Suggestions

1. Recenter the paper's claims to match what is demonstrated. Replace phrases like "real neural data" in the abstract with "real neural data with simulated stimulation effects" — the Discussion already uses this more precise language (line 252).
2. Add at least one nontrivial baseline: either a parametric alternative (e.g., linear stimulus-response model), a random-search optimization baseline, or a simplified implementation of one of the cited existing methods (Minai et al., Wagenmaker et al., or Yang et al.).
3. Report confidence intervals, bootstrapped error bars, or effect sizes for all quantitative comparisons where claims of "outperformance" are made.
4. Clarify the sparsity penalty in Eq. (8): explain how minimizing (‖u‖₀^max − ‖u‖₁) relates to controlling the number of nonzero entries under box constraints, or replace it with a more standard sparsity-inducing formulation.
5. Validate the parallel-representation comparison in a closed-loop setting, even in simulation, to show that switching based on predictive probability improves stimulation targeting.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>