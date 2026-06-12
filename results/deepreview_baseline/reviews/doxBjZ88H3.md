## Summary

This paper presents an information-theoretic framework for optimizing experimental designs to distinguish between two competing hypotheses about how sensory neural populations encode uncertainty: likelihood coding (probabilistic population codes) versus posterior coding (neural sampling codes). The authors derive an "information gap" measure—the expected difference in decoder performance when applying likelihood versus posterior decoders to neural populations—and validate it through extensive simulations. They demonstrate that maximizing this information gap yields stimulus distributions that optimally differentiate the two coding hypotheses, providing a principled approach for designing decisive experiments.

## Strengths

- **Novel and important problem formulation**: The paper addresses a fundamental open question in computational neuroscience—how to experimentally distinguish between likelihood and posterior coding in sensory populations—and provides a principled theoretical framework rather than relying on heuristic experimental designs. This bridges a critical gap between theory and experiment.

- **Rigorous theoretical derivation**: The information gap is derived analytically using KL divergence and Bayes-optimal estimators, with clear mathematical formulations for both coding hypotheses (Eqs. 1-5). The derivations are well-motivated and the key insight about task-marginalized surrogate posteriors is elegant.

- **Strong empirical validation**: The simulations demonstrate remarkable agreement between theoretical predictions and empirical decoder performance across diverse settings (multiple contrast levels, two neural models, varying trial/neuron counts). The convergence results in Figures 3-4 are convincing and thorough.

- **Practical actionable guidance**: The information gap landscapes (Figures 5-6) provide concrete, interpretable guidance for experimental design, identifying "sweet spots" in parameter space. The analysis of why heavy-tailed priors fail is insightful and practically useful.

- **Empirical demonstration on real data**: The Allen Institute dataset analysis (Figure 7) effectively demonstrates why existing single-context experiments cannot distinguish the hypotheses, strengthening the case for the proposed framework.

## Weaknesses

### Fatal
None.

### Major

- **Limited validation on real neural data**: While the Allen dataset analysis is included, it only confirms the null case (no prior manipulation). The paper would be substantially stronger with validation on a dataset where prior manipulation was actually performed, or with a clear roadmap for how the framework would be applied in practice. The framework's core claim—that optimized designs will actually work in real experiments—remains untested.

- **Computational complexity of posterior coding information gap**: The derivation for Δ_p^info involves solving an implicit equation via fixed-point iteration (Eq. 5) and requires identifying observation pairs satisfying Eq. 4. The paper does not discuss computational cost, convergence guarantees, or sensitivity to initialization for this procedure, which could be a practical barrier for experimenters.

- **Assumption of explicit context cuing**: The framework assumes subjects adopt context-specific priors without having to infer context from stimuli. This is a strong assumption that may not hold in practice, and the paper does not discuss how violations (e.g., subjects using imperfect or inferred priors) would affect the information gap or experimental conclusions.

### Minor

- **Gaussian observation model limitation**: The simulations use Gaussian observation models and Poisson spiking. While reasonable, the paper would benefit from discussion of how non-Gaussian or more complex observation models (e.g., with correlated noise) would affect the framework.

- **Asymmetry in information gap magnitudes**: The paper notes that Δ_L^info is an order of magnitude larger than Δ_p^info, but does not fully discuss the practical implications for statistical power—specifically, how many trials/neurons would be needed to reliably detect the smaller posterior-coding gap in real experiments.

### Trivial
None.

## Nice-to-Haves

- A practical guide or pseudocode for experimenters to compute the information gap for their specific setup would increase adoption.
- Discussion of how to handle discrete versus continuous stimulus spaces in practice (the paper mentions this briefly but could expand).
- Analysis of robustness to misspecification of the generative model p(x|θ).

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is the identification of the fundamental asymmetry between distinguishing likelihood versus posterior coding: posterior-coding populations are inherently harder to distinguish because only observation pairs satisfying the posterior-equivalence condition (Eq. 4) contribute to the information gap. This explains why heavy-tailed priors fail and why careful optimization is necessary. The paper also reveals that the optimal experimental design depends critically on stimulus contrast, with lower contrast expanding the parameter region yielding substantial information gaps—a non-obvious prediction that could guide practical experiments.

## Suggestions

- Provide a concrete example of how an experimenter would use the framework: e.g., "Given a planned experiment with 200 neurons and 10,000 trials, here is the minimum detectable information gap and the corresponding optimal task parameters."
- Include a sensitivity analysis showing how the optimal task parameters change with the number of neurons/trials available, to help experimenters with resource constraints.
- Discuss how to handle the case where the true generative model p(x|θ) is unknown and must be estimated from data, including potential biases this introduces.

## Score and Decision

The paper makes a significant theoretical contribution to a fundamental question in computational neuroscience, with rigorous derivations and thorough simulation validation. The framework is novel, principled, and practically actionable. The main limitations are the lack of validation on real data with prior manipulation and some practical implementation details that could be clarified. However, the paper's core contribution is strong and well-supported.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>