## Summary

This paper introduces the problem of reliability scoring for datasets when the ground truth is unobserved but auxiliary observations from an unknown experiment are available. The authors formalize ground-truth-based reliability orderings (exact-match, Blackwell, and distance-based) as benchmarks and propose the Gram determinant score, which measures the volume of the parallelepiped spanned by the empirical joint distribution of reported data and observations. They prove that this score preserves several of these orderings under linearly independent experiments and is, up to scaling, the unique experiment-agnostic score. Experiments on synthetic noise models, CIFAR-10 embeddings, and employment data validate the approach.

## Strengths

- **Novel problem formalization.** The paper provides a clean mathematical framework for evaluating dataset reliability without access to ground truth, using auxiliary observations from an unknown experiment. The three ground-truth-based orderings (exact-match, Blackwell, dist) are well-motivated and cover different practical notions of reliability.

- **Elegant theoretical contributions.** The Gram determinant score admits a natural geometric interpretation (volume of a parallelepiped) and the multiplicative decomposition $\Gamma(PQ)=\det(P^T P)\det(Q)^2$ decouples the experiment from the misreport matrix, enabling strong guarantees. The uniqueness result (Proposition 4.3) showing that the Gram determinant is the only continuous experiment-agnostic reliability score up to scaling is a compelling justification.

- **Matching impossibility results.** Section 3 establishes necessary limitations on what combinations of experiments and misreport matrices can be handled, and the positive results in Theorem 4.2 nearly match these lower bounds, demonstrating that the theory is tight rather than overly conservative.

- **Clear writing and organization.** The paper is well-structured, definitions are precise, and the geometric intuition in Figure 1 effectively conveys the core idea before formal theorems.

## Weaknesses

### Fatal

None.

### Major

- **Limited empirical scale and diversity.** The synthetic experiments use only $d=5$ categories and $N=4000$, the CIFAR-10 experiment uses only 8-dimensional embeddings, and the employment dataset has only $N=209$ points. While the theoretical results are the primary contribution, the empirical validation would be stronger with higher-dimensional label spaces (e.g., ImageNet subset with many classes) or larger real-world datasets. The employment experiment relies on a single external observation (tax deposits) and shows only that revisions improve the score—a more challenging test would compare the score's ranking against an independent ground-truth metric.

- **Reliance on finite $\mathcal{Y}$ in core theory.** Definition 4.1 and Theorem 4.2 assume $\mathcal{Y}$ is finite. The kernel extension in Section 4.3 handles continuous spaces but the theoretical guarantees for preserving orderings in the kernelized setting are only sketched (deferred to appendix). A reader cannot fully assess the strength of the guarantees for the CIFAR-10 experiment without consulting the appendix.

- **Implication of "experiment agnosticism"** is somewhat overstated. While Proposition 4.3 shows that the Gram determinant ranking is invariant to the experiment for *invertible* $Q$, in practice $Q$ may be singular or near-singular, and the uniqueness result requires continuity and a specific scaling property that may not hold for all plausible scores.

### Minor

- The plug-in estimator in Definition 4.4 uses $\frac{1}{N^2}$ normalization which includes the $n=n'$ diagonal terms, making it slightly biased even asymptotically (the diagonal contributes $1/N$). The authors could discuss this bias more explicitly.

- The experimental plots (Figures 2 and 3) show monotonic trends but error bars are sometimes large, especially at high corruption levels for some manipulations. The paper could comment on variance behavior.

### Trivial

- The notation in Proposition 2.1 uses $\pi$ as a superscript for the ordering symbol, which is not defined explicitly (presumably denoting the true data $\mathbf{x}$). Minor confusion.

## Nice-to-Haves

- An ablation study examining how the Gram determinant score degrades when the experiment $P$ is nearly linearly dependent (close to violating the $\mathcal{P}_{\text{indep}}$ condition).
- A comparison against baselines such as simple correlation between $y$ and $\hat{x}$, or mutual information, to contextualize the advantage of the Gram determinant.

## Novel Insights

Beyond its own contributions, the paper highlights a useful perspective: the reliability of reported data can be measured by how much the class-conditional observation distributions "spread apart," which is captured by the determinant of a Gram matrix. The uniqueness result ties this geometric quantity to a natural invariance principle, suggesting that any reasonable experiment-agnostic reliability score must be a monotone function of the determinant. This observation could inspire future work on other spectral or volume-based reliability metrics.

## Suggestions

- In the experiments, include a higher-dimensional categorical setting (e.g., $d=20$ or $d=50$) to test scalability of the theory, or use a dataset like Amazon product reviews where star ratings are the labels and text embeddings are observations, with known fake-review benchmarks.
- Discuss the practical implications of the $\mathcal{Q}_{L,1/(64 L^2 d^2)}$ bound for the $\alpha$-dist ordering—how restrictive is this in real applications?

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>