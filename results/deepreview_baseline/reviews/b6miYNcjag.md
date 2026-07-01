## Summary

This paper introduces the problem of *reliability scoring* for datasets when ground truth is unavailable but auxiliary observations from an unknown experiment are available. The authors formalize ground-truth-based reliability orderings (exact match, Blackwell, Hamming/dist) and propose the *Gram determinant score*, which measures the volume spanned by the empirical joint distribution of reported data and observations. They prove that this score preserves several of these orderings under linearly independent experiments and mild conditions on misreport matrices, and that it is uniquely experiment-agnostic up to scaling. Experiments on synthetic categorical data, CIFAR-10 embeddings, and real employment data demonstrate that the score correlates well with label corruption levels.

## Strengths

- **Novel problem formulation and theoretical foundation.** The paper formalizes a practically important but understudied problem—assessing data reliability without ground truth—and provides a rigorous theoretical framework with well-defined reliability orderings and impossibility results.
- **Strong theoretical results.** The Gram determinant score is shown to preserve exact-match, Blackwell, and approximate Hamming/dist orderings under nearly tight conditions. The uniqueness result (Proposition 4.3) that the score is the only experiment-agnostic reliability measure up to scaling is particularly elegant and compelling.
- **Clear geometric intuition.** The interpretation of the score as the squared volume of a parallelepiped spanned by class-conditional observation distributions is intuitive and well-illustrated.
- **Practical estimators and kernel extension.** The plug-in estimator and kernelized version make the score applicable to finite-sample and continuous observation settings, broadening its potential impact.

## Weaknesses

### Major

- **Limited empirical validation.** The experiments only show that the Gram determinant score correlates monotonically with corruption levels and error metrics. There is no comparison against any baseline reliability score (e.g., mutual information, entropy, or other determinant-based measures). Without baselines, it is unclear whether the score offers practical advantages over simpler alternatives.
- **Employment data experiment is weak.** The real-world experiment uses only 209 time points, discretizes continuous changes into four quantile buckets, and reports only a single score per vintage. This provides limited evidence that the score works reliably in realistic settings with small sample sizes and arbitrary discretization choices.

### Minor

- **Assumptions may be restrictive in practice.** The theoretical guarantees require linearly independent experiments and diagonally dominant misreport matrices (with additional balance and bounded Hamming distance for the dist ordering). While the paper shows these are nearly necessary, it is unclear how often they hold in real applications.
- **Finite-sample guarantees are not presented in the main text.** The conclusion mentions "finite-sample guarantees" for the estimators, but the main body only provides asymptotic preservation (Proposition 4.5). The practical reliability of the score for small N is not fully addressed.
- **Kernelized version lacks theoretical analysis in the main text.** The paper states that a reliability-ordering result analogous to Theorem 4.2 exists for kernels (Appendix F), but the main text does not include this result, leaving the theoretical grounding of the kernelized score somewhat incomplete for the reader.

### Trivial

- The notation is occasionally dense, making some sections (e.g., the definition of $\mathcal{Q}_{L,\delta}$) harder to follow than necessary.

## Nice-to-Haves

- A comparison with simple baselines (e.g., entropy of reported labels, mutual information between reports and observations) in the experiments would strengthen the empirical contribution.
- A discussion of computational complexity and scalability for large label spaces $d$ would be helpful for practitioners.
- An ablation study on the effect of the experiment matrix $\mathbf{P}$ (e.g., varying the degree of linear independence) would illustrate the robustness of the score.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the determinant of the Gram matrix of class-conditional observation distributions naturally factorizes into a term depending only on the experiment and a term depending only on the misreport matrix. This factorization is what enables experiment-agnostic ranking and connects the score to the volume of a parallelepiped. The uniqueness result further suggests that any reliability score satisfying experiment agnosticism and mild continuity must be a power of the Gram determinant, which is a strong theoretical justification for the proposed approach.

## Suggestions

- Add baseline comparisons (e.g., mutual information, entropy of reported labels, or the determinant mutual information from Kong (2024)) to the synthetic and CIFAR-10 experiments to demonstrate the practical advantage of the Gram determinant score.
- Include a small-scale experiment with finite-sample sizes (e.g., N=50, 100) to show how the plug-in estimator behaves when the asymptotic regime is not reached.
- Provide a brief discussion of how to check or relax the linearly independent experiment assumption in practice (e.g., using condition number of the estimated Gram matrix).

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>