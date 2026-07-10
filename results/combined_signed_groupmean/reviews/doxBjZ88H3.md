## Summary

This paper presents an information-theoretic framework for designing experiments that can distinguish whether early sensory neural populations encode likelihood functions or posterior distributions — a key open question in computational neuroscience. The authors derive a quantity called the "information gap" (the expected decoder performance difference between matched and mismatched probabilistic content, expressed as a KL divergence), analytically compute Bayes-optimal estimators for mismatched decoding (Eqs. 1–5), validate via simulations that DNN decoders converge to these theoretical limits, and produce information gap landscapes (Figs. 5–6) that identify optimal task parameters for discriminating the two coding hypotheses. An analysis of the Allen Brain Visual Coding dataset confirms the null prediction that single-context designs cannot adjudicate the hypotheses.

## Strengths

- **The "information gap" concept is theoretically principled and the derivations are nontrivial.** Defining the expected performance difference as a KL divergence between the true posterior and a task-marginalized surrogate posterior (Eqs. 1 and 3) is a clean theoretical move. The derivation of Bayes-optimal estimators for the mismatched decoding cases — particularly the fixed-point equation in Eq. 5 for the likelihood decoder on posterior-coding populations — constitutes a genuine theoretical contribution that goes beyond heuristic framing.

- **The information gap landscapes (Figs. 5 and 6) provide concrete, non-obvious guidance for experimental design.** The findings that optimal task parameters differ between the two hypotheses, that low contrast expands the high-gap region, and that heavy-tailed priors are ineffective for distinguishing posterior-coding populations are all actionable conclusions that follow from the theory. These landscapes give practicing experimentalists specific parameter recommendations.

- **The paper correctly identifies and formalizes the core experimental challenge.** The framing (Section 2) of the trade-off between needing sufficient prior differences to generate distinguishable population responses while maintaining adequate stimulus overlap for meaningful comparisons across contexts is precise and well-motivated. This gives the work a clear rationale.

## Weaknesses

### Major

- **Limited scope of simulation validation.** The simulations construct populations that exactly instantiate the assumed coding schemes (Poisson neurons with tuning curves encoding likelihoods or posteriors). While the convergence of DNN decoders (which are not guaranteed to be optimal with finite data) to the theoretical limit is a meaningful consistency check, the validation never tests scenarios where the neural encoding deviates from these idealized assumptions — e.g., noise correlations, saturation nonlinearities, or other biologically realistic features. The gain-modulated Poisson model (Goris et al., 2014) stays within the same mathematical family. This limits the evidence that the information gap would predict decoder performance in real neural populations whose encoding is unknown and likely more complex.

- **The paper never demonstrates that following the optimized designs actually enables successful hypothesis discrimination.** The information gap landscapes are computed from theory and "sweet spots" are identified (Figs. 5–6), but there is no test — even in simulation — that applies an optimized design, generates multi-context data, runs the decoder-based analysis, and shows the correct hypothesis is reliably identified. Without this closed-loop demonstration, the central claim that maximizing the information gap "yields stimulus distributions that optimally differentiate likelihood and posterior coding hypotheses" (abstract) remains a theoretical promise rather than an empirically supported conclusion. Adding even a single synthetic experiment that closes this loop would substantially strengthen the paper.

### Minor

- **No sensitivity analysis for discretization.** The posterior-coding information gap depends on observation pairs satisfying exact equality of posteriors across contexts (Eq. 4). Observations are discretized to make this tractable, but no analysis is provided of how sensitive the predicted gap is to discretization granularity or whether the fixed-point iteration (Eq. 5) converges reliably across the parameter space. Given the posterior-coding gap is already an order of magnitude smaller than the likelihood-coding gap, this is a practically relevant concern for experimentalists relying on these predictions.

- **The empirical demonstration (Section 5, Fig. 7) only confirms the null case.** Showing zero information gap under a single context with uniform prior — which the theory trivially predicts — confirms the null case but provides no positive evidence that the framework's optimized designs would discriminate the hypotheses. The paper frames this honestly as demonstrating why single-context designs are insufficient, but a simulated placebo test (e.g., subsampling the Allen data to emulate two contexts and applying the optimized design) would have strengthened the evidential base considerably.

### Trivial

- None.

## Nice-to-Haves

- Translating the information gap (in nats) into statistical power or sample size requirements would substantially increase practical utility for experimentalists planning studies.
- A sensitivity analysis exploring how misspecification of the generative model \(p(x|\theta)\) affects the optimized designs would strengthen practical guidance.

## Removed Points

These points are flagged to be removed, treat them with caution:

- *"Simulation validation is circular"* — Overstated; the DNN decoders are not guaranteed to be optimal with finite data, so the convergence is non-trivial. However, the limited validation scope is retained as a Major weakness.
- *"Notation inconsistency on line 125"* — Removed per formatting/typo rule; this is a trivial notation issue that does not affect scientific content.
- *"Connection between x and r handled loosely"* — This is a standard modeling assumption in the field, not a weakness.
- *"Claim about existing work overstated"* — The paper's claim is appropriately qualified; removed.
- *"Scales differ by an order of magnitude"* — The paper already discusses this asymmetry and its implications; removed.
- *"Optimization limited to two parameters"* — Scope creep; the paper presents a framework, not an exhaustive optimization.
- *"Framework optimizes for wrong target (statistical power)"* — Moved to Nice-to-Haves; this is additional work beyond the paper's stated scope.
- *"Missing practical limitation about known generative model"* — The paper acknowledges this in Section 6; moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions — the reviews do not surface observations that the paper itself does not already contain.

## Suggestions

- **Add a closed-loop simulation experiment:** Apply an optimized design from the landscapes to a synthetic multi-context population with known ground truth, run the decoder analysis, and report whether the correct coding hypothesis is reliably identified. This single experiment would substantially close the evidential gap.
- **Provide a discretization sensitivity analysis:** Report how bin width affects the posterior-coding information gap and whether the fixed-point iteration (Eq. 5) converges reliably across the parameter space.
- **Validate on a non-idealized neural encoding model:** Test whether the information gap predicts decoder performance when the population encoding includes noise correlations, response nonlinearities, or other features not captured by the Poisson-plus-tuning-curve model.

## Score and Decision

**Calibration summary:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| cNmu0hZ4CL (OT neural dynamics) | 8.00 | R1 | Yes | Stronger paper: better presentation, more comprehensive synthetic experiments, clear demonstration of advantage over baselines |
| RWJX5F5I9g (Brain Bandit) | 8.00 | R2 | Yes | Stronger paper: theory + simulation + comparison with real behavioral data, closed-loop validation |
| h8yg0hT96f (BOED diffusions) | 7.33 | R2 | Yes | Stronger paper: clear quantitative improvement over baselines, more thorough empirical validation |
| zxO4WuVGns (Inverse decision-making) | 6.00 | R2 | Yes | **Closest anchor:** similar strengths (novel method for neuroscience, synthetic+real data, clear writing) and weaknesses (limited validation scope, no comparative baselines) |
| 4ltiMYgJo9 (Closed-loop EEG) | 5.75 | R1 | Yes | Similar weaknesses (framework proposed but validation incomplete) but less rigorous theory |
| SyPrLti4PG (Few-shot neural latents) | 5.67 | R1 | Yes | Similar style paper, similar validation gaps |
| 4GfEOQlBoc (Image statistics & perception) | 5.25 | R1 | Yes | Weaker: conceptual issues about what was being tested |
| MNGMpHxi1I (Info-theoretic uncertainty) | 3.00 | R1 | Yes | Weaker: serious novelty and conceptual issues |
| gwZ90hFSL2 (Cross-lingual robots) | 1.00 | R1 | No | Irrelevant topic |

**Round 1 bracket:** (5.5, 7.5) — the paper has a genuine theoretical contribution and clear presentation but significant validation gaps that prevent it from being a strong accept.

**Round 2 narrowing:** The closest anchor is the inverse decision-making paper (6.00). Both have similar impact profiles: strong theoretical contribution and clear writing (impact +9 to +10 for shared strengths), but weaknesses about limited validation scope and lack of comprehensive comparative experiments (impact -9 to -10 for shared weaknesses). The paper under review has a more original theoretical derivation (the Bayes-optimal estimator for mismatched decoding) but also has a larger gap between its claims and its evidence (no closed-loop demonstration). I place it at **6.0**, comparable to the inverse decision-making paper — a borderline accept with genuine merit.

**Final score: 6.0 — Borderline Accept.** The paper makes a genuine theoretical contribution to an important problem in computational neuroscience, is clearly written, and provides practically useful design landscapes. However, the validation is incomplete: the simulations do not test robustness to violations of core assumptions, and the paper never demonstrates that following the optimized designs actually enables successful hypothesis discrimination (even in simulation). A revision that closes this loop could strengthen the paper considerably.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>