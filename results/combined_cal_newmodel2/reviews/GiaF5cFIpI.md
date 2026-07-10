Now let me synthesize everything into the final review.

**Round 1 bracket:** Based on calibration against the anchors, the narrowest plausible score range for this paper is between 4.0 and 5.5. The paper is clearly stronger in contribution novelty and framework design than MRINE (avg 4.25) and comparable to iSSM (avg 5.00) but with more evaluation gaps.

**Final anchoring:** My draft's top strengths (favorability 15.35, 13.72) compare favorably with iSSM's top strengths (15.29, 14.15) and BRAID's (15.33, 13.21). However, my most negative weakness (baselines, favorability -5.08) is more severe than iSSM's comparable "no comparisons" weakness (-2.83). Unlike iSSM, which validated on real perturbation data and provided a theoretical identifiability proof, this paper's evaluation relies on synthetic stimulation effects on real data and does not test the high-dimensional optimization regime. The paper also lacks comparison against any of the prior methods it cites. These gaps place it below iSSM's average of 5.00.

**All anchor papers retrieved:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| u1cQYxRI1H.md | 0.50 | R1 | No | Unrelated topic (diffusion illumination) |
| nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated (financial markets) |
| gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated (Chinese NLP for robots) |
| P49gSPmrvN.md | 1.00 | R1 | No | Unrelated (UMAP for discourse) |
| BBldjKEBlJ.md | 3.00 | R1 | No | Neural activity forecasting - weaker than this paper |
| NPzuN3Rxi8.md | 3.00 | R1 | No | TAVRNN - weaker evaluation than this paper |
| nwDRD4AMoN.md | 3.00 | R1 | No | Artificial Kuramoto neurons (score 9.00, different topic) |
| A5utJ4xf27.md | 2.33 | R1 | No | Brain-based object localization |
| eR1119aUlL.md | 4.25 | R1,R2 | Yes | Real-time latent dynamics - weaker contribution, stronger eval |
| 4AlNpszv66.md | 4.75 | R1 | No | Neural controllability |
| LNp7KW33Cg.md | 5.00 | R1,R2 | No | Neural dynamics decoding |
| 0CvJYiOo2b.md | 4.50 | R1 | No | PCA time series |
| 4ltiMYgJo9.md | 5.75 | R1,R2 | No | Closed-loop EEG - similar topic but different modality |
| UvfI4grcM7.md | 6.75 | R1 | No | Barrel cortex model |
| MFCjgEOLJT.md | 5.75 | R1 | No | Control inputs locomotion |
| 3usdM1AuI3.md | 6.25 | R1 | Yes | BRAID - stronger evaluation and baselines |
| kbjJ9ZOakb.md | 8.00 | R1 | No | Neural invariance manifolds (top-tier paper) |
| cNmu0hZ4CL.md | 8.00 | R1 | No | Comparing neural dynamics (top-tier paper) |
| Xo0Q1N7CGk.md | 8.00 | R1 | No | Grid cells (top-tier paper) |
| RWJX5F5I9g.md | 8.00 | R1 | No | Brain Bandit (top-tier paper) |
| FwW3jqchtY.md | 5.00 | R2 | Yes | iSSM - most similar; stronger theory and real perturbations |
| wCUw8t63vH.md | 6.80 | R2 | No | Spectral learning of shared dynamics |
| TVnkjz4MqV.md | 5.50 | R2 | No | Neural Manifold Regularization |
| N83O2FcqzN.md | 5.00 | R3 | Yes | TiDeSPL-VAE - neural latent model, better baselines |
| WQwV7Y8qwa.md | 5.80 | R2 | No | Switching nonlinear dynamical systems |

**Final score placement:** The paper sits between iSSM (5.00) and MRINE (4.25). It has a stronger architecture and clearer motivation than MRINE, but weaker evaluation than iSSM (which tested on real perturbations and had a theoretical proof). The favorability comparison confirms: my top strengths are on par with 5.0-level papers, but my most damaging weakness (baselines, -5.08) is more severe than comparable weaknesses in the 5.0 anchors. Score: 4.5.

---

## Summary

This paper presents a modular framework for closed-loop latent-space neural stimulation that integrates streaming dimensionality reduction (including a novel sjPCA method), kernel-regression-based stimulus-response modeling with temporal discounting, and constrained optimization to select high-dimensional stimulation patterns. The framework is demonstrated on a toy model and on real neural recordings (calcium imaging and electrophysiology) where stimulation effects are synthetically added via an AR(1) process.

## Strengths

- **Modular and sensible architecture.** The separation into streaming latent space construction, dynamical modeling, a nonparametric stimulus-response estimator, and a constrained stimulation optimizer (Algorithm 1) is well-designed and allows independent development and testing of each component. The use of kernel regression with temporal discounting (Eq. 7) is a pragmatic design choice for handling non-stationarity.

- **Impressive computational speed.** End-to-end runtimes under 10 ms on average and below 100 ms (lines 23, 154) are a meaningful engineering achievement that clears the bar for real-time closed-loop neuroscience applications.

- **Parallel comparison of latent representations.** The framework provides a principled way to compare multiple latent space representations (sjPCA, proSVD, mmICA) and dynamical models in parallel (Figure 1c, lines 98–108), enabling adaptive selection based on predictive performance.

## Weaknesses

### Fatal

None.

### Major

- **Real neural data experiments use synthetic stimulation effects, not real stimulations.** The "real neural data" experiments (lines 177–178) add an AR(1) autoregressive process to pre-recorded neural traces to simulate stimulation responses. This sidesteps the biological complexities (nonlinear network interactions, off-target effects, opsin heterogeneity, state-dependent responses) that the paper's own motivation (lines 17, 21, 112) identifies as critical challenges. While the Discussion (lines 258–259) acknowledges this limitation, the abstract's claim of demonstrating "on both simulated and real neural data" is misleading without the qualification that stimulation effects on real data are synthetic. The paper's evaluation does not test the method against the hardest parts of the problem it sets out to solve.

- **High-dimensional stimulation optimization is not tested in a challenging regime.** The paper motivates its optimization framework by targeting the combinatorial challenge of selecting from >10^45 stimulation combinations (line 13). However, the toy model uses binary stimulation with a 1D effect (Eq. 9), and the real-data experiments use a simple AR(1) additive response model (line 178) that is linear and known. Neither setting tests the regime where the optimization across high-dimensional u with complex, nonlinear response mappings is necessary or beneficial. The method may work for this regime, but no experiment in the paper demonstrates it.

- **Baseline comparisons are too weak to establish state-of-the-art value.** The method is compared only against a "blind" model that ignores stimulation (Fig. 2e) and random/shuffled stimulation strategies (Fig. 4a). The paper cites directly relevant prior methods — active learning for stimulation design (Wagenmaker et al., 2024), Bayesian optimization (Minai et al., 2024), input-output dynamical modeling (Yang et al., 2021), and uncertainty-based design (Draelos & Pearson, 2020) — but does not compare against any of them. The current baselines establish only that the method is better than nothing, not that it advances the state of the art.

### Minor

- **Sparsity penalty formulation in Eq. (8) does not match its described purpose.** The term `λ_1 (||u||_0^{max} − ||u||_1)` is described as encouraging a solution with a specific number of non-zero elements (line 148). However, for continuous u ∈ [0,1]^N, this term is minimized when ||u||_1 is maximized, which encourages dense, high-magnitude stimulation rather than sparsity. A standard L1 sparsity penalty would use +λ||u||_1. The mathematical form of this term does not produce the behavior the text claims.

- **Adaptive latent representation selection is described but not demonstrated.** The abstract and methods (lines 98–108) describe the ability to switch between latent representations based on predictive performance, but no experiment demonstrates the system actually switching or selecting stimulations to discriminate between latent subspace hypotheses.

- **Limited statistical reporting on key quantitative claims.** Several claims (e.g., "learn within 10–20 stimulations," "517/600 optimizations < 1°") are presented without confidence intervals or discussion of variance across conditions.

### Trivial

None.

## Nice-to-Haves

- Compare against at least one relevant prior method (e.g., Bayesian optimization or active learning for stimulation design) to demonstrate that the proposed approach advances beyond existing work.
- Test on a simulated neural population model (e.g., a trained RNN) with nonlinear, state-dependent, interactive response structure to demonstrate the high-dimensional optimization regime.
- Clarify or correct the sparsity penalty formulation in Equation (8).

## Removed Points

These points are flagged to be removed, treat them with caution:

- "Novel sjPCA method described only briefly" — presentation note, not a substantive weakness.
- Various section-by-section editorial observations about the toy model — subsumed under the high-dimensional testing weakness.
- The critic's framing of the synthetic stimulation issue as "fatal" or "invalidates central claim" — downgraded to Major because the paper is transparent about this limitation and does not claim a real closed-loop experiment was performed. The approach's components (streaming latent space, kernel regression estimator, optimization) are validated individually.
- Strength "The problem is well-motivated and timely" — generic; dropped.
- Suggestions for "realistic simulated neural model or actual closed-loop experiment" — moved to Nice-to-Haves.
- "Strengthening the Paper on Its Own Terms" content — moved to Nice-to-Haves/Suggestions.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's review identifies real evaluation gaps but does not contribute observations beyond what a careful reading of the paper's own discussion of its limitations would surface.

## Suggestions

1. Add comparisons against at least one prior stimulation design method (e.g., Bayesian optimization or active learning) to substantiate the claim of advancing the state of the art.
2. Test the optimization on a setting with genuinely nonlinear, interactive stimulus-response mappings (e.g., a trained RNN where stimulation has network-mediated effects) to validate the high-dimensional search capability.
3. Clarify or correct the sparsity penalty term in Equation (8) so its mathematical effect matches the text's description.
4. Either add a demonstration of adaptive representation switching, or remove or qualify that claim in the abstract.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>