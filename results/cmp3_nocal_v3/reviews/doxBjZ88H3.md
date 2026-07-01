Now I have all the evidence I need. Let me write the final consolidated review.

## Summary

This paper addresses the unresolved question of whether early sensory neural populations encode likelihood functions (as in probabilistic population codes) or posterior distributions (as in neural sampling codes). The authors develop an information-theoretic framework that derives the *information gap* — the expected difference in decoder performance when applying likelihood versus posterior decoders to neural population responses under a given task design. The framework yields analytic expressions (Eqs. 1–5) for this gap under each coding hypothesis, validated through simulation with Poisson and gain-modulated Poisson neuron models across diverse task parameters. The key applied contribution is using the information gap landscapes to identify stimulus prior distributions (separation between context means and standard deviation) that maximally differentiate the two hypotheses. The paper demonstrates that existing single-context datasets (Allen Brain Observatory) cannot resolve the question and provides actionable guidance for designing multi-context experiments.

## Strengths

1. **Non-trivial derivation of Bayes-optimal mismatched decoders.** The derivations for what an optimal decoder produces when applied to mismatched probabilistic content (Eq. 2 for posterior decoder on likelihood-coding populations; Eq. 5 for likelihood decoder on posterior-coding populations) are the technical core of the paper. The insight that the optimal posterior decoder on likelihood-coding populations converges to a task-marginalized Bayes estimator (Eq. 2) is clean and correct. The fixed-point characterization for the posterior-coding case (Eq. 5) goes beyond simply asserting that KL divergence is the right measure — it derives what the decoders would actually compute under optimality.

2. **Thorough simulation validation with convergence evidence.** The paper validates the information gap against empirical decoder performance across three contrast levels, two neural noise models (Poisson and gain-modulated Poisson), multiple task parameter settings (≥10 per condition), and both scaling regimes (varying trials and varying neurons). Figures 3 and 4 show good agreement between theory and simulation, with convergence as data increases. The use of both a simple and a more biologically realistic noise model strengthens confidence.

3. **Non-obvious and practically relevant findings from the landscape analysis.** The information gap landscapes (Figs. 5, 6) yield concrete, non-trivial insights: (a) optimal experimental parameters differ between the two hypotheses, so one-size-fits-all designs are suboptimal; (b) posterior-coding information gaps are an order of magnitude smaller than likelihood-coding ones, making posterior-coding populations inherently harder to distinguish — this has real implications for statistical power; (c) heavy-tailed priors (Student's t, Cauchy) are essentially useless for distinguishing posterior-coding populations; (d) lower contrast expands the region of informative task parameters, consistent with the intuition that priors matter more when sensory evidence is weak.

4. **Honest about limitations.** The Discussion (lines 196–199) explicitly acknowledges the need for a generative model, the requirement for sufficient data, and the existence of mixed/intermediate coding hypotheses. This self-awareness is appropriate for a framework paper.

5. **Useful empirical consistency check on real data.** The Allen dataset analysis (Section 5, Fig. 7) shows that single-context data yields Δ^info ≈ 0, consistent with the framework's prediction. While this is a null result, it serves its stated purpose: demonstrating that existing data cannot resolve the question and motivating the need for multi-context designs.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **The "strategic task design" sweet-spot selection is ad hoc, not a principled optimization.** The paper's abstract and Section 4 claim to enable "principled, theory-driven experimental designs," but the actual selection of sweet spots (asterisks in Fig. 5) is described qualitatively: "one might prioritize parameters that maximize posterior-coding discriminability while maintaining *adequate* likelihood-coding sensitivity" (line 151). No formal objective function (maximin, weighted sum, Pareto front) is stated, and "adequate" / "sufficient" are not defined. For a paper whose central applied contribution is optimization of task parameters, this is a noticeable gap between rhetoric and method. The landscapes are informative, but the step from landscape to recommended design is not rigorous.

2. **The posterior-coding information gap (Eq. 3) depends on a matching condition (Eq. 4) whose practical fragility is underexplored.** The gap for posterior-coding populations only receives contributions from observation pairs (xⱼ, xₖ) whose posteriors are *exactly* equal across contexts (Eq. 4). The paper discretizes observations (x ∈ {xᵢ}) to make this tractable, but does not discuss how the discretization resolution affects the gap values, nor whether the matching condition can be meaningfully approximated in continuous-stimulus experiments with finite neural populations. The paper acknowledges the resulting order-of-magnitude asymmetry (line 125), but an experimenter needs to know whether the near-zero posterior gaps for certain parameter regimes are a real physical limitation or a modeling artifact of the discretization. This does not invalidate the framework but limits its practical utility for the posterior-coding case.

3. **The empirical evidence that the framework's optimized designs would succeed in real experiments is limited to simulation.** The paper's core applied claim is that maximizing the information gap yields optimal experimental designs. This is validated only in simulations where the ground truth (likelihood vs. posterior coding) is known by construction. The Allen dataset analysis is a consistency check on single-context data (Δ^info ≈ 0), not a predictive test of the optimization. The paper is appropriately scoped as a framework, and simulation validation is standard for theoretical work, but the practical claim is proportionally weaker than if it had been tested with a forward prediction on real data. A sensitivity analysis showing how the optimal parameters shift under plausible model misspecifications (e.g., tuning curve shape, noise correlations) would strengthen this aspect.

4. **No discussion of what constitutes a "decisive" result size.** The paper identifies optimal designs in terms of maximizing the information gap, but never addresses the decision-theoretic step: how large must the gap be to confidently reject one hypothesis in favor of the other? An experimenter who obtains a gap of 0.1 nats needs to know whether this is decisive. The scaling results in Fig. 3 could be extended to provide explicit sample-size / effect-size guidance.

5. **The assumption that subjects adopt the intended prior (line 59) is stated but not stress-tested.** The paper assumes contexts are "explicitly cued to ensure that subjects adopt the intended context-specific prior" (line 59), and mentions imperfect priors as an extension (line 196). However, it does not quantify how sensitive the optimal designs are to partial or biased prior adoption — a likely scenario in practice, especially early in training. This matters because the information gap directly depends on the assumed prior.

### Trivial

- The paper uses discretized observations throughout but does not discuss how discretization resolution affects the results or provide guidelines for choosing the resolution.

## Nice-to-Haves

- **Sensitivity analysis under model misspecification.** Systematically vary the assumed generative model (tuning curve width, noise correlations, noise distribution) and recompute the information gap landscapes. If optimal parameters are stable, this substantially strengthens the practical claim; if they shift, this is important guidance for experimenters.
- **Formalize the multi-objective trade-off** between the two information gaps using a principled criterion (e.g., maximin design, weighted sum with known cost ratios).
- **Sample-size recommendations.** Extend the scaling results (Fig. 3) to provide explicit guidance: given a target effect size and expected trial count, what power can an experimenter expect for distinguishing each hypothesis?

## Removed Points

These points appeared in the input review but are removed per filtering rules:

- **Fixed-point iteration convergence (Issue 2, part).** The reviewer noted that convergence properties of Eq. 5 are not discussed in the main text and speculated the appendix may address it. Per the hard rule, critiques that depend on missing appendix content are removed. The paper refers to Appendix A.1 for details, which is stripped by the parser.
- **"Appendix may address this" phrasing** throughout — removed per hard rule about missing appendix.
- **Strengths-filtered:** None needed — all six strengths in the input are concrete and grounded in specific paper content.

## Novel Insights

The input review's most insightful observation is the tension between the paper's claimed "principled optimization" and its actual ad hoc sweet-spot selection (Issue 3). This is not a superficial mismatch: the paper derives a rigorous mathematical framework for computing information gaps, then falls back on visual inspection of landscapes to pick operating points. A formal decision criterion (e.g., maximin over the two gaps, or minimizing the Bayes error rate of a hypothesis test that compares observed decoder performance to the two predicted gaps) would complete the pipeline from theory to experimental protocol. The review also identifies a deeper point: the matching condition in Eq. 4 means the posterior-coding gap is fundamentally discrete in a way the likelihood-coding gap is not. This structural asymmetry is acknowledged (line 125) but its practical consequences — and whether the discretization coarseness can be chosen to avoid gap starvation — are not explored. These observations point to clear, actionable improvements without undermining the paper's core theoretical contribution.

## Suggestions

1. Formalize the sweet-spot selection into an explicit objective function, e.g., choose task parameters (d, σ) that maximize min(Δ_L^info, Δ_P^info / α) where α accounts for the magnitude asymmetry, or a weighted sum.
2. Add a brief analysis of how the information gap varies with discretization resolution, especially for the posterior-coding case, to assure experimenters that the reported gaps are not artifacts of bin size.
3. Include a "practical guide" subsection translating the information gap values into sample-size recommendations: given N trials and M neurons, what gap is detectable, and what design achieves it?

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>