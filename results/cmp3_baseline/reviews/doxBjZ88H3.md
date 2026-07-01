## Summary

This paper presents an information-theoretic framework for optimizing experimental designs to distinguish between two competing hypotheses about how sensory neural populations encode uncertainty: likelihood coding (probabilistic population codes) versus posterior coding (neural sampling codes). The authors derive an "information gap" measure—the expected difference in decoder performance when applying likelihood versus posterior decoders to neural populations—and validate through simulations that this measure accurately predicts empirical decoder performance differences. They demonstrate how maximizing the information gap yields stimulus distributions that optimally differentiate the two coding hypotheses, providing a principled approach for designing experiments to resolve a fundamental debate in computational neuroscience.

## Strengths

- **Novel and important research question**: The paper addresses a fundamental open problem in computational neuroscience—how to experimentally distinguish between likelihood and posterior coding hypotheses in sensory populations. This question has remained unresolved despite years of debate, and the paper provides a principled theoretical framework for designing decisive experiments.

- **Rigorous theoretical derivation**: The authors derive analytic expressions for the information gap under both coding hypotheses (Eqs. 1-5), providing a solid mathematical foundation. The derivation of Bayes-optimal estimators for mismatched decoding (Eqs. 2 and 5) is particularly elegant and captures the core insight that task-marginalized surrogates arise when decoding mismatched probabilistic content.

- **Strong empirical validation**: The simulation results (Figures 3 and 4) convincingly demonstrate convergence of empirical decoder performance differences to theoretical predictions across diverse task parameters, contrast levels, and neural models (both Poisson and gain-modulated Poisson). The agreement across multiple random seeds and parameter settings provides robust support for the framework.

- **Practical actionable insights**: The information gap landscapes (Figures 5 and 6) directly translate theory into practical experimental guidance, identifying "sweet spots" for task parameters. The analysis of why heavy-tailed priors are unsuitable and the demonstration that single-context designs cannot distinguish hypotheses (Figure 7) provide concrete, useful conclusions for experimentalists.

- **Clear exposition of asymmetry**: The paper explicitly identifies and explains the order-of-magnitude asymmetry between likelihood and posterior coding information gaps, providing intuitive understanding of why distinguishing posterior-coding populations is inherently more challenging.

## Weaknesses

### Major

- **Limited validation on real neural data**: While the Allen Institute analysis (Figure 7) confirms that single-context designs yield zero information gap, the paper lacks validation of the framework's core prediction—that optimized multi-context designs actually produce distinguishable decoder performance on real neural data. The entire framework rests on the assumption that the theoretical information gap translates to empirical distinguishability, but this is only tested on synthetic data. Given that the paper claims to guide "principled, theory-driven experimental designs," the absence of any real neural data experiment with manipulated priors is a significant gap.

- **Computational tractability concerns for posterior coding information gap**: The derivation of the posterior coding information gap (Eqs. 3-5) requires solving an implicit equation via fixed-point iteration and identifying observation pairs satisfying Eq. 4. The paper does not discuss the computational complexity of this procedure, how it scales with the discretization of the observation space, or whether convergence of the fixed-point iteration is guaranteed. For practical experimental design, researchers would need to compute this efficiently, and the paper provides no guidance on computational feasibility.

- **Assumption of perfect decoder optimality**: The framework assumes that decoders can achieve the theoretical Bayes-optimal performance. While the simulations show convergence with sufficient data, the paper does not address how far real experimental decoders (with limited data, finite neural populations, and practical training constraints) might deviate from this ideal. The practical utility of the framework depends on whether the information gap ranking of task designs is preserved under realistic decoder suboptimality.

### Minor

- **Limited exploration of non-Gaussian observation models**: The simulations focus exclusively on Gaussian observation models $p(x|\theta)$ and Gaussian tuning curves. While the framework is presented as general, the paper would benefit from demonstrating its applicability to other observation models (e.g., von Mises distributions for circular variables, or more complex naturalistic stimulus distributions).

- **The strategic task design selection (asterisks in Figure 5) appears somewhat ad hoc**: The paper states that asterisks identify "sweet spots" where posterior-coding information gap approaches its maximum while likelihood-coding maintains sufficient signal, but the precise criterion for selecting these points is not formalized. A more rigorous multi-objective optimization approach would strengthen this aspect.

### Trivial

- The notation in Eq. 3 uses both $x_i$ and $(x_j, x_k)$ inconsistently; the sum notation could be clarified.

## Nice-to-Haves

- A discussion of how the framework could be extended to handle more than two contexts, or continuous context spaces
- An analysis of how robust the optimal task designs are to misspecification of the generative model parameters
- A practical guide or pseudocode for experimentalists to implement the framework for their specific experimental setup

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is the identification and explanation of the asymmetry between likelihood and posterior coding distinguishability: the information gap for likelihood coding is systematically larger because every observation contributes to the gap, whereas for posterior coding only observation pairs satisfying a specific equality condition (Eq. 4) contribute. This asymmetry has important practical implications—it means that experiments designed to detect posterior coding require substantially more statistical power, and that the common intuition of "just use very different priors" may be suboptimal because it reduces the number of observation pairs that satisfy the critical condition. The paper also provides the counterintuitive finding that heavy-tailed priors, which might seem useful for creating strong prior effects, are actually ineffective for distinguishing the hypotheses because they produce almost no observation pairs satisfying Eq. 4.

## Suggestions

- Validate the framework's core prediction by applying the optimized task designs to a real neural dataset where priors are manipulated (e.g., existing datasets with context-dependent tasks, or by reanalyzing data from studies that incidentally varied stimulus statistics across sessions). Even a post-hoc analysis showing that decoder performance differences correlate with the information gap in existing data would substantially strengthen the paper.

- Provide a practical algorithm or pseudocode for computing the information gap, including the fixed-point iteration for posterior coding, with discussion of convergence criteria and computational complexity. This would significantly lower the barrier for experimentalists to adopt the framework.

- Add a sensitivity analysis showing how robust the optimal task parameters are to deviations from the assumed generative model, as experimentalists will inevitably have imperfect knowledge of neural response properties.

## Score and Decision

The paper presents a novel, theoretically rigorous, and practically important framework for a long-standing problem in computational neuroscience. The theoretical derivations are sound, the simulation validation is thorough, and the practical implications are clearly articulated. The major weakness is the lack of validation on real neural data with manipulated priors, which limits the immediate impact of the work. However, the theoretical contribution is substantial enough to warrant acceptance, and the framework provides clear, testable predictions that can guide future experiments.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>