I've done my analysis and calibration. Let me now write the final review.

## Summary

The paper proposes a streaming framework for closed-loop design of high-dimensional neural stimulations that target specific directions in a low-dimensional latent space of neural dynamics. It combines streaming latent space estimation (including a novel streaming jPCA method via Orthogonal Procrustes stabilization), a nonparametric kernel regression model for learning stimulus-response mappings, and a constrained optimization problem (L1-sparsity + box constraints on cosine alignment) that designs stimulation patterns to drive latent dynamics in desired directions. Validated on a toy model and on real neural recordings (calcium imaging, electrophysiology) with simulated AR-process stimulations, with runtime benchmarks showing sub-100ms loop times.

## Strengths

1. **Well-motivated and practically relevant problem.** The paper targets a genuine gap: neuroscientists who want to causally test latent-space hypotheses (e.g., ring attractors, rotational dynamics) need methods to design high-dimensional stimulations that produce targeted low-dimensional perturbations in real time. No existing framework addresses all components together.

2. **Clean modular pipeline design.** The separation into streaming latent estimation, nonparametric stimulus-response modeling, and constrained optimization is well structured, and components can be swapped independently (demonstrated with multiple latent space methods and dynamical models).

3. **Runtime validation is credible and meaningful.** Sub-10ms average and sub-100ms worst-case computation times are demonstrated on realistic hardware (lines 154-155), meeting a hard requirement for real-time in vivo optogenetics.

4. **Nonstationarity handling via time-dependent kernels.** The use of a temporal kernel to down-weight old observations, with demonstrated recovery from a 180° flip and continuous drift (Figure 2e), is a thoughtful design choice that addresses a genuine experimental concern. This is one of the paper's more substantive contributions.

## Weaknesses

### Fatal
None.

### Major

1. **The "real data" experiments use simulated stimulations, creating an evidential gap between framing and validation.** The paper states (lines 178-179): "For each of the real datasets, we simulated stimulations using an autoregressive function… y_t = r_t + a_t, a_t = 0.8·a_{t-1} + u_t." No actual optogenetic or electrical stimulation was delivered; the "response" is a hand-designed AR(1) overlay. The abstract says "We demonstrate our approach on both simulated and real neural data" — technically true, but the reader could easily infer that real stimulation experiments were conducted. The paper's framing emphasizes enabling "future in vivo applications" (which is appropriate as a forward-looking claim), but the experimental section does not adequately qualify that the stimulation effects on real data are entirely synthetic. The AR(1) model is a gross simplification of biological optogenetic responses (nonlinearities, cell-type specificity, network effects, opsin-expression variability). The authors acknowledge this in the Discussion (lines 258-259: "our real data experiments were performed offline"), but this acknowledgment is insufficiently prominent relative to the claims in the abstract. The core methodology remains sound, but the validation does not rise to the level suggested by the presentation.

2. **The optimization validation compares only against trivial random baselines.** Section 4.2 compares the method against stimulating random individual neurons, random groups, and shuffled versions of the method's own stimuli. The paper states this shows the method "outperforms random methods" — which is a minimal bar. No comparison against any structured alternative (e.g., Bayesian optimization over stimuli, which is cited as prior work in Minai et al. 2024; greedy selection based on neuron tuning; or a simple linear least-squares solution) is provided. Without such comparisons, the reader cannot assess whether the specific design choices (kernel-regression-based S_hat, L1-regularized cosine alignment objective) add value over simpler alternatives.

3. **Several claimed contributions receive only thin validation.** The streaming jPCA (sjPCA) and the parallel comparison of latent representations are listed as contributions in the abstract (line 9), but their validation is minimal. sjPCA convergence is shown in a single panel (Figure 1a) demonstrating agreement with offline jPCA — which is expected behavior for a correctly implemented online version. The streaming estimator for comparing latent representations (Figure 1c) is presented only as a qualitative heatmap with no quantitative evaluation of its accuracy or utility relative to an oracle or ground truth.

### Minor

4. **Ambiguity about which data produced which results in Section 4.2.** The optimization experiments (Figures 4–5) involve comparing predicted vs. observed stimulation effects. The paper states (lines 226–228) that some experiments "assumed that the result of a stimulation u was simply its projection into the latent space S(u) = Q^T u," but it is not always clear whether the figures come from the toy model, the real data with simulated AR stimulations, or a separate synthetic setup. Explicit dataset labels for each figure panel would improve clarity.

5. **Algorithm 1 has a subtle design limitation with dynamics model staleness.** When stimulations are delivered (lines 46–48), the dynamics model f is not updated (line 13/50 is skipped). The paper explains this design choice (lines 118–121: training f only on non-stimulation timepoints), but does not discuss sensitivity to stimulation frequency or density. If stimulations occur frequently, f could become stale, degrading the computation of s_obs = x_t - x_hat_t.

6. **The kernel regression estimator's computational cost grows linearly with observed stimulations.** The paper reports sub-100ms runtimes tested with ~10–20 stimulations (abstract). For longer experiments with hundreds of stimulations, the cost of evaluating all stored stimulus-response pairs would increase. The paper does not discuss this scaling behavior or potential mitigations.

7. **The confirmation that "stimulations had the intended effect" on real data is circular.** On the real data with simulated AR stimulations (line 188), the "intended effect" (pushing activity along Q0 in the latent space) is built into the construction y_t = r_t + a_t where a_t = 0.8·a_{t-1} + u_t and u is designed to push along Q0. Observing movement along Q0 in the latent projection is then expected by construction, not an independent validation.

### Trivial
None.

## Nice-to-Haves

- Compare optimization against at least one structured alternative baseline (e.g., Bayesian optimization, greedy selection, or linear least-squares) to demonstrate that the specific design choices matter.
- Include a simulation study with a nonlinear, realistic model of optogenetic responses (as opposed to the AR(1) model) to test robustness to realistic nonlinearities.
- Add a sensitivity analysis for how performance degrades when S_hat and f are jointly uncertain or when stimulation frequency increases.
- Discuss exploration vs. exploitation: the method purely exploits the current S_hat; deliberate exploratory stimulations to improve S_hat in uncertain regions would be a useful extension.
- Provide explicit dataset labels for each figure panel and a table mapping experiments to data sources.
- Quantitatively evaluate the streaming representation comparator against an oracle baseline.

## Removed Points

- **"Kernel hyperparameters not specified"**: Removed — the appendix (where these would be detailed) was stripped by the parser; the original submission contains this information.
- **"Missing appendix, proofs, or references"**: Removed — the parser strips these sections from all papers; they exist in the original submission.
- **"The infeasible directions analysis does not belong primarily in Results"**: Removed — showing sanity checks of the optimization formulation is a standard part of results sections.
- **"Nonlinear latent spaces limitation treated too casually"**: Removed — the paper clearly scopes itself to linear latent spaces and acknowledges this as a limitation (lines 255-257); requesting a full nonlinear treatment is scope creep.
- **"Missing related works"**: Removed — I cannot independently verify the existence of missing citations.
- **"Runtime benchmarking not fully specified"**: Removed — hardware specs are provided (lines 154-155), and the stimulation counts (~10-20) and dimensionality context are stated. This is adequate for the level of detail expected.
- **"The paper's methodological novelty is modest" (as a standalone weakness)**: Integrated into Weakness #3 with specific evidence (thin validation of specific components). The general claim that the paper "combines existing techniques" is both true and not inherently a weakness — integration for a specific application is a valid contribution mode.
- **Formatting/presentation nitpicks**: Removed as parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Narrow the central claim to match the evidence.** Either replace the "real data with simulated stimulations" experiments with a simulation study using more realistic nonlinear response dynamics, or prominently state in the abstract and introduction that the real-data validation tests data-integration and streaming compatibility, not closed-loop stimulation efficacy.

2. **Add a nontrivial optimization baseline.** Even a simple baseline (linear least-squares under an identity mapping, or Bayesian optimization as cited in prior work) would substantially strengthen the claim that the kernel regression + L1 formulation provides meaningful benefit.

3. **Provide quantitative evaluation of the streaming representation comparator.** If this is a contribution, back it with numbers (e.g., agreement with an oracle or offline comparison).

4. **State clearly which dataset produced each figure** in the figure captions or in a dedicated table.

## Score and Decision

**Calibration anchors retrieved (all rounds):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FwW3jqchtY.md` — avg 5.00, Round 1 (itemized). "Identifying neural dynamics using interventional state space models." Closest topical match; had a genuine fatal theoretical flaw (Assumption 3.4 requiring separate interventions on each latent dimension). Our paper has no such fatal flaw and is slightly stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4ltiMYgJo9.md` — avg 5.75, Round 1 (itemized). "A closed-loop EEG-based visual stimulation framework." Similar evidential gap (no real closed-loop demonstration) but additional presentation issues. Our paper is cleaner but has a similar validation limitation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4AlNpszv66.md` — avg 4.75, Round 1 (itemized). "Identifying Feedforward and Feedback Controllable Subspaces." Significant presentation issues and lack of validation. Our paper is stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eR1119aUlL.md` — avg 4.25, Round 1 (itemized). "Dynamical modeling for real-time inference of nonlinear latent factors." Novelty issues and limited experiments. Our paper is stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BBldjKEBlJ.md` — avg 3.00, Round 1 (itemized). "QuantFormer: Learning to quantize for neural activity forecasting." Major confounds in evaluation. Our paper is clearly stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LNp7KW33Cg.md` — avg 5.00, Round 2 (itemized). "Stabilized Neural Dynamics for Behavioral Decoding." Extensive experiments but methodological concerns. Comparable quality.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3usdM1AuI3.md` — avg 6.25, Round 2 (itemized). "BRAID: Input-driven Nonlinear Dynamical Modeling." More comprehensive evaluation and baselines. Our paper is weaker.

**Bracket and narrowing:** Round 1 bracket was 3.5–5.5 based on topical similarity to FwW3jqchtY (5.00) and eR1119aUlL (4.25). Round 2 narrowed using closed-loop stimulation queries, comparing against 4ltiMYgJo9 (5.75) and 3usdM1AuI3 (6.25). Our paper shares key heavy-weight weaknesses with FwW3jqchtY (evidential gap between framing and experiments: weight -4) and 4ltiMYgJo9 (no real closed-loop demonstration: weight -4), but avoids the fatal theoretical flaw of FwW3jqchtY (weight -5). Our paper also lacks the comprehensive baselines and ablations of 3usdM1AuI3 (weight +2/+3 for baselines). The paper's strongest shared heavy-weight strengths are problem importance (comparable to +4 in FwW3jqchtY) and clear pipeline design. This places it between 5.00 and 5.75, consistent with a 5.5 score.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>