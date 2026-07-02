## Summary

This paper introduces an information-theoretic framework for optimizing experimental designs to distinguish between two competing hypotheses about how sensory neural populations encode uncertainty: likelihood coding (e.g., probabilistic population codes) versus posterior coding (e.g., neural sampling codes). The authors derive the "information gap"—the expected performance difference between likelihood and posterior decoders when applied to neural populations—by evaluating KL divergences between true posteriors and task-marginalized surrogate posteriors. Through extensive simulations, they validate that the information gap accurately predicts decoder performance differences, and demonstrate that maximizing this gap yields stimulus distributions that optimally differentiate the two coding hypotheses, providing principled guidance for future neurophysiology experiments.

## Strengths

- **Significant and well-motivated research question**: The paper addresses a fundamental, unresolved question in systems neuroscience—how probabilistic information is encoded in sensory populations—and provides a rigorous framework for designing experiments that can adjudicate between competing theories. The problem definition is clear and the motivation is compelling.

- **Rigorous theoretical derivation**: The authors provide analytic derivations for the information gap under both coding hypotheses (Equations 1-5), with clear logical structure. The key insight of task-marginalized Bayes-optimal estimators for mismatched decoding is novel and well-executed.

- **Comprehensive empirical validation**: The simulation experiments systematically validate theoretical predictions across diverse conditions: multiple contrast levels, two neural models (Poisson and gain-modulated Poisson), varying numbers of neurons and trials, and multiple task parameter settings (Figures 3-4). The convergence results and scatter plots provide strong evidence that the theory correctly predicts empirical decoder behavior.

- **Actionable optimization results**: The information gap landscapes (Figures 5-6) provide concrete, interpretable guidance for experimental design, identifying "strategic sweet spots" where discriminative power is maximized. The analysis of non-Gaussian priors (heavy-tailed distributions being unsuitable) demonstrates the framework's ability to rule out inefficient designs.

- **Empirical validation on real data**: The analysis of the Allen Brain Observatory dataset (Figure 7) convincingly demonstrates that existing single-context experimental designs cannot distinguish the hypotheses (information gap ≈ 0), underscoring the practical necessity of the proposed framework.

## Weaknesses

### Fatal
None.

### Major

- **Limited practical guidance on decoder implementation**: The paper relies on "optimal decoders" that reach theoretical limits, but does not adequately address how close empirical neural network decoders can practically get to the theoretical information gap in real experimental settings. The simulated decoders converge to theoretical values under idealized conditions (Figure 3), but real neural data has complexities (noise correlations, non-stationarity, limited trial counts) that could substantially reduce effective discriminability. The paper would benefit from explicit guidance on required sample sizes for statistical significance given realistic effect sizes.

- **The asymmetry explanation for posterior-coding gaps requires stronger justification**: The authors state that posterior-coding populations show smaller information gaps because "only pairs satisfying Eq. 4 contribute to the estimate." However, the derivation of Eq. 4 relies on the assumption that identical population responses must map to different likelihood functions. This assumption deserves more scrutiny—in practice, population responses for posterior-coding neurons will not be *identical* across contexts even for matching posteriors, and the conditions for non-zero contributions need clearer biological interpretation and sensitivity analysis.

- **Optimization results lack cross-validation on unseen simulated data**: While the information gap landscapes are informative (Figure 5), there is no demonstration that the "optimal" designs actually yield significantly different experimental outcomes when evaluated on held-out simulated populations or under slightly misspecified generative models. A robustness analysis showing how sensitive the optimal parameters are to model misspecification (e.g., wrong tuning curve parameters, incorrect noise model) would strengthen practical recommendations.

### Minor

- **Limited exploration of mixed/intermediate hypotheses**: Section 6 and Appendix A.5 briefly discuss extending the framework to mixed coding hypotheses, but the treatment is superficial (one paragraph and a figure reference). Given that these intermediate cases are acknowledged as potentially more realistic, more analysis on the framework's sensitivity to graded departures from pure likelihood or posterior coding would strengthen the contribution.

- **The decoding approach for posterior-coding populations is computationally intensive**: The fixed-point iteration required for Equation 5 to compute the information gap for posterior-coding populations may limit practical adoption by experimentalists. The paper could benefit from discussing approximations or closed-form bounds that reduce computational burden while maintaining accuracy.

### Trivial

- Figure 2 is referenced inconsistently in the text (panel D is mentioned but only A-C are shown).

## Nice-to-Haves

- Discussion of optimal experimental designs with more than two contexts or continuous prior manipulations
- Extension to non-orientation stimulus features (e.g., motion direction, spatial frequency) to demonstrate generality
- Power analysis or sample size recommendations for real experiments based on the information gap magnitudes found in simulations

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add explicit quantitative recommendations for experimental design (e.g., "For high contrast stimuli with Gaussian priors, a separation of d ≈ 20° and σ ≈ 10° yields maximal discriminability"). This would significantly increase practical utility for experimental neuroscientists.

- Include a robustness analysis showing how the optimal task parameters change when the generative model is slightly misspecified (e.g., wrong tuning curve width, incorrect noise distribution).

## Score and Decision

The paper makes a significant theoretical contribution by providing a principled, quantitative framework for a long-standing experimental challenge in systems neuroscience. The derivations are rigorous, the validation is thorough, and the practical implications are clear and actionable. The weaknesses (limited decoder gap analysis, implementation concerns, and robustness issues) are addressable and do not invalidate the core contribution. This is strong, well-executed work appropriate for a top venue.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>