## Summary

This paper initiates the study of *reliability scoring* for datasets when the ground truth is unobserved but outcomes of an unknown statistical experiment (auxiliary observations) are available. The authors formalize ground-truth-based reliability orderings (exact match, Blackwell, Hamming/dist) and propose the *Gram determinant score*, which measures the volume spanned by class-conditional observation distributions. They prove that this score preserves several reliability orderings under mild conditions, is *experiment-agnostic* (ranking independent of the experiment), and is unique up to scaling. Experiments on synthetic data, CIFAR-10 embeddings, and real employment data demonstrate that the score correlates with label quality.

## Strengths

- **Novel problem formulation.** The paper provides a rigorous framework for data reliability without ground truth, which is a practically relevant and under-explored problem. The setup (true data unseen, auxiliary observations available) is well motivated by realistic scenarios (e.g., insurance, regulatory data).
- **Strong theoretical contributions.** The Gram determinant score is elegantly connected to the volume geometry of joint distributions. The authors prove preservation of exact-match, Blackwell, and approximate Hamming/dist orderings, and complement these with impossibility results that demarcate the feasible regime. The uniqueness result (Proposition 4.3) adds depth.
- **Experiment-agnosticism.** The fact that the score’s ranking depends only on the misreport matrix (not on the experiment) is a compelling property, and the uniqueness result strengthens the argument for the determinant.
- **Clean empirical validation.** The experiments on synthetic data (multiple manipulation policies, Kendall-tau ranking recovery), CIFAR-10 (kernelized score with continuous embeddings), and a real-world employment dataset provide evidence that the score behaves as expected and scales to practical settings.

## Weaknesses

### Major

- **Restrictive assumptions for Hamming/dist ordering preservation.** Theorem 4.2(3) requires the true data to be $L$-balanced, the misreport matrix to be in $\mathcal{Q}_{L,1/64L^2d^2}$ (strong diagonal dominance and very bounded Hamming distance), and the aspect ratio $\Delta$ to be considered. This covers only a narrow slice of realistic misreport patterns. While the impossibility results show this is nearly tight, it still limits the practical scope of the fine-grained ordering guarantees.
- **Finite label and observation spaces.** The core theory assumes $\mathcal{X}$ and $\mathcal{Y}$ are finite sets. The kernel extension (Section 4.3) is mentioned but not accompanied by analogous ordering-preservation theorems in the main text (deferred to Appendix F). The paper would be stronger if at least a high-level theoretical guarantee for the kernelized version were stated in the main body.
- **Scalability concerns.** The plug-in estimator requires computing a $d \times d$ Gram matrix and its determinant, which is feasible for small $d$ (5, 10 in experiments). For large label spaces (e.g., thousands of classes), the estimator becomes expensive and the determinant may be unstable. The paper acknowledges this as future work, but it is a significant limitation for real-world applicability.

### Minor

- **Experiment design.** The synthetic experiments use a fixed ground-truth dataset $(\mathbf{x}, \mathbf{y})$ and vary corruption. While this is reasonable, showing results across multiple random ground-truth draws (to account for variability in $\mathbf{P}$ and $\mathbf{x}$) would increase robustness. The employment experiment with $N=209$ is small; the discretization into quartiles is somewhat arbitrary.
- **Omitted details.** The stratified matching estimator (mentioned in Section 4.2) is deferred entirely to the appendix with no summary in the main text. A brief description would help completeness.
- **Clarity of impossibility results.** Proposition 3.1 states “there exists a $\mathcal{P}$” and “for any $\mathcal{P}$…” – the implications for the Gram determinant score (which uses $\mathcal{P}_{\text{indep}}$) are clear, but the presentation could be streamlined to directly connect to the chosen experiment class.

### Trivial

- The notation $\mathcal{Q}$ is overloaded (set of matrices, set of pairs $(\mathbf{x},\hat{\mathbf{x}})$). While defined, it occasionally causes confusion when reading.

## Nice-to-Haves

- An empirical evaluation on a dataset with a larger label space (e.g., CIFAR-100 or a subset of ImageNet) would better test scalability and the kernelized score’s behavior.
- A sensitivity analysis of the plug-in estimator under varying $N$ and $d$ (beyond the fixed $d=5$ used in Fig. 2d) would be informative.
- A small ablation showing how the score degrades when the independence assumption (columns of $\mathbf{P}$ are linearly independent) is violated.

## Novel Insights

Beyond its own contributions, the paper provides a clean geometric picture: the Gram determinant score measures the volume collapse caused by misreporting. The uniqueness result shows that if one demands experiment-agnostic rankings and scale-invariance, the squared determinant is essentially forced. This connects seemingly unrelated desiderata (volume, ranking invariance) into a single closed-form solution. The impossibility results also offer a useful taxonomy of when reliability scoring is inherently impossible, which may guide future work.

## Suggestions

- Add a brief statement of the kernelized ordering guarantee in Section 4.3 (e.g., “Under the same conditions, the kernelized score preserves the orderings provided the kernel is characteristic or injective in the sense of…”) rather than fully deferring to the appendix.
- In the experiments, report average and standard deviation across multiple random ground-truth draws (e.g., 10 different $\mathbf{P}$ and $\mathbf{x}$ seeds) to strengthen generalizability.
- Discuss more concretely how the Gram determinant score would be estimated when $d$ is large, e.g., via low-rank approximations or random features.

## Score and Decision

Based on the review, the paper presents a solid theoretical foundation for a novel problem, with clean geometric intuition, non-trivial theoretical results, and reasonable empirical support. The main weaknesses lie in the restrictive conditions for fine-grained ordering guarantees and limited scalability to large label spaces, which are acknowledged. Given that the paper is a first formalization of the problem, it meets the bar for acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>