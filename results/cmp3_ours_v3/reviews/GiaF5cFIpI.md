Now let me write the final review.

## Summary

This paper presents a real-time computational framework for designing neural stimulations that drive activity along desired directions in latent neural spaces. The framework integrates streaming dimensionality reduction (including a novel sjPCA method), dynamical modeling, nonparametric stimulus-response modeling via kernel regression, and constrained optimization to select high-dimensional stimulation patterns. Tests on a toy model and two real neural datasets (calcium imaging, electrophysiology) demonstrate the method's computational feasibility. However, key claims about modeling and designing real neural stimulations are not supported by the evidence presented.

## Strengths

- **Well-motivated problem.** Causal testing of latent neural manifold hypotheses via targeted stimulation is a genuinely important and timely challenge in neuroscience, and the paper articulates this motivation clearly.

- **Coherent end-to-end pipeline.** The framework integrates streaming latent construction, dynamical modeling, nonparametric stimulus-response estimation, and constrained optimization into a single real-time-compatible loop (Algorithm 1). The modular architecture is a non-trivial contribution.

- **Handling of non-stationary stimulus-response mappings.** The temporal kernel in Equation (7) and the explicit demonstration of recovery from a sudden flip and continuous drift (Figure 2d–e) address a real experimental problem that most stimulation methods ignore. This is demonstrated convincingly on the toy model.

- **Practical constraints.** The framework incorporates non-negativity, sparsity, and magnitude limits on stimulation (Equation 8), reflecting real optogenetic constraints that prior work often neglects.

## Weaknesses

### Fatal

None.

### Major

1. **Real-data experiments use simulated, not real, stimulation effects.** On real neural data (calcium imaging, electrophysiology), the paper does not deliver actual stimulations and measure real responses. Instead (lines 178–179): the authors inject a synthetic autoregressive stimulation effect into the recordings and then evaluate whether their method can learn this synthetic mapping. The ground-truth stimulus-response function is therefore known by construction, not discovered from biological responses. The paper's core claim — that the method can *"design neural stimulations that perturb latent dynamics in arbitrary directions"* (§1) — is not supported by evidence from experiments where stimulation was actually delivered and real neural responses measured. While the toy model (§3) provides a useful proof-of-concept with known ground truth, it does not substitute for the missing biological validation. The Discussion (lines 258–259) acknowledges the offline nature but does not address the more fundamental gap: the central claim about designing *effective real stimulations* remains untested.

2. **Very weak baselines.** The optimization evaluation (Figure 4) compares the proposed method against: (i) randomly chosen single neurons, (ii) randomly chosen groups of neurons, and (iii) shuffled versions of the method's own stimuli. These are not meaningful baselines. The response model is compared against a "blind" model that ignores stimulation entirely — a strawman guaranteed to fail during stimulation periods. The paper cites relevant prior work on stimulation design (Minai et al., 2024; Wagenmaker et al., 2024; Yang et al., 2021) but does not compare against any of these approaches. The open-loop (identity) comparison in Figure 5 is a step in the right direction, but the evaluation overall does not establish that the method outperforms—or even compares favorably to—existing approaches.

### Minor

1. **Optimization sparsity constraint is mathematically mis-specified in Equation (8).** The term λ₁(‖u‖₀^max − ‖u‖₁) is minimized by making ‖u‖₁ *large* — i.e., pushing u toward the all-ones vector, which is the opposite of sparsity. Under the box constraint [0,1]^N, minimizing (constant − ‖u‖₁) is equivalent to maximizing ‖u‖₁, producing dense solutions. The text (line 148) claims this term "encourages a solution with the number of non-zero elements close to n," but the written formulation does not achieve this. This is likely fixable (e.g., minimizing ‖u‖₁ directly), and the experimental results suggest the alignment term may dominate in practice, but the formulation as presented is incorrect.

2. **Lack of statistical reporting for key results.** Several results (§4.2) are reported as point counts ("517/600 optimizations gave an optimization misalignment of less than 1°") without confidence intervals, error bars, or significance tests. Given the small underlying sample, bootstrap confidence intervals would be appropriate.

### Trivial

None.

## Nice-to-Haves

- An ablation study isolating how sensitive the stimulus-response estimate Ŝ is to misspecification of the dynamics model f̂ would strengthen the paper. Errors in f̂ propagate into the residual used to train Ŝ (line 48), and this coupling is not explored.
- A discussion of how the kernel regression (Equation 7) scales with the number of observed stimulations (O(N_obs) per timepoint) would be useful, since this could eventually exceed the real-time budget.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- **Open-loop baseline absent** (Harsh Critic §3): Figure 5 explicitly includes an open-loop (identity) comparison. The criticism was factually wrong and is removed.
- **sjPCA convergence not evidence of practical value** (Harsh Critic §4): The paper only claims sjPCA provides a stable streaming approximation to offline jPCA (line 68: "demonstrate that all algorithms are stable approximations"), not that it is superior. This criticism attacks a claim the paper does not make and is removed.
- **Only KF used in main results** (Section-by-Section Notes): The appendix (which would contain cross-model comparisons) is stripped by the parser; the paper states the full comparison is in Appendix C. This criticism cannot be verified and is removed.
- **Missing appendix content / formatting nitpicks / missing related works**: Removed per hard rules.
- **Core claim "invalidation" downgraded from Fatal**: The simulated-stimulation issue is real but does not invalidate the entire paper — the toy model validates the framework with known ground truth, the real-data experiments test the computational pipeline on real neural statistics, and the paper acknowledges the limitation. It remains a Major weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. The most impactful revision would be to validate the framework with real stimulation data — even a single controlled experiment (e.g., a well-characterized neural preparation where stimulations are delivered and responses measured) would transform the evidence base. Barring that, the claims should be sharply reframed: the paper presents a computationally validated proof-of-concept, not a validated method for real stimulation design.

2. Correct the optimization formulation in Equation (8) to actually enforce sparsity (e.g., minimize ‖u‖₁ directly or use a hard cardinality constraint).

3. Add at least one meaningful baseline from the prior work cited in the introduction (e.g., Bayesian optimization or active learning), and include error bars/confidence intervals for all main quantitative claims.

## Score and Decision

Based on calibration against the human-review corpus, my round-1 bracket was 3.5–5.0. Round 2 narrowed this to approximately 4.0. The most directly comparable anchor papers are:

| Anchor Paper | Avg Score | Comparison |
|---|---|---|
| iSSM (FwW3jqchtY) | 5.0 (Reject) | Addresses neural dynamics under perturbations with real stimulation data — our paper has a more complete design pipeline but lacks real stimulation validation |
| BRAID (3usdM1AuI3) | 6.25 (Accept) | Models input-driven neural dynamics with real data — more comprehensive evaluation than our paper |
| Closed-loop EEG (4ltiMYgJo9) | 5.75 (Reject) | Similar offline evaluation gap — claimed closed-loop but didn't demonstrate it |
| Real-time inference (eR1119aUlL) | 4.25 (Reject) | Real-time neural modeling with comparable evaluation gap |

Our paper sits below the iSSM paper (which had real stimulation data) and above papers with more severe structural flaws. The genuine technical contributions are undermined by the absence of real stimulation validation and weak baselines.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>