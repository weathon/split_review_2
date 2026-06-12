## Summary
This paper develops an information-theoretic framework for optimizing experimental designs to distinguish two competing hypotheses about how probabilistic information is encoded in early sensory neural populations: the likelihood coding hypothesis (neural populations encode likelihood functions) versus the posterior coding hypothesis (neural populations encode posterior distributions). The authors derive analytic expressions for the "information gap"—the expected decoder performance difference between likelihood and posterior decoders—validate these predictions through extensive simulations on synthetic neural populations, and demonstrate how maximizing the information gap yields principled, optimal experimental designs for discriminating between the two coding hypotheses.

## Strengths
- **Well-motivated and important problem.** The paper addresses a genuinely unresolved question in computational neuroscience—whether early sensory populations encode likelihoods or posteriors—and provides a principled, quantitative framework to resolve it. The problem is clearly articulated with strong grounding in the literature (Ma et al. 2006, Walker et al. 2020, Orbán et al. 2016).
- **Rigorous theoretical derivation with empirical validation.** The analytic expressions for the information gap under both coding hypotheses (Eqs. 1–5) are derived carefully, and the simulations demonstrate excellent convergence between theoretical predictions and empirical decoder performance across diverse task parameters, contrast levels, and two different neural model classes (standard Poisson and gain-modulated Poisson). Figure 4 showing near-perfect alignment along the diagonal is particularly convincing.
- **Practical value through information gap landscapes.** The framework transforms parameter selection from heuristic search to principled optimization. The analysis of optimal "sweet spots" (Fig. 5), the strategic prioritization of posterior-coding discriminability given the order-of-magnitude asymmetry, and the comparison of Gaussian vs. heavy-tailed priors (Fig. 6) provide concrete, actionable guidance for experimentalists.
- **Negative control on real data.** The Allen Brain Observatory analysis (Section 5) serves as a well-designed empirical validation: under single-context uniform priors, the theory predicts Δinfo = 0, and the data confirms this (difference = 0.0024 ± 0.064, p = 0.63), underscoring why current datasets are insufficient and motivating the proposed paradigm.

## Weaknesses
### Fatal
None.

### Major
- **Limited empirical validation on real neural data.** The real-data analysis only demonstrates the negative case (single-context design yields zero information gap), which is essentially a trivial prediction of the framework. The positive case—that optimized multi-context designs actually succeed in distinguishing coding hypotheses on real neural populations—remains entirely unvalidated. While this is understandable given practical constraints, it substantially limits the demonstrated impact and leaves open the question of whether confounds in real neural data (noise correlations, nonlinearities, imperfect context cueing, learning effects) would undermine the framework's predictions.
- **Order-of-magnitude asymmetry raises practical concerns.** The information gap for posterior-coding populations is consistently ~10x smaller than for likelihood-coding populations (Figs. 4–5). The authors explain this theoretically (Eq. 4 restricts contributing observation pairs for posterior coding), but this asymmetry implies that even with optimized designs, distinguishing posterior coding from likelihood coding may require impractically large datasets. The paper would benefit from a more explicit analysis of the statistical power required in practice (e.g., minimum number of neurons/trials needed to achieve significance for each hypothesis).

### Minor
- **Assumption of explicitly cued contexts.** The framework assumes subjects are explicitly told the context and adopt the intended prior. In practice, subjects may have imperfect or biased priors. While the authors mention this can be handled via psychophysical estimation (A.4), the sensitivity of the framework to prior misspecification deserves more attention in the main text.
- **Simplified generative models in simulation.** The simulations use Gaussian tuning curves and Poisson noise, which are standard but relatively simple. Noise correlations between neurons, which are known to substantially affect population coding, are not modeled. The gain-modulated Poisson model adds some realism but still omits correlations.
- **Mixed coding hypotheses are only briefly addressed.** The paper acknowledges that intermediate hypotheses (populations encoding mixtures of likelihood and posterior) are possible and defers analysis to an appendix. Given that the binary framing may be overly restrictive, a more substantive discussion of how the framework discriminates continuous intermediate hypotheses would strengthen the contribution.

### Trivial
None.

## Nice-to-Haves
- An analysis of how noise correlations would affect the information gap predictions, even if preliminary, would significantly strengthen the paper's relevance to real neural data.
- A comparison with alternative optimal experimental design approaches (e.g., Bayesian adaptive design, Fisher information-based methods) would help contextualize the novelty of the information-gap framework.
- Concrete recommendations for specific experimental protocols (number of trials, sessions, neurons) would increase practical utility for experimentalists.

## Novel Insights
The key novel insight is that the mismatch between the probabilistic quantity a decoder is trained to extract and what the neural population actually encodes produces a predictable performance gap that can be analytically characterized. The derivation of task-marginalized Bayes-optimal estimators for this mismatch case (Eq. 2 for decoding posteriors from likelihood populations, Eq. 5 for decoding likelihoods from posterior populations) is a non-trivial theoretical contribution. The observation that heavy-tailed priors yield near-zero information gaps for posterior coding—because few observation pairs satisfy the proportionality condition (Eq. 4)—is an insightful and practically useful finding that directly constrains experimental design choices. The order-of-magnitude asymmetry between likelihood and posterior information gaps, explained by the structural difference in which observations contribute to each, is also a novel and practically important observation.

## Suggestions
- Provide a power analysis showing minimum dataset sizes (neurons × trials) required to achieve statistically significant discrimination between coding hypotheses under optimized designs, to give experimentalists concrete feasibility estimates.
- Discuss how the framework would need to be modified if context is not explicitly cued but must be inferred from the stimulus statistics (a more ecologically valid scenario).
- Consider presenting a brief case study or "design recipe" walking through how an experimentalist would use the information gap landscapes to set up a concrete experiment.

## Score and Decision
The paper presents a novel, theoretically rigorous, and practically useful framework for an important open question in computational neuroscience. The derivations are sound, the simulations are thorough and convincing, and the real-data analysis provides meaningful context. The main limitation is the absence of positive empirical validation on real neural data with optimized designs, and the practical challenges suggested by the large asymmetry between coding hypotheses. These limitations prevent a strong accept but the overall contribution is solid and above the acceptance threshold.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>