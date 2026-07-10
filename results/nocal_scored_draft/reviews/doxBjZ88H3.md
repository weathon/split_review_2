## Summary

This paper presents an information-theoretic framework for designing experiments that can distinguish whether early sensory neural populations encode likelihood functions or posterior distributions. The authors derive the *information gap* — the expected decoder performance difference when applying likelihood vs. posterior decoders to neural populations — computed as KL divergences between true and surrogate posteriors using Bayes-optimal estimators. They validate the derivation through simulations showing that neural-network decoders converge to the theoretical values, compute information gap landscapes across task parameters to identify "sweet spots" for experimental design, and confirm on the Allen dataset that single-context designs cannot distinguish the hypotheses.

## Strengths

- **Well-motivated, well-scoped problem (Section 1).** The paper targets a genuine open question in computational neuroscience and correctly identifies why existing experiments cannot distinguish the two hypotheses: without context-dependent prior manipulation, both can fit the same data. The framing is clear and the scope is appropriately narrow (the paper provides tools for designing experiments, not settling the debate).

- **Novel derivation of the information gap under both hypotheses (Section 2, Eqs. 1–5).** The analytic derivation of Bayes-optimal estimators for mismatched decoders is non-trivial and theoretically clean. The insight that the optimal posterior decoder on likelihood-coding populations converges to the marginal posterior over contexts (Eq. 2), and the condition relating observation pairs that yield identical neural responses across contexts (Eq. 4), are genuine theoretical contributions.

- **The information-gap magnitude asymmetry is an interesting finding (Section 3, Fig. 4, Fig. 5).** The observation that Δ^info for posterior-coding populations is an order of magnitude smaller than for likelihood-coding populations, with a clear theoretical explanation rooted in Eq. 4, provides non-trivial guidance for experimental design — it tells experimenters that discriminating posterior-coding populations will require substantially more statistical power.

## Weaknesses

### Fatal
None.

### Major

- **The central claim that maximizing the information gap yields optimal experimental designs is not validated.** The paper computes Δ^info landscapes and identifies "sweet spots" (Section 4, Fig. 5) but never conducts an experiment — simulated or otherwise — showing that a Δ^info-maximizing design actually outperforms alternatives at distinguishing which hypothesis generated the data. The paper also does not compare against intuitive baseline designs (e.g., maximally separated priors, uniform priors, random parameter choices) to demonstrate the value added by optimization. Lines 161 ("maximize statistical power") and 194 ("optimally discriminate") assert claims that go beyond what has been demonstrated: the Section 3 validation only shows Δ^info matches decoder performance differences under the same generative assumptions — it does not test whether the optimization translates into better hypothesis discrimination. This gap concerns the paper's advertised core contribution (a framework for optimal experimental design), not a missing ablation.

### Minor

- **Experimental feasibility implications of the asymmetry are not quantified.** The paper notes (line 125) that posterior-coding Δ^info values are an order of magnitude smaller than likelihood-coding, but does not investigate what this means in practice: how many more trials, neurons, or sessions would be needed to detect posterior coding? Without this, experimenters cannot judge whether distinguishing posterior-coding populations is practically feasible with the proposed designs.

- **No statistical decision framework provided.** The paper does not specify how an experimenter would actually use the decoder performance difference to choose between hypotheses — what effect sizes or Δ^info values constitute evidence for one hypothesis over the other, what false-positive rate to expect, or what sample sizes are needed. This limits the practical actionability of the framework.

- **"Sufficient discriminative signal" is not quantitatively defined.** The strategic sweet spots (Section 4, Fig. 5 caption, line 151) are selected where posterior-coding Δ^info "approaches its maximum while likelihood-coding maintains sufficient discriminative signal," but "sufficient" is never defined. This makes the parameter selection somewhat subjective despite the paper's framing of principled optimization.

- **The Allen dataset analysis (Section 5, Fig. 7) is a sanity check, not evidence for the framework's utility.** The paper confirms Δ^info = 0 for a single-context/uniform-prior design, which follows directly from the theory (as the paper acknowledges at line 171). While the confirmation on real data is a reasonable consistency check, the framing as "empirical results" that "highlight the necessity of the context-dependent prior manipulation" (line 175) overstates what this analysis adds beyond the already-established problem statement.

### Trivial
None.

## Nice-to-Haves

- A simulated discrimination experiment where designs with different Δ^info values are compared on classification accuracy of which hypothesis generated the simulated data. This would directly test whether maximizing Δ^info translates into better hypothesis discrimination.
- Sample-size and power analysis for the optimized designs: given the Δ^info values found at the sweet spots, estimate how many trials, neurons, or sessions would be needed to detect the decoder performance difference at a given false-positive rate.
- Use the Allen dataset to estimate realistic noise parameters, then simulate power calculations for the proposed multi-context optimized designs to ground the theoretical predictions in empirically plausible numbers.

## Removed Points

- **"Validation is circular / only shows internal consistency"** (Harsh Critic Critical Issue 1): The reviewer claimed the simulation validation is "circular" because it uses the same parametric assumptions as the derivation. This is standard practice for theory papers — the simulations confirm that the mathematical derivations are correct and that neural-network decoders converge to the theoretically predicted values. The paper is clear about what the simulations show and does not claim to have validated the framework against real multi-context data (which does not yet exist). This is not a genuine weakness.
- **Generic presentation observations** from the Harsh Critic's Section-by-Section Notes (notation clarity, first-read confusion about equation indexing) do not rise to the level of weaknesses and do not affect evaluation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run a simulated discrimination experiment: generate data from both hypotheses under optimized vs. non-optimized designs, train both decoders, compute classification accuracy of which hypothesis generated the data, and show that Δ^info-maximizing designs yield higher accuracy. This directly validates the framework's central claim.
2. Provide a power/sample-size analysis linking Δ^info values to the number of trials or neurons needed for reliable discrimination at standard significance thresholds.
3. Define a quantitative criterion for "sufficient discriminative signal" (e.g., a minimum Δ^info value that corresponds to a target classification accuracy or statistical power), removing the subjectivity from sweet-spot selection.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>