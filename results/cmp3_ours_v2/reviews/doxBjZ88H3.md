## Summary

This paper presents an information-theoretic framework for optimizing experimental designs to distinguish between two competing hypotheses in computational neuroscience: whether early sensory populations encode likelihood functions or posterior distributions. The key construct — the "information gap" — quantifies the expected difference in cross-entropy loss between optimal likelihood and posterior decoders under each hypothesis. The authors derive analytic expressions for this gap (Eqs. 1–5), validate them extensively through simulations showing DNN decoders converge to the theoretical predictions (Figs. 3–4), and compute information gap landscapes to identify stimulus prior parameters that maximize discriminability (Figs. 5–6). An analysis of the Allen Brain Observatory dataset confirms that single-context designs cannot adjudicate the hypotheses (Fig. 7).

## Strengths

1. **Well-motivated problem with a clean formalization.** The paper translates an unresolved debate in computational neuroscience (likelihood vs. posterior coding) into a well-defined quantitative question. The "information gap" as the expected decoder cross-entropy difference between matched and mismatched decoders is a natural and insightful formalization.

2. **Genuine theoretical contribution in the derivations of Bayes-optimal decoders for mismatched content.** Equation 2 (the optimal posterior decoder on a likelihood-coding population converges to a task-marginalized posterior) and Equation 5 (the fixed-point equation for the optimal likelihood decoder on a posterior-coding population) are the paper's core intellectual contribution. The insight that the posterior-coding information gap only receives contributions from observation pairs satisfying Eq. 4 provides a principled explanation for why posterior coding is harder to distinguish.

3. **Strong quantitative validation of the metric.** Figures 3 and 4 convincingly show that the theoretical information gap accurately predicts empirical decoder performance differences across multiple contrast levels, two neural models (Poisson and gain-modulated Poisson), and a wide range of task parameters. The convergence in trials and neurons (Fig. 3) and the scatter plots falling on the diagonal (Fig. 4) are solid evidence that the derivations are correct.

4. **Practical, actionable insights from the information gap landscape.** Figure 5 provides concrete parameter recommendations (e.g., for low contrast: d ≈ 30°, σ ≈ 20° for Gaussian priors). The analysis of heavy-tailed priors (Fig. 6) showing near-zero posterior-coding information gap is a useful negative result that could save experimenters from pursuing unpromising designs.

5. **Honest treatment of scope and limitations.** The Discussion acknowledges the need for pre-existing generative models, sufficient neural data, the possibility of mixed coding hypotheses, and the extension to imperfect priors.

## Weaknesses

### Major

1. **The central claim about "optimal experimental designs" is not validated in closed loop.** The paper validates that the information gap *predicts* decoder performance differences (Figs. 3, 4) and computes its landscape to identify maxima (Figs. 5, 6). However, it never closes the loop by asking: do task designs at the identified "sweet spots" actually improve the ability to determine which hypothesis generated the data, compared to designs elsewhere in the parameter space? The missing experiment is straightforward: simulate data from both hypotheses at multiple points in parameter space (including the optimum, sub-optimal points, and a heuristic baseline), apply a simple decision rule (e.g., "choose the hypothesis whose decoder achieves lower cross-entropy"), and report classification accuracy or statistical power as a function of trial count. The abstract claims maximizing the information gap "yields stimulus distributions that optimally differentiate likelihood and posterior coding hypotheses," but this is asserted rather than demonstrated. The evidence supports a weaker claim: "the framework identifies stimulus distributions that maximize a theoretical quantity (information gap) that correlates with decoder performance differences." This gap is major enough that it prevents the paper from being a strong accept, but it is addressable with additional simulations.

### Minor

2. **No explicit connection between the information gap and hypothesis-testing power.** The paper mentions "statistical power" (lines 125, 161) but never defines a decision rule or quantifies how the information gap translates to the ability to adjudicate between hypotheses with finite data. The posterior-coding Δ^info values in Fig. 5 top out at ~0.06 nats — is this detectable? With how many trials or neurons? The framework identifies designs that maximize a proxy but cannot tell an experimenter whether a given design is *adequate* for the binary hypothesis test. This weakens the practical actionability. (Note: connecting the metric to hypothesis testing is somewhat beyond the paper's stated scope of experimental *design* optimization rather than inference, which is why this is Minor rather than Major.)

3. **The trade-off between hypotheses is handled informally.** The optimal parameters for maximizing Δ_L^info and Δ_P^info differ (Fig. 5). The paper recommends prioritizing the posterior-coding optimum because it's "an order of magnitude smaller," and identifies "sweet spots" by visual inspection of contour plots (lines 151–155). However, "sufficient discriminative signal" is undefined, and no formal joint optimization objective (e.g., maximin, Pareto frontier, expected value under a prior over hypotheses) is formulated. A principled approach to the trade-off would strengthen the framework.

4. **The posterior-coding information gap derivation depends on a measure-zero condition with limited practical guidance.** Δ_P^info (Eqs. 3–5) depends on pairs (xⱼ, xₖ) satisfying Eq. 4: p^A(θ|xⱼ) = p^B(θ|xₖ). With continuous observations, exact equality occurs with probability zero under any absolutely continuous observation model. The paper mentions "discretized sensory observations" (line 63) but does not specify: (a) how the discretization resolution affects the computed Δ_P^info, (b) how to handle approximate (rather than exact) equality of posteriors, (c) whether the fixed-point iteration (Eq. 5) converges reliably, or (d) how many observation pairs contribute in practice. Since the posterior-coding gap is already an order of magnitude smaller than the likelihood-coding gap, sensitivity to discretization or approximation choices could materially affect the optimization landscape.

5. **Missing baseline comparisons.** The paper claims the framework "transforms parameter selection from heuristic search to principled optimization" (line 161) but never quantifies how much better the optimized designs are compared to intuitive heuristic alternatives (e.g., equal priors, maximally separated priors, priors matched to previous experimental work). Without this comparison, the practical value of the optimization is asserted rather than demonstrated.

### Trivial

6. **Typo on line 125.** Both subscripts are `p` in "information gaps for likelihood-coding populations (Δ_p^{info}) exceed those for posterior-coding populations (Δ_p^{info})". One should be Δ_L^{info}.

## Nice-to-Haves

- The Allen dataset analysis (Section 5) provides a useful sanity check showing that single-context designs yield Δ ≈ 0, but this is consistent with both hypotheses. The paper's framing of this result as supporting the framework is appropriate but should not be over-interpreted — it confirms that the framework does not produce false positives, not that the optimization is useful.
- A formal joint optimization objective (maximin, Pareto, or expected value with a prior) would replace the visual-inspection-based "sweet spot" selection with a mathematically grounded design choice.

## Removed Points

- **Criticism that Section 5 claims are over-stated** (from Harsh Critic Section-by-Section Notes): Removed because the paper's actual language ("agrees with our theoretical prediction," "underscores why future experiments...will be essential") is measured and appropriate. The paper does not over-claim this result.
- **Missing Figure 8**: Removed because this is an appendix figure stripped by the parser; the original submission contains it.
- **Criticism framed as "fatal" about measure-zero events** (Harsh Critic Critical Issue 4): The reviewer framed this as a critical issue, but the paper does mention discretized observations, and the concern is technical and addressable rather than destructive. Moved to Minor weakness #4 above with appropriate framing.
- **Generic strengths removed**: Generic statements about the problem being important were removed. The kept strengths are those with specific, verifiable evidence in the paper.
- **Strawman about the Allen dataset not providing positive evidence**: Removed because the paper does not claim it as positive evidence for the optimization — it's presented as a sanity check motivating the need for multi-context designs.

## Novel Insights

Beyond the paper's own contributions, the reviews surface a useful meta-insight: the paper has a genuine theoretical contribution (the information gap derivations) that is well-validated as a *predictive* metric, but the leap to *optimization* (that maximizing this metric yields truly optimal experimental designs) is a distinct claim that requires a separate validation loop. This distinction between a metric that predicts and a metric that optimizes is an important one that many papers in the experimental-design literature could benefit from observing. The reviewers also correctly note that the posterior-coding gap's dependence on measure-zero events (Eq. 4) creates a practical fragility that would be worth analyzing systematically.

## Suggestions

1. **Add a closed-loop validation study (highest priority):** Simulate data from both hypotheses at multiple points in parameter space (the identified optimum, several sub-optimal points, and a heuristic baseline like maximally separated priors). Apply a simple decision rule (e.g., "choose the hypothesis whose decoder achieves lower cross-entropy") and report classification accuracy or AUC as a function of trial count. Show that the optimized design yields reliably better discrimination.

2. **Formalize the joint optimization:** Replace the visual-inspection-based "sweet spot" selection with a formal objective function (e.g., maximize Δ_P^info subject to Δ_L^info ≥ threshold, or maximize the minimum of the two gaps, or maximize expected information gap under a prior over hypotheses).

3. **Characterize the discretization dependence of Δ_P^info:** Report how the computed posterior-coding gap varies with discretization resolution, and provide practical guidance on handling approximate (non-exact) equality of posteriors.

4. **Connect the information gap to statistical power:** Show analytically or through simulation how Δ^info relates to the minimum number of trials/neurons needed to distinguish the hypotheses at a given confidence level.

5. **Add a comparison against heuristic baselines:** Quantify the improvement in Δ^info at the optimized design versus simple heuristic designs.

## Score and Decision

**Calibration report:** I retrieved 24 anchor papers across six score bands (strong reject through strong accept) from the human-review corpus using the query "information-theoretic experimental design neuroscience neural coding." I read four anchors in full:
- **ADDCErFzev.md** (avg 6.0, Accept): Dropout/efficiency-robustness paper; clean empirical findings, simpler theory. The current paper has stronger theoretical depth but a wider gap in its central claim.
- **L07zWidgdW.md** (avg 6.75, Accept): Finding shared concepts in brain via CLIP; mixed reviews (5,6,8,8). The current paper has comparable theoretical novelty.
- **4GfEOQlBoc.md** (avg 5.25, Reject): Image statistics/perception paper; criticized for using proxies rather than validating the central link. The current paper's theory is stronger and its validation is more direct.
- **cNmu0hZ4CL.md** (avg 8.0, Accept): Causal OT metric for neural dynamics; complete closed-loop validation despite some limitations (Gaussian assumption). The current paper has a similar structure but lacks the closed-loop validation, placing it below this anchor.

**Bracket determination:** Round 1 bracketing placed the paper in the 5.5–7.5 range. Comparing to anchors: stronger theory than the 6.0 dropout paper, comparable theoretical depth to the 6.75 concept-finding paper, but weaker validation than the 8.0 OT paper. The gap between the paper's central claim ("maximizing the information gap yields optimal experimental designs") and what is actually demonstrated is the main factor limiting the score. Within the 5.5–7.5 bracket, the paper sits near the lower end because this gap is structural rather than incremental.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>