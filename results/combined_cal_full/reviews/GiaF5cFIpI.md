Now I have strong calibration. Let me compile the final review.

All anchor papers referenced:

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| iSSM | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FwW3jqchtY.md | 5.00 | 1,2 | Yes | Same topic (neural dynamics under causal perturbations). Our paper has weaker strengths (+4.27 vs +5.76) but a less severe fatal weakness (-9.40 vs -11.74). Comparable overall. |
| BRAID | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3usdM1AuI3.md | 6.25 | 1 | Yes | Better evaluation with extensive baselines and ablations (+5.43 for comparison strength). Our paper is weaker on empirical validation. |
| Closed-loop EEG | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4ltiMYgJo9.md | 5.75 | 1,2 | Yes | Also closed-loop stimulation framework. Has similar validation gaps (-11.88), but our paper is better structured. |
| MR-SDS | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/WQwV7Y8qwa.md | 5.80 | 2 | No | Neural dynamics modeling with more comprehensive evaluation. Our paper has a more ambitious stimulation-design component. |
| FCCA | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4AlNpszv66.md | 4.75 | 2 | No | Different topic (controllability subspaces). Slightly higher than our estimated score. |
| Neural Manifold Regularization | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TVnkjz4MqV.md | 5.50 | 2 | No | Similar topic (latent dynamics for behavior). More comprehensive evaluation. |
| Stabilized Neural Dynamics | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LNp7KW33Cg.md | 5.00 | 1 | No | Domain adaptation for neural dynamics. Comparable score range. |

Round 1 bracket: Between 4.0 and 6.0. Our draft's strengths weigh (+4.27, +4.00, +3.46, +2.57) and weaknesses weigh (-9.40, -7.06, -6.15, -3.54, -1.59). Compared to iSSM (score 5.00), which has a fatal flaw at -11.74 but stronger positives at +5.24 and +5.76, our paper has less severe negative weights but also weaker positive weights. Compared to BRAID (6.25), our paper lacks the comprehensive evaluation and baselines that BRAID's strengths highlight (+5.43 for comparisons/ablations). The missing-baselines weakness (-9.40) is the single heaviest item pulling the score down, and no strength fully compensates for it. Narrowing to **4.5**.

---

## Summary

This paper proposes an end-to-end framework for real-time adaptive stimulation of latent neural dynamics. The method integrates streaming latent space construction (including a novel sjPCA method), kernel regression-based stimulus-response mapping, and constrained optimization to design high-dimensional stimulation patterns that perturb low-dimensional latent dynamics in desired directions. The authors demonstrate the pipeline on simulated data and real neural recordings (calcium imaging and electrophysiology) with synthetically added stimulation effects, and report runtimes under 10 ms average and 100 ms worst-case.

## Strengths

- **Ambitious, practically motivated end-to-end framework.** The integration of streaming latent space → dynamical model → stimulus-response mapping → constrained optimization addresses a genuine open problem in systems neuroscience: how to design high-dimensional optogenetic stimulations to causally test hypotheses about low-dimensional latent dynamics.
- **Credible real-time feasibility evidence.** Runtime benchmarks (<10 ms average, <100 ms worst-case) convincingly demonstrate that the computational pipeline could keep pace with real-time neural data acquisition (30 Hz electrophysiology, 15 Hz calcium imaging).
- **Acknowledgment of practical challenges.** The paper identifies and handles non-stationarity in the stimulus-response mapping (jump discontinuities, continuous drift), response delays, and experimental feasibility constraints (non-negativity, sparsity), reflecting genuine engagement with experimental reality.
- **Parallel comparison of multiple latent space representations.** The framework compares sjPCA, proSVD, and mmICA alongside multiple dynamical models (KF, VJF, Bubblewrap), enabling adaptive selection of the best-performing model at any timepoint.

## Weaknesses

### Fatal
None.

### Major
- **No comparison against existing stimulation-design methods.** The paper cites specific prior work on stimulation design (Minai et al., 2024; Wagenmaker et al., 2024; Yang et al., 2021; Draelos & Pearson, 2020) in the Introduction and describes how they address parts of the problem, yet never compares the proposed method against any of them. The only baselines are a "blind" model that ignores stimulation entirely and random stimulation patterns. This cannot substantiate the claim of methodological advance over existing approaches and is the most significant weakness.
- **The sjPCA "novel streaming method" is underspecified and insufficiently validated.** It is described in roughly one paragraph (lines 70–83) with no formal derivation, convergence analysis, or ablation isolating its contribution over simply running proSVD + batch jPCA. Figure 1a tests sjPCA, proSVD, and mmICA on different synthetic data with different error metrics, making cross-method comparison impossible. The added value of the Orthogonal Procrustes stabilization step (Eq. 2) is not justified or ablated.
- **Unaddressed curse of dimensionality in the kernel regression.** The kernel K₂(u, U_i) in Equation (7) operates directly on the high-dimensional stimulation vector u (N = 130 or 592 neurons). With only 10–20 stimulation samples (as claimed in the abstract), a Nadaraya-Watson estimator in hundreds of dimensions will generalize poorly. The paper does not discuss this issue, does not report the number of stimulation samples used in real-data experiments, and does not validate that the learned Ŝ generalizes to unseen stimulation patterns.

### Minor
- **Evaluation on real data uses simulated stimulation effects, not actual neural responses to delivered stimulation.** The paper is transparent about this (lines 178, 252, 258–259), and the core algorithmic contributions are not invalidated. However, the framing in the abstract ("demonstrate our approach on both simulated and real neural data") and claims about "adaptive stimulation of latent neural activity" could give the impression that the method was validated with real stimulations. A method that learns from real stimulations may face qualitatively different challenges than those captured by the synthetic additive model.
- **No ablation studies.** The framework has multiple interacting components (streaming latent space, dynamical model, kernel regression for Ŝ, optimization), yet no component is removed or replaced to assess its contribution. For example: replacing kernel regression with linear regression, using fixed vs. streaming latent spaces, or comparing sjPCA against proSVD on the same data with the same metric.
- **Unresolved notation and hyperparameter issues in the optimization.** The term ‖u‖₀^{max} in Equation (8) is not defined. The regularization parameter λ₁ is not discussed (how it was chosen, sensitivity of results to its value). The objective combines a bounded term (cosine similarity ∈ [-1,1]) with an unbounded penalty, making the tradeoff scale-dependent without principled normalization.
- **The interaction between streaming latent space updates and stored stimulus-response pairs is not addressed.** The latent space Q is updated online (Algorithm 1, line 7), meaning the basis in which latent states and responses are expressed changes over time. Stimulus-response pairs stored in the kernel regression history were observed under a previous basis, and the paper does not discuss how this drift is handled.

### Trivial
None.

## Nice-to-Haves

- Compare against at least one existing stimulation-design method (e.g., Bayesian optimization as in Minai et al., 2024) rather than only blind/random baselines.
- Add ablation studies isolating each component: replace kernel regression with linear regression, use fixed vs. streaming latent spaces, compare sjPCA against proSVD on the same data and metric.
- Analyze or mitigate the curse of dimensionality in the kernel regression, e.g., via dimensionality reduction on u, structured kernels, or demonstrating that it outperforms a simple linear model.
- Report confidence intervals and statistical tests for key claims (e.g., "learns within 10-20 stimulations," "recovery within 15s").
- Discuss sensitivity of results to key hyperparameters (λ₁, kernel bandwidths, delay d).

## Removed Points

These points from the harsh critic review were removed or downgraded during filtering:

1. **"The paper does not demonstrate adaptive stimulation of real neural dynamics"** — Retained as Minor (not Fatal) since the paper is transparent about this limitation. The abstract accurately says "real neural data" (the recordings are real), and the Discussion explicitly acknowledges the limitation and states experiments were performed offline. The core contribution is algorithmic, not a wet-lab validation.
2. **"mmICA is not a dimensionality reduction method"** — Removed. The paper accurately describes mmICA as constructing latent spaces and acknowledges the two-stage procedure (proSVD reduction followed by mmICA).
3. **"Toy model S function is discontinuous / all-or-nothing"** — Removed. The toy model is only a simple demonstration; the continuous stimulation space is tested in the real-data experiments. This criticism nitpicks a testbed rather than engaging with the method.
4. **"Line 170 appears mid-paragraph like a copy-paste error"** — Removed as a formatting nitpick.
5. **"One pending stimulus at a time is restrictive"** — Removed. This is an explicit simplifying assumption stated by the authors; asking for more generality scope-creeps beyond what the paper claims.

## Novel Insights

None beyond the paper's own contributions. The review surfaces the key patterns: the paper identifies an important problem and proposes a reasonable decomposition, but the evaluation is substantially weaker than what would be needed to support the claimed contributions.

## Suggestions

The highest-leverage improvement would be to compare against at least one existing stimulation-design method (Bayesian optimization (Minai et al., 2024) or active learning (Wagenmaker et al., 2024) are natural choices) rather than only blind and random baselines. The sjPCA contribution should either be rigorously validated against proSVD + batch jPCA on the same data with the same metric, or the novelty claim should be tempered. The kernel regression's behavior in high dimensions with few samples should be explicitly analyzed — perhaps with dimensionality reduction on u, structured/product kernels, or a demonstration that it meaningfully outperforms a simple linear model. These three issues (baselines, sjPCA validation, curse of dimensionality) are the ones that most limit the paper's contribution claim.

## Score and Decision

**MY FINAL SCORE:** <score>4.5</score>
**MY FINAL DECISION:** <decision>Reject</decision>